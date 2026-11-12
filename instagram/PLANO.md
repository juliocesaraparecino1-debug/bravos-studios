# Plano de Instagram da Bravos Studios

Pedido do responsável (resumo fiel). Uma publicação por dia, às 10h00 (horário de Brasília), seguindo um rodízio fixo: Reels, imagem estática, carrossel, e repete. Publicar usando a extensão Claude in Chrome, abrindo UMA NOVA ABA para a conta do Instagram destinada aos posts (o responsável já usa outra extensão do Instagram em outra aba/conta).

## Situação (a retomar na sessão no computador)
- A sessão na nuvem não alcança o Chrome. O responsável vai abrir uma sessão no computador (Claude Desktop ou `claude remote-control` na pasta deste repositório) com o Chrome e a extensão conectados.
- Ainda não analisei os perfis: o Instagram não abre sem login. Na sessão no computador, abrir cada link pela extensão (ou usar prints/vídeos baixados) e extrair os pontos em comum.
- Perguntar ao responsável, antes do primeiro post: qual é a conta que recebe os posts (Bravos Studios, @bravos_studios?) e se quer aprovar cada post antes de publicar (recomendado: sim, é conta pública).

## Referências a analisar
- https://www.instagram.com/lucassena : informação sobre a atualidade do mundo da IA e tecnologia; vídeos com texto animado, fundo bege, mockups e terminal (ver `referencias/lucassena-reel-referencia.mp4`).
- https://www.instagram.com/gabrielsodre.design : estilo de criação que o responsável mais gosta (arte de impacto).
- https://www.instagram.com/spotdesignn
- https://www.instagram.com/p/DZdI71cDQSE/
- https://www.instagram.com/p/C4xuRH0uOSn/
- Print em `referencias/jdevco-pinterest-print.png` (@jdevco, "Referências no Pinterest"): tipografia gigante cortada, pincelada vermelha, estátua clássica em preto e branco com faixa de cor, papel rasgado, rabiscos, etiquetas e códigos pequenos nas bordas, hierarquia forte. É o tipo de criação que o responsável quer reproduzir, adaptado à Bravos.

## Duas linhas de conteúdo
1. **Informativa** (estilo Lucas): IA, atualidades, dicas de marketing e vendas para pequenos negócios. Reels com texto animado e mockups.
2. **Criativa** (estilo Gabriel / print acima): posts estáticos e carrosséis de impacto para mostrar o nível do estúdio.

## Rodízio
Dia 1 Reels, dia 2 imagem estática, dia 3 carrossel, dia 4 Reels, e assim por diante. Alternar linha informativa e criativa.

## Como produzir
- Imagens: gerador de imagens do ElevenLabs (conexão completa `mcp__ElevenLabs-c70c56f0__*`). Usar modelo que aceite 4:5 direto (aspect_ratio 4:5, resolution 2K); o modelo antigo devolvia 1280x720 mesmo pedindo vertical. Gasta créditos: gerar poucas variações e escolher.
- Textos, tipografia e acabamento: montar em HTML/CSS e renderizar com Playwright (como em `graficos/fonte/`), usando a imagem gerada como base. Evitar texto gerado pela IA dentro da imagem quando possível.
- Reels: motor `seek(t)` em `video/fonte-v3/` e `video/comerciais/brasa-fonte/`; som com as 3 ferramentas de `ferramentas/` (ver CLAUDE.md).
- Guardar cada post em `instagram/posts/AAAA-MM-DD-tipo-tema/` com arte final, fonte, `legenda.md` (legenda + hashtags) e `status.md` (rascunho, aprovado, publicado).

## Regras de criação
- Adaptar o estilo à Bravos; NÃO copiar posts de outros criadores nem usar o nome, a marca ou o rosto deles. Não usar logos de terceiros (Nike, Pinterest etc.) nem marcas alheias nas artes.
- O mascote (águia) só quando fizer sentido (abertura/final de vídeos, ocasiões específicas). Não colocar em todo post.
- A paleta não precisa ficar presa ao laranja e preto: testar tons novos que combinem (vermelho/preto como no print, bege, etc.). Evitar verde fora de contexto, a menos que o post peça.
- Fonte de marca: Bricolage Grotesque; pode misturar com tipografia de impacto e manuscrita nos posts criativos.
- Não usar fotos soltas de roupa, tênis etc., exceto para mostrar o site da Referência Grifes.
- Contato nos posts: WhatsApp (16) 99371-9284, bravosstudio.digital, @bravos_studios.
- Nunca guardar senhas ou tokens no repositório.

## Publicação diária (na sessão no computador)
1. Abrir nova aba no Chrome (não reutilizar a aba do outro Instagram), entrar na conta destinada aos posts.
2. Criar a publicação (imagem, carrossel ou Reels), colar a legenda de `legenda.md`, conferir a prévia.
3. Se o responsável pediu aprovação, esperar o ok; senão publicar às 10h00 e marcar `status.md` como publicado.
4. Agendamento: criar tarefa agendada (10h00 de Brasília) na sessão do computador; a nuvem não alcança o Chrome.
