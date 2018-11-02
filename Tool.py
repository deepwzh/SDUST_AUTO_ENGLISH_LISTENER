import http
import http.cookiejar
import json
import os
# import fcntl
def make_cookie(name, value):
    """
    生成cookie对象
    :param name: 要添加的cookie的键
    :param value: 要添加的cookie的值
    :return: cookie对象
    """
    return http.cookiejar.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain="",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )

def write_list(data):
    with open('data.json', 'w') as fp:
        json.dump(data, fp, indent = 4, separators=(',', ': '))
    # fp = open('data.json', 'w')
    # fcntl.flock(fp, fcntl.LOCK_EX)
    # json.dump(data, fp)
    # fcntl.flock(fp, fcntl.LOCK_UN)
    # fp.close()

def read_list():
    with open('data.json', 'r') as fp:
        data = json.load(fp)
        return data

def backup():
    os.system("cp %s %s" % ("data.json", "data.tmp.json"))