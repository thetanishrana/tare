# Build oracle outputs (the hidden answers) with the admiral templates.
#   data/oracle/std/{adsl,adae,adlb}.parquet     standard chain: ADSL feeds ADAE and ADLB
#   data/oracle/<variant-id>/<dataset>.parquet   sponsor variants (patched template, std ADSL chained)
#   data/oracle/<id>/manifest.json               versions, script hash, patches
# Run from the repo root:  Rscript r/oracle_build.R [oracle_id ...]
# Oracle outputs are git-ignored and must never be mounted into a sandbox or shown in a prompt.

suppressPackageStartupMessages({library(arrow); library(jsonlite)})
source("r/variants/variants.R")
source("r/perturb.R")
source("r/ophtha.R")

root <- "data/oracle"
tmpl_dir <- file.path(root, "_templates")
dir.create(tmpl_dir, recursive = TRUE, showWarnings = FALSE)
templates <- c(adsl = "ad_adsl.R", adae = "ad_adae.R", adlb = "ad_adlb.R", advs = "ad_advs.R")
for (n in names(templates)) {
  admiral::use_ad_template(adam_name = n, save_path = file.path(tmpl_dir, templates[[n]]),
                           package = "admiral", overwrite = TRUE)
}

run_template <- function(name, adsl = NULL, patches = NULL, sdtm = NULL) {
  tmp <- function(x) if (is.null(x)) "NA" else { f <- tempfile(fileext = ".rds"); saveRDS(x, f); f }
  out <- tempfile(fileext = ".rds")
  args <- c("r/run_template.R", name, file.path(tmpl_dir, templates[[name]]), tmp(sdtm), tmp(adsl), out)
  if (!is.null(patches)) args <- c(args, tmp(patches))
  err <- tempfile()
  status <- system2("Rscript", args, stdout = FALSE, stderr = err)
  if (status != 0 || !file.exists(out)) stop("template ", name, " failed:\n", paste(readLines(err), collapse = "\n"))
  readRDS(out)$data
}

sha <- function(paths) {
  vapply(paths, function(p) digest_file(p), "")
}
digest_file <- function(p) {
  out <- system2("shasum", c("-a", "256", p), stdout = TRUE)
  strsplit(out, " ")[[1]][1]
}

manifest <- function(id, datasets, extra = list()) {
  dir <- file.path(root, id)
  write_json(c(list(
    oracle_id = id,
    datasets = datasets,
    built = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z"),
    R = R.version.string,
    admiral = as.character(packageVersion("admiral")),
    pharmaversesdtm = as.character(packageVersion("pharmaversesdtm")),
    pharmaverseadam = as.character(packageVersion("pharmaverseadam")),
    script_sha256 = list(oracle_build = digest_file("r/oracle_build.R"),
                         run_template = digest_file("r/run_template.R"),
                         variants = digest_file("r/variants/variants.R"))
  ), extra), file.path(dir, "manifest.json"), auto_unbox = TRUE, pretty = TRUE)
}

write_ds <- function(df, id, name) {
  dir.create(file.path(root, id), recursive = TRUE, showWarnings = FALSE)
  write_parquet(df, file.path(root, id, paste0(name, ".parquet")))
}

wanted <- commandArgs(trailingOnly = TRUE)
want <- function(id) length(wanted) == 0 || id %in% wanted

# Standard chain
adsl_std <- NULL
if (want("std") || length(wanted) > 0) {
  adsl_std <- run_template("adsl")
  if (want("std")) {
    adae <- run_template("adae", adsl = adsl_std)
    adlb <- run_template("adlb", adsl = adsl_std)
    advs <- run_template("advs", adsl = adsl_std)
    for (nm in c("adsl", "adae", "adlb", "advs")) write_ds(get(if (nm == "adsl") "adsl_std" else nm), "std", nm)
    manifest("std", c("adsl", "adae", "adlb", "advs"))
    message("std: adsl ", nrow(adsl_std), " adae ", nrow(adae), " adlb ", nrow(adlb))
  }
}

# Sponsor variants
for (id in names(variants)) {
  if (!want(id)) next
  v <- variants[[id]]
  df <- run_template(v$dataset, adsl = if (v$dataset == "adsl") NULL else adsl_std, patches = v$patches)
  write_ds(df, id, v$dataset)
  manifest(id, v$dataset, list(description = v$description, patches = v$patches,
                               adsl_chained_from = if (v$dataset == "adsl") NULL else "std"))
  message(id, ": ", v$dataset, " ", nrow(df), " rows")
}

