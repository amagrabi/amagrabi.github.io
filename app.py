import os
from datetime import datetime, timedelta
from functools import lru_cache

import feedparser
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, send_from_directory, url_for
from flask_talisman import Talisman

app = Flask(__name__)

# Configure Talisman for security headers
Talisman(app, 
    content_security_policy={
        'default-src': [
            "'self'",
            "'unsafe-inline'",
            "'unsafe-eval'",
            "cdnjs.cloudflare.com",
            "*.googletagmanager.com",
            "*.google-analytics.com",
            "www.youtube.com",
            "fonts.googleapis.com",
            "fonts.gstatic.com",
        ],
        'img-src': [
            "'self'",
            "data:",
            "*.medium.com",
            "miro.medium.com",
            "cdn-images-1.medium.com",
            "www.youtube.com",
            "*.ytimg.com",
            "i.ytimg.com",
            "img.youtube.com",
            "i9.ytimg.com", 
            "s.ytimg.com",
            "*.googleusercontent.com",
        ],
        'frame-src': [
            "'self'",
            "www.youtube.com",
            "youtube.com",
            "*.youtube-nocookie.com",
        ],
        'font-src': [
            "'self'",
            "cdnjs.cloudflare.com",
            "fonts.gstatic.com",
            "fonts.googleapis.com",
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",
            "cdnjs.cloudflare.com",
            "fonts.googleapis.com",
        ],
        'connect-src': [
            "'self'",
            "www.youtube.com",
            "*.google-analytics.com",
            "*.googletagmanager.com",
        ],
    },
    content_security_policy_nonce_in=['script-src']
)

# Cache the Medium feed for 1 hour to avoid hitting rate limits
@lru_cache(maxsize=1)
def get_medium_posts():
    cache_time = datetime.now()
    try:
        medium_feed = feedparser.parse("https://medium.com/feed/@amadeus.magrabi")
        posts = []
        
        for entry in medium_feed.entries[:6]:  # Limit to 6 most recent posts
            try:
                post_content = entry.content[0].value if "content" in entry else entry.summary
                soup = BeautifulSoup(post_content, "html.parser")
                image_tag = soup.find("img")
                
                # Extract a short description for SEO
                text_content = soup.get_text()
                description = text_content[:160] + "..." if len(text_content) > 160 else text_content
                
                # Format the date
                published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
                formatted_date = published_date.strftime("%d %b %Y")
                iso_date = published_date.strftime("%Y-%m-%d")
                
                post = {
                    "title": entry.title,
                    "link": entry.link,
                    "published": formatted_date,
                    "iso_date": iso_date,
                    "description": description,
                    "image": image_tag["src"] if image_tag else url_for("static", filename="img/brain_half.jpg"),
                }
                posts.append(post)
            except Exception as e:
                app.logger.error(f"Error processing post {entry.title}: {str(e)}")
                continue
                
        return posts, cache_time
    except Exception as e:
        app.logger.error(f"Error fetching Medium feed: {str(e)}")
        return [], cache_time

@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static/img", "favicon.png", mimetype="image/vnd.microsoft.icon")

@app.route("/")
def home():
    posts, cache_time = get_medium_posts()
    
    # If cache is older than 1 hour, invalidate it
    if datetime.now() - cache_time > timedelta(hours=1):
        get_medium_posts.cache_clear()
        posts, _ = get_medium_posts()
    
    # Generate dynamic meta data for SEO
    meta = {
        "title": "Dr. Amadeus Magrabi | AI Engineer",
        "description": "Personal website of Dr. Amadeus Magrabi, specializing in AI, Machine Learning, and Data Science.",
        "url": request.url,
        "image": url_for("static", filename="img/brain_full_r.jpg", _external=True)
    }
    
    return render_template("index.html", posts=posts, meta=meta)

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")

@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
