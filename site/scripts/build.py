#!/usr/bin/env python3
"""
LUME — gerador estático do site.

Como usar:
  1. Edite data/products.json (adicione/edite produtos reais).
  2. Coloque as fotografias reais em assets/img/produtos/<slug>/ (opcional; enquanto
     não houver fotos, o site mostra um bloco de placeholder identificado).
  3. Rode:  python3 scripts/build.py
  4. Isso regenera index.html, produtos.html e produtos/<slug>/index.html a partir
     dos templates abaixo — sem precisar redesenhar nada.

Este script não tem dependências externas (só a biblioteca padrão do Python).
"""
import json
import os
import re
from html import escape
from urllib.parse import quote

def e(value):
    return escape(str(value), quote=True)

def price(p):
    value=p.get("preco")
    if value is not None:
        return e(f"{float(value):.2f}".replace(".", ",") + " €")
    return e(p.get("preco_label") or "Preço sob consulta")

def info(value):
    return e(value) if value is not None and value != "" else "Informação a confirmar"


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "products.json")

with open(DATA_PATH, encoding="utf-8") as f:
    DATA = json.load(f)

CATEGORIAS = DATA["categorias"]
PRODUTOS = DATA["produtos"]
CAT_LABEL = {c["slug"]: c["label"] for c in CATEGORIAS}

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  <link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'


def ph_image(label, desc, extra_class=""):
    return f'<!-- PLACEHOLDER: fotografia real pendente --><div class="ph-image {extra_class}" role="img" aria-label="Fotografia a confirmar"><span>Fotografia a confirmar</span></div>'

def product_image(p, depth="", index=0, eager=False):
    images=p.get("imagens", [])
    if not images: return ph_image(p["nome"], "")
    item=images[index]
    return f'<img class="product-photo" src="{depth}{e(item["src"])}" alt="{e(item["alt"])}" loading="{"eager" if eager else "lazy"}" decoding="async" width="{item.get("width", 1000)}" height="{item.get("height", 1000)}">'

def pillars():
    return '<div class="pillars-grid">'+''.join(f'<div class="pillar"><span class="pillar-mark mark-{i}" aria-hidden="true"></span><h3>{title}</h3><p>{text}</p></div>' for i,(title,text) in enumerate([
      ("ESTIMULAR","Recursos pensados para apoiar novas habilidades e experiências."),
      ("DESENVOLVER","Soluções que favorecem aprendizagem, autonomia e desenvolvimento."),
      ("INCLUIR","Design funcional e acessível pensado para diferentes necessidades.")]))+'</div>'


def base_page(title, description, active, content, depth="", extra_head=""):
    nav_items = [
        ("index.html", "Home", "home"),
        ("produtos.html", "Produtos", "produtos"),
        ("sobre.html", "Sobre", "sobre"),
        ("contato.html", "Contacto", "contato"),
    ]
    links_html = ""
    for href, label, key in nav_items:
        cls = ' class="active" aria-current="page"' if key == active else ""
        links_html += f'<li><a href="{depth}{href}"{cls}>{label}</a></li>\n        '

    route = ("produtos/" + extra_head.split('data-slug="')[1].split('"')[0] + "/") if 'data-slug="' in extra_head else {"home":"", "produtos":"produtos.html", "sobre":"sobre.html", "contato":"contato.html"}.get(active, {"Termos":"termos.html", "Política de Privacidade":"politica-de-privacidade.html", "Envios e Devoluções":"envios-e-devolucoes.html"}.get(title,""))
    site_url = DATA.get("site_url", "").rstrip("/")
    social_image = (site_url + "/" if site_url else depth) + "assets/img/lume-logo-full.png"
    canonical = f'<link rel="canonical" href="{e(site_url + "/" + route)}"><meta property="og:url" content="{e(site_url + "/" + route)}">' if site_url else '<!-- TODO: definir site_url em data/products.json para URLs sociais absolutas. -->'
    return f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)} · Lume</title>
<meta name="description" content="{e(description)}">
{FONTS}
<link rel="icon" href="{depth}assets/img/lume-icon.png">
<link rel="stylesheet" href="{depth}assets/css/style.css">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_PT">
<meta property="og:site_name" content="Lume">
<meta property="og:title" content="{e(title)} · Lume">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{e(social_image)}">
<meta property="og:image:alt" content="Lume — Recursos Terapêuticos e Educativos">
<meta name="twitter:card" content="summary_large_image">
{canonical}
{extra_head}
</head>
<body>
<a class="skip-link" href="#conteudo">Saltar para o conteúdo</a>
<header class="site-header">
  <nav class="container nav" aria-label="Navegação principal">
    <a href="{depth}index.html" class="nav-brand">
      <img src="{depth}assets/img/lume-icon.png" alt=""><span>Lume<small>Recursos terapêuticos e educativos</small></span>
    </a>
    <ul class="nav-links" id="menu-principal">
        {links_html}
    </ul>
    <div class="nav-cta">
      <a href="{depth}produtos.html" class="btn btn-ghost">Ver produtos</a>
      <button class="nav-toggle" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu-principal">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </nav>
