import random
import requests
import json
from num2words import num2words
from flask import Flask, render_template, abort, request, redirect, url_for

app = Flask(__name__)


# proxies = {
    # "http": "http://192.168.2.1:3128",
    # "https": "http://192.168.2.1:3128"
# }


def comp_handle(e):
    return e[0]

def comp_rating(e):
    return e[1]


@app.route('/')
def menu():
    return render_template("menu.html")


@app.route('/task1/haba/')
def hello_world():
    s = ["hey, man!?!",
         "   what are you doing here?",
         "      never mind",
         "         #define aidar asadullin"]
    out = "<pre>{}</pre>".format("\n".join(s))
    return out


@app.route('/task1/random/')
def rand():
    s = f"Yusuf's mark is {random.randint(0, 100)}"
    return render_template("random.html", s=s)


@app.route('/task1/i_will_not/')
def willnot():
    s = ["I will not miss Ramil abiy's lessons"] * 100
    third_out = "<ul id=blackboard>"
    for i in range(100):
        f = s[i]
        third_out += "<li>{}</li>".format(f)
    third_out += "</ul>"
    return third_out


@app.route('/task2/avito/<city>/<category>/<ad>/')
def avitooo(city, category, ad):
    ans = city + category + ad
    x = ad.split('_')
    return render_template("links_task2.html", city=city, category=category, ad=ad, ans=ans, x=x)


@app.route('/task2/cf/profile/<username>/')
def codeforces(username):
    data = requests.get(f'https://codeforces.com/api/user.info?handles={username}').json()
    # print(data)
    if data['status'] == 'OK':
        rating = data['result'][0]['rating']
        return render_template("cfs.html", username=username, rating=rating)
    else:
        s = 'User not found'
        return s


@app.route('/task2/num2words/<int:num>/')
def numbers_to_words(num):
    json_dict = dict()
    if 0 <= num <= 999:
        ch = False
        if num % 2 == 0:
            ch = True
        json_dict["status"] = "OK"
        json_dict["number"] = num
        json_dict["isEven"] = ch
        json_dict["words"] = num2words(num)
    else:
        json_dict["status"] = "FAIL"
    return json.dumps(json_dict)


@app.route('/task3/cf/profile/<handle>/')
def only(handle):
    return redirect(url_for('single', handle=handle, page_number='1'))


@app.route('/task3/cf/profile/<handle>/page/<page_number>/')
def single(handle, page_number):
    page_number = int(page_number)
    p_n = int(page_number)
    data = requests.get(f'http://codeforces.com/api/user.status?handle={handle}&from=1&count=100').json()
    print(data)
    if data['status'] == 'OK':
        time = list()
        problem = list()
        verdict = list()
        for txt in data['result']:
            time.append(txt["creationTimeSeconds"])
            pr = txt["problem"]
            problem.append(pr["name"])
            verdict.append(txt["verdict"])
        page_cnt = len(time) // 25 if len(time) % 25 == 0 else len(time) // 25 + 1

        if page_number > page_cnt:
            return abort(404)

        start = (p_n - 1) * 25
        end = min(start + 25, len(time))
        was_f = True
        was_l = True
        return render_template("links.html", time=time, problem=problem, verdict=verdict, handle=handle,
                               page_cnt=page_cnt, page_number=page_number, start=start, end=end)
    else:
        return abort(404)


@app.route('/task3/cf/top/')
def cf_top():
    handles = request.args.get('handles').split('|')
    sort_check = request.args.get('orderby')
    elements = list()
    for i in range(len(handles)):
        handle = handles[i]
        data = requests.get(f'https://codeforces.com/api/user.info?handles={handle}').json()
        rating = data['result'][0]['rating']
        elements.append((handle, rating))
    if sort_check == 'handle':
        elements.sort(key=comp_handle)
    elif sort_check == 'rating':
        elements.sort(key=comp_rating, reverse=True)
    return render_template("top.html", elements=elements)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.debug = True
    app.run()
