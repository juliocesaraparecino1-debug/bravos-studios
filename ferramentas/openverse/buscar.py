#!/usr/bin/env python3
"""Busca mídia livre (CC0, CC BY, etc.) na API pública do Openverse e baixa o arquivo.

Uso:
  python3 ferramentas/openverse/buscar.py audio "whoosh" --licenca cc0 -n 5
  python3 ferramentas/openverse/buscar.py images "barbearia" -n 5 --baixar saida/
Mostra título, autor, licença, link da página e URL do arquivo. Guarde a atribuição
quando a licença exigir crédito (tudo que não for CC0 / domínio público).
Docs da API: https://api.openverse.org/v1/
"""
import argparse, json, os, sys, urllib.parse, urllib.request

API = "https://api.openverse.org/v1"
UA = {"User-Agent": "bravos-studios-ferramentas/1.0"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("tipo", choices=["audio", "images"])
    p.add_argument("consulta")
    p.add_argument("-n", type=int, default=5)
    p.add_argument("--licenca", help="ex.: cc0, by, by-sa, pdm (separe por vírgula)")
    p.add_argument("--baixar", metavar="PASTA", help="baixa os resultados nessa pasta")
    a = p.parse_args()
    q = {"q": a.consulta, "page_size": a.n}
    if a.licenca:
        q["license"] = a.licenca
    data = json.loads(get(f"{API}/{a.tipo}/?" + urllib.parse.urlencode(q)))
    for i, it in enumerate(data.get("results", []), 1):
        print(f"{i}. {it.get('title')} — {it.get('creator')} [{it.get('license')} {it.get('license_version') or ''}]")
        print(f"   página: {it.get('foreign_landing_url')}\n   arquivo: {it.get('url')}")
        if a.baixar:
            os.makedirs(a.baixar, exist_ok=True)
            ext = os.path.splitext(urllib.parse.urlparse(it["url"]).path)[1] or (".mp3" if a.tipo == "audio" else ".jpg")
            dest = os.path.join(a.baixar, f"{it['id']}{ext}")
            open(dest, "wb").write(get(it["url"]))
            open(dest + ".json", "w").write(json.dumps({k: it.get(k) for k in ("title", "creator", "license", "license_version", "foreign_landing_url", "url", "attribution")}, ensure_ascii=False, indent=1))
            print(f"   salvo: {dest}")
    if not data.get("results"):
        print("nada encontrado", file=sys.stderr)

if __name__ == "__main__":
    main()
