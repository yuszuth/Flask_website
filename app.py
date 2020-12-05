from flask import Flask, render_template

import random

app = Flask(__name__)


@app.route('/<city>/<category>/<ad>/')
def menu(city, category, ad):
    s = [city, category, ad]
    nouns = ("puppy", "car", "rabbit", "girl", "monkey")
    verbs = ("runs", "hits", "jumps", "drives", "barfs")
    adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
    adj = ("adorable", "clueless", "dirty", "odd", "stupid")
    ans = random.choice(adj) + " " + random.choice(nouns) + " " + random.choice(verbs) + " " + random.choice(adv)
    x = ad.split('_')
    return render_template("links.html", city=city, category=category, ad=ad, ans=ans, x=x)


if __name__ == "__main__":
    app.debug = True
    app.run()
