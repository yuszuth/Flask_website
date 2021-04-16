import random
import requests
import json
import hashlib
from num2words import num2words
from flask import Flask, render_template, abort, request, redirect, url_for

app = Flask(__name__)


# proxies = {
#     "http": "http://192.168.2.1:3128",
#     "https": "http://192.168.2.1:3128"
# }


# Task3 functions
def comp_handle(e):
    return e[0]


def comp_rating(e):
    return e[1]


# Task1
@app.route('/')
def menu():
    return render_template("task1_menu.html")


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
    return render_template("task1_random.html", s=s)


@app.route('/task1/i_will_not/')
def willnot():
    s = ["I will not miss Ramil abiy's lessons"] * 100
    third_out = "<ul id=blackboard>"
    for i in range(100):
        f = s[i]
        third_out += "<li>{}</li>".format(f)
    third_out += "</ul>"
    return third_out


# Task2
@app.route('/task2/avito/<city>/<category>/<ad>/')
def avitooo(city, category, ad):
    ans = city + category + ad
    x = ad.split('_')
    return render_template("task2_links.html", city=city, category=category, ad=ad, ans=ans, x=x)


@app.route('/task2/cf/profile/<username>/')
def codeforces(username):
    data = requests.get(f'https://codeforces.com/api/user.info?handles={username}').json()
    # print(data)
    if data['status'] == 'OK':
        rating = data['result'][0]['rating']
        return render_template("task2_cfs.html", username=username, rating=rating)
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


# Task3
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
        return render_template("task3_links.html", time=time, problem=problem, verdict=verdict, handle=handle,
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
        cur_handle = data['result'][0]['handle']
        rating = data['result'][0]['rating']
        elements.append((cur_handle, rating))
    if sort_check == 'rating':
        elements.sort(key=comp_rating, reverse=True)
    else:
        elements.sort(key=comp_handle)
    return render_template("task3_top.html", elements=elements)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('task3_404.html'), 404


# Task4

santa_set = {
    "token": "4UffYATBFJOqTiy9aJDnajwBa5XrSTfy",
    "secret": "f61a804d43aff225ef9986f247de5112",
    "command": "set",
    "key": "",
    "value": ""
}

data_set = santa_set

santa_get = {
    "token": "4UffYATBFJOqTiy9aJDnajwBa5XrSTfy",
    "secret": "f61a804d43aff225ef9986f247de5112",
    "command": "get",
    "key": ""
}

data_get = santa_get


@app.route('/task4/santa/create', methods=['POST', 'GET'])
def creation():
    if request.method == 'POST':
        form_input = request.form
        game_name = form_input["input_name"]
        link_pad = hashlib.md5(bytes(str(random.randint(0, 2 ** 128)) + game_name, encoding='utf-8')).hexdigest()
        secret = hashlib.md5(bytes(str(random.randint(0, 2 ** 128)), encoding='utf-8')).hexdigest()
        game_link = f"/task4/santa/play/{link_pad}"
        toss_link = f" /task4/santa/toss/{link_pad}/{secret}"
        post_data = {"name": game_name, "pad": link_pad, "secret": secret, "link_play": game_link,
                     "link_toss": toss_link, "activity": True, "players": []}
        data_set['key'] = link_pad
        data_set['value'] = json.dumps(post_data)
        requests.post('https://arsenwisheshappy2021.herokuapp.com/query', data=data_set)
        return render_template("task4_created.html", game=game_link, toss=toss_link)
    else:
        return render_template("task4_create.html")


@app.route('/task4/santa/play/<link>', methods=['POST', 'GET'])
def player(link):
    if request.method == 'POST':
        form_input = request.form
        player_name = form_input["name"]
        if player_name.strip(' ') == '':
            new_link = f'/task4/santa/play/{link}'
            return render_template('task4_player.html', link=new_link, player_name_fail=True, finished_game_fail=False)
        data_get["key"] = link
        _get = requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_get)
        game_info = json.loads(_get.text)
        game_info["players"].append(player_name)
        data_set["key"] = link
        data_set["value"] = json.dumps(game_info)
        requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_set)

        return render_template("task4_successful_game.html", name=player_name)
    else:
        new_link = f'/task4/santa/play/{link}'
        data_get["key"] = link
        _get = requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_get)
        game_info = json.loads(_get.text)
        if not game_info["activity"]:
            return render_template("task4_player.html", link=new_link, player_name_fail=False, finished_game_fail=True)
        else:
            return render_template("task4_player.html", link=new_link, player_name_fail=False, finished_game_fail=False)


@app.route('/task4/santa/toss/<link>/<secret>', methods=['POST', 'GET'])
def toss(link, secret):
    if request.method == 'GET':
        data_get["key"] = link
        _get = requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_get)
        game_info = json.loads(_get.text)
        if game_info["activity"] == "False":
            finished_game_fail = True
        else:
            finished_game_fail = False
        players = game_info["players"]
        if len(players) == 0 or len(players) % 2 == 1:
            players_count_fail = True
        else:
            players_count_fail = False
        new_link = "/task4/santa/toss/{link}/{secret}".format(link=link, secret=secret)
        return render_template("task4_pre_toss.html", finished_game_fail=finished_game_fail,
                               players_count_fail=players_count_fail, players=players, new_link=new_link)
    else:
        data_get["key"] = link
        _get = requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_get)
        game_info = json.loads(_get.text)
        players = game_info["players"]
        random.shuffle(players)
        pairs = dict()
        for i in range(0, len(players) // 2):
            pairs.update({players[i * 2]: players[i * 2 + 1]})
        game_info["activity"] = "False"
        data_set["key"] = link
        data_set["value"] = json.dumps(game_info)
        requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_set)
        first_players = list(pairs.keys())
        return render_template("task4_post_toss.html", pairs=pairs, first_players=first_players)


if __name__ == "__main__":
    app.debug = True
    app.run()
