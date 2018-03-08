import requests
import re
from lxml import etree


class StockCode(object):
    def __init__(self):
        self.start_url = "http://quote.eastmoney.com/stocklist.html#sh"
        self.headers = {
            "User-Agent": ":Mozilla/5.0 (Windows NT 6.1; WOW64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }

    def parse_url(self):
        response = requests.get(self.start_url, headers=self.headers)
        if response.status_code == 200:
            return etree.HTML(response.content)

    def get_code_list(self, response):
        node_list = response.xpath('//*[@id="quotesearch"]/ul[1]/li')
        code_list = []
        for node in node_list:
            try:
                code = re.match(r'.*?\((\d+)\)', etree.tostring(node).decode()).group(1)
                code_list.append(code)
            except:
                continue
        return code_list

    def run(self):
        html = self.parse_url()
        return self.get_code_list(html)


class DownloadStock(object):
    def __init__(self, code):
        self.code = code
        self.start_url = "http://quotes.money.163.com/trade/lsjysj_" + self.code + ".html"
        self.headers = {
            "User-Agent": ":Mozilla/5.0 (Windows NT 6.1; WOW64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }

    def download(self, start_date, end_date):
        print('Now downloading stock code:', self.code)
        download_url = "http://quotes.money.163.com/service/chddata.html?code=0" \
                       + self.code + "&start=" + start_date + "&end=" + end_date \
                       + "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
        data = requests.get(download_url)
        title = 'D:/data/' + self.code + '.csv'  # SET DOWNLOAD PATH AND FILE NAME
        f = open(title, 'wb')
        for chunk in data.iter_content(chunk_size=10000):
            if chunk:
                f.write(chunk)
        f.close()
        print('Download completed')


code = StockCode()
code_list = code.run()
code_list_sz = [code for code in code_list if 600000 <= int(code) <= 609999]  # Get stock codes start with '60'
for code in code_list_sz:
    download = DownloadStock(code)
    download.download('20170101', '20171231')  # Set download date

