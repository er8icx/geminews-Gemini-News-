import google.generativeai as genai
from flask import Flask, render_template, request
import requests

app = Flask(__name__)
news_api_key = "your-news-api-key"
genai.configure(api_key="your-api-key")

def get_news(category=None, query=None):
    if query:
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={news_api_key}"
    else:
        url = url = f"https://newsapi.org/v2/everything?q={category}&sortBy=publishedAt&language=en&apiKey={news_api_key}"
    res = requests.get(url).json()
    return res.get("articles", [])

def summary(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Summarize the following news article in 2 lines:\n{text}")
    return response.text.strip()

@app.route('/', methods=['GET', 'POST'])
def home():
    articles = []
    summaries = []
    query = None

    if request.method == "POST":
        query = request.form.get("search")  
        articles = get_news(query=query)
    else:
        articles = get_news(category="general")

    for article in articles[:5]:
        text = article.get("description", "")
        summaries.append(summary(text))

    return render_template("newsindex.html",
                           articles=zip(articles, summaries),
                           query=query or "",
                           category="Search Results" if query else "General")
@app.route('/news/<category>', methods=['GET', 'POST'])
def news_by_category(category):
    articles = []
    summaries = []
    query = None

    if request.method == "POST":
        query = request.form.get("search")
        articles = get_news(category=category, query=query)
    else:
        articles = get_news(category=category)

    summaries = [summary(article.get("title", "")) for article in articles]
    return render_template("newsindex.html",
                           articles=zip(articles, summaries),
                           query=query or "",
                           category=category.title())

if __name__ == "__main__":
    app.run(debug=True)
