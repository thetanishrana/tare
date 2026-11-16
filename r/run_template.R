# Worker (used by k1_oracle_check.R and oracle_build.R): runs ONE admiral template in a fresh R process.
# Usage: Rscript r/run_template.R <name> <template_path> <sdtm_rds|NA> <adsl_rds|NA> <out_rds> [patches_rds]
# patches_rds: list of list(from=, to=) exact-text replacements (sponsor variants); each `from`
# must occur exactly once in the template text.
# Data reads are redirected through shims; the template is cut at its "Save output" block
# (the originals write to a user-level cache directory).
args <- commandArgs(trailingOnly = TRUE)
patches_rds <- if (length(args) >= 6) args[6] else NA
name <- args[1]; path <- args[2]; sdtm_rds <- args[3]; adsl_rds <- args[4]; out_rds <- args[5]

.k1_sdtm <- if (sdtm_rds != "NA") readRDS(sdtm_rds) else NULL
.k1_adsl <- if (adsl_rds != "NA") readRDS(adsl_rds) else NULL
.get_sdtm <- function(n) {
  if (!is.null(.k1_sdtm) && n %in% names(.k1_sdtm)) .k1_sdtm[[n]]
  else getExportedValue("pharmaversesdtm", n)
}
.get_adsl <- function() if (!is.null(.k1_adsl)) .k1_adsl else getExportedValue("admiral", "admiral_adsl")

code <- readLines(path, warn = FALSE)
cut <- grep("^# Save output ----", code)
stopifnot(length(cut) == 1)
code <- code[seq_len(cut - 1)]
if (!is.na(patches_rds)) {
  txt <- paste(code, collapse = "\n")
  for (p in readRDS(patches_rds)) {
    hits <- gregexpr(p$from, txt, fixed = TRUE)[[1]]
    if (length(hits) != 1 || hits[1] == -1) stop("patch must match exactly once: ", substr(p$from, 1, 60))
    txt <- sub(p$from, p$to, txt, fixed = TRUE)
  }
  code <- strsplit(txt, "\n", fixed = TRUE)[[1]]
}
code <- gsub("pharmaversesdtm::([A-Za-z0-9_]+)", ".get_sdtm('\\1')", code)
code <- gsub("admiral::admiral_adsl", ".get_adsl()", code, fixed = TRUE)

warns <- character()
secs <- system.time(
  withCallingHandlers(
    eval(parse(text = code), envir = globalenv()),
    warning = function(w) {
      warns <<- c(warns, conditionMessage(w))
      invokeRestart("muffleWarning")
    }
  )
)[["elapsed"]]
saveRDS(list(data = get(name, envir = globalenv()), seconds = secs, warnings = unique(warns)), out_rds)
