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
        return fundCode, nav

if __name__ == '__main__':
    mutual = ["https://www.wealthmagik.com/FundInfo/FundProfile-BBLAM-EQF-BKA-%E0%B8%81%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B8%E0%B8%99%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B8%9A%E0%B8%B1%E0%B8%A7%E0%B9%81%E0%B8%81%E0%B9%89%E0%B8%A7", \
        "https://www.wealthmagik.com/FundInfo/FundProfile-BBLAM-FIFEQ-B%20INNOTECH-%E0%B8%81%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B8%E0%B8%99%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B8%9A%E0%B8%B1%E0%B8%A7%E0%B8%AB%E0%B8%A5%E0%B8%A7%E0%B8%87%E0%B9%82%E0%B8%81%E0%B8%A5%E0%B8%9A%E0%B8%AD%E0%B8%A5%E0%B8%AD%E0%B8%B4%E0%B8%99%E0%B9%82%E0%B8%99%E0%B9%80%E0%B8%A7%E0%B8%8A%E0%B8%B1%E0%B9%88%E0%B8%99%E0%B9%81%E0%B8%A5%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%84%E0%B9%82%E0%B8%99%E0%B9%82%E0%B8%A5%E0%B8%A2%E0%B8%B5",\
        "https://www.wealthmagik.com/FundInfo/FundProfile-KrungsriAsset-FIFEQ-KF%20GTECH-%E0%B8%81%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B8%E0%B8%99%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B8%81%E0%B8%A3%E0%B8%B8%E0%B8%87%E0%B8%A8%E0%B8%A3%E0%B8%B5%E0%B9%82%E0%B8%81%E0%B8%A5%E0%B8%9A%E0%B8%AD%E0%B8%A5%E0%B9%80%E0%B8%97%E0%B8%84%E0%B9%82%E0%B8%99%E0%B9%82%E0%B8%A5%E0%B8%A2%E0%B8%B5%E0%B8%AD%E0%B8%B4%E0%B8%84%E0%B8%A7%E0%B8%B4%E0%B8%95%E0%B8%B5%E0%B9%89",\
        "https://www.wealthmagik.com/FundInfo/FundProfile-KAsset-FIXMT-K%20FIXED-%E0%B8%81%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B8%E0%B8%99%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B9%80%E0%B8%84%20%E0%B8%95%E0%B8%A3%E0%B8%B2%E0%B8%AA%E0%B8%B2%E0%B8%A3%E0%B8%AB%E0%B8%99%E0%B8%B5%E0%B9%89",\
        "https://www.wealthmagik.com/FundInfo/FundProfile-KrungsriAsset-EQF-KFTSTAR%20D-%E0%B8%81%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B8%E0%B8%99%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B8%81%E0%B8%A3%E0%B8%B8%E0%B8%87%E0%B8%A8%E0%B8%A3%E0%B8%B5%E0%B9%84%E0%B8%97%E0%B8%A2%E0%B8%AD%E0%B8%AD%E0%B8%A5%E0%B8%AA%E0%B8%95%E0%B8%B2%E0%B8%A3%E0%B9%8C%E0%B8%9B%E0%B8%B1%E0%B8%99%E0%B8%9C%E0%B8%A5",\
        "https://www.wealthmagik.com/FundInfo/FundProfile-KAsset-FIXST-K%20SF-%E0%B8%81%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B8%E0%B8%99%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B9%80%E0%B8%84%20%E0%B8%95%E0%B8%A3%E0%B8%B2%E0%B8%AA%E0%B8%B2%E0%B8%A3%E0%B8%AB%E0%B8%99%E0%B8%B5%E0%B9%89%E0%B8%A3%E0%B8%B0%E0%B8%A2%E0%B8%B0%E0%B8%AA%E0%B8%B1%E0%B9%89%E0%B8%99",\
        "https://www.wealthmagik.com/FundInfo/FundProfile-SCBAM-LTF-SCBLT2-%E0%B8%81%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B8%E0%B8%99%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B9%84%E0%B8%97%E0%B8%A2%E0%B8%9E%E0%B8%B2%E0%B8%93%E0%B8%B4%E0%B8%8A%E0%B8%A2%E0%B9%8C%E0%B8%AB%E0%B8%B8%E0%B9%89%E0%B8%99%E0%B8%A3%E0%B8%B0%E0%B8%A2%E0%B8%B0%E0%B8%A2%E0%B8%B2%E0%B8%A7%20%E0%B8%9E%E0%B8%A5%E0%B8%B1%E0%B8%AA",\
        "https://www.wealthmagik.com/FundInfo/FundProfile-SCBAM-FIFMIX-SCBROBOA-%E0%B8%81%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B8%E0%B8%99%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B9%84%E0%B8%97%E0%B8%A2%E0%B8%9E%E0%B8%B2%E0%B8%93%E0%B8%B4%E0%B8%8A%E0%B8%A2%E0%B9%8C%20%E0%B9%82%E0%B8%81%E0%B8%A5%E0%B8%9A%E0%B8%AD%E0%B8%A5%E0%B9%82%E0%B8%A3%E0%B9%82%E0%B8%9A%E0%B8%95%E0%B8%B4%E0%B8%81%E0%B8%AA%E0%B9%8C%20%E0%B8%8A%E0%B8%99%E0%B8%B4%E0%B8%94%E0%B8%AA%E0%B8%B0%E0%B8%AA%E0%B8%A1%E0%B8%A1%E0%B8%B9%E0%B8%A5%E0%B8%84%E0%B9%88%E0%B8%B2",\
        "https://www.wealthmagik.com/FundInfo/FundProfile-TFUND-EQF-T%20PRIMELOWBETA-%E0%B8%81%E0%B8%AD%E0%B8%87%E0%B8%97%E0%B8%B8%E0%B8%99%E0%B9%80%E0%B8%9B%E0%B8%B4%E0%B8%94%E0%B8%98%E0%B8%99%E0%B8%8A%E0%B8%B2%E0%B8%95%20Prime%20Low%20Beta"]


    for key in mutual:    
        scraping = Scraping(key)
        fundCode, nav = scraping.scrapingNAV()
        
        print(fundCode + " : " + nav)    



