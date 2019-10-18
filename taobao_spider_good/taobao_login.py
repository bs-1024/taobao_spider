import json
import os
import re

import requests
COOKIES_FILE_PATH = 'taobao_login_cookies.txt'


class TaobaoLogin(object):
    """
    login登陆成功-->含有token链接-->此链接申请st码-->st链接验证信息
    """
    def __init__(self):
        # 判断是否需要验证码的url, post请求，
        self.nick_check_url = 'https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8'
        # 验证淘宝用户名密码URL
        self.login_url = 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fwww.taobao.com%2F'
        # 访问st码URL
        self.vst_url = 'https://login.taobao.com/member/vst.htm?st={}'
        # 淘宝个人 主页
        self.my_taobao_url = 'http://i.taobao.com/my_taobao.htm'

        # 淘宝用户名
        self.username = 18520968024
        # ua
        self.ua = '121#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'
        # 加密密码
        self.TPL_password2 = '2ee02007770f2f650e5a2bb049e4b307b2052145c00f36d9743441f00a2e25fc427ac98acd8a5d04c069acbf3152b81522a4953d4e61e761c6bdf9b2a67a33c70ac844855bc210f894f0d081e436dfde5658ed36eadfa4ccb279f4259dfb4ebd3fa6b33d5ed19984c36f6b537c4e7d2f50e1c0a6bbdb310c27b79a3c957df3a5'
        # 请求超时时间
        self.timeout = 3
        # session对象，用于共享cookies
        self.session = requests.Session()

    def _nick_check(self):
        data = {
            'username': self.username,
            'ua': self.ua
        }
        try:
            resp = self.session.post(self.nick_check_url, data=data, timeout=self.timeout)
        except Exception as e:
            print("失败原因{}".format(e))
            return True
        needcode = resp.json()['needcode']
        print("是否需要验证码：%s" % '是' if needcode else '否')
        return needcode

    def _verify_password(self):
        """
        登陆，包含headers和body
        :return:
        """
        verify_password_headers = {
             'Connection': 'keep-alive',
             'Cache-Control': 'max-age=0',
             'Origin': 'https://login.taobao.com',
             'Upgrade-Insecure-Requests': '1',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
             'Content-Type': 'application/x-www-form-urlencoded',
             'Referer': 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3Dxiezi1%26imgfile%3D%26commend%3Dall%26ssid%3Ds5-e%26search_type%3Ditem%26sourceId%3Dtb.index%26spm%3Da21bo.2017.201856-taobao-item.1%26ie%3Dutf8%26initiative_id%3Dtbindexz_20170306',
             # 'Cookie': '_uab_collina=157124118839121665791043; thw=cn; v=0; t=ef08515147d52838723ffb8a1d82d59d; cookie2=1102b2fa44d667c1c5b38294236747d5; _tb_token_=7e5d5831e1ee3; cna=uyouFiw/VwICAd9JPIIEFoKO; isg=BOnpxOzlkL-KV6wLxzSnW-sb-JWDHtyPEv5B6IveZVAPUglk0wbtuNdAFLZBUXUg; l=dBgJleScq67JBy9sBOCanurza77OSIRYYuPzaNbMi_5CJ6T_xo_OkgXNMF96VjS1g2TB4cULng29-etkZ7N1b7IpXUJs1AkxGe3oGiMSExf..'
            # 'cookie':'_uab_collina=157128303221499827697535; thw=cn; cna=kY0uFkyGzSACAd9JPKnQ0qyk; v=0; t=8162bb87b78a6606751cc076aef88546; cookie2=17c2e7bec6e989fc1d80eebb9c4e6756; _tb_token_=37535eee1e557; l=dB_qJs7Rq6WnfnJoBOfiVuI8L17tiIOfhsPzw4OG2ICP_7AWkB55WZIuaBbXCnGVn65MS3P11tW0BoYZ_y4Fh9KwNBQ7XPQlKpLh.; isg=BCcnQvg0Npmk8rIVdlXz72WltlsxBPrpYUD-gvmVRrbO6EGqB38X3wkqCqhTANMG'
        }
        verify_password_data = {
            'TPL_username': self.username,
            'ncoToken': '1f9836da2b30e3c246783e2e70d7482caf654644',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': 0,
            'newlogin': 0,
            'TPL_redirect_url': 'http://www.taobao.com/',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'loginType': '3',
            'gvfdcname': '10',
            'TPL_password_2': self.TPL_password2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'oslanguage': 'zh-CN',
            'sr': '1440*900',
            'naviVer': 'chrome|77.038659',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'osPF': 'Win32',
            'appkey': '00000000',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.201864-2.d1.5af911d9pqPahL&f=top&redirectURL=http://www.taobao.com/&useMobile=true',
            'showAssistantLink': 'false',
            'um_token': 'TE8FCA46154D480E51A8A39F962B8072E914E9C89C1B272A36EF7C5DF15',
            'ua': self.ua
        }

        resp = self.session.post(self.login_url, headers=verify_password_headers, data=verify_password_data, timeout=self.timeout)
        st_token_url = re.search(r'<script src="(.*?token.*?)"></script>', resp.text)
        if st_token_url:
            return st_token_url.group(1)
        else:
            return False

    def _apply_st(self):
        """
        申请st码
        :return: st码
        """
        apply_st_url = self._verify_password()
        st_code = None
        try:
            resp = self.session.get(apply_st_url)
            st_code = re.findall(r'"data":{"st":"(.*?)"}', resp.text)
        except Exception as e:
            print(e)
        if st_code:
            print('获取st码成功，st码：{}'.format(st_code[0]))
            return st_code[0]
        else:
            raise RuntimeError('获取st码失败')

    def login(self):
        """
        登陆
        :return:
        """
        # 加载cookies文件
        if self._load_cookies():
            print("已经有cookies了")
            return True
        st = self._apply_st()
        headers = {
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        my_taobao = None
        try:
            resp = self.session.get(self.vst_url.format(st), headers=headers)
            my_taobao = re.findall(r'top.location.href = "(.*?)"', resp.text)
        except Exception as e:
            raise e
        if my_taobao:
            self._serialization_cookies()
            print(my_taobao[0])
        else:
            print('没有获取到用户名')

    def _serialization_cookies(self):
        """
        序列化
        保存cookies到文件中
        :return:
        """
        cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        print('cookies_dict', cookies_dict)
        with open(COOKIES_FILE_PATH, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(cookies_dict))
            print('保存cookies文件成功！')

    def _deserialization_cookies(self):
        """
        反序列化cookies
        加载cookies
        :return:
        """
        with open(COOKIES_FILE_PATH, 'r+', encoding='utf-8') as f:
            cookies_dict = json.loads(f.read())
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            print('读取文件成功')
            return cookies

    def _load_cookies(self):
        # 1、判断cookies序列化文件是否存在
        if not os.path.exists(COOKIES_FILE_PATH):
            return False
        # 2、加载cookies
        self.session.cookies = self._deserialization_cookies()
        # 3、判断cookies是否过期
        try:
            self.get_taobao_name()
        except Exception as e:
            os.remove(COOKIES_FILE_PATH)
            print("cookies过期")
            return False
        print('cookies登陆成功')
        return True

    def get_taobao_name(self):
        """
        获取淘宝昵称
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        resp = self.session.get(self.my_taobao_url, headers=headers)
        taobao_name = re.findall(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', resp.text)
        print(taobao_name[0])


if __name__ == '__main__':
    login = TaobaoLogin()
    # print(login._nick_check())
    # print(login._verify_password())
    login.login()
    login.get_taobao_name()

