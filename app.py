from flask import Flask, request, render_template
import socket
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def get_geo(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return res if res["status"] == "success" else None
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        domain = request.form["domain"]
        ip = get_ip(domain)
        if ip:
            geo = get_geo(ip)
            if geo:
                data = {
                    "domain": domain,
                    "ip": ip,
                    "location": f'{geo["city"]}, {geo["regionName"]}, {geo["country"]}',
                    "lat": geo["lat"],
                    "lon": geo["lon"],
                    "isp": geo["isp"],
                    "org": geo["org"],
                    "timezone": geo["timezone"],
                }
    google_maps_key = os.getenv("GOOGLE_MAPS_API_KEY")
    return render_template("index.html", data=data, google_maps_key=google_maps_key)

if __name__ == "__main__":
    app.run(debug=True)
