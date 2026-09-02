# Portfólio — Leandro Ludviger

Site publicado em **https://leandro-ludviger.github.io**

| Projeto | Endereço |
| --- | --- |
| Sanctu | `/projetos/sanctu/` |
| App Mercado Bitcoin | `/projetos/mercado-bitcoin/` |
| Meridian · Financial OS | `/projetos/meridian/` |
| Sanctu · Monitoring | `/projetos/sanctu-monitoring/` *(em breve)* |
| Sanctu · Land Design | `/projetos/sanctu-land-design/` *(em breve)* |

Para o link em inglês, acrescente `?lang=en` no fim:
`https://leandro-ludviger.github.io/projetos/meridian/?lang=en`

---

## Como o site é organizado

```
index.html            o site inteiro — textos, layout e código, tudo aqui
support.js            o motor que desenha a página (não precisa mexer)
build.py              gera as páginas de projeto a partir do index.html
assets/               imagens, vídeos e fontes
  export/             Sanctu (telas em português)
  export/en/          Sanctu (telas em inglês)
  mb/                 Mercado Bitcoin
  meridian/           Meridian
  og/                 imagens de prévia de link (LinkedIn, WhatsApp)
projetos/             gerado automaticamente — não edite à mão
sitemap.xml           gerado automaticamente
robots.txt            gerado automaticamente
```

**O `index.html` é o único arquivo de conteúdo.** As páginas dentro de
`projetos/` são cópias dele com o cabeçalho trocado — quem as escreve é o
`build.py`. Editar um arquivo dentro de `projetos/` não adianta: a próxima
geração apaga a mudança.

---

## Como mudar alguma coisa

**1. Mexeu no texto ou nas imagens?** Edite o `index.html` e depois rode:

```bash
python3 build.py
```

Isso reescreve as cinco páginas de projeto com o conteúdo novo. Sem esse
passo, a home muda e as páginas de projeto continuam antigas.

**2. Quer ver antes de publicar?**

```bash
python3 -m http.server 8765
```

Abra `http://localhost:8765` no navegador. Encerre com `Ctrl+C`.

**3. Publicar:**

```bash
git add -A && git commit -m "descreva o que mudou" && git push
```

O GitHub Pages atualiza sozinho em um ou dois minutos.

---

## Mexendo nos projetos

Os textos de cada projeto ficam no `index.html`, dentro de uma lista chamada
`data`, na ordem em que aparecem no site. Cada projeto tem os campos
`title`, `intro`, `tagline`, `result` e as seções Contexto, Problema,
Estratégia, Solução, Meu papel e Aprendizados — sempre em duas versões,
português e inglês, no formato `pt ? 'português' : 'inglês'`.

Os dois projetos marcados `comingSoon: true` são os que ainda não têm
conteúdo. Eles têm endereço funcionando, mas estão marcados para o Google
não indexar enquanto estiverem vazios — quando o conteúdo entrar, tire o
`"em_breve": True` do `build.py` e rode a geração de novo.

**Se acrescentar ou remover um projeto**, a lista `routes` dentro do
`index.html` e a lista `PROJETOS` no `build.py` precisam mudar junto, na
mesma ordem — é o que liga cada endereço ao projeto certo.