# Perturbed inputs: SDTM perturbed, then the ADLB template regenerated with the standard ADSL chained in
perturbed <- list(
  "pert-sameday-lb" = list(
    dataset = "adlb",
    description = "Same-day duplicate lab records (new LBSEQ, different value) added on selected baseline and last on-treatment records plus a few others; ADLB regenerated. See r/perturb.R.",
    build = function(adsl_std) {
      adlb_std <- read_parquet("data/oracle/std/adlb.parquet")
      lb <- as.data.frame(getExportedValue("pharmaversesdtm", "lb"))
      lb_p <- perturb_sameday_lb(lb, as.data.frame(adlb_std))
      list(df = run_template("adlb", adsl = adsl_std, sdtm = list(lb = tibble::as_tibble(lb_p))), added = nrow(lb_p) - nrow(lb))
    }
  )
)
# Perturbed exposure: SDTM EX perturbed, then ADSL, ADAE and ADLB regenerated on it (chained).
# The perturbed EX is also written to data/oracle/pert-edge/sdtm/ex.parquet for task inputs.
if (want("pert-edge")) {
  ex <- as.data.frame(getExportedValue("pharmaversesdtm", "ex"))
  ex_p <- perturb_edge_ex(ex)
  groups <- attr(ex_p, "groups")
  attr(ex_p, "groups") <- NULL
  sdtm_p <- list(ex = tibble::as_tibble(ex_p))
  adsl_p <- run_template("adsl", sdtm = sdtm_p)
  adae_p <- run_template("adae", adsl = adsl_p)
  adlb_p <- run_template("adlb", adsl = adsl_p)
  for (nm in c("adsl", "adae", "adlb")) write_ds(get(paste0(nm, "_p")), "pert-edge", nm)
  dir.create(file.path(root, "pert-edge", "sdtm"), showWarnings = FALSE)
  write_parquet(ex_p, file.path(root, "pert-edge", "sdtm", "ex.parquet"))
  manifest("pert-edge", c("adsl", "adae", "adlb"), list(
    description = "Exposure edge cases (blank last dose dates, missing doses, partial start dates) in EX; ADSL, ADAE, ADLB regenerated. See r/perturb.R.",
    subjects_per_group = as.list(groups), seed = 20261028))
  message("pert-edge: adsl ", nrow(adsl_p), " adae ", nrow(adae_p), " adlb ", nrow(adlb_p))
}
# Perturbed exposure for vital signs: the same perturbed EX as pert-edge (same seed), ADSL regenerated on it,
# then ADVS regenerated with that ADSL chained in. Written to its own id so pert-edge is left untouched.
if (want("pert-edge-advs")) {
  ex <- as.data.frame(getExportedValue("pharmaversesdtm", "ex"))
  ex_p <- perturb_edge_ex(ex)
  groups <- attr(ex_p, "groups")
  attr(ex_p, "groups") <- NULL
  adsl_p <- run_template("adsl", sdtm = list(ex = tibble::as_tibble(ex_p)))
  advs_p <- run_template("advs", adsl = adsl_p)
  write_ds(advs_p, "pert-edge-advs", "advs")
  manifest("pert-edge-advs", "advs", list(
    description = "The pert-edge exposure edge cases (blank last dose dates, missing doses, partial start dates); ADSL regenerated, then ADVS. See r/perturb.R.",
    subjects_per_group = as.list(groups), seed = 20261028))
  message("pert-edge-advs: advs ", nrow(advs_p))
}
# Perturbed exposure for AE last-dose variables: pert-edge's ADAE was built without the perturbed EX in its
# SDTM input (its LDOSEDTM and DOSEON still reflect the original EX), so this id regenerates ADAE with the
# perturbed EX passed in. Written to its own id; pert-edge is untouched.
if (want("pert-edge-adae")) {
  ex <- as.data.frame(getExportedValue("pharmaversesdtm", "ex"))
  ex_p <- perturb_edge_ex(ex)
  groups <- attr(ex_p, "groups")
  attr(ex_p, "groups") <- NULL
  sdtm_p <- list(ex = tibble::as_tibble(ex_p))
  adsl_p <- run_template("adsl", sdtm = sdtm_p)
  adae_p <- run_template("adae", adsl = adsl_p, sdtm = sdtm_p)
  write_ds(adae_p, "pert-edge-adae", "adae")
  manifest("pert-edge-adae", "adae", list(
    description = "The pert-edge exposure edge cases; ADSL regenerated, then ADAE with the perturbed EX also passed as SDTM input. See r/perturb.R.",
    subjects_per_group = as.list(groups), seed = 20261028))
  message("pert-edge-adae: adae ", nrow(adae_p))
}
# Perturbed AE dates: SDTM AE perturbed, then ADSL (LSTALVDT uses AE dates) and ADAE regenerated.
if (want("pert-aedates")) {
  ae <- as.data.frame(getExportedValue("pharmaversesdtm", "ae"))
  ae_p <- perturb_ae_dates(ae)
  sdtm_p <- list(ae = tibble::as_tibble(ae_p))
  adsl_p <- run_template("adsl", sdtm = sdtm_p)
  adae_p <- run_template("adae", adsl = adsl_p, sdtm = sdtm_p)
  for (nm in c("adsl", "adae")) write_ds(get(paste0(nm, "_p")), "pert-aedates", nm)
  dir.create(file.path(root, "pert-aedates", "sdtm"), showWarnings = FALSE)
  write_parquet(ae_p, file.path(root, "pert-aedates", "sdtm", "ae.parquet"))
  manifest("pert-aedates", c("adsl", "adae"), list(
    description = "AE start and end dates partially or fully blanked in AE; ADSL and ADAE regenerated. See r/perturb.R.",
    seed = 20261029))
  message("pert-aedates: adsl ", nrow(adsl_p), " adae ", nrow(adae_p))
}
# Held-out ophthalmology slice: STUDYEYE, per-eye IOP baseline and change, AE in the study eye.
if (want("oph")) {
  res <- build_ophtha(adsl_std)
  for (nm in names(res)) write_ds(res[[nm]], "oph", nm)
  manifest("oph", names(res), list(
    description = "Ophthalmology slice from pharmaversesdtm sc_ophtha, oe_ophtha (IOP) and ae_ophtha with base admiral functions (r/ophtha.R); heldout split only."))
  message("oph: adsl ", nrow(res$adsl), " adoe ", nrow(res$adoe), " adae ", nrow(res$adae))
}
for (id in names(perturbed)) {
  if (!want(id)) next
  pt <- perturbed[[id]]
  res <- pt$build(adsl_std)
  write_ds(res$df, id, pt$dataset)
  manifest(id, pt$dataset, list(description = pt$description, records_added = res$added, seed = 20261026, adsl_chained_from = "std"))
  message(id, ": ", pt$dataset, " ", nrow(res$df), " rows (", res$added, " records added)")
}
