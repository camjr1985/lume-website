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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "products.json")

with open(DATA_PATH, encoding="utf-8") as f:
    DATA = json.load(f)

CATEGORIAS = DATA["categorias"]
PRODUTOS = DATA["produtos"]
CAT_LABEL = {c["slug"]: c["label"] for c in CATEGORIAS}

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  <link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'


def ph_image(label, desc, extra_class=""):
    """Bloco de imagem placeholder claramente identificado (sem inventar fotos)."""
    return (
        f'<div class="ph-image {extra_class}"><div><span>[IMAGEM NECESSÁRIA]</span>{label}'
        f'<br><small>{desc}</small></div></div>'
    )


def base_page(title, description, active, content, depth="", extra_head=""):
    nav_items = [
        ("index.html", "Home", "home"),
        ("produtos.html", "Produtos", "produtos"),
        ("sobre.html", "Sobre", "sobre"),
        ("contato.html", "Contato", "contato"),
    ]
    links_html = ""
    for href, label, key in nav_items:
        cls = ' class="active"' if key == active else ""
        links_html += f'<li><a href="{depth}{href}"{cls}>{label}</a></li>\n        '

    return f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · Lume</title>
<meta name="description" content="{description}">
{FONTS}
<link rel="icon" href="{depth}assets/img/lume-icon.png">
<link rel="stylesheet" href="{depth}assets/css/style.css">
{extra_head}
</head>
<body>
<header class="site-header">
  <div class="container nav">
    <a href="{depth}index.html" class="nav-brand">
      <img src="{depth}assets/img/lume-icon.png" alt="Lume">
      <span>Lume</span>
    </a>
    <ul class="nav-links">
        {links_html}
    </ul>
    <div class="nav-cta">
      <a href="{depth}produtos.html" class="btn btn-ghost">Ver produtos</a>
      <button class="nav-toggle" aria-label="Abrir menu" aria-expanded="false">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>
  </div>
</header>

{content}

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{depth}assets/img/lume-icon.png" alt="Lume">
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
          <li><a href="{depth}contato.html">Contato</a></li>
        </ul>
      </div>
      <div>
        <h4>Contato</h4>
        <ul>
          <li><a href="https://wa.me/351917980307" target="_blank" rel="noopener">WhatsApp: +351 917 980 307</a></li>
          <li><a href="mailto:marcellyreisrocha@gmail.com">marcellyreisrocha@gmail.com</a></li>
          <li><a href="https://instagram.com/lume.recursos" target="_blank" rel="noopener">Instagram</a></li>
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
    badge = '<span class="badge-placeholder">Placeholder</span>' if p.get("is_placeholder") else ""
    return f"""
      <a class="product-card" href="{depth}produtos/{p['slug']}/index.html" data-category="{p['categoria']}">
        {ph_image(p['nome'], 'Foto do produto isolado, fundo creme')}
        <div class="pc-body">
          <div class="pc-cat">{CAT_LABEL.get(p['categoria'], '')}</div>
          <h3>{p['nome']}</h3>
          <p class="pc-desc">{p['resumo']}</p>
          <div class="pc-foot">
            <span class="pc-price">{p['preco_label']}</span>
            {badge}
          </div>
        </div>
      </a>"""


