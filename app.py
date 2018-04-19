# https://gist.github.com/bretthancox/4cce4193fa0468f3d3cbafb7bc2fb028
# Modify the Flask config object to read from YML rathern than a Python Class
from flask_extended import Flask
from flask import render_template, request, jsonify, url_for
from slugify import slugify
import os, glob, re, string, sys, yaml, requests

# TODO: Build absolute paths for all URLs

def get_config():
    stream = open('config.yml', 'r')
    config = yaml.load(stream)
    return config

app = Flask(__name__)
application = app
app.config.from_yaml(os.path.join(app.root_path, 'config.yml'))

config = get_config()

if config['SITE']['path_to_use'] == "local":
    path = config['SITE']['local_path']
elif config['SITE']['path_to_use'] == "remote":
    path = config['SITE']['remote_path']
else:
    raise ValueError("No path set in config.yml")

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
        self.slug = "files/" + slugify(title)

def check_for_title(txt, slug):
    for i, line in enumerate(txt):
        if "title: " in txt[i]:
            title = slugify(txt[i][7:].rstrip().lower())
            # print(title, slug)

            if title == slug:
                # print("Matched title and slug, return True")
                return True
            else:
                # print("They did not match, return False")
                return False

@app.errorhandler(404)
def page_not_found(e):
    config = get_config()
    return render_template('404.html', nav=config['SOCIAL'], site=config['SITE']), 404

@app.route('/')
def index():
    config = get_config()
    content = []

    if config['SITE']['path_to_use'] == 'local':
        dir = os.listdir(path)
        for file in dir:
            if not file.startswith('.'):
                with open(path + file, 'r') as f:
                    item = process_text_file(f.readlines())
                    content.append(item)

    elif config['SITE']['path_to_use'] == 'remote':
        req = requests.get(path).json()
        for f in req:
            item = process_json_file(f)
            content.append(item)
    else:
        raise ValueError('No path defined in config')

    sorted_content = sorted(content, key=lambda blog: blog.post_date, reverse=True)

    return render_template('index.html', content=sorted_content, nav=config['SOCIAL'], site=config['SITE'])

@app.route('/files/<slug>')
def single_post(slug):
    config = get_config()

    if config['SITE']['path_to_use'] == 'local':
        dir = os.listdir(path)

        for file in dir:
            if not file.startswith('.'):
                # print('not a dotfile, opening and reading')
                with open(path + file, 'r') as f:
                    txt = f.readlines()
                    if check_for_title(txt, slug):
                        # print("Matched a title and slug")
                        item = process_text_file(txt)
                        break
    elif config['SITE']['path_to_use'] == 'remote':
        req = requests.get(path).json()
        for f in req:
            item = requests.get(f['download_url'])
            str = item.content.decode('ascii')
            txt = str.split('\n')
            if check_for_title(txt, slug):
                # print("Processing the text for display")
                item = process_text_file(txt)
                break
    else:
        return render_template('entry.html', content="Define a path in config.yml", nav=config['SOCIAL'], site=config['SITE'])

    return render_template('entry.html', content=item, nav=config['SOCIAL'], site=config['SITE'] )

def process_text_file(txt):
    # print("Processing the list")
    for i, line in enumerate(txt):

        if "title: " in txt[i]:
            title = txt[i][7:]

        if "date: " in txt[i]:
            post_date = txt[i][6:]

        if "---" in txt[i]:
            body = txt[i+1:]

    body = [line.rstrip() for line in body if line.rstrip()]

    # print(title, post_date, body)
    item = make_item(title, post_date, body)
    return item

def process_json_file(item):
    req = requests.get(item['download_url'])
    str = req.content.decode('ascii')

    txt = str.split('\n')

    item = process_text_file(txt)

    return item

if __name__ == "__main__":
    app.run()
