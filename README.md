# fred-processing

This repository has scripts for obtaining and processing some data from
[FRED](https://fred.stlouisfed.org/ "“Federal Reserve Economic Data | FRED | St. Louis Fed”. Retrieved October 27, 2017.").
The main script is `proc.py`, which does tags fetching, series ID fetching, and
the actual data gathering.

`modify_sql.py` modifies the output of `proc.py` by parsing each line and
transforming it. This allows us to download the data from the API once, then
transform it later. (It might have been better to download the data in a more
"neutral" format like a TSV so that the parsing would have been simpler.)

## License

CC0

## See also

- [penn-world-table-data](https://github.com/riceissa/penn-world-table-data)
- [maddison-project-data](https://github.com/riceissa/maddison-project-data)
- [world development indicators](https://github.com/riceissa/world-development-indicators)
- [total-economy-database](https://github.com/riceissa/total-economy-database)