def build_home():
    pillar_marks = {
        "estimular": '<svg class="mark" viewBox="0 0 46 46"><circle cx="23" cy="23" r="20" fill="#E3A73C"/></svg>',
        "desenvolver": '<svg class="mark" viewBox="0 0 46 46"><rect x="7" y="7" width="32" height="32" rx="8" fill="#1F6E68" transform="rotate(45 23 23)"/></svg>',
        "incluir": '<svg class="mark" viewBox="0 0 46 46"><path d="M4 34a19 19 0 0 1 38 0z" fill="#4E7FB5"/></svg>',
    }

    stages = [
        ("Crianças", "Criança manuseando um recurso educativo em ambiente doméstico"),
        ("Adolescentes e adultos", "Adulto jovem utilizando recurso de coordenação"),
        ("Idosos", "Pessoa idosa utilizando recurso de autonomia no dia a dia"),
        ("Profissionais e cuidadores", "Educador ou terapeuta apresentando um recurso"),
    ]
    stages_html = "".join(
        f'<div class="stage-card">{ph_image(label, desc)}<div class="stage-label">{label}</div></div>'
        for label, desc in stages
    )

    featured = PRODUTOS[:3]
    featured_html = "".join(product_card(p) for p in featured)

    insta_items = [
        "Produto em uso",
        "Impressão 3D em andamento",
        "Bastidores da produção",
        "Novidade do catálogo",
    ]
    insta_html = "".join(
        f'<a class="ph-image" href="https://instagram.com/lume.recursos" target="_blank" rel="noopener">{item}</a>'
        for item in insta_items
    )

    content = f"""
<section class="hero">
  <div class="container hero-grid">
    <div>
      <div class="hero-kicker">
        <span><i style="background:#E3A73C"></i>Estimular</span>
        <span><i style="background:#1F6E68"></i>Desenvolver</span>
        <span><i style="background:#4E7FB5"></i>Incluir</span>
      </div>
      <h1>Recursos que ampliam possibilidades.</h1>
      <p class="lead">Recursos terapêuticos e educativos desenvolvidos com tecnologia, criatividade e propósito para diferentes fases da vida.</p>
      <div class="hero-actions">
        <a href="#recursos" class="btn btn-primary">Conheça os recursos</a>
        <a href="produtos.html" class="btn btn-ghost">Ver produtos</a>
      </div>
    </div>
    <div class="hero-media">
      {ph_image('Foto hero', 'Fotografia profissional com 2–3 produtos reais da Lume, fundo creme, luz natural')}
    </div>
  </div>
</section>

<section class="pillars" id="recursos">
  <div class="container">
    <div class="section-head center">
      <div class="eyebrow">ESTIMULAR · DESENVOLVER · INCLUIR</div>
      <h2>O que move a Lume</h2>
    </div>
    <div class="pillars-grid">
      <div class="pillar">
        {pillar_marks['estimular']}
        <h3>Estimular</h3>
        <p>Recursos que favorecem experiências sensoriais, cognitivas e motoras.</p>
      </div>
      <div class="pillar">
        {pillar_marks['desenvolver']}
        <h3>Desenvolver</h3>
        <p>Soluções que apoiam habilidades, aprendizagem e autonomia.</p>
      </div>
      <div class="pillar">
        {pillar_marks['incluir']}
        <h3>Incluir</h3>
        <p>Recursos pensados para ampliar participação, acessibilidade e possibilidades.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">CATÁLOGO</div>
      <h2>Recursos em destaque</h2>
    </div>
    <div class="product-grid">
      {featured_html}
    </div>
    <p style="margin-top:32px"><a href="produtos.html" class="btn btn-outline-petrol">Ver todos os produtos</a></p>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">PARA QUEM É A LUME</div>
      <h2>Recursos para diferentes momentos da vida</h2>
      <p>A Lume não atende apenas crianças — os recursos acompanham diferentes fases, contextos e necessidades.</p>
    </div>
    <div class="stages-grid">
      {stages_html}
    </div>
  </div>
</section>

<section class="band-petrol">
  <div class="container">
    <div class="split">
      <div>
        <div class="eyebrow">COMO SÃO PRODUZIDOS</div>
        <h2>Da ideia à forma</h2>
        <p>Muitos recursos da Lume nascem de um processo próprio de desenvolvimento e são produzidos por impressão 3D — o que permite cuidado no detalhe, ajustes e evolução constante.</p>
      </div>
      <div class="split-media">
        {ph_image('Impressão 3D em andamento', 'Foto real do processo de impressão 3D em produção', 'ph-image')}
      </div>
    </div>
    <div class="process-strip" style="margin-top:56px">
      <div class="process-step"><div class="num">1</div><h3>Ideia</h3><p>Identificação de uma necessidade real.</p></div>
      <div class="process-step"><div class="num">2</div><h3>Desenvolvimento</h3><p>Modelagem e testes do formato.</p></div>
      <div class="process-step"><div class="num">3</div><h3>Impressão</h3><p>Produção em impressão 3D.</p></div>
      <div class="process-step"><div class="num">4</div><h3>Acabamento</h3><p>Revisão cuidadosa de cada peça.</p></div>
      <div class="process-step"><div class="num">5</div><h3>Produto</h3><p>Pronto para ampliar possibilidades.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="container split reverse">
    <div class="split-media">
      {ph_image('Produto sendo personalizado', 'Fotografia mostrando variação de cor/tamanho do mesmo produto')}
    </div>
    <div>
      <div class="eyebrow">PERSONALIZAÇÃO</div>
      <h2>Uma solução mais adequada à sua necessidade?</h2>
      <p>Determinados produtos podem ter opções de cores, tamanhos ou adaptações quando disponíveis. Conte-nos o contexto e vemos juntos o que faz sentido.</p>
      <a href="https://wa.me/351917980307" target="_blank" rel="noopener" class="btn btn-primary">Falar com a Lume</a>
    </div>
  </div>
</section>

<section style="background:var(--paper)">
  <div class="container">
    <div class="insta-head">
      <div>
        <div class="eyebrow">INSTAGRAM</div>
        <h2 class="mt-0">@lume.recursos</h2>
      </div>
      <a href="https://instagram.com/lume.recursos" target="_blank" rel="noopener" class="btn btn-ghost">Seguir no Instagram</a>
    </div>
    <div class="insta-grid">
      {insta_html}
    </div>
  </div>
</section>
"""
    return base_page(
        "Recursos que ampliam possibilidades",
        "Recursos terapêuticos e educativos desenvolvidos com tecnologia, criatividade e propósito.",
        "home",
        content,
    )


