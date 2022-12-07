from itertools import groupby
from json import loads, dumps
from collections import defaultdict
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import time

dataList = []

def ipInfo(addr=''):
    from urllib.request import urlopen
    from json import load
    if addr == '':
        #url = 'https://ipinfo.io/json'
        return
    else:
        #url = '"ipinfo.io/198.21.229.245?token=ab8a3627612625/' + addr + '/json'
        url = 'https://ipinfo.io/'+addr+'?token=ab8a3627612625'
    res = urlopen(url)
    #response from url(if res==None then check connection)
    data = load(res)

    #will load the json response into data

    dataList.append(data)
    #for attr in data.keys():
       #will print the data line by line
    #   print(attr,' '*13+'\t->\t',data[attr])


if __name__ == "__main__":
    with open('ip_address_dump_v3.txt') as f:
        for line in f:
            print(line)
            ipInfo(line.rstrip('\n'))
   
    print(dataList)

    res = {}
    notFound = []
    for x in dataList:
        if 'country' not in x.keys() :
            notFound.append(x)
            continue
        if x["country"] in res:
            res[x["country"]]["data"].append(x)
            res[x["country"]]["count"] += 1
        else :
            res[x["country"]] = {"data": [], "count": 0}
            res[x["country"]]["data"].append(x)
            res[x["country"]]["count"] += 1


    print("Not Found: ")
    print(notFound)

    x = []
    y = []
    for key in res.keys():
        x.append(key)
        y.append(res[key]["count"])


    #print(x)
    #print(y)


    colors = ["b", "g", "r", "c", "m", "y", "k", '#bcbcbc']

    plt.bar(x, y, label=x, color=colors)

    plt.xlabel("Country")
    plt.ylabel("Number of Server")
    plt.title("Bar Graph")
    plt.legend()
    #plt.show()

    plt.savefig('bar_graph_v2.png')

    res = {}
    notFound = []
    hostname = []
    for x in dataList:
        print(x, x.keys())

        if 'hostname' not in x.keys():
            notFound.append(x)
            continue

        name = "others"
        if x["hostname"].find("amazonaws") != -1:
            name = "amazonaws"
        if x["hostname"].find("cloudfront") != -1:
            name = "cloudfront"
        if x["hostname"].find("adobedc") != -1:
            name = "adobedc"
        if x["hostname"].find("googleusercontent") != -1:
            name = "googleusercontent"
        if x["hostname"].find("akamaitechnologies") != -1:
            name = "akamaitechnologies"

        if name in res:
            print("hostname: ", hostname)
            res[name]["data"].append(x)
            res[name]["count"] += 1
            hostname.append(x["hostname"])
        else:
            print("hostname: ", hostname, "len: ", len(x["hostname"]))
            res[name] = {"data": [], "count": 0}
            res[name]["data"].append(x)
            res[name]["count"] += 1
            hostname.append(x["hostname"])
    # print(notFound)

    x = []
    y = []
    for key in res.keys():
        x.append(key)
        y.append(res[key]["count"])

    print(x)
    print(y)

    colors = ["b", "g", "r", "c", "m", "y", "k", '#bcbcbc']

    plt.bar(x, y, color=colors)

    plt.xlabel("Hostname")
    plt.ylabel("Number of Server")
    plt.title("Bar Graph")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.4)
    plt.legend()
    # plt.show()

    plt.savefig('bar_graph_host.png')

    print(hostname)


