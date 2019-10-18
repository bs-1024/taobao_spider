import json

import requests

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
#     # 'Cookie': 'thw=cn; cna=DMOkFY0u/mACAXkI4x2DMa1Q; t=d9d33f6a427cb179bb81ce5a193fd3a9; v=0; cookie2=178e702d9dd50cefc195c80c9c52166e; _tb_token_=55353e11e3d36; _m_h5_tk=e6993e36a708787e937f46df2cc4e95d_1571246750653; _m_h5_tk_enc=5b1d3f801915acbf8fdff88c9aeaad9f; isg=BObmQ7lBh9Z9Z1OtfcJQshwMN1yobyvmqV8ecdCPyInkU4dtOFJTkPILr09feyKZ; l=dB_gPEfqqEm0xG_zBOCgCuI8L17OSIRAguPRwCmXi_5IL6L_RyQOkgYPhFp6VjWfT18B4cULngv9-etkVZqNApDgcGAw_xDc.'
# }
#
# # url = 'https://www.taobao.com'
# #
# #
# # url1 = 'https://s.taobao.com/search?q=xiezi&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=4&p4ppushleft=1%2C48&ntoffset=4&s=0'
# # resp = requests.get(url1, headers=headers)
# # print(resp.text)
#
# url = 'https://odin.re.taobao.com/m/Nwalltbuad?sbid=sem2_kgb_activity&ignore=CATID,RANKINFO,MATCHTYPE&pvid=_TL-41832&refpid=mm_26632258_3504122_32554087&clk1=1119b67da62e20d5e8962adff2729d49&pid=430680_1006&keyword=女装2019新款潮&count=60&offset=0&relacount=8&t=157126647797'
# aaa = 'https://odin.re.taobao.com/m/Nwalltbuad?sbid=sem2_kgb_activity&ignore=CATID,RANKINFO,MATCHTYPE&pvid=_TL-41832&refpid=mm_26632258_3504122_32554087&clk1=1119b67da62e20d5e8962adff2729d49&pid=430680_1006&keyword=女装2019新款潮&count=60&offset=60&relacount=8&t=1571267142066&callback=mn9'
# resp = requests.get(url, headers=headers)
# html_str = resp.content.decode()
# html_dict = json.loads(html_str)
# print(html_dict['code'])

# data = '1人付款款+'
# data = data.strip("+|人付款")
# print(data)


# d = {'a': 1, 'c': 3, 'b': 2}  # 首先建一个字典d
#
# d.items()  # 得到: dict_items([('a', 1), ('c', 3), ('b', 2)])
# print(list(d))
# print(list(d.items()))
# L = list(d.items())  # 得到列表: L=[('a', 1), ('c', 3), ('b', 2)]
#
# L.sort(key=lambda x: x[1], reverse=False)  # 按列表中，每一个元组的第二个元素从小到大排序。
# # x代表从L中遍历出的一个元组
# print(L)














