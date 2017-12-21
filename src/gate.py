import json
import urllib2

data = json.load(urllib2.urlopen("http://data.gate.io/api2/1/tickers"))


def filter_coin(name):
    return name[-4:] == "usdt"


poss = []

for k, v in data.iteritems():
    high = float(v["high24hr"])
    low = float(v["low24hr"])
    cur = float(v["last"])
    if not filter_coin(k) or cur >= high:
        continue
    poss.append({
        "name": k,
        "potential": int((high - cur) * 100 / cur),
        "has_up": int((cur - low) * 100 / low),
        "cur": cur,
        "all": int(cur * float(v["quoteVolume"]) /10000)

    })


def cmp(x, y):
    if x["potential"] > y["potential"]:
        return -1
    return 1


poss.sort(cmp)

for v in poss:
    if v["all"] >= 100:
        print v["name"], v["potential"], v["has_up"], v["cur"], v["all"]
