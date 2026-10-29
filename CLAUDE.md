# Connect the Notes

Jogo de conectar artistas por colaborações reais. React (CRA + craco) no
`frontend/`, dados canônicos em `data/source_data.py`.

## Comandos

- `python3 data/build.py` — regenera `frontend/src/data/dataset.js` a partir de
  `data/source_data.py`. **Sempre rode depois de mexer nos dados.**
- `cd frontend && CI=false npx craco build` — valida que compila.
- `python3 tools/sim_random.py [n]` — mede o sorteio aleatório (antes × depois).

## Deploy

Produção é publicada pela Vercel a partir da branch `main`.

**Link do jogo:** https://connect-the-notes-matheusmarques13s-projects.vercel.app

Ao terminar uma tarefa, sempre mandar esse link para o usuário e avisar se o
deploy correspondente já está no ar (checar o estado na Vercel — `READY` — e não
apenas o push).

## Dados

Regra que vale para todo o dataset: **só entra colaboração real, verificada em
catálogo** (MusicBrainz / Deezer / Discogs). Na dúvida, não entra.

### Pipeline de auditoria (tools/)

O dataset original foi escrito de memória de modelo, não colhido de catálogo, e
tinha ~3,5% de arestas fabricadas (título que era rótulo de gênero, formato ou
evento) além de acabar em 2022. As ferramentas abaixo consertaram isso e devem
ser rodadas de novo sempre que os dados crescerem:

- `audit_edges.py` — marca arestas cujo título não é nome de música. Local, sem rede.
- `repair_edges.py` → `verify_br_pairs.py` — pergunta ao MusicBrainz e ao Deezer
  se o par realmente gravou junto. **Não achar não é prova**: a cobertura de
  lançamento brasileiro recente é fraca, e 57% dos pares BR que o MusicBrainz
  rejeitou eram reais.
- `harvest_recent.py` → `apply_harvest.py` — colhe colaborações 2023+ que o
  dataset nunca teve. Só aceita gravação em que **todos** os creditados já estão
  no roster; nunca inventa artista.
- `verify_casts.py` → `apply_cast_fixes.py` — acha artista creditado em música
  onde não está (era o caso da Shakira em *I Like It*).
- `prune_lives.py` — live sem fonte em catálogo: internacional sai; brasileira é
  conferida no Deezer e no MusicBrainz e fica se existir (ou ganha o título da
  gravação real da dupla, se o título estava inventado).
- `verify_old_rows.py` — confere cada linha sem fonte (as do seed): música
  exata no Deezer **e** no MusicBrainz antes de qualquer troca de título (o
  Deezer credita *SICKO MODE* só ao Travis Scott; sozinho, trocaria por *Fair
  Trade*). Par real com título inventado → título da gravação real; par sem
  gravação conjunta em nenhum dos dois → sai, salvo se for da mesma banda
  (filiações do Wikidata e do MusicBrainz). Membro creditado pelo grupo conta,
  só com a música exata: *RITMO* é do Black Eyed Peas e vale para will.i.am,
  *Walk It Talk It* é dos Migos e vale para Offset. Consulta que falhou fica. Dupla
  famosa que nenhum catálogo confirma passa por busca na web com segunda
  checagem independente (`data/web_check.json`); `--restore` devolve as achadas.
- `prune_orphans.py` — tira do roster quem ficou sem nenhuma colaboração.

Tudo é reversível: linha removida vai para `data/quarantine.json` com o texto
original, artista removido para `data/pruned_artists.json`.

### Armadilhas já pagas

Cada uma dessas custou dado real ou quase custou:

- **"Ao vivo" não é sinal de fabricação.** No sertanejo e no pagode o DVD ao vivo
  é o formato primário de lançamento. Purgar ao vivo apagaria repertório real.
  O eixo certo é *existe no catálogo × inventado*, nunca *ao vivo × estúdio*.
- **Acústico ≠ ao vivo.** *Poesia Acústica* é cypher de estúdio.
- **Membro de grupo.** Catálogos creditam "Migos" onde nós creditamos Offset e
  Quavo. Sem `data/artist_groups.json` a verificação de elenco os apagaria.
- **Franquia numerada.** *Mayor Que Yo* tem cinco elencos diferentes entre as
  partes 1, 2 e 3 — ano errado na linha faz a correção remover o artista certo.
