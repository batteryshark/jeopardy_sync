#!/usr/bin/python3
# A Simple Configuration Class for JSync
import os,json


class JSyncConfig(object):
    def __init__(self,cfg_path):
        self.cfg_path = cfg_path
        self.reddit_user_list = ['jibjabjrjr']
        self.hash_db = {}
        self.output_path = "./"
        if(self.load() is False):
            self.save()

    def save(self):
        so = {
            'output_path': self.output_path,
            'reddit_user_list':self.reddit_user_list,
            'hash_db':self.hash_db
        }
        with open(self.cfg_path,"w") as g:
            json.dump(so,g)


    def load(self):
        try:
            with open(self.cfg_path,"r") as f:
                so = json.load(f)
                self.reddit_user_list = so.get('reddit_user_list',['jibjabjrjr'])
                self.hash_db = so.get('hash_db',{})
                self.output_path = so.get('output_path','./')
            return True
        except:
            return False


    def update_hashdb(self,nhash):
        self.hash_db[nhash] = ''
        self.save()