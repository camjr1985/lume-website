# Lume — site institucional

Site estático (HTML/CSS/JS puro, sem dependências, sem build step em produção) pronto
para publicar via **GitHub Pages**.

## Estrutura

```
index.html                 Home
produtos.html               Catálogo (com filtro por categoria)
produtos/<slug>/index.html  Página individual de cada produto (uma por item do catálogo)
sobre.html
contato.html
politica-de-privacidade.html / termos.html / envios-e-devolucoes.html
assets/css/style.css        Design system (cores, tipografia, componentes)
assets/js/main.js           Menu mobile + filtro de categorias
assets/img/                 Logo oficial (lume-logo-full.png, lume-icon.png)
data/products.json          Fonte única de dados do catálogo
scripts/build.py            Gerador: regenera todas as páginas a partir de products.json
IMAGENS_NECESSARIAS.md      Lista completa de fotos ainda pendentes
```

## Como publicar no GitHub Pages

1. Crie um repositório novo no GitHub (ex.: `lume-site`).
2. Suba **todo o conteúdo desta pasta** para a raiz do repositório (não dentro de uma
   subpasta) — pelo GitHub Desktop, `git push`, ou upload manual pela interface web.
3. No repositório, vá em **Settings → Pages**.
4. Em "Build and deployment" → **Source**, selecione **Deploy from a branch**.
5. Em **Branch**, selecione `main` e a pasta `/ (root)` → **Save**.
6. Aguarde 1–2 minutos. O GitHub mostra a URL pública (algo como
   `https://seu-usuario.github.io/lume-site/`).

Não é necessário nenhum passo de build no GitHub — os arquivos já são o site final.

## Como adicionar ou editar um produto

1. Abra `data/products.json`.
2. Copie um dos objetos existentes dentro de `"produtos"` e edite os campos (nome,
   categoria, descrição, preço, cores, material, dimensões, cuidados). Dê um `slug`
   novo e único (usado na URL da página do produto).
3. Quando tiver as fotos reais, coloque-as em `assets/img/produtos/<slug>/` (veja
   `IMAGENS_NECESSARIAS.md` para os nomes sugeridos) e troque `"is_placeholder": true`
   para `false`.
4. Rode no terminal, dentro da pasta do site:
   ```
   python3 scripts/build.py
   ```
   Isso regenera `index.html`, `produtos.html` e todas as páginas de produto — sem
   precisar mexer em HTML/CSS manualmente.
5. Suba as mudanças para o GitHub (commit + push). O site publicado atualiza sozinho.

## Sobre o catálogo atual

Os 7 produtos hoje no site são **placeholders** — um exemplo por categoria, para validar
a estrutura visual. Nome, preço, descrição e imagem de cada um estão marcados como
provisórios (badge "Placeholder" no card + aviso na página do produto) e devem ser
substituídos pelos dados reais da Lume antes da divulgação oficial.

## Contato configurado

- WhatsApp: `+351 917 980 307` (botões "Falar com a Lume" abrem diretamente o WhatsApp)
- E-mail: `marcellyreisrocha@gmail.com`

Para trocar esses dados no futuro, edite `scripts/build.py` (busque por
`351917980307` e `marcellyreisrocha@gmail.com`) e rode o build de novo.

## Preparado para o futuro (carrinho, estoque, variantes)

A arquitetura já separa **dados** (`data/products.json`) de **apresentação** (templates
em `scripts/build.py` + `assets/css/style.css`). Isso significa que, quando a Lume
quiser adicionar carrinho de compras, controle de estoque ou variantes de produto, dá
para migrar `products.json` para um backend/CMS real sem reconstruir o design — o botão
"Comprar / Encomendar" em cada página de produto já está isolado e pronto para receber
essa integração.
