import random
import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/task2/<city>/<category>/<ad>/')
def avitooo(city, category, ad):
    s = [city, category, ad]
    nouns = ("puppy", "car", "rabbit", "girl", "monkey")
    verbs = ("runs", "hits", "jumps", "drives", "barfs")
    adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
    adj = ("adorable", "clueless", "dirty", "odd", "stupid")
    ans = random.choice(adj) + " " + random.choice(nouns) + " " + random.choice(verbs) + " " + random.choice(adv)
    x = ad.split('_')
    return render_template("links.html", city=city, category=category, ad=ad, ans=ans, x=x)


@app.route('/task2/cf/profile/<username>/')
def codeforces(username):
    data = requests.get(f'https://codeforces.com/api/user.info?handles={username}').json()
    print(data)
    if data['status'] == 'OK':
        rating = data['result'][0]['rating']
        return render_template("cfs.html", username=username, rating=rating)
    else:
        s = 'User not found'
        return s


if __name__ == "__main__":
    app.debug = True
    app.run()