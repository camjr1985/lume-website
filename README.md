# Lume — site existente atualizado

Site estático, preservando HTML/CSS/JavaScript e o gerador Python original.

- `data/products.json`: 16 recursos identificados nas imagens, seis categorias, campos comerciais e proveniência das fotografias. Os sete exemplos iniciais estão preservados em `rascunhos_originais`.
- `scripts/build.py`: gera Home, catálogo, Sobre, Contacto, páginas de produto e páginas institucionais. Executar `python scripts/build.py` depois de editar os dados.
- `assets/css/style.css` e `assets/js/main.js`: estilos responsivos, menu, filtros, galeria e preparação da mensagem de WhatsApp.
- `assets/img/produtos/` e `assets/img/instagram/`: imagens fornecidas e versões WebP para carregamento. Originais conservados.

## Atualizar um produto

Editar o objeto em `produtos`; manter slug único e categoria existente. `imagens` contém src, alt, width e height. Campos pendentes usam `null` ou listas vazias. `preco` recebe um número em euros; sem preço apresenta «Preço sob consulta». Preencher `cores_disponiveis`, `disponibilidade`, `stock`, `personalizacao`, `prazo_producao`, `beneficios`, `finalidade`, `publico`, `material`, `dimensoes` e `cuidados` com dados confirmados.

As encomendas abrem WhatsApp com o nome do produto; o formulário prepara uma mensagem que o visitante envia no WhatsApp. Não existe pagamento, reserva automática de stock nem backend.

## Pré-visualizar e publicar

Executar `python -m http.server 8765` nesta pasta e abrir `http://localhost:8765`. Publicar o conteúdo da pasta num alojamento estático. Antes de publicar, preencher `site_url` com o endereço HTTPS completo (incluindo subpasta, se existir) para canonical e Open Graph; aprovar textos de privacidade, termos e envios. Essas páginas e os exemplos antigos têm noindex enquanto pendentes.

Contactos preservados: WhatsApp +351 917 980 307, marcellyreisrocha@gmail.com e Instagram @lume.recursos. Para alterar, editar o gerador.

Backup anterior às alterações: `C:/Users/Carlos Junior/OneDrive - EDP/Documents/ChatGPT/Lume/backup-lume-site-20260914`.

## Publicação no GitHub Pages — versão validada em 16/09/2026

Estrutura pública esperada:
- `index.html`
- `produtos.html`
- `produtos/<slug>/index.html` — somente produtos oficiais do catálogo
- `assets/` — CSS, JavaScript e imagens WebP usadas pelo site
- `data/products.json` — fonte de dados do catálogo
- `scripts/build.py` — regeneração das páginas estáticas
- `.nojekyll` — publicação direta pelo GitHub Pages

Para atualizar o repositório `lume-website`, extraia o ZIP e envie **o conteúdo da pasta**, preservando a mesma estrutura de diretórios. Não envie o ZIP como ficheiro para dentro do repositório esperando que o GitHub o extraia.

Depois de editar `data/products.json`, execute `python scripts/build.py` antes de publicar.
