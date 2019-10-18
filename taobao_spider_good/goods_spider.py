import json
import os
import random
import time

import pandas as pd
import requests

from taobao_login import TaobaoLogin

GOODS_EXCEL_PATH = 'taobao_goods.xlsx'


class GoodSpider(object):
    def __init__(self, search_keyword):
        self.search_keyword = search_keyword
        # 超时
        self.timeout = 15
        # 淘宝登陆
        self.taobao = TaobaoLogin()
        self.taobao.login()
        self.headers = {
            'referer': 'https://www.taobao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        #  self.proxies = {
        #             'http': '120.25.239.141:8118'
        # }

    def _get_goods_info(self, url):
        # resp = self.taobao.session.get(url, headers=self.headers, timeout=self.timeout, verify=False, proxies=self.proxies)
        resp = self.taobao.session.get(url, headers=self.headers, timeout=self.timeout, verify=False)
        goods_json = resp.content.decode()
        goods_dict = json.loads(goods_json)
        goods_list = goods_dict['mods']['itemlist']['data']['auctions']
        new_good_list = []
        for goods in goods_list:
            item = {}
            item['title'] = goods.get('raw_title')
            item['price'] = goods.get('view_price')
            item['location'] = goods.get('item_loc')
            item['sales'] = goods.get('view_sales')
            item['comment_url'] = goods.get('comment_url')
            new_good_list.append(item)
        return new_good_list

    def _save_excel(self, new_good_list):
        if os.path.exists(GOODS_EXCEL_PATH):
            df = pd.read_excel(GOODS_EXCEL_PATH)
            df = df.append(new_good_list)
        else:
            df = pd.DateFrame(new_good_list)
        writer = pd.ExcelFile(GOODS_EXCEL_PATH)
        df.to_excel(excel_writer=writer,
                    columns=['title', 'price', 'location', 'sales', 'comment_url'],
                    index=False,
                    encoding='utf-8',
                    sheet_name='Sheet'
        )
        writer.save()
        writer.close()

    def goods_spider(self):
        # 写入数据前先清空之前的数据
        if os.path.exists(GOODS_EXCEL_PATH):
            os.remove(GOODS_EXCEL_PATH)
        for i in range(0, 1):
            url = 'https://s.taobao.com/search?data-key=s&data-value={}&ajax=true&q={}&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20191017&ie=utf8&bcoffset=4&p4ppushleft=%2C48'.format(i*44, self.search_keyword)
            # 获取每天商品数据
            new_good_list = self._get_goods_info(url)
            # 保存到excel中
            self._save_excel(new_good_list)
            time.sleep(random.randint(10, 15))


if __name__ == '__main__':
    goodspider = GoodSpider('避孕套')
    goodspider.goods_spider()


# https://s.taobao.com/search?data-key=s%2Cps&data-value=0%2C1&ajax=true&q=%E9%81%BF%E5%AD%95%E5%A5%97&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20191017&ie=utf8&bcoffset=4&p4ppushleft=%2C48&s=44
# https://s.taobao.com/search?data-key=s&data-value=0&ajax=true&q=%E9%81%BF%E5%AD%95%E5%A5%97&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20191017&ie=utf8&bcoffset=4&p4ppushleft=%2C48&s=0
# https://s.taobao.com/search?data-key=s&data-value=44&ajax=true&q=%E9%81%BF%E5%AD%95%E5%A5%97&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20191017&ie=utf8&bcoffset=4&p4ppushleft=%2C48&s=0
# https://s.taobao.com/search?data-key=s&data-value=88&ajax=true&q=%E9%81%BF%E5%AD%95%E5%A5%97&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20191017&ie=utf8&bcoffset=4&p4ppushleft=%2C48&s=44
# https://s.taobao.com/search?data-key=s&data-value=132&ajax=true&q=%E9%81%BF%E5%AD%95%E5%A5%97&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20191017&ie=utf8&bcoffset=4&p4ppushleft=%2C48&s=88