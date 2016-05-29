#!/usr/bin/env python
"""
Query MediaWiki API for article Infobox

References
    https://en.wikipedia.org/wiki/Help:Infobox
    https://meta.wikimedia.org/wiki/Wiki_syntax
    https://www.mediawiki.org/wiki/API:Main_page

    exemple: https://fr.wikipedia.org/w/api.php?action=parse&format=json&page=Brad_Pitt&prop=parsetree&disablelimitreport=&disableeditsection=&disabletoc=&contentmodel=text
"""

import argparse
import os
import sys
import time

import pycurl

from io import BytesIO
from string import Template

import lxml.html
import json

from collections import defaultdict
from lxml import etree

import string


def printMediaWikiInfobox(title):

    ENDPOINT = "http://fr.wikipedia.org"
    QUERY = Template(("${WIKI}/w/api.php?action=parse"
                                    "&format=json"
                                    "&page=${page}"
                                    "&prop=parsetree"
                                    "&disablelimitreport="
                                    "&disableeditsection="
                                    "&disabletoc="
                                    "&contentmodel=text"))

    title = title.lower()

    while True:

        #construct the query
        page = title.replace(" ", "+")
        page = page[0].upper() + page[1:]
        qry = QUERY.substitute(WIKI=ENDPOINT, page=page)

        #setup a curl object for our query
        crl = pycurl.Curl()
        crl.setopt(crl.FOLLOWLOCATION, True)

        crl.setopt(crl.SSL_VERIFYHOST, False)
        crl.setopt(crl.SSL_VERIFYPEER, False)

        try:
            crl.setopt(crl.URL, qry)
        except UnicodeEncodeError:
            crl.setopt(crl.URL, qry.encode('utf-8'))

        #download data from the webserver
        try:
            bfr = BytesIO()
            crl.setopt(crl.WRITEFUNCTION, bfr.write)
            crl.perform()
            data = bfr.getvalue()
            bfr.close()
        except Exception as detail:
            print("RETRY Caught exception: %s" % detail)
            return

        #locate the infobox dict
        try:
            dataDict = None
            dataDict = json.loads(data.decode("utf-8"))
            ptree = dataDict["parse"]["parsetree"]["*"].encode('utf-8')
            title = dataDict["parse"]["title"].encode('utf-8')

            for htmlitem in etree.fromstring(ptree).xpath("//template"):
                if "box" in htmlitem.find('title').text:
                    #infobox found! convert to a json dict and print
                    obj = dict()
                    for item in htmlitem:
                        try:
                            name = item.findtext('name')
                            tmpl = item.find('value').find('template')
                            if tmpl is not None:
                                pass #value = etree.tostring(tmpl)
                            else:
                                value = item.findtext('value')
                            if name and value:
                                obj[name.strip()] = value.strip()
                        except:
                            pass #obj["%s ERROR" % __name__] = etree.tostring(item)
                    return(json.dumps(obj))

            #no infobox found, trying to find a redirect
            redirect = ""
            for htmlitem in etree.fromstring(ptree).xpath("//text()"):
                if htmlitem.startswith("#REDIRECT"):
                    redirect = htmlitem.strip().split("REDIRECT")[-1].strip().strip("[[").strip("]]")
                    break;

            #if a redirect is found, we will retry with this new title
            if redirect != "":
                #print("found redirection: %s" % redirect)
                title = redirect
                continue

            print("No infobox found")
            return
            
        except:
            #error when decoding wikipedia's json
            if dataDict != None:
                obj = dataDict["error"]["info"].encode('utf-8')
                print(json.dumps(obj))
            else:
                print("Syntax error while loading json data: %s" % data)
            return


if __name__ == "__main__":
    desc = "Query MediaWiki API for article Infobox"
    argp = argparse.ArgumentParser(description=desc)
    argp.add_argument("title",
                      help="article title")
    args = argp.parse_args()

    printMediaWikiInfobox(args.title)
