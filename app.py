from flask import Flask
import ra
app = Flask(__name__)

@app.route('/')
@app.route('/haba')
def hello_world():

    s = ["Hello, Haba!",
        "Hello, Arsen!",
        "Hello, Karim!",]

    out = "<pre>{}</pre>".format("\n".join(s))
    return out

@app.route('/random')
def random():
	print("Haba's mark if ", sep="", end="")
	print(random.randint(0, 100))