def build_produtos():
    chips = '<button class="chip active" data-filter="todos">Todos</button>' + "".join(
        f'<button class="chip" data-filter="{c["slug"]}">{c["label"]}</button>' for c in CATEGORIAS
    )
    cards = "".join(product_card(p) for p in PRODUTOS)
    content = f"""
<section style="padding-top:52px">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">CATÁLOGO</div>
      <h1>Produtos</h1>
      <p>Recursos terapêuticos, educativos e de apoio à autonomia, organizados por categoria. Este catálogo cresce continuamente.</p>
    </div>
    <div class="chip-row">
      {chips}
    </div>
    <div class="product-grid">
      {cards}
    </div>
  </div>
</section>
"""
    return base_page(
        "Produtos",
        "Catálogo de recursos terapêuticos e educativos da Lume, organizado por categoria.",
        "produtos",
        content,
    )


def build_produto_page(p):
    others_same_cat = [x for x in PRODUTOS if x["categoria"] == p["categoria"] and x["slug"] != p["slug"]][:3]
    related_html = "".join(product_card(x, depth="../../") for x in others_same_cat) or "<p class='text-muted'>Mais produtos desta categoria em breve.</p>"

    cores_html = "".join(
        f'<span class="pd-color-dot" title="{c}" style="background:{_color_hex(c)}"></span>' for c in p["cores_disponiveis"]
    )
    placeholder_note = (
        """<div class="pd-note">Este produto é um exemplo (placeholder) para estruturar o catálogo. Nome, preço, descrição e imagem são provisórios e serão substituídos por dados reais da Lume.</div>"""
        if p.get("is_placeholder")
        else ""
    )

    content = f"""
<section style="padding-top:40px">
  <div class="container">
    <div class="pd-breadcrumb"><a href="../../produtos.html">Produtos</a> / {CAT_LABEL.get(p['categoria'],'')} / {p['nome']}</div>
    <div class="pd-grid">
      <div>
        <div class="pd-gallery-main">
          {ph_image(p['nome'], 'Foto principal do produto, fundo creme, ângulo frontal')}
        </div>
        <div class="pd-thumbs">
          {ph_image('Ângulo 2', 'Detalhe/textura')}
          {ph_image('Ângulo 3', 'Produto em uso')}
          {ph_image('Ângulo 4', 'Variação de cor')}
        </div>
      </div>
      <div>
        <div class="pc-cat" style="margin-bottom:10px">{CAT_LABEL.get(p['categoria'],'')}</div>
        <h1 class="mt-0">{p['nome']}</h1>
        <p>{p['descricao_longa']}</p>
        <div class="pd-price">{p['preco_label']}</div>
        <p class="text-muted" style="margin-top:-6px">Cores disponíveis</p>
        <div class="pd-colors">{cores_html}</div>
        <div class="pd-actions">
          <a href="#" class="btn btn-primary">Comprar / Encomendar</a>
          <a href="https://wa.me/351917980307" target="_blank" rel="noopener" class="btn btn-outline-petrol">Falar com a Lume</a>
        </div>
        {placeholder_note}
        <dl class="pd-specs">
          <div class="pd-spec-row"><dt>Finalidade</dt><dd>{p['finalidade']}</dd></div>
          <div class="pd-spec-row"><dt>Público indicado</dt><dd>{p['publico']}</dd></div>
          <div class="pd-spec-row"><dt>Material</dt><dd>{p['material']}</dd></div>
          <div class="pd-spec-row"><dt>Dimensões</dt><dd>{p['dimensoes']}</dd></div>
          <div class="pd-spec-row"><dt>Cuidados</dt><dd>{p['cuidados']}</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section style="background:var(--paper)">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">RELACIONADOS</div>
      <h2>Mais desta categoria</h2>
    </div>
    <div class="product-grid">
      {related_html}
    </div>
  </div>
</section>
"""
    return base_page(p["nome"].replace("[PLACEHOLDER] ", ""), p["resumo"], "produtos", content, depth="../../")


