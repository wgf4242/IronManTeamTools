import json
import os

PROXY = 'http://127.0.0.1:8080'
# os.environ.update(http_proxy=PROXY, https_proxy=PROXY)


from requests_html import HTMLSession, HTML
from pathlib import Path

session = HTMLSession()
headers = {'referer': 'https://www.cmd5.com/'}


def get_json_file():
    path = Path(__file__).parent / 'user.json'
    return str(path.absolute())


def main(data):
    cookies = {
        # 'user': '3pcm5dhfJ09BGP0S3aDU30Om4DsDksRmThQtfYytQNZSgL+NjL5hZHI9rQwcQXwO1RytGOmq/R3Z7ZDN5PK0JP1i4/reeuIdDtnJWWvR96bVQji56BZg5Ni4yFLbLaXsuLdKwjgTKeKqbQEsdkaqJnZiTfKu9MARv/qtptuGkMnPJ77uNM+GLW31NeIoULEfdjCiGELMXOmCH68B88mQTbvXtsGKItxG',
    }

    response = session.post('https://www.cmd5.com/', cookies=cookies, headers=headers, data=data, verify=False, timeout=3)
    html = response.html  # type: HTML
    el_xpath = "//table[@id='ctl00_ContentPlaceHolder1_table3']/tr/td/div[1]"
    element = html.xpath(el_xpath, first=True)
    text = element.text
    import re
    text_clean = re.findall(r'查询结果：(.*?)本站', text, flags=re.DOTALL)[0]
    print(text_clean.strip())
    if not text_clean:
        return "没有md5查询结果"
    if '验证码' in text_clean:
        return "需要验证码"
    return text_clean.strip()


def get_captcha(url='https://www.cmd5.com/checkcode.aspx/0'):
    res = session.get(url, headers=headers)
    return ocr_captcha(res.content)


def ocr_captcha(data: bytes):
    import ddddocr
    ocr = ddddocr.DdddOcr(show_ad=False)
    # with open("a.jpg", 'rb') as f:
    #     image = f.read()
    res = ocr.classification(data)
    print(res)
    return res


