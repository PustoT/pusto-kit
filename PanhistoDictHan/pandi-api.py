# coding:utf-8
from hanzi2mc import hanzis2mcinfos
import json
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    params = parse_qs(environ['QUERY_STRING'])
    # name = params['name'][0]    ## 得到网址中的参数
    name = params.get('name', [''])[0]
    print('hier', name)
    #dic = {name: hanzis2mcinfos(name)}   ##字典查值并返回为字典
    #return [json.dumps(dic)]    ## 网页返回值
    return [('<meta charset="UTF-8"> ' + hanzis2mcinfos(name)).encode('utf-8')]

if __name__ == "__main__":
    port = 5088  ##自定义开启的端口
    httpd = make_server("0.0.0.0", port, application)
    print("serving http on port {0}...".format(str(port)))
    httpd.serve_forever()
