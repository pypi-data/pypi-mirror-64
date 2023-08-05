# covid_19 Data Packages

An assortment of Data Scraping packages from publicly available git repos and website scrapings

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

This package is hosted on Pypi

```
python3 -m pip install covid-19-dryampy
```


### Example Scripts

```
from covid_19.us_tests_cdc import us_tests_cdc

scraper = us_tests_cdc()
print(scraper.fetch())

```

## Authors

* **Steven Yampolsky**

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE.md](LICENSE.md) file for details
