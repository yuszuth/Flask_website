from flask import Flask
import urllib

import random

app = Flask(__name__)

@app.route('/')
def menu():
    f = open("links.html")
    out = "<pre>{}</pre>".format("\n".join(f))
    return out

@app.route('/haba')
def hello_world():
    s = ["Hello, Haba!",
         "Hello, Arsen!",
         "Hello, Karim!", ]

    out = "<pre>{}</pre>".format("\n".join(s))
    return out


@app.route('/random')
def rand():
    s = [f"Haba's mark if {random.randint(0, 100)}"]

    sec_out = "<pre>{}</pre>".format("\n".join(s))
    return sec_out


@app.route('/i_will_not')
def willnot():
    s = ["I will not waste time"] * 100

    third_out = "<pre>{}</pre>".format("\n".join(s))
    return third_out


if __name__ == "__main__":
    app.debug = True
    app.run()
