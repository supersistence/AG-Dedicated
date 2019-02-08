library(rvest)



# # Create a list of all the urls to be parsed based on the TMKs of dedicated parcels
# urls <- sprintf("http://qpublic9.qpublic.net/hi_honolulu_display.php?county=hi_honolulu&KEY=%s", dedications$TMK) 

for(i in (dedications$TMK[5663])) {
  
  # Main page on QPublic Parcel Data
  html <- read_html(sprintf("http://qpublic9.qpublic.net/hi_honolulu_display.php?county=hi_honolulu&KEY=%s",i))
  
  #Historical assessments page of QPublic
  html2 <- read_html(sprintf("http://qpublic9.qpublic.net/hi_honolulu_display.php?KEY=%s&show_history=1&",i))
  
  # land information print page
  html3 <- read_html(sprintf("http://qpublic9.qpublic.net/hi_honolulu_land_print.php?KEY=%s", i))
  
  # Create empty list to add table data into
  tbls <- list()
  
  # Specify which table(s) from html you want to grab & name them something useful (e.g., Ownership, ... , Uses)
  
  # Owner and Parcel Information
  tbls$Ownership <- html %>%
    html_nodes("table") %>%
    .[3] %>%
    html_table(fill = TRUE) %>%
    .[[1]]
  tbls$Ownership <- tbls$Ownership[-1,] # remove redundant header
  tbls$Ownership <- subset( tbls$Ownership, select = 1:2)
 # View(tbls$Ownership)
  
  # Assessment Information, grabs full assessment history from html2 urls
  tbls$Assessment <- html2 %>%
    html_nodes("table") %>%
    .[5] %>%
    html_table(fill = TRUE) %>%
    .[[1]]
  tbls$Assessment <- tbls$Assessment[-1,] # remove redundant header
  tbls$Assessment <- head(tbls$Assessment, -1) # remove note at bottom ("2019 amended values not..." )
  View(tbls$Assessment)
  
  #  Appeal Information
  tbls$Land <- html %>%
    html_nodes("table") %>%
    .[6] %>%
    html_table(fill = TRUE) %>%
    .[[1]]
#  View(tbls$Appeal)
  
  #  Land Information
  tbls$Land <- html %>%
    html_nodes("table") %>%
    .[7] %>%
    html_table(fill = TRUE) %>%
    .[[1]]
#  View(tbls$Land)
  
  # Agricultural Assessment Information
  tbls$AgAssess <- html %>%
    html_nodes("table") %>%
    .[8] %>%
    html_table(fill = TRUE) %>%
    .[[1]]
#  View(tbls$AgAssess)
  
  # Agricultural Assessment Information (print page)
  tbls$AgAssessP <- html3 %>%
    html_nodes("table") %>%
    .[4] %>%
    html_table(fill = TRUE) %>%
    .[[1]]
 # View(tbls$AgAssessP)
  
  # Historical Tax Information
  tbls$AllTax <- html2 %>%
    html_nodes("table") %>%
    .[15] %>%
    html_table(fill = TRUE) %>%
    .[[1]]
 # View(tbls$AllTax)
  
  # # Historical Tax Information
  # tbls$AllTax <- html2 %>%
  #   html_nodes("table") %>%
  #   .[15] %>%
  #   html_table(fill = TRUE) %>%
  #   .[[1]]
  # View(tbls$AllTax)
  
}

