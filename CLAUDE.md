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
- **Ainda não resolvido:** cover e tributo entram como colaboração. Seu Jorge
  regravando Bowie e Lorde no tributo do Brits viraram arestas. Estão nas ~8,6k
  arestas antigas sem fonte.

- `data/artist_fame.json` — fãs do Deezer + id do artista por nó, usado pelo
  build para calcular o score de fama (0..1000) e o pool `FAMOUS_IDS`, de onde
  saem TODOS os sorteios aleatórios. Regenerado por `.github/workflows/artist-fame.yml`
  (dispara ao tocar `.github/fame-kick`), que publica em `deezer-results`.
- A branch `deezer-results` guarda as auditorias (vereditos por catálogo, dados
  multi-fonte). **Nunca force-push nela** — ela carrega arquivos que o checkout
  do CI não tem.
