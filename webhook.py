# -*- coding: utf-8 -*-
# Copyright (C) 2017-2020
# Chenglin Ning, chenglinning@gmail.com
import os
import sys
import json
import tornado.web
from tornado.web import asynchronous
from sqlite import getMDatabaseInstance
from models import SaledData

class SkWebHook(tornado.web.RequestHandler):
    def options(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        return
    def setDefaultHeader(self):
        self.set_header("Content-Type", "applicaiton/json")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    @asynchronous
    def post(self):
        _request = json.loads(self.request.body)
        intent = _request['intent']
        utterance = _request['utterance']
        if intent == 'sx_query':
            _response = self.sx_query_intent(entities=_request['entities'])
        else:
            _response = self.default_intent(utterance=utterance)

        js = json.dumps(_response, ensure_ascii=True, sort_keys=True, indent=4, encoding="UTF-8")
        self.setDefaultHeader()
        self.write(json.dumps(_response))
        self.finish()

    def default_intent(self, utterance=None):
        _response = {}
        _response['version'] = "1.00"
        _response['out_speech'] =  utterance
        _response['content_type'] = "text"
        return _response

    def sx_query_intent(self, entities=None):
        if entities:
            dbsession= getMDatabaseInstance('mydb.db').getSessionClass()()
            entity = entities[0]
            if entity['name']==u'zone':
                outspeech = u"无效的销售地区."
                entity_val = entity['val']
                row = dbsession.query(SaledData).filter_by(zone=entity_val).scalar()
                if row:
                    amt = row.val
                    biliion = int(amt / 10000)
                    ten_million = int ((amt % 10000) / 1000)
                    if biliion:
                        if ten_million:
                            outspeech = u"%s地区销售价金额为%d亿%d千万元" % (entity_val, biliion, ten_million)
                        else:
                            outspeech = u"%s地区销售价金额为%d亿元" % (entity_val, biliion)
                    else:
                        outspeech = u"%s地区销售价金额为%d千万元" % (entity_val, ten_million)
            else:
                outspeech = u"抱歉！我不明白你在说什么。"
        else:
            outspeech =u"抱歉！我不明白你在说什么。"
        _response = {}
        _response['version'] = "1.00"
        _response['out_speech'] = outspeech
        _response['content_type'] = "text"
        return _response