</header>

<main id="conteudo">{content}</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{depth}assets/img/lume-logo-full.png" alt="Lume — Tecnologia com propósito">
        <p>Recursos Terapêuticos e Educativos. Tecnologia com propósito.</p>
        <div class="footer-pillars">
          <span style="color:#E3A73C">Estimular</span>
          <span style="color:#4E9F97">Desenvolver</span>
          <span style="color:#8FB4DE">Incluir</span>
        </div>
      </div>
      <div>
        <h4>Navegação</h4>
        <ul>
          <li><a href="{depth}produtos.html">Produtos</a></li>
          <li><a href="{depth}sobre.html">Sobre</a></li>
          <li><a href="{depth}contato.html">Contacto</a></li>
        </ul>
      </div>
      <div>
        <h4>Contacto</h4>
        <ul>
          <li><a href="https://wa.me/351917980307" target="_blank" rel="noopener">WhatsApp: +351 917 980 307</a></li>
          <li><a href="mailto:marcellyreisrocha@gmail.com">marcellyreisrocha@gmail.com</a></li>
          <li><a href="https://instagram.com/lume.recursos" target="_blank" rel="noopener">@lume.recursos</a></li>
        </ul>
      </div>
      <div>
        <h4>Institucional</h4>
        <ul>
          <li><a href="{depth}politica-de-privacidade.html">Política de Privacidade</a></li>
          <li><a href="{depth}termos.html">Termos</a></li>
          <li><a href="{depth}envios-e-devolucoes.html">Envios e Devoluções</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Lume — Recursos Terapêuticos e Educativos.</span>
      <span>Estimular · Desenvolver · Incluir</span>
    </div>
  </div>
</footer>
<script src="{depth}assets/js/main.js"></script>
</body>
</html>
"""


def product_card(p, depth=""):
    return f'<article class="product-card" data-category="{e(p["categoria"])}">{product_image(p,depth)}<div class="pc-body"><div class="pc-cat">{e(CAT_LABEL[p["categoria"]])}</div><h3>{e(p["nome"])}</h3><p class="pc-desc">{e(p["resumo"])}</p><div class="pc-foot"><span>{price(p)}</span><a class="card-link" href="{depth}produtos/{e(p["slug"])}/" aria-label="Ver produto: {e(p["nome"])}">Ver produto <span aria-hidden="true">↗</span></a></div></div></article>'


def build_home():
    category_cards=''.join(f'<a class="category-card" href="produtos.html?categoria={e(c["slug"])}"><span class="category-number">0{i+1}</span><h3>{e(c["label"])}</h3><span aria-hidden="true">↗</span></a>' for i,c in enumerate(CATEGORIAS))
    featured=''.join(product_card(p) for p in PRODUTOS[:3])
    return base_page("Recursos terapêuticos e educativos em impressão 3D", "Lume — Recursos terapêuticos e educativos em impressão 3D para aprendizagem, autonomia, desenvolvimento e inclusão.", "home", f"""
