# Sponsor variants: each is a small, exact-text change to one admiral template call.
# A variant's oracle = the patched template run on the standard SDTM, with the standard ADSL
# chained in for ADAE and ADLB. Each `from` must occur exactly once in the template.
# `description` is for humans; the task spec (benchmark/specs/) is written separately.

variants <- list(

  "var-trtsdt-active" = list(
    dataset = "adsl",
    description = "TRTSDT from the first exposure record with EXDOSE > 0 only (placebo rows do not count).",
    patches = list(list(
      from = "    filter_add = (EXDOSE > 0 |
      (EXDOSE == 0 &
        str_detect(EXTRT, \"PLACEBO\"))) &
      !is.na(EXSTDTM),",
      to = "    filter_add = EXDOSE > 0 & !is.na(EXSTDTM),"))
  ),

  "var-trtdurd-noplus1" = list(
    dataset = "adsl",
    description = "TRTDURD = TRTEDT - TRTSDT (no +1).",
    patches = list(list(
      from = "  derive_var_trtdurd()",
      to = "  derive_vars_duration(new_var = TRTDURD, start_date = TRTSDT, end_date = TRTEDT, add_one = FALSE)"))
  ),

  "var-saffl-2rec" = list(
    dataset = "adsl",
    description = "SAFFL = Y only with at least two qualifying exposure records.",
    patches = list(list(
      from = "  derive_var_merged_exist_flag(
    dataset_add = ex,
    by_vars = exprs(STUDYID, USUBJID),
    new_var = SAFFL,
    false_value = \"N\",
    missing_value = \"N\",
    condition = (EXDOSE > 0 | (EXDOSE == 0 & str_detect(EXTRT, \"PLACEBO\")))
  ) %>%",
      to = "  left_join(
    ex %>%
      filter(EXDOSE > 0 | (EXDOSE == 0 & str_detect(EXTRT, \"PLACEBO\"))) %>%
      count(STUDYID, USUBJID, name = \"N_QUAL_EX\"),
    by = c(\"STUDYID\", \"USUBJID\")
  ) %>%
  mutate(SAFFL = if_else(!is.na(N_QUAL_EX) & N_QUAL_EX >= 2, \"Y\", \"N\"), N_QUAL_EX = NULL) %>%"))
  ),

  "var-agegr1-65-75" = list(
    dataset = "adsl",
    description = "AGEGR1 groups: <65, 65-74, >=75.",
    patches = list(list(
      from = "    x < 18 ~ \"<18\",
    between(x, 18, 64) ~ \"18-64\",
    x > 64 ~ \">64\",",
      to = "    x < 65 ~ \"<65\",
    between(x, 65, 74) ~ \"65-74\",
    x >= 75 ~ \">=75\","))
  ),

  "var-eosstt-safety" = list(
    dataset = "adsl",
    description = "EOSSTT splits discontinuations into safety (adverse event, death) and other.",
    patches = list(list(
      from = "    !is.na(x) ~ \"DISCONTINUED\",",
      to = "    x %in% c(\"ADVERSE EVENT\", \"DEATH\") ~ \"DISCONTINUED - SAFETY\",
    !is.na(x) ~ \"DISCONTINUED - OTHER\","))
  ),

  "var-lstalvdt-addvs" = list(
    dataset = "adsl",
    description = "LSTALVDT also considers vital-sign dates (VS.VSDTC) as a source.",
    patches = list(
      list(from = "lb <- pharmaversesdtm::lb\n", to = "lb <- pharmaversesdtm::lb\nvs <- pharmaversesdtm::vs\n"),
      list(from = "lb <- convert_blanks_to_na(lb)\n", to = "lb <- convert_blanks_to_na(lb)\nvs <- convert_blanks_to_na(vs)\n"),
      list(from = "      event(
        dataset_name = \"adsl\",",
           to = "      event(
        dataset_name = \"vs\",
        order = exprs(VSDTC, VSSEQ),
        condition = !is.na(VSDTC),
        set_values_to = exprs(
          LSTALVDT = convert_dtc_to_dt(VSDTC, highest_imputation = \"M\"),
          seq = VSSEQ
        ),
      ),
      event(
        dataset_name = \"adsl\","),
      list(from = "source_datasets = list(ae = ae, lb = lb, adsl = adsl),", to = "source_datasets = list(ae = ae, lb = lb, vs = vs, adsl = adsl),"))
  ),

  "var-trtemfl-w0" = list(
    dataset = "adae",
    description = "TRTEMFL window after last dose is 0 days instead of 30.",
    patches = list(list(from = "    end_window = 30", to = "    end_window = 0"))
  ),

  "var-astdt-dayonly" = list(
    dataset = "adae",
    description = "ASTDT imputes only a missing day (to the 15th); missing month or year gives no date.",
    patches = list(list(
      from = "    dtc = AESTDTC,
    new_vars_prefix = \"AST\",
    highest_imputation = \"M\",",
      to = "    dtc = AESTDTC,
    new_vars_prefix = \"AST\",
    highest_imputation = \"D\",
    date_imputation = \"mid\","))
  ),

  "var-ablfl-strict" = list(
    dataset = "adlb",
    description = "Baseline record must be strictly before the first dose date.",
    patches = list(list(from = "ADT <= TRTSDT & !is.na(BASETYPE)", to = "ADT < TRTSDT & !is.na(BASETYPE)"))
  ),

  "var-lstalvdt-complete" = list(
    dataset = "adsl",
    description = "LSTALVDT uses complete dates only: AE start, AE end and lab dates that are partial are dropped before the latest date is chosen (not imputed, and not left as missing).",
    patches = list(
      list(from = "condition = !is.na(AESTDTC),", to = "condition = !is.na(AESTDTC) & nchar(AESTDTC) >= 10,"),
      list(from = "condition = !is.na(AEENDTC),", to = "condition = !is.na(AEENDTC) & nchar(AEENDTC) >= 10,"),
      list(from = "condition = !is.na(LBDTC),", to = "condition = !is.na(LBDTC) & nchar(LBDTC) >= 10,"))
  ),

  "var-ontrtfl-w7" = list(
    dataset = "adlb",
    description = "ONTRTFL extends 7 days past the last dose date.",
    patches = list(list(
      from = "    ref_end_date = TRTEDT,
    filter_pre_timepoint = AVISIT == \"Baseline\"",
      to = "    ref_end_date = TRTEDT,
    ref_end_window = 7,
    filter_pre_timepoint = AVISIT == \"Baseline\""))
  ),

  "var-aoccifl-bysoc" = list(
    dataset = "adae",
    description = "AOCCIFL flags, within each subject and body system, the first occurrence of the most severe treatment-emergent event.",
    patches = list(list(
      from = "      by_vars = exprs(USUBJID),
      order = exprs(desc(ASEVN), ASTDTM, AESEQ),",
      to = "      by_vars = exprs(USUBJID, AEBODSYS),
      order = exprs(desc(ASEVN), ASTDTM, AESEQ),"))
  ),

  "var-chg-ontrt" = list(
    dataset = "adlb",
    description = "CHG only for post-baseline on-treatment records (ONTRTFL = Y).",
    patches = list(list(
      from = "    derivation = derive_var_chg,
    filter = AVISITN > 0",
      to = "    derivation = derive_var_chg,
    filter = AVISITN > 0 & ONTRTFL == \"Y\""))
  )
)
