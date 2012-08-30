#!/usr/bin/env python 
import sys
import re
import json
import requests
import signal

def handler(signum, frame):
    raise Exception('Request timout')

signal.signal(signal.SIGALRM, handler)

UA = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

def load_bugs_db(filename):
    bugs = json.load(open(filename))["bugs"]
    for bug in bugs:
        pattern = bug["pattern"].replace("\\", "").replace("*)?", "*?)")
        bug["re"] = re.compile(pattern)
    return bugs

def find_bugs(text):
    bugs = set()
    for bug in bugs_db:
        if bug["re"].search(text):
            bugs.add(bug["name"])
    return list(bugs)

def process_url(url):
    signal.alarm(60)
    r = requests.get(url, headers={'user-agent:': UA})
    signal.alarm(0)
    if r.text:
        return find_bugs(r.text)
    return []

if __name__ == "__main__":

    bugs_db = load_bugs_db("./data/bugs.js")

    for line in sys.stdin:
        url = "http://" + line.strip()

        result = { "ok": True, "errstr": "", "bugs": [] }
        try:
            bugs = process_url(url)
            result["bugs"] = bugs
        except Exception, e:
            result["ok"] = False
            result["errstr"] = str(e)

        print url, json.dumps(result)

