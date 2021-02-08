# -*- coding:utf-8 -*-
import leancloud as lc
from os import getenv
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from cgi import *
from base64 import b64encode,b64decode
from urllib.parse import parse_qs,quote
import sys
from importlib import reload
reload(sys)
appid = getenv("APPID")
masterkey = getenv("MASTERKEY")
classname = getenv("CLASS")
passwd = getenv("PASSWORD")
def tostr(text):
    return b64decode(b64encode(text)).decode('utf-8').strip("'")
class handler(BaseHTTPRequestHandler):
    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            st = tostr(self.rfile.read(length))
            print(st)
            postvars = parse_qs(st)
        else:
            postvars = {}
        ret = {}
        for key in postvars:
            key2 = tostr(key.encode())
            v = []
            for i in postvars[key]:
                v.append(tostr(i.encode()))
            ret[key2]=v
        return ret
    def do_POST(self):
        print("Recieved Post requests processing")
        if appid==None or masterkey==None or classname==None:
            print("QwQ")
            self.send_error(502,"Environment Varibles Error")
            return
        try:
            postar = self.parse_POST()
            if passwd==postar["password"][0]:
                lc.init(appid,master_key=masterkey)
                Content = lc.Object.extend(classname)
                content = Content()
                print(postar)
                content.set("content",postar["content"][0])
                content.save()
            else:
                self.send_error(502,"Password Error")
        except Exception as e:
            self.send_error(502,str(e))
            print(e)
            return
        finally:
            self.send_response(200)
            self.send_header("Content-Type","application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write('{"status": "success"}'.encode())
            return
    def do_GET(self):
        self.send_response(301)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Location", "/")
        self.end_headers()

if __name__=="__main__":
    server = HTTPServer(('',8000),handler)
    server.serve_forever()