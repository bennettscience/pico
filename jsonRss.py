import requests
import urllib.request
import urllib.parse
import yaml
import re
import sys
from slugify import slugify
from flask_extended import Flask

'''
If you can get JSON, you can make a feed
---
Creates an RSS feed from JSON. Built using the GitHub JSON model.
'''

indent = "   "
items = []
outfile = 'feed.rss'

# You can define an image URL here to be inclded in the feed
# Default value is none
image = None

def get_config():
    stream = open('config.yml', 'r')
    config = yaml.load(stream)
    return config

def read_item(item):
    txt = requests.get(item)
    list = txt.content.decode('ascii').split('\n')
    for i, line in enumerate(list):
        item = {}

        if "title: " in list[i]:
            title = list[i][7:]

        if "date: " in list[i]:
            post_date = list[i][6:]

        if "---" in list[i]:
            body = list[i+1:]

            body = [line.rstrip() for line in body if line.rstrip()]


    guid =  "{0}<guid>{1}</guid>\n".format(indent * 3, slugify(title))
    pubDate = "{0}<pubDate>{1}</pubDate>\n".format(indent * 3, post_date)
    link = "{0}<link>{1}</link>\n".format(indent * 3, config['SITE']['home'] + '/files/' + slugify(title))
    title = "{0}<title>{1}</title>\n".format(indent * 3, title)
    description = "{0}<description>{1}</description>\n".format(indent * 3, body[0])
    author = "{0}<author>{1}</author>\n".format(indent * 3, config['SITE']['author'])

    return "{0}<item>\n{1}{2}{3}{4}{5}{6}{0}</item>\n".format(indent * 2, guid, link, title,
                                                            description, pubDate, author)

config = get_config()

req = requests.get(config['SITE']['remote_path'])
req = req.json()

for f in req:
    items.append(read_item(f['download_url']))

if outfile is not None:
    outfp = open(outfile,"w")
else:
    outfp = sys.stdout

outfp.write('<?xml version="1.0" encoding="UTF-8"?>\n')
outfp.write('<rss version="2.0">\n')
outfp.write('   <channel>\n')
outfp.write('      <title>{0}</title>\n'.format(config['SITE']['title']))
outfp.write('      <description>{0}</description>\n'.format(config['SITE']['desc']))
outfp.write('      <link>{0}</link>\n'.format(config['SITE']['home']))

if image is not None:
    if image.lower().startswith("http://") or image.lower().startswith("https://"):
        imgurl = image
    else:
        imgurl = urllib.quote(host + opts.image,":/")

    outfp.write("      <image>\n")
    outfp.write("         <url>{0}</url>\n".format(imgurl))
    outfp.write("         <title>{0}</title>\n".format(title))
    outfp.write("         <link>{0}</link>\n".format(link))
    outfp.write("      </image>\n")

for item in items:
    outfp.write(item)

outfp.write('')
outfp.write('   </channel>\n')
outfp.write('</rss>\n')

if outfp != sys.stdout:
    outfp.close()