def login(username, password):
    login_captcha = 'https://www.cmd5.com/checkcode.aspx/3'
    captcha = get_captcha(login_captcha)

    data = {
        '__VIEWSTATE': 'uA4ZB9I8nc9ZNWkUrOcrmL2NMc6kmw6zfdR/58kaCP+UnI4cOgmnGlmQ8PzXUtZf8MIr5Rva3g10lMKR2F9T+gGMKBf+dJvrZiWjGVr9WRLweQzuufh2A1Dw9gHLF72Uz1nshsqE8fHQ16SkC2K48gJm+4qRxjls9EWPrQoQay0PXTYTLv3jWuVTx8RM2oYZ5pkx9Z/7CETIXiUw8+bKyL8o+a6Qt3TRgakW1mjVHn7+U+OilSbcqdCccsjslT/JSuJ3DANGh8BxEnXzjGP/oB3O5nnMOdlLnAo9/aFDQpYWL19SAW7un/aPy9xAEJEyg4KkhXYMainwtajuCdfsc3uSCNDIyceph4XwI6ReW0mYGiFTmWGMGJjTdQtLvc7oEV+wQFan20TjtK9OaKeBfFb+nvklVFpQllrKtkQIvLX1RbG7cs6RH2nNmoLczyxPvtfKrQfOGxI3oJFrEKdXmxQA3ur5JDcdMiyU6HOkVBFBBRfESoZifYF1HkvM0Og46iKj2PfuPl3yf98nJNY/bLOWyefDJXMK+5rD+LgqeMejV37OVFi/u9B6Vy6CrwaENafY6/KpVPh6VnOgQo5kbHDu0ofOGOtmrfAqa4oJcoZazBSxq2Rwl/JlXGL7rO1XpVASbfJK1ACLPyD+0bgYvjNxWm7LMNcdP2rhcXb+BwfPu3E42/iOHYmJuY4Vz7xdJ4yvKP/OV8KGPtHGhYwtJ3enjE1zt2183MlIWG+1OeStz8gp7uDqMleyTnqwtCgOCyf0hZlg9e4Tkyag5m0KDnFG1PYhkiNIZ0fRaCfbD4pEkWCboKSc151C1II8gxQXBLd13+ptVgnlAm5oinX3PPNBhY5yqG+ZwH1EI1NxKPxEMkHCjGOtl512UtfMMZi3C8YgfU9vrym5rHH6FFcbyJoxRuWXVrFinLvA/+a4HRmPeFtuKtTxEMzdAV9OZ4IUvflI1ifHtNL8lCLAaFSAb1NFg3FIbu/4PJD7+gkozTKx5vFsrCSm3blHxDyGmTywHZeKRn2+hhBkXh6WwTA99TUUfunxSCS4elGbR8r1eiF5h5yZ44OJ4bIJRuQuim8TxtC94OG38nvU1VvyGrVbfnmA2QYHSnW1aBk4e4PdtjttRNofzfuduEn2sUD8z5erhquhB68qWr55J0FIfptYfeQRneFk8r7vRbz3CHcbBK3f34d2nCSbDM+w0JwsNgGiD0HdTxyN0EoOAGeJQHlj2+sMCIg6OrQMrGPkSnQ7nANIDTRiZgCs3ym293T+at6VAMc6Ya/anDRTEQMu0E2fOfF6LfhijD+JZ04tKiPkGpR8nc2uWf4Z8I0ef1fUzdK4l7WCX74kuz0p5insuJO1RfzfsZpgcpIDflMXgzCXyStTWZI3sKGsaoGc2Y6GIX6ERVqbnmKdgNWyBPmEpGiza0IkmwXKJVHblcVjN74iX+8A/4tIbH138RPTzuM8KedePk+GJ045gUc4P4GCYnejXIFsiqwcuVQDJESzC4/eLlzvJ5eX5rPr5t+60AoaZQvUh7vSINa10mRUTSKURR5TWwQpJR5eRUsdntT3bgicGzPIaFJdxC7A/KtRuJ1HIVPpFpuAD6veIh60pnBZQt2+CNa8Hs2oNVcghFOcn0UJ6rrqkgQaAxJ2RzpSP1Lh9uTZMFowfjRUbiRDWIudTHieyVO2mJqLs4tmTSTIGw9r6SrFf5tqexPUgJAiGzEpnHWr8cqa7zd/xIv7SaYAUwCaED3ggDQi7H3u3xBDgqf19AdJjREQ',
        '__VIEWSTATEGENERATOR': 'C2EE9ABB',
        '__EVENTVALIDATION': '+8eRdAKD7qxXRZDgFb9bnJaTFpKHy6S9An+QbYsNj2kEJU2JRcMvATkmY7v5RZiz0gutfCjFH1dEdWSE1VwfYKpD2KiAbHThQ2s4IZ2hIODFZCruGf7ljIfpDWZ3cR5ZGWZ0LCyhrnTACTJWZBKJe9naGBrlGW4yKPbayk623r6JYeXjY2vpj12VHiYK/YLOXrAqwLsz64RJ3lTL5ns4tSVxhPyBWHdnXK+l1bQRXIGtgM7kBjtqFeejTkgy0RiD52ZSuvjn5i46zXM6',
        'ctl00$ContentPlaceHolder1$TextBoxCmd5_E': username,
        'ctl00$ContentPlaceHolder1$TextBoxCmd5_P': password,
        'ctl00$ContentPlaceHolder1$TextBoxCode': captcha,
        'ctl00$ContentPlaceHolder1$CheckBox1': 'on',
        'ctl00$ContentPlaceHolder1$Button1': '提交',
        'ctl00$ContentPlaceHolder1$HiddenFieldAliCode': '',
    }

    response = session.post('https://www.cmd5.com/login.aspx', data=data)

    obj = json.load(open(get_json_file()))
    user = session.cookies.get_dict()['user']
    obj['user'] = user
    json.dump(obj, open(get_json_file(), 'w'))
    print(response.text)


def req_md5(md5):
    set_cookies_user()

    data = {
        '__VIEWSTATE': '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',
        'ctl00$ContentPlaceHolder1$TextBoxInput': md5,
        'ctl00$ContentPlaceHolder1$InputHashType': 'md5',
        'ctl00$ContentPlaceHolder1$Button1': '查询',
        # 'ctl00$ContentPlaceHolder1$TextBoxCode': '8548',
    }
    res = main(data)
    if '验证码' in res:
        captcha = get_captcha()
        data['ctl00$ContentPlaceHolder1$TextBoxCode'] = captcha
        res = main(data)
    if '请登录' in res:
        if not os.path.exists(get_json_file()):
            return "请将user.json.bak 复制为 user.json 填好用户名密码"
        obj = json.load(open(get_json_file()))

        username = obj['username']
        password = obj['password']
        login(username, password)
        res = main(data)
    return res


def set_cookies_user():
    obj = json.load(open(get_json_file()))
    if user := obj.get('user', ''):
        session.cookies.set('user', user)


if __name__ == '__main__':
    md5 = '8fa14cdd754f91cc6554c9e71929cce7'
    res = req_md5(md5)
    assert res == 'f'
