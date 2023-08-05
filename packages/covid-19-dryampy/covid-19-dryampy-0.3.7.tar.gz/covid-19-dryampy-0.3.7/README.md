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

or something a bit more complex;

```
from covid_19.csse_data import csse_retrieve
from covid_19.us_tests_cdc import us_tests_cdc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


[data, dim_loc, dim_metric] = csse_retrieve().fetch()
test_dat = us_tests_cdc().fetch()

US_ids = dim_loc[dim_loc['Country/Region'] == 'US'].index.tolist()
US_data = data[data['loc_id'].isin(US_ids)]
US_case_data = US_data[US_data['metric_id'] == 0]
US_conf_cases = US_case_data[['counts', 'date']].groupby(['date']).agg(['sum'])
US_conf_cases.columns = ['total_counts']
US_conf_cases['daily_counts'] = np.gradient(US_conf_cases['total_counts'])

US_tests = test_dat[test_dat['status'] == 'complete']
US_tests['test_add'] = US_tests['cdc'] + US_tests['other']
US_tests = US_tests[['date', 'test_add']].groupby(['date']).agg(['sum'])
US_tests.columns = ['daily_counts']
US_tests['total_counts'] = US_tests['daily_counts'].cumsum()

final = US_conf_cases.join(US_tests, lsuffix='_cases', rsuffix='_tests')

ax = plt.gca()
plt.title('US tests and confirmed cases over time')

final2 = final.reset_index()
#final2.plot(kind='line',x='date',y='total_counts_tests', ax=ax, logy=True)
#final2.plot(kind='line',x='date',y='total_counts_cases', color='red', ax=ax, logy=True)
final2.plot(kind='line',x='date',y='total_counts_tests', color='blue', ax=ax)
final2.plot(kind='line',x='date',y='total_counts_cases', color='red', ax=ax)

plt.show()
```

![Image description](https://github.com/DrYampy/covid_19/blob/master/Readme_example.png)

## Authors

* **Steven Yampolsky**

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE.md](LICENSE.md) file for details
