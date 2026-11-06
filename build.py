"""Genera public/index.html a partir de src/index.src.html y los datos de src/data.

Uso:  python build.py
Después: git add, commit y push; Cloudflare publica public/ automáticamente.
"""
import os

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "src")
data = os.path.join(src, "data")

def read(*p):
    with open(os.path.join(*p), encoding="utf-8") as f:
        return f.read()

page = (read(src, "index.src.html")
        .replace("/*TP*/", read(data, "tp.js"))
        .replace("/*STATIONS*/", read(data, "stations.json"))
        .replace("/*ZONES*/", read(data, "zones.json"))
        .replace("/*COAST*/", read(data, "coast.json")))

# La fuente no lleva <head>: se separa en el primer </style> y se envuelve en un documento completo.
i = page.index("</style>") + len("</style>")
head, body = page[:i], page[i:]
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
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
       "<meta name=\"description\" content=\"Planificador de pesca desde costa en España: mejor hora, cebo, "
       "mareas, parte de mar, solunar, tallas y licencias.\">\n"
       + reset + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")

import hashlib
os.makedirs(os.path.join(here, "public"), exist_ok=True)
version = hashlib.sha256(doc.encode("utf-8")).hexdigest()[:12]
with open(os.path.join(here, "public", "sw.js"), "w", encoding="utf-8") as f:
    f.write(read(src, "sw.src.js").replace("__VERSION__", version))
with open(os.path.join(here, "public", "index.html"), "w", encoding="utf-8") as f:
    f.write(doc)
print("public/index.html:", len(doc.encode("utf-8")), "bytes · sw", version)
