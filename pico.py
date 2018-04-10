from flask import Flask, render_template, request, url_for
import os, glob, datetime, re, string
from urllib.parse import urlparse
from werkzeug.contrib.atom import AtomFeed


app = Flask(__name__)
app.config.from_pyfile('settings.py')

@app.route('/')

def index():
    content = []

    dir = os.listdir('files')

    for file in dir:
        if not file.startswith('.'):
            with open('files/' + file, 'r') as f:
                item = parse_txt_file(f)

                content.append(item)

    sorted_content = sorted(content, key=lambda blog: blog.post_date, reverse=True)

    return render_template('index.html', content=sorted_content)

def parse_txt_file(item):
    txt = item.readlines()
    for i, line in enumerate(txt):

        if "title: " in txt[i]:
            title = txt[i][7:]

        if "date: " in txt[i]:
            post_date = txt[i][6:]

        if "---" in txt[i]:
            body = txt[i+1:]

    body = [line.rstrip() for line in body if line.rstrip()]

    item = make_item(title, post_date, body)
    return item

def make_item(title, post_date, body):
    item = Blog(title, post_date, body)
    return item

class Blog(object):
    title = ""
    body = ""
    post_date = ""

    def __init__(self, title="", post_date="", body=""):
        self.title = title
        self.post_date = post_date
        self.body = body

def make_external(url):
    return urljoin(request.url_root, url)


# TODO: Create ATOM feed from txt files
@app.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Articles',feed_url=request.url, url=request.url_root)
    articles = glob.glob('files/*.txt')

    for article in articles:
        article = parse_txt_file(article)
        feed.add(article.title, article.body,
                 content_type='html',
                 # author=article.author.name,
                 url=make_external(article.url),
                 # updated=article.last_update,
                 published=article.published)
    return feed.get_response()


if __name__ == "__main__":
    app.run()
