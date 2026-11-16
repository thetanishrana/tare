# Held-out ophthalmology slice (oracle id `oph`): base admiral functions applied to the pharmaversesdtm
# ophthalmology datasets (sc_ophtha, oe_ophtha, ae_ophtha). admiral has no ophthalmology template, so this
# is our own script built from admiral derivation functions; the subject-level dates come from the standard
# ADSL oracle. Tasks built on it belong to the `heldout` split only (docs/04_BENCHMARK_SPEC.md).
#   adsl.parquet : STUDYEYE (RIGHT/LEFT) from the focus-eye record in sc_ophtha (OD = right, OS = left), TRTSDT
#   adoe.parquet : intraocular pressure (IOP) per eye with ABLFL, BASE and CHG, by eye
#   adae.parquet : ae_ophtha with AESTEFL (adverse event in the study eye)
suppressPackageStartupMessages({library(dplyr); library(admiral)})

build_ophtha <- function(adsl_std) {
  get_sdtm <- function(n) as.data.frame(getExportedValue("pharmaversesdtm", n))
  sc <- get_sdtm("sc_ophtha"); oe <- get_sdtm("oe_ophtha"); ae <- get_sdtm("ae_ophtha")
  adsl <- adsl_std %>%
    select(STUDYID, USUBJID, TRTSDT) %>%
    left_join(
      sc %>% filter(SCTESTCD == "FOCID") %>%
        transmute(USUBJID, STUDYEYE = case_when(SCSTRESC == "OD" ~ "RIGHT", SCSTRESC == "OS" ~ "LEFT")),
      by = "USUBJID")

  adoe <- oe %>%
    filter(OETESTCD == "IOP") %>%
    derive_vars_dt(new_vars_prefix = "A", dtc = OEDTC) %>%
    mutate(PARAMCD = OETESTCD, AVAL = OESTRESN) %>%
    derive_vars_merged(dataset_add = adsl, by_vars = exprs(STUDYID, USUBJID), new_vars = exprs(TRTSDT, STUDYEYE)) %>%
    restrict_derivation(
      derivation = derive_var_extreme_flag,
      args = params(by_vars = exprs(USUBJID, PARAMCD, OELAT), order = exprs(ADT, OESEQ),
                    new_var = ABLFL, mode = "last"),
      filter = !is.na(AVAL) & !is.na(ADT) & !is.na(TRTSDT) & ADT <= TRTSDT & OETPT == "PRE-DOSE"
    ) %>%
    derive_var_base(by_vars = exprs(USUBJID, PARAMCD, OELAT), source_var = AVAL, new_var = BASE) %>%
    restrict_derivation(
      derivation = derive_var_chg,
      filter = !is.na(ADT) & !is.na(TRTSDT) & ADT > TRTSDT
    )

  adae <- ae %>%
    derive_vars_merged(dataset_add = adsl, by_vars = exprs(STUDYID, USUBJID), new_vars = exprs(STUDYEYE)) %>%
    mutate(AESTEFL = case_when(
      is.na(AELAT) ~ NA_character_,
      AELAT == "BOTH" | AELAT == STUDYEYE ~ "Y",
      TRUE ~ "N"
    ))
  list(adsl = adsl, adoe = adoe, adae = adae)
}
