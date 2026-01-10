import os,re,datetime

BLOG_DIR="blog"
INDEX="blog/index.html"
SITEMAP="blog-sitemap.xml"

def read(f): return open(f,encoding="utf-8").read()

posts=[]
for f in os.listdir(BLOG_DIR):
    if f.endswith(".html") and f!="index.html":
        c=read(f"{BLOG_DIR}/{f}")
        title=re.search(r"<title>(.*?)</title>",c,re.I)
        desc=re.search(r'name="description" content="(.*?)"',c,re.I)
        img=re.search(r'og:image" content="(.*?)"',c)
        date=re.search(r'datetime="(.*?)"',c)
        posts.append({
            "file":f,
            "title":title.group(1) if title else f,
            "desc":desc.group(1) if desc else "",
            "img":img.group(1) if img else "../assets/images/logo.png",
            "date":date.group(1) if date else "2025-01-01"
        })

posts.sort(key=lambda x:x["date"],reverse=True)

cards=""
for p in posts:
    cards+=f"""
<div class="blog-card">
<img src="{p['img']}">
<div class="blog-info">
<span class="badge">ARTICLE</span>
<h3><a href="{p['file']}">{p['title']}</a></h3>
<p>{p['desc']}</p>
<time>{p['date']}</time>
</div>
</div>
"""

featured=f"""
<div class="blog-card">
<img src="{posts[0]['img']}">
<div class="blog-info">
<span class="badge">FEATURED</span>
<h3><a href="{posts[0]['file']}">{posts[0]['title']}</a></h3>
<p>{posts[0]['desc']}</p>
</div>
</div>
"""

html=read(INDEX)
html=re.sub("<!-- BLOG_START -->.*?<!-- BLOG_END -->",
f"<!-- BLOG_START -->{cards}<!-- BLOG_END -->",html,flags=re.S)

html=re.sub("<!-- FEATURED_START -->.*?<!-- FEATURED_END -->",
f"<!-- FEATURED_START -->{featured}<!-- FEATURED_END -->",html,flags=re.S)

open(INDEX,"w",encoding="utf-8").write(html)

# Sitemap
urls=""
for p in posts:
    urls+=f"""
<url><loc>https://dentistjalpaiguri.github.io/blog/{p['file']}</loc></url>
"""

open(SITEMAP,"w").write(f"""<?xml version="1.0"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>""")
