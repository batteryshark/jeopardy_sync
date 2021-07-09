#!/usr/bin/python3
from jeopardy_sync import JSync


if(__name__=="__main__"):
    jsync = JSync()
    if(jsync.is_valid == False):
        print("JSync Init Error")
        exit(-1)
    print("JSync Running")
    jsync.sync()