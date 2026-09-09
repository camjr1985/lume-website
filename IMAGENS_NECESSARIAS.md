# Lume — Lista completa de imagens necessárias

Todas as imagens abaixo aparecem hoje no site como um bloco placeholder identificado
(`[IMAGEM NECESSÁRIA]` + descrição), nunca como fotografia inventada. Substitua cada uma
seguindo o nome de arquivo sugerido e o local indicado — nenhuma mudança de código é
necessária, só trocar o arquivo e (nas páginas de produto) rodar `python3 scripts/build.py`
de novo caso a imagem venha do catálogo de produtos.

## 1. Identidade (já resolvida)
- `assets/img/lume-logo-full.png` — logotipo completo oficial (já em uso, arquivo real).
- `assets/img/lume-icon.png` — símbolo isolado, recortado do logotipo oficial (já em uso, nav/footer/favicon).

## 2. Home

| Arquivo sugerido | Proporção | Onde é usada | Descrição exata | Tipo |
|---|---|---|---|---|
| `hero-produtos-lume.jpg` | 4:5 (retrato) | Hero da Home | Fotografia profissional com 2–3 produtos reais da Lume, fundo creme/off-white, luz natural, composição limpa | Foto real |
| `processo-impressao-3d.jpg` | 5:4 (paisagem) | Seção "Da ideia à forma" | Foto real do processo de impressão 3D em andamento (impressora em funcionamento, peça sendo formada) | Foto real |
| `produto-personalizacao.jpg` | 5:4 (paisagem) | Seção "Personalização" | Fotografia mostrando variações de cor/tamanho do mesmo produto lado a lado | Foto real |
| `momento-criancas.jpg` | 4:5 (retrato) | "Recursos para diferentes momentos da vida" | Criança manuseando um recurso educativo, ambiente doméstico/escolar, luz natural | Foto real |
| `momento-adolescentes-adultos.jpg` | 4:5 (retrato) | Idem | Adolescente ou adulto jovem utilizando um recurso de coordenação | Foto real |
| `momento-idosos.jpg` | 4:5 (retrato) | Idem | Pessoa idosa utilizando um recurso de autonomia no dia a dia | Foto real |
| `momento-profissionais.jpg` | 4:5 (retrato) | Idem | Educador, terapeuta ou cuidador apresentando/utilizando um recurso | Foto real |
| `instagram-01.jpg` a `instagram-04.jpg` | 1:1 (quadrado) | Teaser do Instagram | Miniaturas reais dos posts mais recentes do @lume.recursos (produto em uso, impressão 3D, bastidores, novidade) | Foto real (recorte do Instagram) |

## 3. Página Sobre

| Arquivo sugerido | Proporção | Onde é usada | Descrição exata | Tipo |
|---|---|---|---|---|
| `sobre-equipa-ou-processo.jpg` | 5:4 (paisagem) | Página Sobre, ao lado do texto institucional | Foto institucional real — equipa, ateliê/oficina de impressão 3D, ou processo de produção | Foto real |

## 4. Catálogo de produtos — por item (7 placeholders atuais)

Cada produto tem hoje 4 blocos de imagem (1 foto principal + 3 miniaturas). Ao publicar
um produto real, adicione as fotos em `assets/img/produtos/<slug-do-produto>/` com estes
nomes e edite o campo correspondente em `data/products.json`:

| Produto (placeholder) | Slug | Fotos necessárias |
|---|---|---|
| Conjunto de Encaixe Rotativo | `conjunto-encaixe-rotativo` | `principal.jpg` (1:1, produto isolado, fundo creme, ângulo frontal), `detalhe.jpg` (1:1, textura/encaixe), `em-uso.jpg` (1:1, produto sendo utilizado), `cor-alternativa.jpg` (1:1, variação de cor) |
| Sequência Associativa Modular | `sequencia-associativa-modular` | mesmos 4 tipos acima |
| Painel de Atenção Visual | `painel-atencao-visual` | mesmos 4 tipos acima |
| Esfera Tátil Multitextura | `esfera-tatil-multitextura` | mesmos 4 tipos acima |
| Kit de Utensílios com Pega Adaptada | `kit-utensilios-pega-adaptada` | mesmos 4 tipos acima |
| Suporte Adaptado Modular | `suporte-adaptado-modular` | mesmos 4 tipos acima |
| Conjunto de Exercício Manual | `conjunto-exercicio-manual-adulto` | mesmos 4 tipos acima |

Padrão para todas as fotos de produto: **foto real**, fundo creme/off-white ou neutro,
produto na cor real (sem alterar cor/formato), luz uniforme, sem elementos de marca
sobrepostos.

## 5. Observação importante

Nenhuma imagem de produto foi inventada ou gerada como "produto fictício realista" —
onde ainda não existe uma fotografia real, o site mostra apenas o bloco de placeholder
identificado, exatamente como pedido no briefing.
