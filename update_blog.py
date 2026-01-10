import os, re
from datetime import datetime, timedelta

BLOG_DIR = "blog"
INDEX_FILE = "blog/index.html"
SITE_URL = "https://dentistjalpaiguri.github.io"

FEATURED_START = "<!-- FEATURED_START -->"
FEATURED_END = "<!-- FEATURED_END -->"
BLOG_START = "<!-- BLOG_START -->"
BLOG_END = "<!-- BLOG_END -->"

TODAY = datetime.utcnow()

def read(file):
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

def write(file, data):
    with open(file, "w", encoding="utf-8") as f:
        f.write(data)

def extract(pattern, text, default=""):
    m = re.search(pattern, text, re.I)
    return m.group(1).strip() if m else default

def get_post(file):
    html = read(file)

    title = extract(r"<title>(.*?)</title>", html, "Untitled")
    desc = extract(r'<meta name="description" content="(.*?)"', html, "")
    date = extract(r'<time datetime="(.*?)">', html, "2025-01-01")
    image = extract(r'<meta property="og:image" content="(.*?)"', html, "../assets/images/logo.png")
    keywords = extract(r'<meta name="keywords" content="(.*?)"', html, "General Dentistry")

    post_date = datetime.strptime(date, "%Y-%m-%d")
    is_new = (TODAY - post_date).days <= 7

    # Discover image rule
    discover_ok = "1200" in image or "1200x" in image

    return {
        "file": os.path.basename(file),
        "title": title,
        "desc": desc,
        "date": date,
        "image": image,
        "category": keywords.split(",")[0],
        "new": is_new,
        "featured": discover_ok
    }

def card(p):
    badge = '<span class="badge">NEW</span>' if p["new"] else ""
    return f"""
    <article class="blog-card">
        <img src="{p['image']}" alt="{p['title']}" loading="lazy">
        <div class="blog-info">
            {badge}
            <span class="category">{p['category']}</span>
            <h3><a href="{p['file']}">{p['title']}</a></h3>
            <p>{p['desc']}</p>
            <time datetime="{p['date']}">{p['date']}</time>
        </div>
    </article>
    """

def main():
    posts = []

    for f in os.listdir(BLOG_DIR):
        if f.endswith(".html") and f != "index.html":
            posts.append(get_post(os.path.join(BLOG_DIR, f)))

    posts.sort(key=lambda x: x["date"], reverse=True)

    featured = next((p for p in posts if p["featured"]), posts[0])

    index = read(INDEX_FILE)

    index = re.sub(
        f"{FEATURED_START}.*?{FEATURED_END}",
        FEATURED_START + card(featured) + FEATURED_END,
        index,
        flags=re.S
    )

    index = re.sub(
        f"{BLOG_START}.*?{BLOG_END}",
        BLOG_START + "".join(card(p) for p in posts) + BLOG_END,
        index,
        flags=re.S
    )

    write(INDEX_FILE, index)
    print("✅ Blog index auto-updated successfully")

if __name__ == "__main__":
    main()
