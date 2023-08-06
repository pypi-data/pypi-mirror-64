from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup
class Scraping:
    def __init__(self, url):        
        self.url = url

    def scrapingNAV(self):
        webopen = req(self.url)
        page_html = webopen.read()
        webopen.close()

        #print(page_htnl)
        data = soup(page_html, 'html.parser')
        nav = data.find(id="ctl00_ContentPlaceHolder1_lblNAV").text
        fundCode = data.find(id="ctl00_ContentPlaceHolder1_lblFundCode").text
        lastUpdateDate = data.find(id="ctl00_ContentPlaceHolder1_lblLastUpdateDate").text
        
        return fundCode, nav, lastUpdateDate




