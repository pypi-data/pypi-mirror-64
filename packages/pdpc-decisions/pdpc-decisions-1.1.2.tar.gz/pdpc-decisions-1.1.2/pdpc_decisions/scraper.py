#  MIT License Copyright (c) 2020. Houfu Ang

"""
Looks over the PDPC website and creates PDPC Decision objects

Requirements:
* Chrome Webdriver to automate web browser
"""
import re
from dataclasses import dataclass
from datetime import datetime

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement


def get_url(item: WebElement):
    link = item.find_element_by_tag_name('a')
    return link.get_property('href')


def get_summary(item: WebElement):
    return item.find_element_by_class_name('rte').text.replace('\n', '. ')


def get_published_date(item: WebElement):
    return datetime.strptime(item.find_element_by_class_name('press__date').text, "%d %b %Y").date()


def get_respondent(item: WebElement):
    link = item.find_element_by_tag_name('a')
    text = link.text
    return re.split(r"\s+[bB]y|[Aa]gainst\s+", text, re.I)[1].strip()


def get_title(item: WebElement):
    return item.find_element_by_tag_name('a').text


class Scraper:
    def __init__(self):
        options = Options()
        # Uncomment the next three lines for a headless chrome
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')

        self.driver = Chrome(options=options)
        self.driver.implicitly_wait(5)

    def refresh_pages(self):
        group_pages = self.driver.find_element_by_class_name('group__pages')
        return group_pages.find_elements_by_class_name('page-number')

    @classmethod
    def scrape(cls, site_url="https://www.pdpc.gov.sg/Commissions-Decisions/Data-Protection-Enforcement-Cases"):
        print('Starting the scrape')
        self = cls()
        result = []
        try:
            self.driver.get(site_url)
            pages = self.refresh_pages()
            for page_count in range(len(pages)):
                pages[page_count].click()
                print("Now at Page ", page_count)
                pages = self.refresh_pages()
                decisions = self.driver.find_elements_by_class_name('press-item')
                for decision in decisions:
                    item = PDPCDecisionItem.from_element(decision)
                    print("Added:", item)
                    result.append(item)
        finally:
            self.driver.close()
            print('Ending scrape.')
        return result


@dataclass
class PDPCDecisionItem:
    published_date: datetime.date
    respondent: str
    title: str
    summary: str
    download_url: str

    @classmethod
    def from_element(cls, decision: WebElement):
        published_date = get_published_date(decision)
        respondent = get_respondent(decision)
        title = get_title(decision)
        summary = get_summary(decision)
        download_url = get_url(decision)
        return cls(published_date, respondent, title, summary, download_url)

    def __str__(self):
        return "PDPCDecision object: {} {}".format(self.published_date, self.respondent)