<section class="hero"><div class="container hero-grid"><div><div class="eyebrow">TECNOLOGIA COM PROPÓSITO</div><h1>Recursos terapêuticos e educativos em impressão 3D</h1><p class="lead">Criamos soluções pensadas para apoiar a aprendizagem, a autonomia e o desenvolvimento com funcionalidade, cuidado e propósito.</p><div class="hero-actions"><a class="btn btn-primary" href="produtos.html">Ver produtos</a><a class="btn btn-ghost" href="contato.html">Falar com a Lume</a></div><p class="hero-signature">Estimular · Desenvolver · Incluir</p></div><figure class="hero-media">{product_image(PRODUTOS[0],eager=True)}<figcaption>Pequenos gestos. Novas possibilidades.</figcaption></figure></div></section>
<section class="pillars"><div class="container">{pillars()}</div></section>
<section><div class="container"><div class="section-head"><div class="eyebrow">EXPLORAR A LUME</div><h2>Conheça os nossos produtos</h2><p>Encontre um recurso para a atividade, a rotina ou a descoberta que tem em mente.</p></div><div class="category-grid">{category_cards}</div><div class="product-grid">{featured}</div><p><a class="btn btn-outline-petrol" href="produtos.html">Ver todos os produtos</a></p></div></section>
<section class="band-petrol"><div class="container split"><div><div class="eyebrow">SOBRE A LUME</div><h2>Tecnologia que ganha propósito no dia a dia.</h2></div><div><p>A Lume cria recursos terapêuticos e educativos em impressão 3D que unem funcionalidade, acessibilidade e cuidado. Cada solução é pensada para apoiar pessoas, famílias, terapeutas e educadores em diferentes momentos do desenvolvimento.</p><a href="sobre.html" class="btn btn-ghost-light">Sobre a Lume</a></div></div></section>
<section><div class="container split"><div><div class="eyebrow">DO PRIMEIRO CONTACTO À ENCOMENDA</div><h2>Vamos encontrar o recurso adequado?</h2><p>Conte-nos o que procura. Confirmamos consigo as opções, o preço e o prazo de produção antes da encomenda.</p><a class="btn btn-primary" href="contato.html">Falar com a Lume</a></div><div class="order-steps"><p><strong>01 · Escolha</strong><br>Explore os produtos e os seus detalhes.</p><p><strong>02 · Converse</strong><br>Partilhe a sua necessidade e esclareça dúvidas.</p><p><strong>03 · Confirme</strong><br>Combine os detalhes da encomenda com a Lume.</p></div></div></section>
<section class="instagram-section"><div class="container"><div class="insta-head"><div><div class="eyebrow">@LUME.RECURSOS</div><h2>Acompanhe a Lume no Instagram</h2><p>Recursos, novidades e um olhar mais próximo sobre a Lume.</p></div><a href="https://www.instagram.com/lume.recursos/" target="_blank" rel="noopener" class="btn btn-ghost">@lume.recursos ↗</a></div><div class="launch-grid">{''.join(f'<a href="produtos.html" aria-label="Explorar produtos: lançamento {i}"><img src="assets/img/instagram/lancamento-story-0{i}.webp" alt="Lançamento Lume: {label}" loading="lazy" width="1080" height="1920"></a>' for i,label in [(1,'conheça os produtos'),(2,'jogos de encaixe'),(3,'apoio à autonomia'),(4,'leitura e aprendizagem')])}</div><!-- Futuras novidades: inserir publicações autorizadas neste contentor. --><div id="instagram-novidades"></div></div></section>
""")


def build_produtos():
    chips='<button class="chip active" data-filter="todos" aria-pressed="true">Todos</button>'+''.join(f'<button class="chip" data-filter="{e(c["slug"])}" aria-pressed="false">{e(c["label"])}</button>' for c in CATEGORIAS)
    content=f'<section><div class="container"><div class="section-head"><img class="catalog-cover" src="assets/img/instagram/capa-produtos.webp" alt="Capa da coleção de produtos Lume" width="1080" height="1080"><div class="eyebrow">CATÁLOGO LUME</div><h1>Recursos para descobrir possibilidades.</h1><p>Jogos, recursos de aprendizagem e soluções de apoio à autonomia. Escolha uma categoria para explorar.</p></div><div class="chip-row" role="group" aria-label="Filtrar por categoria">{chips}</div><p id="catalog-status" role="status">{len(PRODUTOS)} produtos</p><div class="product-grid">{"".join(product_card(p) for p in PRODUTOS)}</div><noscript><p>Todos os produtos estão apresentados. Ative JavaScript para filtrar por categoria.</p></noscript></div></section>'
    return base_page("Produtos", "Explore os recursos terapêuticos e educativos em impressão 3D da Lume: jogos de encaixe, leitura, autonomia e recursos sensoriais.", "produtos", content)


def build_produto_page(p):
    related=[x for x in PRODUTOS if x["categoria"]==p["categoria"] and x["slug"]!=p["slug"]]
    related += [x for x in PRODUTOS if x["slug"]!=p["slug"] and x not in related]
    wa="https://wa.me/351917980307?text="+quote("Olá, Lume! Gostaria de encomendar ou saber mais sobre: "+p["nome"]+". Podem confirmar o preço e a disponibilidade?")
    thumbs=''.join(f'<button class="gallery-thumb" aria-label="Ver fotografia {i+1} de {e(p["nome"])}" aria-pressed="{"true" if i==0 else "false"}" data-image="../../{e(item["src"])}" data-alt="{e(item["alt"])}">{product_image(p,"../../",i)}</button>' for i,item in enumerate(p.get("imagens",[])))
    specs=''.join(f'<div class="pd-spec-row"><dt>{label}</dt><dd>{info(p.get(key))}</dd></div>' for key,label in [("finalidade","Finalidade"),("publico","Público indicado"),("material","Materiais"),("dimensoes","Dimensões"),("cuidados","Cuidados")])
    sale=''.join(f'<div><dt>{label}</dt><dd>{info(p.get(key))}</dd></div>' for key,label in [("disponibilidade","Disponibilidade"),("stock","Stock"),("personalizacao","Personalização"),("prazo_producao","Prazo de produção")])
    benefits='<ul>'+''.join(f'<li>{e(b)}</li>' for b in p['beneficios'])+'</ul>' if p.get('beneficios') else '<p>Informação a confirmar</p>'
    colors=', '.join(p.get('cores_disponiveis',[])) or 'Informação a confirmar'
    content=f"""<section><div class="container"><nav class="pd-breadcrumb" aria-label="Percurso"><a href="../../produtos.html">Produtos</a> / <a href="../../produtos.html?categoria={e(p['categoria'])}">{e(CAT_LABEL[p['categoria']])}</a> / {e(p['nome'])}</nav><div class="pd-grid"><div><div class="pd-gallery-main">{product_image(p,'../../',eager=True)}</div><div class="pd-thumbs">{thumbs}</div></div><div><div class="eyebrow">{e(CAT_LABEL[p['categoria']])}</div><h1>{e(p['nome'])}</h1><p>{e(p['descricao_longa'])}</p><div class="pd-price">{price(p)}</div><p class="pd-colors"><strong>Cores:</strong> {e(colors)}</p><div class="pd-actions"><a class="btn btn-primary" href="{wa}" target="_blank" rel="noopener">Encomendar</a><a class="btn btn-outline-petrol" href="{wa}" target="_blank" rel="noopener">WhatsApp</a></div><p class="order-note">A encomenda é combinada diretamente com a Lume. Confirmamos preço, opções e prazo consigo.</p><dl class="sale-fields">{sale}</dl></div></div><div class="detail-info"><div><h2>Benefícios</h2>{benefits}</div><div><h2>Detalhes do recurso</h2><dl class="pd-specs">{specs}</dl></div></div></div></section><section class="instagram-section"><div class="container"><h2>Produtos relacionados</h2><div class="product-grid">{''.join(product_card(x,'../../') for x in related[:3])}</div></div></section>"""
    return base_page(p['nome'],p['resumo'],'produtos',content,depth='../../',extra_head=f'<!-- data-slug="{e(p["slug"])}" -->')


def _color_hex(name):
    m = {
        "amarelo mostarda": "#E3A73C", "azul petróleo": "#1F6E68", "verde": "#4E9F6B",
        "azul": "#4E7FB5", "grafite": "#4C555B", "mostarda": "#E3A73C",
        "cinza": "#9AA1A6", "rosa": "#D98CA6",
    }
    return m.get(name.lower(), "#C9C2AD")


def build_sobre():
    content=f"""<section><div class="container about-hero"><div><div class="eyebrow">ESTIMULAR · DESENVOLVER · INCLUIR</div><h1>Sobre a Lume</h1><p class="lead">Acreditamos que bons recursos podem abrir novas possibilidades de aprendizagem, autonomia e participação.</p><h2>Quem somos</h2><p>A Lume nasceu para transformar ideias em recursos funcionais, acessíveis e pensados para o dia a dia.</p><h2>O que fazemos</h2><p>Desenvolvemos recursos terapêuticos e educativos utilizando impressão 3D, combinando tecnologia, funcionalidade e design.</p></div><img class="brand-story" src="assets/img/instagram/capa-sobre.webp" alt="Símbolo da Lume: estimular, desenvolver e incluir" width="1080" height="1080"></div></section><section class="instagram-section"><div class="container split"><div><div class="eyebrow">PESSOAS E POSSIBILIDADES</div><h2>Para quem criamos</h2><p>Recursos para diferentes contextos e momentos do desenvolvimento.</p></div><ul class="audience-list">{''.join('<li>'+x+'</li>' for x in ['Crianças','Famílias','Educadores','Terapeutas ocupacionais','Psicólogos','Fisioterapeutas','Outros profissionais'])}</ul></div></section><section><div class="container"><h2>A nossa proposta</h2>{pillars()}<div class="brand-launches"><img src="assets/img/instagram/marca-story-01.webp" alt="Bem-vindos à Lume: tecnologia com propósito" loading="lazy" width="1080" height="1920"><img src="assets/img/instagram/marca-story-03.webp" alt="Estimular, desenvolver e incluir: funcionalidade, cuidado e propósito" loading="lazy" width="1080" height="1920"><img src="assets/img/instagram/marca-story-04.webp" alt="A Lume une inovação, acessibilidade e cuidado" loading="lazy" width="1080" height="1920"></div></div></section><section class="band-petrol"><div class="container"><h2>Tecnologia com propósito.</h2><p>Uma ideia, um recurso, novas possibilidades.</p><a class="btn btn-primary" href="produtos.html">Conheça os nossos produtos</a></div></section>"""
    return base_page('Sobre a Lume','Conheça a Lume: recursos terapêuticos e educativos em impressão 3D para apoiar aprendizagem, autonomia e participação.','sobre',content)


def build_contato():
    content = """
