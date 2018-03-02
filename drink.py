# -*- coding: utf-8 -*-
from vial import Vial, render_template
from signin import signin
from register import register
from logout import logout
from redirect import redirect
from home import home
from view import view
from addsnippet import addsnippet
from editpassword import editpassword

def index(headers, body, data):
    return 'Hello', 200, {}


def hello(headers, body, data, name):
    return 'Howdy ' + name, 200, {}


def upload(headers, body, data):
    return render_template('upload.html', headers=headers, body=body, data=data), 200, {}


routes = {
    '/': home,
    '/hello/{name}': hello,
    '/upload': upload,
    '/register': register,
    '/signin': signin,
    '/logout': logout,
    '/redirect': redirect,
    '/home': home,
    '/addsnippet': addsnippet,
    '/view': view,
    '/view/': view,
    '/view/{snippet_title}': view,
    '/editpassword': editpassword,
}

app = Vial(routes, prefix='', static='/static').wsgi_app()
