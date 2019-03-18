__author__ = 'point'
__date__ = '2019-03-12'

import hashlib


def get_md5(url):
    """
    获取 URL 字符串对应的 MD5 值
    :param url: url
    :return:
    """

    # 如果 URL 是 str 的实例，说明 URL 字符串的编码是 Unicode
    if isinstance(url, str):
        # 将 URL 编码为 utf-8
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    print(get_md5('http://www.jobbole.com'))
