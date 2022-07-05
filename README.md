# DailyMLBRosters

[![mlb-roster-scraper](https://github.com/dtreisman/DailyMLBRosters/actions/workflows/scraper-schedule.yml/badge.svg)](https://github.com/dtreisman/DailyMLBRosters/actions/workflows/scraper-schedule.yml)

There is currently no public data source for daily active MLB rosters that includes the player IDs *and* specific player positions (rather than the general categories the MLB api provides). This repo provides a script to pull the current daily active rosters from ESPN team roster pages and is scheduled in order to compile a data source for historical active rosters by day with specific position information.

> The file is located at data/DailyMLBRosters.csv

The first available day of rosters is 07/05/2022. Data is updated at 20:00 UTC.

Many lines of code were sourced from [this repo](https://github.com/canovasjm/covid-19-san-juan) and [this repo](https://github.com/nflverse/nflverse-data). 
