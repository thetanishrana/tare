# Input perturbations for the benchmark. The oracle is regenerated on the perturbed SDTM, so the
# answers stay exact (docs/04_BENCHMARK_SPEC.md, "Perturbations").

# same-day: add a repeat lab record on the same date as selected existing records, as an
# unscheduled visit (the admiral ADLB template requires a unique subject/parameter/date/visit key,
# so the repeat gets a new visit number x.5 above or below the original), with a different value
# and a new, higher LBSEQ. Records that are currently the baseline record
# or the last on-treatment record (per the standard oracle) are picked with high probability so
# that tie-breaking rules decide the answer; a small share of other records are duplicated too.
# Deterministic: fixed seed, selection by sorted keys.
perturb_sameday_lb <- function(lb, adlb_std, seed = 20261026L, p_flagged = 0.35, p_other = 0.03) {
  set.seed(seed)
  orig <- adlb_std[is.na(adlb_std$DTYPE), c("USUBJID", "LBSEQ", "ABLFL", "LVOTFL")]
  key <- paste(lb$USUBJID, lb$LBSEQ)
  okey <- paste(orig$USUBJID, orig$LBSEQ)
  flagged <- key %in% okey[orig$ABLFL %in% "Y" | orig$LVOTFL %in% "Y"]
  # the ADLB template derives absolute WBC differentials and requires (subject, visit, date, parameter)
  # to be unique for those tests, so they are left alone
  wbc <- c("WBC", "BASO", "BASOLE", "LYM", "LYMLE")
  eligible <- !is.na(lb$LBSTRESN) & !is.na(lb$LBDTC) & nchar(lb$LBDTC) >= 10 & !(lb$LBTESTCD %in% wbc)
  ord <- order(lb$USUBJID, lb$LBSEQ)
  pick <- logical(nrow(lb))
  pick[ord] <- (eligible & ifelse(flagged, runif(nrow(lb)) < p_flagged, runif(nrow(lb)) < p_other))[ord]
  dup <- lb[pick, ]
  dup <- dup[order(dup$USUBJID, dup$LBSEQ), ]
  delta <- sample(c(-0.2, -0.1, -0.05, 0.05, 0.1, 0.2), nrow(dup), replace = TRUE)
  # a repeat of an exact zero would tie with its original on value; give it a distinct non-zero value
  dup$LBSTRESN <- ifelse(dup$LBSTRESN == 0, delta, round(dup$LBSTRESN * (1 + delta), 4))
  dup$LBSTRESC <- as.character(dup$LBSTRESN)
  if ("LBORRES" %in% names(dup)) dup$LBORRES <- dup$LBSTRESC
  max_seq <- tapply(lb$LBSEQ, lb$USUBJID, max)
  shift <- sample(c(-0.5, 0.5), nrow(dup), replace = TRUE)
  dup$VISITNUM <- dup$VISITNUM + shift
  dup$VISIT <- paste("UNSCHEDULED", format(dup$VISITNUM, nsmall = 1, trim = TRUE))
  dup$LBSEQ <- as.numeric(max_seq[dup$USUBJID]) + ave(seq_len(nrow(dup)), dup$USUBJID, FUN = seq_along)
  out <- rbind(lb, dup)
  out[order(out$USUBJID, out$LBSEQ), ]
}

# edge: exposure-record edge cases that the standard data never shows, so that open points in
# ambiguous specs become measurable (a missing last dose date, missing doses, partial start dates).
# Subjects are drawn without overlap from the sorted subject list with a fixed seed:
#   ongoing   all EXENDTC blank (TRTEDT missing, TRTSDT present)
#   nodose1   single-record subjects: that record's EXDOSE missing
#   nodose2   multi-record subjects: first record's EXDOSE missing, later records intact
#   partial2  multi-record subjects: first record's EXSTDTC cut to year-month, later records intact
#   partial1  single-record subjects: EXSTDTC cut to year-month
perturb_edge_ex <- function(ex, seed = 20261028L, p = 0.1) {
  set.seed(seed)
  ex <- ex[order(ex$USUBJID, ex$EXSEQ), ]
  n_rec <- table(ex$USUBJID)
  subj <- sort(unique(ex$USUBJID))
  multi <- subj[n_rec[subj] > 1]
  single <- subj[n_rec[subj] == 1]
  draw <- function(pool, k) { s <- sample(pool, min(k, length(pool))); s }
  k <- ceiling(p * length(subj))
  ongoing <- draw(subj, k)
  rest <- setdiff(multi, ongoing)
  nodose2 <- draw(rest, k); rest <- setdiff(rest, nodose2)
  partial2 <- draw(rest, k)
  s_rest <- setdiff(single, ongoing)
  nodose1 <- draw(s_rest, ceiling(k / 2)); s_rest <- setdiff(s_rest, nodose1)
  partial1 <- draw(s_rest, ceiling(k / 2))
  first <- !duplicated(ex$USUBJID)
  ex$EXENDTC[ex$USUBJID %in% ongoing] <- ""
  ex$EXDOSE[ex$USUBJID %in% nodose1] <- NA_real_
  ex$EXDOSE[first & ex$USUBJID %in% nodose2] <- NA_real_
  cut <- (first & ex$USUBJID %in% c(partial2, partial1))
  ex$EXSTDTC[cut] <- substr(ex$EXSTDTC[cut], 1, 7)
  attr(ex, "groups") <- sapply(list(ongoing = ongoing, nodose1 = nodose1, nodose2 = nodose2,
                                    partial2 = partial2, partial1 = partial1), length)
  ex
}

# aedates: adverse event date edge cases (partial and missing start and end dates), so that date
# imputation and its interaction with the first dose date are exercised. Per record, fixed seed:
#   start: 15% cut to year-month, 7% cut to year, 5% blank (the rest unchanged)
#   end:   15% cut to year-month, 10% blank
perturb_ae_dates <- function(ae, seed = 20261029L) {
  set.seed(seed)
  ae <- ae[order(ae$USUBJID, ae$AESEQ), ]
  n <- nrow(ae)
  u <- runif(n); v <- runif(n)
  s <- ae$AESTDTC
  ae$AESTDTC <- ifelse(u < 0.15, substr(s, 1, 7), ifelse(u < 0.22, substr(s, 1, 4), ifelse(u < 0.27, "", s)))
  e <- ae$AEENDTC
  ae$AEENDTC <- ifelse(v < 0.15, substr(e, 1, 7), ifelse(v < 0.25, "", e))
  ae
}
