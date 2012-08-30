#!/usr/bin/python
import os
import json
from collections import defaultdict
import operator


# read results

text = ""
for dirname, dirnames, filenames in os.walk("output"):
    for filename in filenames:
        text += open(os.path.join(dirname, filename), "r").read()
text = text.strip()


# parse results

d = {}
for line in text.split("\n"):
    i = line.find(' ')
    d[line[:i]] = json.loads(line[i:])


# output results in json format

f = open("results.json", "w")
json.dump(d, f, indent=4)
f.close()


# gather stats: error percentage, errors' and bugs' tops

total = len(d)
errors = 0.0
errstat = defaultdict(int)
bugstat = defaultdict(int)
for key, val in d.iteritems():
    if val["ok"]:
        for bug in val["bugs"]:
            bugstat[bug] += 1
    else:
        errors += 1
        errstat[val["errstr"]] += 1


# output stats

def seetop(h, limit):
    total = float(sum(h.values()))
    top = sorted(h.items(), key=operator.itemgetter(1))
    for i in range(1, limit+1):
        print "{:2.2f}% {}".format(top[-i][1]*100/total, top[-i][0])

print "Top Bugs:"
print
seetop(bugstat, 20)
print
print
print "Errors: {0}%".format(errors/total*100)
print
print
print "Top Errors:"
print
seetop(errstat, 5)

