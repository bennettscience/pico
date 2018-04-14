# https://gist.github.com/bretthancox/4cce4193fa0468f3d3cbafb7bc2fb028
# Modify the Flask config object to read from YML rathern than a Python Class
from flask_extended import Flask
from flask import render_template, request, jsonify, url_for
from slugify import slugify
import os, glob, re, string, sys, yaml

# TODO: Build absolute paths for all URLs

app = Flask(__name__)
app.config.from_yaml(os.path.join(app.root_path, 'config.yml'))

dir = os.listdir('files')

def get_config():
    stream = open('config.yml', 'r')
    config = yaml.load(stream)
    return config

def make_item(title, post_date, body):
    item = Entry(title, post_date, body)
    return item

class Entry(object):
    title = ""
    body = ""
    post_date = ""
    slug = ""

# TODO: Relative path for slug
    def __init__(self, title="", post_date="", body=""):
        self.title = title
        self.post_date = post_date
        self.body = body
        self.slug = "post/" + slugify(title)

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

@app.errorhandler(404)
def page_not_found(e):
    config = get_config()

    return render_template('404.html', nav=config['SOCIAL'], site=config['SITE']), 404

@app.route('/')
def index():

    config = get_config()

    content = []

    for file in dir:
        if not file.startswith('.'):
            with open('files/' + file, 'r') as f:
                item = process_text_file(f)

                content.append(item)

    sorted_content = sorted(content, key=lambda blog: blog.post_date, reverse=True)

    print(app.config)

    return render_template('index.html', content=sorted_content, nav=config['SOCIAL'], site=config['SITE'])

@app.route('/post/<slug>')
def single_post(slug):
    config = get_config()

    for file in dir:
        if not file.startswith('.'):
            # print('not a dotfile, opening and reading')
            with open('files/' + file, 'r') as f:
                if check_for_title(file, slug):
                    item = process_text_file(f)
                    return render_template('entry.html', content=item, nav=config['SOCIAL'], site=config['SITE'] )

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

if __name__ == "__main__":
    app.run()
