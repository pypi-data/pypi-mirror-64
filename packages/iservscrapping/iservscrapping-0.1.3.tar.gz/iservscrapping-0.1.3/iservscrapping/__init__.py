"""
This is a scrapper to get some data from iserv servers providing Untis plans.
Copyright (C) Alwin Lohrie / Niwla23, MIT Licensed
"""

import re
import requests
from bs4 import BeautifulSoup
import requests_cache
from string import Template

requests_cache.install_cache('cache', expire_after=3600)


def remove_duplicates(lis):
    """
    This function removes duplicates from a list.
    """
    y, s = [], set()
    for t in lis:
        w = tuple(sorted(t)) if isinstance(t, list) else t
        if w not in s:
            y.append(t)
            s.add(w)
    return y


numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


class Iserv:
    def __init__(self, url, username, password):
        self.username = username
        self.password = password
        self.time_to_next_substitution_request = 0
        self.url = url
        self.session = requests.Session()

    def get_untis_substitution_plan(self, path, schoolclass, request_delay_min=5):
        """
        Gets untis substitution plan data for a given class.
        """
        headers = {'User-Agent': 'Mozilla/5.0'}
        payload = {'_username': self.username, '_password': self.password}
        self.session.post(self.url + '/iserv/login_check', headers=headers, data=payload)
        # chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        res = self.session.get(self.url + path)
        plan_soup = BeautifulSoup(res.text, 'lxml')
        rows = []
        for row in plan_soup.find_all('tr', class_='list'):
            pattern = Template('^$number.*$char.*$')
            rowlist = []
            for i in row:
                rowlist.append(i.text)
            if len(rowlist) < 2:
                continue
            currentclass = rowlist[4].strip()

            patternresult = re.search(pattern.safe_substitute(number=schoolclass[0], char=schoolclass[1]), currentclass)
            if patternresult and currentclass[0] in numbers or currentclass == schoolclass:
                text = []
                for cell in row.find_all('td'):
                    if schoolclass not in cell.text and cell.text.isspace() is not True:
                        temptext = ""
                        for test in cell.children:
                            try:
                                for test2 in test.children:
                                    temptext = temptext + str(test2)
                            except AttributeError:
                                temptext = temptext + test
                        text.append(temptext)
                rows.append(text)
            rows = list(filter(lambda x: x, rows))
        rows = remove_duplicates(i if isinstance(i, list) else i for i in remove_duplicates(rows))
        date = plan_soup.find('div', class_="mon_title").text.split(" ")[0]
        return rows, date

    def get_next_tests_formatted(self, path="/iserv"):
        """
        Same as get_next_tests() but does not parse the data, just gives a string per test, not a dict
        """
        test_list = []

        res = self.session.get(self.url + path)
        soup = BeautifulSoup(res.text, 'lxml')

        tests = soup.find("ul", "pl mb0")

        for i in tests.find_all("li"):
            test_list.append(i.text)
        return test_list

    def get_next_tests(self, path="/iserv"):
        """
        Returns the next classtests from iserv. path is the url to search for the box.
        """
        test_list = []

        res = self.session.get(self.url + path)
        soup = BeautifulSoup(res.text, 'lxml')

        tests = soup.find("ul", "pl mb0")

        for i in tests.find_all("li"):
            entry = {}
            parsed = i.text.split(" - ")
            entry['date'] = parsed[0]
            entry['time'] = parsed[1]
            entry['class'] = parsed[2]
            entry['subject'] = parsed[3]
            test_list.append(entry)
        return test_list