<section style="padding-top:52px">
  <div class="container contact-grid">
    <div>
      <div class="eyebrow">CONTACTO</div>
      <h1>Falar com a Lume</h1>
      <p>Dúvidas sobre um recurso, personalização ou parcerias — conte-nos o contexto e respondemos o quanto antes.</p>
      <form id="contact-form" action="https://wa.me/351917980307" method="get">
<p>Prepare a sua mensagem e continue no WhatsApp para a enviar.</p>
        <div class="form-field"><label for="nome">Nome</label><input id="nome" name="nome" autocomplete="name" required type="text" placeholder="O seu nome"></div>
        <div class="form-field"><label for="email">E-mail</label><input id="email" name="email" autocomplete="email" type="email" placeholder="seu@email.com"></div>
        <div class="form-field"><label for="assunto">Assunto</label>
          <select id="assunto">
            <option>Dúvida sobre um produto</option>
            <option>Personalização</option>
            <option>Parcerias / profissionais</option>
            <option>Outro</option>
          </select>
        </div>
        <div class="form-field"><label for="mensagem">Mensagem</label><textarea id="mensagem" name="mensagem" required rows="5" placeholder="Como podemos ajudar?"></textarea></div>
        <button class="btn btn-primary" type="submit">Continuar no WhatsApp</button>
