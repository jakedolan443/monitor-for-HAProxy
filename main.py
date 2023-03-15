from flask import Flask, render_template, request, jsonify
import json
from geoip import GeolocationDB
import hashlib


app = Flask(__name__, static_url_path='', static_folder='public/static', template_folder='public/serve')


def get_id_from_row(row):
    return row.split(" ")[-1]

def get_user_config(username):
    try:
        with open("users/{}.json".format(username), "r") as f:
            user_data = json.loads(f.read())
        user_data['passkey_hash'] = "";
        return user_data
    except FileNotFoundError:
        return {}

def get_user_hash(username):
    try:
        with open("users/{}.json".format(username), "r") as f:
            user_data = json.loads(f.read())
        return user_data['passkey_hash']
    except FileNotFoundError:
        return ""
    
def verify_auth(passkey, username):
    user_hash = get_user_hash(username)
    if user_hash == hashlib.md5(passkey.encode('utf-8')).hexdigest():
        return True
    else:
        return False
        
    
    
    
def data_to_line(data):
    line = data.split(" ")[5:]
    new_ls = []
    print(line)
    new_ls.append(line[0])
    new_ls.append(line[1].split(":")[0])
    new_ls.append(line[1].split(":")[1])
    geoinfo = GeoDB.IPToGeolocation(line[1].split(":")[0])
    print(geoinfo)
    new_ls.append(geoinfo['country'])
    new_ls.append(geoinfo['region'])
    new_ls.append(geoinfo['city'])
    new_ls.append(geoinfo['lat'])
    new_ls.append(geoinfo['lon'])
    new_ls.append(line[2].split(":")[0])
    new_ls.append(line[2].split(":")[1])
    new_ls.append(line[3])
    new_ls.append(line[4])
    new_ls.append(line[5])
    new_ls.append(line[6])
    new_ls.append(line[7])
    new_ls.append(line[8])
    return new_ls
    GeoDB.IPToGeolocation("195.191.219.132")

@app.route("/live", methods=["POST"])
def Live_POST():
    req = request.json
    if verify_auth(req['token'], req['username']):
        with open("haproxy.log", "r") as f:
            data = f.readlines()
        identified = False
        lines = []
        for i in range(len(data)):
            if get_id_from_row(data[i]) == req['ref_id']:
                identified = True
                lines = []
                continue
            if identified:
                line = data_to_line(data[i])
                lines.append(line)
                
        if not identified:
            for i in range(len(data)):
                line = data_to_line(data[i])
                lines.append(line)
                
        return jsonify({"data":lines})
    else:
        return "Unauthorised", 401


@app.route("/login", methods=["POST"])
def Login_POST():
        req = request.json
        if verify_auth(req['password'], req['username']):
            return {"data":"Authorised"}
        else:
            return {"data":"Unauthorised"}

@app.route("/config", methods=["POST"])
def Config_POST():
        req = request.json
        if verify_auth(req['token'], req['username']):
            return jsonify(get_user_config(req['username']))
        else:
            return "Unauthorised", 401




@app.route("/")
def ROUTE_Default():
    return render_template("default.html")

GeoDB = GeolocationDB()
app.run(host="0.0.0.0", port=5000, debug=True)
