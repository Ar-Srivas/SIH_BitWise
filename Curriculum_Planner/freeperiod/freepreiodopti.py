from flask import Flask, render_template, request
from ddgs import DDGS

app = Flask(__name__)

def academic_assistant(query): #keep this in string or else die you fool
    ddgs = DDGS()
    docs_results = ddgs.text(f"{query} beginner tutorial site:docs.python.org OR site:microsoft.com OR site:cloud.google.com", max_results=6)
    docs_links = [r['href'] for r in docs_results if 'href' in r]
    yt_results = ddgs.text(f"{query} beginner tutorial site:youtube.com", max_results=6)
    yt_links = [r['href'] for r in yt_results if 'href' in r]
    for i in yt_links:
        if 'youtube.com' not in i:
            yt_links.remove(i)
            docs_links.append(i)
    return docs_links, yt_links

@app.route("/", methods=["GET", "POST"])
def index():
    docs_links = []
    yt_links = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            docs_links, yt_links = academic_assistant(query)
    return render_template("index.html", docs_links=docs_links, yt_links=yt_links, query=query)

if __name__ == "__main__":
    app.run(debug=True)
