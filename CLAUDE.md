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
catálogo** (Deezer / MusicBrainz / Discogs). Na dúvida, não entra.

- `data/artist_fame.json` — fãs do Deezer + id do artista por nó, usado pelo
  build para calcular o score de fama (0..1000) e o pool `FAMOUS_IDS`, de onde
  saem TODOS os sorteios aleatórios. Regenerado por `.github/workflows/artist-fame.yml`
  (dispara ao tocar `.github/fame-kick`), que publica em `deezer-results`.
- A branch `deezer-results` guarda as auditorias (vereditos por catálogo, dados
  multi-fonte). **Nunca force-push nela** — ela carrega arquivos que o checkout
  do CI não tem.
