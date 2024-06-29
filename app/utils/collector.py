import re
import time

import pandas as pd
import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class StockScraper:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    def remove_blank(self, originText):
        """去除字符串中的空行"""
        new_text = re.sub(r'\n+', '\\n', originText)
        new_text = re.sub(r'\n$', '', new_text)
        new_text = re.sub(r'^\n', '', new_text)
        return new_text

    def get_page_source(self, stock_code):
        """爬取某只股票实时交易数据网址的网页文本内容"""
        stock_code = str(stock_code).zfill(6)  # 确保股票代码是6位的字符串
        if stock_code.startswith('6'):
            stock_code = 'sh' + stock_code
        elif stock_code.startswith('0') or stock_code.startswith('3'):
            stock_code = 'sz' + stock_code
        url = f'https://finance.sina.com.cn/realstock/company/{stock_code}/nc.shtml'

        browser = webdriver.Chrome(options=self.chrome_options)
        browser.get(url)
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "trading"))
            )
        except:
            print(f"等待超时，未找到'trading'元素 - {stock_code}")
        data = browser.page_source
        browser.quit()
        return data

    def parse_stock_data(self, data):
        """解析股票数据"""
        soup = BeautifulSoup(data, 'html.parser')

        print(f"页面标题: {soup.title.string if soup.title else 'No title found'}")

        # 抽取网页中个股股价和涨跌信息
        div = soup.find("div", id="trading")
        if div is None:
            print("无法找到id为'trading'的div元素")
            print("页面内容片段:", soup.get_text()[:500])
            return None
        div_text = div.text
        print("trading div 内容:", div_text[:200])  # 打印前200个字符
        div_text_new = self.remove_blank(div_text)
        trade_lines = div_text_new.splitlines()
        trade_list = []
        for line in trade_lines:
            new_line = line.strip()
            if "：" in new_line:
                trade_list.append(new_line.split("：")[1])
            else:
                trade_list.append(new_line)
        print("提取的交易数据:", trade_list)

        # 抽取网页中个股其他行情信息
        hq_div = soup.find("div", id="hqDetails")
        if hq_div is None:
            print("无法找到id为'hqDetails'的div元素")
            return None
        hq_text = self.remove_blank(hq_div.text)
        print("hqDetails div 内容:", hq_text[:200])  # 打印前200个字符
        hq_lines = hq_text.splitlines()
        hq_list = [hq_lines[i] for i in range(1, len(hq_lines), 2)]
        print("提取的行情数据:", hq_list)

        return trade_list + hq_list

    def scrape_stock(self, stock_code):
        """爬取单只股票数据"""
        try:
            page_source = self.get_page_source(stock_code)
            stock_data = self.parse_stock_data(page_source)
            if stock_data:
                print(f"成功获取股票 {stock_code} 的数据: {stock_data}")
            return stock_data
        except Exception as e:
            print(f"爬取股票 {stock_code} 时发生错误: {str(e)}")
            return None


def read_stock_list(file_path):
    """读取股票列表"""
    df = pd.read_excel(file_path)
    return df.iloc[:, 0].astype(str).str.zfill(6).tolist()


def write_to_excel(data, output_file):
    """将数据写入Excel文件"""
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('股票数据')

    # 设置样式
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True
    style.font = font
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    style.alignment = alignment

    # 写入表头
    headers = ['股票代码', '涨跌额', '涨跌幅', '最新价', '涨停', '跌停', '今开', '最高', '最低', '昨收',
               '成交量', '成交额', '振幅', '换手率', '市净率', '市盈率', '总市值', '流通值', '总股本', '流通股']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, style)

    # 写入数据
    for row, (stock_code, stock_data) in enumerate(data.items(), start=1):
        worksheet.write(row, 0, stock_code)
        for col, value in enumerate(stock_data, start=1):
            worksheet.write(row, col, value)

    workbook.save(output_file)
    print(f"数据已成功写入 {output_file}")


def main():
    stock_list = read_stock_list('D:\\Pycharm_pro\\flask_\\flaskProject1\\static\\GPLIST.xls')
    scraper = StockScraper()
    all_stock_data = {}

    for stock_code in stock_list:
        print(f"\n正在爬取股票 {stock_code} 的数据...")
        stock_data = scraper.scrape_stock(stock_code)
        if stock_data is not None:
            all_stock_data[stock_code] = stock_data
        else:
            print(f"无法获取股票 {stock_code} 的数据")
        time.sleep(2)  # 在每次请求之间添加2秒的延迟

    print(f"\n共成功爬取 {len(all_stock_data)} 只股票的数据")

    if all_stock_data:
        output_file = "D:\\Pycharm_pro\\flask_\\flaskProject1\\static\\data.xls"
        write_to_excel(all_stock_data, output_file)
        print(f"所有股票数据已写入 {output_file}")
    else:
        print("没有成功爬取任何股票数据")


if __name__ == "__main__":
    main()

# D:\\Pycharm_pro\\Spider\\data\\