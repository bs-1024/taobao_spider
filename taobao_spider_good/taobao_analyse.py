import os
import re
from pyecharts import options as opts
from pyecharts.globals import SymbolType
from pyecharts.charts import Pie, Bar, Map, WordCloud
import pandas as pd
import numpy as np
import jieba.analyse
GOODS_EXCEL_PATH = 'taobao_goods.xlsx'
GOODS_STANDARD_EXCEL_PATH = 'taobao_goods_standard.xlsx'
# 清洗词
STOP_WORDS_FILE_PATH = 'stop_words.txt'


class TaobaoAnalyse(object):
    def __init__(self):
        self.data = self._standard_data()
        self.keywords_count_list = self._hot_title_ciyun()

    def _standard_data(self):
        """
        清洗数据
        :return:
        """
        # 1.价格处理
        if not os.path.exists(GOODS_STANDARD_EXCEL_PATH):
            data = pd.read_excel(GOODS_EXCEL_PATH)
            new_sales = []
            for sales in data['sales'].values:
                sales = sales.strip("+|人付款")
                if '万' in sales:
                    num = sales.strip("万")
                    sales = int(float(num)*10000)
                new_sales.append(sales)
            data['sales'] = new_sales

            # 2.地区处理
            raw_location = data['location'].values
            new_location = []
            for location in raw_location:
                if ' ' in location:
                    location = location[:location.find(' ')]
                new_location.append(location)
            data['location'] = new_location

            # 3.生成新的excel
            writer = pd.ExcelWriter(GOODS_STANDARD_EXCEL_PATH)
            # columns参数用于指定生成的excel中列的顺序
            data.to_excel(excel_writer=writer,
                          columns=['title', 'price', 'location', 'sales', 'comment_url'],
                          index=False,
                          encoding='utf-8',
                          sheet_name='Sheet'
            )
            writer.save()
            writer.close()
        return pd.read_excel(GOODS_STANDARD_EXCEL_PATH)

    def _hot_title_ciyun(self):
        """
        词云分析商品标题
        :return:
        """
        # 数据清洗，去掉无效词
        jieba.analyse.set_stop_words(STOP_WORDS_FILE_PATH)
        # 1、词数统计
        keywords_count_list = jieba.analyse.textrank(' '.join(self.data.title), topK=50, withWeight=True)
        print(keywords_count_list)
        word_cloud = (
            WordCloud()
            .add("", keywords_count_list, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts('title="避孕套功能词云TOP50"'))

        )
        word_cloud.render('title-word-cloud.html')
        return keywords_count_list

    def top_20_word(self):
        # 2.1统计词数
        # 取前20高频的关键词
        keywords_count_dict = {i[0]: 0 for i in self.keywords_count_list[:20]}
        cut_words = jieba.cut(' '.join(self.data['title']))
        for word in cut_words:
            for keyword in keywords_count_dict.keys():
                if word == keyword:
                    keywords_count_dict[keyword] += 1
        keywords_list = list(keywords_count_dict.items())
        keywords_list.sort(key=lambda x: x[1], reverse=False)
        keywords_count_dict = dict(keywords_list)
        return keywords_count_dict

    def word_count_bar(self):
        # 2、避孕套商品标题词频分析生成柱状图
        keywords_count_dict = self.top_20_word()
        # 2.2生成柱状图
        keywords_count_bar = (
            Bar()
            .add_xaxis(list(keywords_count_dict.keys()))
            .add_yaxis("", list(keywords_count_dict.values()))
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="避孕套功能TOP20"),
                yaxis_opts=opts.AxisOpts(name="功能"),
                xaxis_opts=opts.AxisOpts(name="商品数")
            )
        )
        keywords_count_bar.render('title-word-count-bar.html')

    def analysis_title_keywords(self, column):
        # 1.获取高频词
        keywords_count_dict = self.top_20_word()
        keywords_column_dict = {i: [] for i in keywords_count_dict.keys()}
        for row in self.data.iterrows():
            for keyword in keywords_column_dict.keys():
                if keyword in row[1].title:
                    # 2、 将标题包含关键字的属性值放在列表中，dict={'keyword1':[价格1,价格2,..]}
                    keywords_column_dict[keyword].append(row[1][column])
        # 3、 求属性值的平均值，dict={'keyword1':平均值1, 'keyword2',平均值2}
        for keyword in keywords_column_dict:
            keywords_column_dict[keyword] = sum(keywords_column_dict[keyword]) / len(keywords_column_dict[keyword])
        # 4、 根据平均值排序，从小到大
        list1 = list(keywords_column_dict.items())
        list1.sort(key=lambda x: x[1], reverse=False)
        # 5、截取平均值最高的20个关键字
        keywords_column_dict = dict(list1[-20:])
        return keywords_column_dict

    def word_price_bar(self):
        """
        分析标题关键字与平均价格关系
        :return:
        """
        keywords_column_dict = self.analysis_title_keywords('price')
        keywords_price_bar = (
            Bar()
            .add_xaxis(list(keywords_column_dict.keys()))
            .add_yaxis("", list(keywords_column_dict.values()))
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="避孕套商品功能与平均售价TOP20"),
                yaxis_opts=opts.AxisOpts(name="功能"),
                xaxis_opts=opts.AxisOpts(name="平均售价")
            )
        )
        keywords_price_bar.render('title-word-price-bar.html')

    def sale_count_bar(self):
        """
        标题高频关键字与平均销量关系
        :return:
        """
        keywords_column_dict = self.analysis_title_keywords('sales')
        keywords_sales_bar = (
            Bar()
                .add_xaxis(list(keywords_column_dict.keys()))
                .add_yaxis("", list(keywords_column_dict.values()))
                .reversal_axis()
                .set_series_opts(label_opts=opts.LabelOpts(position="right"))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="避孕套商品功能与平均销量TOP20"),
                yaxis_opts=opts.AxisOpts(name="功能"),
                xaxis_opts=opts.AxisOpts(name="平均销量")
            )
        )
        keywords_sales_bar.render('title-word-sales-bar.html')

    def analysis_price(self):
        # 设置切分区域
        price_list_bins = [0, 20, 40, 60, 80, 100, 120, 150, 200, 1000000]
        # 设置切分后对应标签
        price_list_labels = ['0-20', '21-40', '41-60', '61-80', '81-100', '101-120', '121-150', '151-200', '200以上']
        data_labels_list = pd.cut(self.data['price'], bins=price_list_bins, labels=price_list_labels, include_lowest=True)
        # 生成一个以listLabels为顺序的字典，这样就不需要后面重新排序
        data_count = {i: 0 for i in price_list_labels}
        # 统计结果
        for value in data_labels_list:
            # get(value, num)函数的作用是获取字典中value对应的键值, num=0指示初始值大小。
            data_count[value] = data_count.get(value) + 1
        bar = (
            Bar()
            .add_xaxis(list(data_count.keys()))
            .add_yaxis("", list(data_count.values()))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="避孕套商品价格区间分布柱状体"),
                yaxis_opts=opts.AxisOpts(name="个商品"),
                xaxis_opts=opts.AxisOpts(name="商品售价：元")
            )
        )
        bar.render('price-bar.html')
        # 生成饼图
        age_count_list = [list(z) for z in zip(data_count.keys(), data_count.values())]
        pie = (
            Pie()
            .add("", age_count_list)
            .set_global_opts(title_opts=opts.TitleOpts(title="避孕套商品价格区间饼图"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        pie.render('price-pie.html')

    def analysis_sales(self):
        """
        销量情况分布
        :return:
        """
        # 设置切分区域
        listBins = [0, 1000, 5000, 10000, 50000, 100000, 1000000]
        # 设置切分后对应标签
        listLabels = ['一千以内', '一千到五千', '五千到一万', '一万到五万', '五万到十万', '十万以上']
        sales_count_list = pd.cut(self.data['price'], bins=listBins, labels=listLabels, include_lowest=True)
        # 生成一个以listLabels为顺序的字典，这样就不需要后面重新排序
        data_count = {i: 0 for i in sales_count_list}
        # 统计结果
        for value in sales_count_list:
            # get(value, num)函数的作用是获取字典中value对应的键值, num=0指示初始值大小。
            data_count[value] = data_count.get(value) + 1

        # 生成柱状图
        bar = (
            Bar()
            .add_xaxis(list(data_count.keys()))
            .add_yaxis("", list(data_count.values()))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="避孕套商品销量区间分布柱状图"),
                yaxis_opts=opts.AxisOpts(name="个商品"),
                xaxis_opts=opts.AxisOpts(name="销售件数")
            )
        )
        bar.render('sales-bar.html')
        # 生成饼图
        age_count_list = [list(z) for z in zip(data_count.keys(), data_count.values())]
        pie = (
            Pie()
            .add("", age_count_list)
            .set_global_opts(title_opts=opts.TitleOpts(title="避孕套商品销量区间饼图"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        pie.render('sales-pie.html')

    def analysis_province_sales(self):
        """
        商品价格与销量关系分析
        :return:
        """
        province_sales = self.data['location'].value_counts()
        province_sales_list = [list(item) for item in province_sales.items()]
        # 1.1 生成热力图
        province_sales_sum_map = (
            Map()
            .add("前两千款避孕套商家数量全国分布图", province_sales_list, "china")
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=647),
            )
        )
        province_sales_sum_map .render('province-sales-sum-map.html')
        # 1.2 生成柱状图
        province_sales_sum_bar = (
            Bar()
            .add_xaxis(province_sales.index.tolist())
            .add_yaxis("", province_sales.values.tolist(), category_gap="50%")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="前两千款避孕套商家数量地区柱状图"),
                yaxis_opts=opts.AxisOpts(name="商家数量"),
                xaxis_opts=opts.AxisOpts(name="地区", axislabel_opts={"rotate": 90})
            )
        )
        province_sales_sum_bar .render('province-sales-sum-bar.html')

        # 3、全国商家省份平均销量分布
        province_sales_mean = self.data.pivot_table(index='location', values='sales', aggfunc=np.mean)
        # 根据平均销量排序
        province_sales_mean.sort_values('sales', inplace=True, ascending=False)
        province_sales_mean_list = [list(item) for item in zip(province_sales_mean.index, np.ravel(province_sales_mean.values))]

        print(province_sales_mean_list)
        # 3.1 生成热力图
        province_sales_mean_map = (
            Map()
                .add("前两千款避孕套商家平均销量全国分布图", province_sales_mean_list, "china")
                .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=1536),
            )
        )
        province_sales_mean_map.render('province-sales-mean-map.html')
        # 3.2 生成柱状图
        province_sales_mean_bar = (
            Bar()
            .add_xaxis(province_sales_mean.index.tolist())
            .add_yaxis("", list(map(int, np.ravel(province_sales_mean.values))), category_gap="50%")
            .set_global_opts(
                title_opts=opts.TitleOpts(title="前两千款避孕套各省商家平均销量地区柱状图"),
                yaxis_opts=opts.AxisOpts(name="平均销量"),
                xaxis_opts=opts.AxisOpts(name="地区", axislabel_opts={"rotate": 90})
            )
        )
        province_sales_mean_bar.render('province-sales-mean-bar.html')


if __name__ == '__main__':
    taobao_analyse = TaobaoAnalyse()
    taobao_analyse.word_count_bar()
    taobao_analyse.word_price_bar()
    taobao_analyse.sale_count_bar()
    taobao_analyse.analysis_price()
    taobao_analyse.analysis_sales()
    taobao_analyse.analysis_province_sales()
























