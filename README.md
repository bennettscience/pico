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

## Known Issues

  - The main layout uses a grid. This can cause some display differences depending on your browser.
  - There is no commenting.

## Want to contribute?

Totally. Fork, remix, and share back your updates.
