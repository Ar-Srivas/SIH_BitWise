from ddgs import DDGS

def academic_assistant(query: str):
    ddgs = DDGS()

    docs_results = ddgs.text(
        f"{query} beginner tutorial site:docs.python.org OR site:microsoft.com OR site:cloud.google.com",
        max_results=6
    )
    docs_links = []
    for r in docs_results:
        if 'href' in r and r['href'].startswith(('http', 'https')):
            docs_links.append({
                'title': r.get('title', 'Documentation'),
                'href': r['href'],
                'snippet': r.get('body', 'Official documentation and tutorial')
            })

    yt_results = ddgs.text(
        f"{query} beginner tutorial site:youtube.com",
        max_results=6
    )
    yt_links = []
    for r in yt_results:
        if 'href' in r and 'youtube.com' in r['href'] and r['href'].startswith(('http', 'https')):
            yt_links.append({
                'title': r.get('title', 'YouTube Tutorial'),
                'href': r['href'],
                'snippet': r.get('body', 'Video tutorial')
            })

    return docs_links, yt_links