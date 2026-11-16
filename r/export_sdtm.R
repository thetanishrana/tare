# Export the pharmaversesdtm domains Tare tasks use to parquet (data/sdtm/, git-ignored).
# Run from the repo root:  Rscript r/export_sdtm.R
suppressPackageStartupMessages(library(arrow))
dir.create("data/sdtm", recursive = TRUE, showWarnings = FALSE)
for (d in c("dm", "ex", "ae", "ds", "lb", "vs", "sc_ophtha")) {
  write_parquet(as.data.frame(getExportedValue("pharmaversesdtm", d)), file.path("data/sdtm", paste0(d, ".parquet")))
}