<noscript><p>Sem JavaScript, contacte-nos através do WhatsApp ou e-mail indicados nesta página.</p></noscript>
      </form>
    </div>
    <div class="contact-info-card">
      <div class="item"><strong>WhatsApp</strong><br><a href="https://wa.me/351917980307" target="_blank" rel="noopener">+351 917 980 307</a></div>
      <div class="item"><strong>E-mail</strong><br><a href="mailto:marcellyreisrocha@gmail.com">marcellyreisrocha@gmail.com</a></div>
      <div class="item"><strong>Instagram</strong><br><a href="https://instagram.com/lume.recursos" target="_blank" rel="noopener">@lume.recursos</a></div>
      <div class="item"><strong>Localização</strong><br>Lisboa · São Paulo</div>
      <div class="item"><strong>Horário de resposta</strong><br>Respondemos em até 2 dias úteis.</div>
    </div>
  </div>
</section>
"""
    return base_page(
        "Contacto",
        "Fale com a Lume sobre produtos, personalização ou parcerias.",
        "contato",
        content,
    )


def build_legal_page(title, eyebrow):
    content = f"""
<section style="padding-top:52px; padding-bottom:100px">
  <div class="container" style="max-width:760px">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{title}</h1>
    <p class="text-muted">Informação em preparação. Para esclarecer este tema, contacte a Lume.</p>
    <!-- PENDENTE: conteúdo institucional aprovado pela Lume. --><p><a class="btn btn-primary" href="contato.html">Falar com a Lume</a></p>
  </div>
</section>
"""
    return base_page(title, f"{title} da Lume.", "", content, extra_head='<meta name="robots" content="noindex,follow">')


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("gerado:", path)


def main():
    write("index.html", build_home())
    write("produtos.html", build_produtos())
    write("sobre.html", build_sobre())
    write("contato.html", build_contato())
    for p in PRODUTOS:
        write(f"produtos/{p['slug']}/index.html", build_produto_page(p))
    # Os rascunhos originais ficam apenas em data/products.json como referência interna.
    # Não são publicados em /produtos para manter o catálogo público limpo e consistente.
    write("politica-de-privacidade.html", build_legal_page("Política de Privacidade", "INSTITUCIONAL"))
    write("termos.html", build_legal_page("Termos", "INSTITUCIONAL"))
    write("envios-e-devolucoes.html", build_legal_page("Envios e Devoluções", "INSTITUCIONAL"))


if __name__ == "__main__":
    main()
