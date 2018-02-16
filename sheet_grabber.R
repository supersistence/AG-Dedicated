
library(readxl) 
library(dplyr)

# Create a function to read all sheets 
read_excel_allsheets <- function(filename) {
  sheets <- readxl::excel_sheets(filename)
  x <-    lapply(sheets, function(X) readxl::read_excel(filename, sheet = X,range = "A2:D45"))
  names(x) <- sheets
  x
}

# Read all of the sheets into a new variable, and bind all rows into a single 
mysheets <- read_excel_allsheets("Marked.ag_2018_12-15-17.xlsx")

# bind all rows into single data fram
mysheets <- as.data.frame(bind_rows(mysheets))

# trim the extra rows from bottom that were captured in the initial read_excel_allsheets function
mysheets <- mysheets[-c(1368:1376), ]
