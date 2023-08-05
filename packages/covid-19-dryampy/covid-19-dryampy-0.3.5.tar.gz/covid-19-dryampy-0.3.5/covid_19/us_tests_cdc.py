import requests
import datetime
import numpy as np
from bs4 import BeautifulSoup


class us_tests_cdc:

    def __init__(self):

        self.url = 'https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/testing-in-us.html'

    def fetch(self):

        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        table = self._format(table)
        return table

    def _format(self, table):

        converted = []

        table = self._table_data_text(table)

        for i in range(len(table)):
            if i == 0:
                converted.append(['date', 'cdc', 'other', 'status'])
            else:
                new_time = datetime.datetime.strptime(table[i][0]+'/20', '%m/%d/%y').date()
                cdc_testing = table[i][1].split('‡')[0]
                if cdc_testing == '':
                    cdc_testing = 0
                else:
                    cdc_testing = np.int(cdc_testing)
                outside_lab = np.int(table[i][2].split('§')[0])
                if len(table[i][2].split('§')) > 1:
                    status = 'in_progress'
                else:
                    status = 'complete'

                converted.append([new_time, cdc_testing, outside_lab, status])

        return converted

    def __row_get_data_text(self, tr, coltag='td'):  # td (data) or th (header)
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]

    def _table_data_text(self, table):
        """Parses a html segment started with tag <table> followed
        by multiple <tr> (table rows) and inner <td> (table data) tags.
        It returns a list of rows with inner columns.
        Accepts only one <th> (table header/data) in the first row.
        """

        rows = []
        trs = table.find_all('tr')
        headerow = self.__row_get_data_text(trs[0], 'th')
        if headerow:  # if there is a header row include first
            rows.append(headerow)
            trs = trs[1:]
        for tr in trs:  # for every table row
            rows.append(self.__row_get_data_text(tr, 'td'))  # data row
        return rows
