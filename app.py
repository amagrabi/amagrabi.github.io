from datetime import datetime

import feedparser
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory, url_for

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static/img", "favicon.png", mimetype="image/vnd.microsoft.icon")


@app.route("/")
def home():
    medium_feed = feedparser.parse("https://medium.com/feed/@amadeus.magrabi")
    posts = []
    for entry in medium_feed.entries:
        post_content = entry.content[0].value if "content" in entry else entry.summary
        soup = BeautifulSoup(post_content, "html.parser")
        image_tag = soup.find("img")
        post = {
            "title": entry.title,
            "link": entry.link,
            "published": datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z").strftime("%d %b %Y"),
            "image": image_tag["src"] if image_tag else url_for("static", filename="img/default_image.jpg"),
        }
        posts.append(post)

    return render_template("index.html", posts=posts)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
