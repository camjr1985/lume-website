# Validação para GitHub Pages — 16/09/2026

- Catálogo público: 16 produtos.
- Pastas em `produtos/`: 16, correspondência exata com `data/products.json`.
- Rascunhos antigos removidos da árvore pública.
- Referências locais HTML (`href`/`src`) quebradas: 0.
- Imagens do catálogo: todas presentes em WebP.
- `site_url`: `https://camjr1985.github.io/lume-website`.
- `.nojekyll` incluído para GitHub Pages.
- `scripts/build.py` validado com `py_compile`.
- `assets/js/main.js` validado com `node --check` quando disponível.
- Imagens raster duplicadas não utilizadas foram removidas para reduzir o pacote.

## Como publicar
Extraia o ZIP e envie o conteúdo extraído para a raiz do repositório `lume-website`, preservando as pastas. Não publique o ZIP fechado como um ficheiro dentro do repositório.
