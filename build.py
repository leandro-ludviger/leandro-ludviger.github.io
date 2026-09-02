#!/usr/bin/env python3
"""
Gera uma pagina por projeto a partir do index.html.

O site e um app React de pagina unica: o index.html contem todo o codigo e
troca de projeto por dentro. Este script cria uma copia dele em
projetos/<endereco>/index.html com o <head> proprio de cada projeto (titulo,
descricao e imagem de previa). O roteamento dentro do app le o endereco da
barra e ja abre o projeto certo.

Rodar depois de qualquer mudanca no index.html:

    python3 build.py
"""

import os
import re
import shutil

SITE = "https://leandro-ludviger.github.io"
AUTOR = "Leandro Ludviger"

# Ordem identica a do array `data` dentro do index.html.
PROJETOS = [
    {
        "slug": "sanctu-monitoring",
        "titulo": "Sanctu · Monitoring",
        "desc": "Plataforma de telemedicina que unifica agendamento, prontuário e "
                "consultas em vídeo em um único fluxo contínuo.",
        "og": None,
        "em_breve": True,
    },
    {
        "slug": "sanctu-land-design",
        "titulo": "Sanctu · Land Design",
        "desc": "Identidade visual e site do festival de design — um sistema gráfico "
                "vivo aplicado em mais de 40 peças, do ingresso ao palco.",
        "og": None,
        "em_breve": True,
    },
    {
        "slug": "sanctu",
        "titulo": "Sanctu",
        "desc": "Landing page da Sanctu — um modelo de negócio de quatro etapas "
                "explicado em uma rolagem, para três públicos diferentes.",
        "og": "/assets/og/sanctu.jpg",
        "em_breve": False,
    },
    {
        "slug": "mercado-bitcoin",
        "titulo": "App Mercado Bitcoin",
        "desc": "O app deixou de ser uma lista de preços para traders e virou um "
                "dashboard de investimentos para qualquer pessoa, numa navegação "
                "inteiramente nova.",
        "og": "/assets/og/mercado-bitcoin.jpg",
        "em_breve": False,
    },
    {
        "slug": "meridian",
        "titulo": "Meridian · Financial OS",
        "desc": "Conceito de banco digital que evolui de “mostre meu saldo” para "
                "inteligência financeira: Safe to Spend, previsão de fluxo de caixa "
                "e recomendações acionáveis.",
        "og": "/assets/og/meridian.jpg",
        "em_breve": False,
    },
]

HOME = {
    "titulo": f"{AUTOR} — Product Designer",
    "desc": "Combino curiosidade, experimentação e pensamento sistêmico para "
            "desenhar soluções escaláveis. Portfólio de product design: Sanctu, "
            "Mercado Bitcoin e Meridian.",
    "og": "/assets/og/home.jpg",
    "url": SITE + "/",
}

INICIO, FIM = "<!-- seo:inicio -->", "<!-- seo:fim -->"


def escapa(texto):
    return (texto.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace('"', "&quot;"))


def bloco_seo(titulo, desc, url, og, noindex=False):
    t, d = escapa(titulo), escapa(desc)
    linhas = [
        INICIO,
        f"<title>{t}</title>",
        f'<meta name="description" content="{d}">',
        f'<link rel="canonical" href="{url}">',
        f'<meta name="author" content="{AUTOR}">',
        # o .ico atende navegador antigo; o .svg troca de cor com o tema do sistema
        '<link rel="icon" href="/favicon.ico" sizes="32x32">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Leandro Ludviger">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:locale" content="pt_BR">',
        '<meta property="og:locale:alternate" content="en_US">',
    ]
    if og:
        linhas += [
            f'<meta property="og:image" content="{SITE}{og}">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:image" content="{SITE}{og}">',
        ]
    else:
        linhas.append('<meta name="twitter:card" content="summary">')
    linhas += [
        f'<meta name="twitter:title" content="{t}">',
        f'<meta name="twitter:description" content="{d}">',
    ]
    if noindex:
        linhas.append('<meta name="robots" content="noindex, follow">')
    linhas.append(FIM)
    return "\n".join(linhas)


def caminhos_absolutos(html):
    """Deixa os caminhos de arquivo absolutos, para funcionarem tambem a
    partir de /projetos/<endereco>/."""
    html = re.sub(r'(["\'])assets/', r"\1/assets/", html)
    html = html.replace('src="support.js"', 'src="/support.js"')
    return html


def aplica_seo(html, seo):
    """Insere (ou substitui) o bloco de SEO logo depois do <meta charset>."""
    html = re.sub(re.escape(INICIO) + r".*?" + re.escape(FIM), "", html, flags=re.S)
    ancora = '<meta name="viewport" content="width=device-width, initial-scale=1">'
    if ancora not in html:
        raise SystemExit("Nao achei a meta viewport no index.html — verifique o arquivo.")
    return html.replace(ancora, ancora + "\n" + seo, 1)


def main():
    raiz = os.path.dirname(os.path.abspath(__file__))
    os.chdir(raiz)

    html = open("index.html", encoding="utf-8").read()
    html = caminhos_absolutos(html)
    html = html.replace("<html>", '<html lang="pt-BR">', 1)

    # 1) home
    home = aplica_seo(html, bloco_seo(HOME["titulo"], HOME["desc"], HOME["url"], HOME["og"]))
    open("index.html", "w", encoding="utf-8").write(home)
    print(f"  /                              {len(home) // 1024} KB")

    # 2) uma pasta por projeto
    if os.path.isdir("projetos"):
        shutil.rmtree("projetos")
    urls = [(HOME["url"], "1.0")]
    for p in PROJETOS:
        url = f"{SITE}/projetos/{p['slug']}/"
        pagina = aplica_seo(html, bloco_seo(p["titulo"], p["desc"], url, p["og"], p["em_breve"]))
        destino = os.path.join("projetos", p["slug"])
        os.makedirs(destino, exist_ok=True)
        open(os.path.join(destino, "index.html"), "w", encoding="utf-8").write(pagina)
        marca = "  (em breve, fora do Google)" if p["em_breve"] else ""
        print(f"  /projetos/{p['slug']}/".ljust(31) + f"{len(pagina) // 1024} KB{marca}")
        if not p["em_breve"]:
            urls.append((url, "0.8"))

    # 3) sitemap e robots, para o Google achar cada projeto
    itens = "\n".join(
        f"  <url><loc>{u}</loc><priority>{pr}</priority></url>" for u, pr in urls
    )
    open("sitemap.xml", "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{itens}\n</urlset>\n"
    )
    open("robots.txt", "w", encoding="utf-8").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"
    )
    print(f"  sitemap.xml + robots.txt       {len(urls)} endereços")


if __name__ == "__main__":
    main()
