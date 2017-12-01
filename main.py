# -*- coding: utf-8 -*-
# Copyright (C) 2017-2020
# Chenglin Ning, chenglinning@gmail.com
import os
import sys
import json
import tornado.ioloop
import tornado.web
import tornado.autoreload
import tornado.httpserver
from tornado.web import asynchronous
import tornado.options
import logging
from webhook import SkWebHook

def make_app():
    return tornado.web.Application(
        [
            (r"/skwebhook/v1.00", SkWebHook),
        ],

        debug=True
    )

tornado.options.define("port", default=8018, help="Run skill webhook on a specific port", type=int)  
tornado.options.define("propagate", default=False, help="disable propagate", type=bool )  
tornado.options.define("debug", default=True, help="enable debug", type=bool )  

if __name__ == "__main__":

    folder, filename = os.path.split(os.path.abspath(__file__))
    sys.path.append(folder) 
    
    tornado.options.parse_command_line()
    _app = make_app()

    _http_server = tornado.httpserver.HTTPServer(_app)
    _http_server.listen(tornado.options.options.port)

    logging.info("SK Webhook Service Running...")
    tornado.ioloop.IOLoop.instance().start()
