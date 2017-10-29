import logging

import flask
from flask import Flask, render_template, json

from classes.iso3166 import ISO3166

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    SERVER_NAME="isoapi.com:5000"
)


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    return render_template('hello.html', name=name)


"""
For subdomains
"""
headers_get = {
    'Content-Type' : 'application/json;charset=utf-8',
    'Access-Control-Allow-Origin' : '*',
    'Access-Control-Allow-Methods' : 'GET',
    'Access-Control-Allow-Headers' : 'Accept, X-Requested-With'
}

resp = flask.Response()
resp.headers = headers_get

@app.route('/', subdomain="api")
def hello_api():
    return "Hello API"


@app.route('/iso3166/all', subdomain="api")
def get_iso3166_all():
    iso3166 = ISO3166()
    resp.data = json.dumps(iso3166.countries)
    return resp


@app.route('/iso3166/alpha2/<alpha2>', subdomain='api')
def get_iso3166_by_alpha2(alpha2):
    iso3166 = ISO3166()
    resp.data = json.dumps(iso3166.filter_by_alpha2(alpha2))
    return resp


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                        help="run in debug mode (for use with PyCharm)", default=False)
    parser.add_argument("-p", "--port", dest="port",
                        help="port of server (default:%(default)s)", type=int, default=5000)

    cmd_args = parser.parse_args()
    app_options = {"port": cmd_args.port}

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False

    app.run(**app_options)