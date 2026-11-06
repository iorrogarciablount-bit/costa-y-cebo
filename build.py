"""Genera public/index.html a partir de src/index.src.html y los datos de src/data.

Uso:  python build.py
Después: git add, commit y push; Cloudflare publica public/ automáticamente.
"""
import os

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "src")
data = os.path.join(src, "data")

import json

def read(*p):
    with open(os.path.join(*p), encoding="utf-8") as f:
        return f.read()

site = json.loads(read(src, "site.json"))
page = (read(src, "index.src.html")
        .replace("/*SITE*/", json.dumps({"url": site["url"], "old": site["old_hosts"]}))
        .replace("/*TP*/", read(data, "tp.js"))
        .replace("/*STATIONS*/", read(data, "stations.json"))
        .replace("/*ZONES*/", read(data, "zones.json"))
        .replace("/*COAST*/", read(data, "coast.json")))

# La fuente no lleva <head>: se separa en el primer </style> y se envuelve en un documento completo.
i = page.index("</style>") + len("</style>")
head, body = page[:i], page[i:]
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
head = head.replace("<title>Costa y Cebo</title>", f"<title>{site['title']}</title>")
reset = ("<style>\n:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);"
         "padding-bottom:env(safe-area-inset-bottom,0px)}\nbody{margin:0}\nimg{max-width:100%}\n"
         "[hidden]{display:none!important}\n</style>\n")
doc = ("<!doctype html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
       "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
       "<meta name=\"theme-color\" content=\"#1b7cc0\">\n"
       "<link rel=\"manifest\" href=\"manifest.webmanifest\">\n"
       "<link rel=\"icon\" href=\"icons/icon-192.png\" type=\"image/png\">\n"
       "<link rel=\"apple-touch-icon\" href=\"icons/apple-touch-icon.png\">\n"
       "<meta name=\"apple-mobile-web-app-capable\" content=\"yes\">\n"
       f"<meta name=\"description\" content=\"{site['description']}\">\n"
       f"<link rel=\"canonical\" href=\"{site['url']}\">\n"
       "<meta property=\"og:type\" content=\"website\">\n"
       "<meta property=\"og:locale\" content=\"es_ES\">\n"
       "<meta property=\"og:site_name\" content=\"Costa y Cebo\">\n"
       f"<meta property=\"og:title\" content=\"{site['title']}\">\n"
       f"<meta property=\"og:description\" content=\"{site['description']}\">\n"
       f"<meta property=\"og:url\" content=\"{site['url']}\">\n"
       f"<meta property=\"og:image\" content=\"{site['url']}og.png\">\n"
       "<meta property=\"og:image:width\" content=\"1200\">\n<meta property=\"og:image:height\" content=\"630\">\n"
       "<meta property=\"og:image:alt\" content=\"Costa y Cebo, planificador de pesca desde costa\">\n"
       "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
       + reset + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")

import hashlib
os.makedirs(os.path.join(here, "public"), exist_ok=True)
with open(os.path.join(here, "public", "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {site['url']}sitemap.xml\n")
with open(os.path.join(here, "public", "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{site["url"]}</loc></url></urlset>\n')
version = hashlib.sha256(doc.encode("utf-8")).hexdigest()[:12]
with open(os.path.join(here, "public", "sw.js"), "w", encoding="utf-8") as f:
    f.write(read(src, "sw.src.js").replace("__VERSION__", version))
with open(os.path.join(here, "public", "index.html"), "w", encoding="utf-8") as f:
    f.write(doc)
print("public/index.html:", len(doc.encode("utf-8")), "bytes · sw", version)
