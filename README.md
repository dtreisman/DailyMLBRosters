# DailyMLBRosters

[![mlb-roster-scraper](https://github.com/dtreisman/DailyMLBRosters/actions/workflows/scraper-schedule.yml/badge.svg)](https://github.com/dtreisman/DailyMLBRosters/actions/workflows/scraper-schedule.yml)

There is currently no public data source for daily active MLB rosters. This repo provides a script to pull the current daily active rosters from MLB.com team pages and is scheduled in order to compile a data source for historical active rosters by day.

> The file is located at data/DailyMLBRosters.csv

Unfortunately, MLB team pages do not include position information. Players are grouped by Pitchers, Catchers, Infielders, Outfielders. There also no player IDs but it is likely possible to join this data to other sources on team, first name, and last name in most cases. 

Players are numbered in the order they appear on MLB.com. 
The first available day of rosters is 07/01/2022.

The majority of the code was sourced from [this repo](https://gist.github.com/Jreyno40/947419b81644d4a0fc714866a0e81cde)
