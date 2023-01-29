import base64

import pymongo
import validators
from flask import Flask, redirect, request, render_template
from waitress import serve

from helpers.config import load_config
from helpers.qrcode import generate_qrcode
from helpers.strings import generate_random_string

app = Flask(__name__)
credentials = load_config()
client = pymongo.MongoClient(
    f"mongodb+srv://{credentials['username']}:{credentials['password']}@cluster0.stl7rpk.mongodb.net/?retryWrites=true&w=majority")
database = client.get_database("SHORTENER")
records = database.get_collection("REDIRECTS")


@app.route("/")
def index():
    return render_template("index.html", data={"message": None})


@app.route("/generate", methods=["POST"])
def generate_shortened_url():
    url = request.form.get("url")
    url_id = generate_random_string()
    data = {"url": url, "url_id": url_id}
    result = records.insert_one(data)
    if result.acknowledged:
        if not validators.url(url):
            message = "The URL is not valid"
            return render_template("index.html", data={"message": message})

        data = {"shortened_url": url_id, "original_url": url, "qr_code": generate_qrcode(url_id)}
        return render_template("success.html", data=data)
    else:
        message = "URL couldn't be registered with the database."
        return render_template("index.html", data={"message": message})


@app.route("/<url_id>")
def validate_url_id(url_id):
    id_record = records.find_one({"url_id": url_id})
    if id_record:
        return redirect(id_record["url"])
    else:
        return render_template("error.html")


if __name__ == "__main__":
    serve(app)
