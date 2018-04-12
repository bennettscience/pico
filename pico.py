from flask import Flask, render_template, request, jsonify, url_for
from slugify import slugify
import os, glob, re, string, sys, yaml


app = Flask(__name__)
app.config.from_pyfile('settings.py')

dir = os.listdir('files')

def make_item(title, post_date, body):
    item = Entry(title, post_date, body)
    return item

class Entry(object):
    title = ""
    body = ""
    post_date = ""
    slug = ""

    def __init__(self, title="", post_date="", body=""):
        self.title = title
        self.post_date = post_date
        self.body = body
        self.slug = slugify(title)

def check_for_title(file, slug):
    # print(file, slug)
    with open('files/' + file, 'r') as f:
        txt = f.readlines()
        for i, line in enumerate(txt):
            if "title: " in txt[i]:
                title = slugify(txt[i][7:].rstrip().lower())
                # print(title)

            if title == slug:
                return True
            else:
                return False

def get_nav():
    stream = open('config.yaml', 'r')
    nav = yaml.load(stream)
    return nav

@app.route('/')
def index():

    nav = get_nav()
    
    content = []

    for file in dir:
        if not file.startswith('.'):
            with open('files/' + file, 'r') as f:
                item = process_text_file(f)

                content.append(item)

    sorted_content = sorted(content, key=lambda blog: blog.post_date, reverse=True)

    return render_template('index.html', content=sorted_content, nav=nav['social'])

@app.route('/post/<slug>')
def single_post(slug):
    nav = get_nav()

    for file in dir:
        if not file.startswith('.'):
            # print('not a dotfile, opening and reading')
            with open('files/' + file, 'r') as f:
                if check_for_title(file, slug):
                    item = process_text_file(f)
                    return render_template('entry.html', content=item, nav=nav['social'])

def process_text_file(item):
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


# TODO: Create ATOM feed from txt files
# @app.route('/recent.atom')
# def make_external(url):
#     return urljoin(request.url_root, url)
#
# def recent_feed():
#     feed = AtomFeed('Recent Articles',feed_url=request.url, url=request.url_root)
#     articles = glob.glob('files/*.txt')
#
#     for article in articles:
#         article = parse_txt_file(article)
#         feed.add(article.title, article.body,
#                  content_type='html',
#                  # author=article.author.name,
#                  url=make_external(article.url),
#                  # updated=article.last_update,
#                  published=article.published)
#     return feed.get_response()


if __name__ == "__main__":
    app.run()
