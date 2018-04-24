## About

Pico is a tiny blogging platform written in Flask. Instead of a database, it reads from .txt files stored anywhere.

I wanted a lightweight blogging platform, Pico was the response. Written in Python, it parses plaintext files into HTML templates. The total project comes in around 30KB for the core, so it's lightning fast and lets the browser interpret most of the details.

The theme is built to be customized. All settings are found in a YAML-formatted config file for readability and customization. If you want something new displayed on the site, create a new class and add the details. Make sure to update your templates.

You can [see a demo of Pico here](https://ohheybrian.com/pico).

## Requirements

Pico was written for Python 3+ and uses packages for Python 3. I'm not planning on making it backwards compatible at this time.

You need to install the following outside modules to run Pico on your server:

  - Flask
  - PyYaml
  - python-slugify

## Installation

If you're using a host with cPanel, you can follow [this excellent tutorial](http://calderonroberto.com/blog/how-to-deploy-a-flask-python-app-for-cheap/) on how to install with your web host. Note that not all hosts include Python in shared hosting.

I've also deployed Pico successfully on [PythonAnywhere](https://pythonanywhere.com). You can sign up for free to deploy your own project.

You can also deploy on any compatible server environment [as documented on the Flask homepage](http://flask.pocoo.org/docs/0.12/deploying/).

## Configuration

Edit `config.yml` with data you'd like to include. You can define your own object keys and values as well, but you'll need to modify templates in order for that data to be displayed on the site.

Pico can be configured to read from two locations: A local file on your server or a GitHub repo. Set the flag in `config.yml` and specify your local and remote paths. Pico will pull text files from the specified location.

```
# Define a file path as either `local` or `remote`
# Local files can be any public, web server directory
# Remote only supports GitHub repos right now
path_to_use: ''

# Path to use for local files. Absolute paths are safer than relative
# Default is 'files/'
local_path: 'files/'

# Path to your GitHub repo. Change your :username, :repo, and :dir in the string.
remote_path: 'https://api.github.com/repos/:username/:repo/contents/:dir'
```

## RSS

The Pico package comes with two RSS Python scripts: one to generate a feed based on local files and another if you're using GitHub.

### Local RSS

The local feed is using a modified version of [genRSS](https://github.com/amsehili/genRSS) by Amine SEHILI. You can set your feed up using a cron job on your server.

### GitHub RSS

GitHub provides some RSS feeds, but only at the commit level. The `jsonRss.py` script queries the GitHub Repos API and builds an RSS feed from the returned JSON object. It can also be configured to run using a cron job.

## Known Issues

  - The main layout uses a grid. This can cause some display differences depending on your browser.
  - There is no commenting.

## Want to contribute?

Totally. Fork, remix, and share back your updates.