def _color_hex(name):
    m = {
        "amarelo mostarda": "#E3A73C", "azul petróleo": "#1F6E68", "verde": "#4E9F6B",
        "azul": "#4E7FB5", "grafite": "#4C555B", "mostarda": "#E3A73C",
        "cinza": "#9AA1A6", "rosa": "#D98CA6",
    }
    return m.get(name.lower(), "#C9C2AD")


def build_sobre():
    content = """
<section style="padding-top:52px">
  <div class="container about-hero">
    <div>
      <div class="eyebrow">SOBRE A LUME</div>
      <h1>Tecnologia com propósito, em cada recurso.</h1>
      <p>A Lume nasceu da vontade de transformar tecnologia em possibilidades. Criamos e selecionamos recursos terapêuticos e educativos que podem apoiar desenvolvimento, aprendizagem, autonomia e inclusão em diferentes fases da vida.</p>
      <p>Cada recurso é pensado com cuidado — da escolha do material ao acabamento final — para acompanhar pessoas, famílias, educadores e profissionais em diferentes contextos, sem promessas que não nos cabem: a Lume desenvolve recursos, não diagnósticos nem tratamentos.</p>
    </div>
    <div>
      __HERO_IMG__
    </div>
  </div>
</section>

<section style="background:var(--paper)">
  <div class="container">
    <div class="section-head center">
      <div class="eyebrow">O QUE NOS GUIA</div>
      <h2>Estimular, desenvolver, incluir</h2>
    </div>
    <div class="value-list">
      <div class="value-item"><h3>Estimular</h3><p>Recursos que favorecem experiências sensoriais, cognitivas e motoras.</p></div>
      <div class="value-item"><h3>Desenvolver</h3><p>Soluções que apoiam habilidades, aprendizagem e autonomia.</p></div>
      <div class="value-item"><h3>Incluir</h3><p>Recursos pensados para ampliar participação, acessibilidade e possibilidades.</p></div>
    </div>
  </div>
</section>
"""
    content = content.replace("__HERO_IMG__", ph_image("Equipa ou processo Lume", "Foto institucional real — equipa, ateliê ou processo de produção"))
    return base_page(
        "Sobre",
        "Conheça a Lume: recursos terapêuticos e educativos feitos com tecnologia e propósito.",
        "sobre",
        content,
    )


def build_contato():
    content = """
<section style="padding-top:52px">
  <div class="container contact-grid">
    <div>
      <div class="eyebrow">CONTATO</div>
      <h1>Falar com a Lume</h1>
      <p>Dúvidas sobre um recurso, personalização ou parcerias — conte-nos o contexto e respondemos o quanto antes.</p>
      <form onsubmit="return false;">
        <div class="form-field"><label for="nome">Nome</label><input id="nome" type="text" placeholder="O seu nome"></div>
        <div class="form-field"><label for="email">E-mail</label><input id="email" type="email" placeholder="seu@email.com"></div>
        <div class="form-field"><label for="assunto">Assunto</label>
          <select id="assunto">
            <option>Dúvida sobre um produto</option>
            <option>Personalização</option>
            <option>Parcerias / profissionais</option>
            <option>Outro</option>
          </select>
        </div>
        <div class="form-field"><label for="mensagem">Mensagem</label><textarea id="mensagem" rows="5" placeholder="Como podemos ajudar?"></textarea></div>
        <button class="btn btn-primary" type="submit">Enviar mensagem</button>
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
        "Contato",
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
    <p class="text-muted">Este é um texto placeholder. Substitua pelo conteúdo jurídico real da Lume antes da publicação definitiva do site.</p>
    <p>[CONTEÚDO NECESSÁRIO — texto de {title.lower()} a ser fornecido pela Lume ou por assessoria jurídica.]</p>
  </div>
</section>
"""
    return base_page(title, f"{title} da Lume.", "", content)


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
    write("politica-de-privacidade.html", build_legal_page("Política de Privacidade", "INSTITUCIONAL"))
    write("termos.html", build_legal_page("Termos", "INSTITUCIONAL"))
    write("envios-e-devolucoes.html", build_legal_page("Envios e Devoluções", "INSTITUCIONAL"))


if __name__ == "__main__":
    main()