- **Lançamento póstumo é normal.** Kygo × Whitney Houston é real. Detector de
  anacronismo não funciona para música (ver `find_impossible.py`).
- **Cover e tributo entram como colaboração**, e o detector automático disso
  (`verify_casts.py --duos`) **não pode rodar sozinho**: medido contra
  verificação na web, tem **24% de precisão**. Ele marcou *Under Pressure*
  (Bowie × Queen), *Hey Jude* (McCartney × Lennon) e *It Wasn't Me*
  (Shaggy × RikRok) como cover. Serve só como fila de revisão humana.
  A causa: o MusicBrainz tem 135 gravações de *Under Pressure* e as do topo
  creditam só o Queen — o detector não distingue "não existe gravação conjunta"
  de "os 10 primeiros resultados creditam só um".
- **Crédito de composição não é colaboração.** Bernie Taupin escreveu para o
  Elton John, Djavan compôs *Álibi* para a Bethânia, Benny Andersson é do
  sample de *Hung Up*. Nenhum tocou na gravação.
- **Nome dentro de outro nome não é crédito.** "MØ" vira "m", que está em
  quase todo crédito; "TINI" está em "Tinie Tempah", "Mora" em "Morad". A
  conferência aceita nome igual, o código do Deezer, ou o nome como palavra
  inteira dentro de um maior — e, se o maior for outro artista do elenco, só
  como parte de dupla ou grupo ("Wisin & Yandel" vale para Wisin; "Camila
  Cabello" não vale para a banda Camila).
- **Mesma pessoa em dois nós.** "Pharrell" e "Pharrell Williams", "Kevinho" e
  "MC Kevinho" são nós separados, e o código do Deezer do nome curto aponta
  para uma página errada (3 fãs). Uma regra de nome estrita demais apagaria
  *Get Lucky*. `verify_old_rows.py --recheck` reconfere provas antigas; as
  rejeições dele se revisam à mão antes de aplicar.
- **Lista de músicas no título é emenda de DJ**, a não ser que seja pot-pourri
  ao vivo ou session (*Bad Blood / Royals / Hold Up* é mashup; *Pot-Pourri:
  Miudinho / Casa de Bamba (Ao Vivo)* é DVD de pagode). *Hitmix*, *Chart Mix* e
  *Intro* solto também não servem como título trocado.

### Como distinguir cover de colaboração (`verify_via_works.py`)

A pergunta certa não é *"existe gravação creditando os dois?"* — o crédito de
gravação é incompleto e o MusicBrainz tem 135 gravações de *Under Pressure*
creditadas só ao Queen. A pergunta é sobre a **obra**:

1. Percorra **todas** as gravações da obra (`?work=<id>`), não os primeiros
   resultados da busca por título. É aí que aparece a versão "Queen + Bowie".
2. Alguma gravação credita os dois → colaboração.
3. Cada um gravou separado e nunca juntos → **cover**.
4. Um só assina a obra e não aparece em nenhuma gravação → **composição**,
   mas só se tiver poucas gravações próprias: Bernie Taupin tem 45, Desmond
   Child 84, John Lennon 8.630. Quem tem milhares está creditado como banda,
   não ausente — foi isso que salvou *Hey Jude*.
5. Qualquer outra coisa → inconclusivo, **mantém a aresta**.

Trava obrigatória antes de tudo: **grupo em comum**, não link direto. Clapton
aponta para "Cream" e Jack Bruce também, mas nenhum aponta para o outro.

Produtor que também toca (Nile Rodgers em *We Are Family*, Lee Perry no Marley)
é zona cinzenta e fica — a regra para remover é *na dúvida, não remove*.

- `data/artist_fame.json` — fãs do Deezer + id do artista por nó, usado pelo
  build para calcular o score de fama (0..1000) e o pool `FAMOUS_IDS`, de onde
  saem TODOS os sorteios aleatórios. Regenerado por `.github/workflows/artist-fame.yml`
  (dispara ao tocar `.github/fame-kick`), que publica em `deezer-results`.
- A branch `deezer-results` guarda as auditorias (vereditos por catálogo, dados
  multi-fonte). **Nunca force-push nela** — ela carrega arquivos que o checkout
  do CI não tem.
