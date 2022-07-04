library(rvest)
library(tidyverse)


team_abbr = c('ari','atl','bal','bos','chc','chw','cin','cle','col','det','hou',
              'kc','laa','lad','mia','mil','min','nym','nyy','oak','phi','pit','sd','sf',
              'sea','stl','tb','tex','tor','wsh')


team_name = c('arizona-dbacks','atlanta-braves','baltimore-orioles','boston-redsox','chicago-cubs',
             'chicago-whitesox','cincinattireds','cleveland-guardians','colorado-rockies',
             'detroit-tigers','houston-astros','kansas-city-royals','los-angeles-angels',
             'los-angeles-dodgers','miami-marlins','milwaukee-brewers','minnesota-twins',
             'new-york-mets','new-york-yankees','oakland-athletics','philadelphia-phillies',
             'pittsburgh-pirates','san-diego-padres','san-francisco-giants','seattle-mariners',
             'st-louis-cardinals','tampa-bay-rays','texas-rangers','toronto-bluejays','washington-nationals')
teams <- bind_cols(team_abbr, team_name) 
names(teams) <- c("team_abbr", "team_name")


roster <- tibble()
date <- Sys.time()

for (i in 1:nrow(teams)) {
  
  
  print(teams$team_abbr[i])
  df <- read_html(glue::glue("https://www.espn.com/mlb/team/roster/_/name/{teams$team_abbr[i]}/{teams$team_name[i]}")) %>% 
    html_nodes(css = ".Table__TD") %>% 
    html_text() %>%
    tibble() %>%
    mutate(col = rep(1:9, n()/9),
           id = rep(1:(n()/9), each = 9)) %>%
    as.data.frame() 
  names(df) <- c("val", "col", "id")
  
  
  df <- df %>%
    pivot_wider(id_cols = id, names_from = col, values_from = val) %>%
    mutate(jersey = str_extract(`2`, pattern = "[0-9]+"),
           `2` = str_replace(string = `2`, pattern = "[0-9]+", replacement = "")) %>%
    #separate(`2`, into = c("first_name", "last_name", "suffix", "suffix_2"), sep = " ") %>%
    mutate(team_abbr = teams$team_abbr[i],
           team_name = teams$team_name[i],
           date = date) %>%
    select(`2`:date)
  
  names(df) <- c("name", "pos", "bats", "throws", "age", 
                 "height", "weight", "birthplace", "jersey", "team_abbr", "team_name", "date")
  
  roster <- bind_rows(roster, df)
  
}


write_csv(x = roster, file = "data/DailyMLBRosters.csv", append = T, col_names = T)
