# Relatório de Auditoria — Connect the Notes

**FASE 1 (auditoria) — nada foi apagado.** Aguardando aprovação para a FASE 3 (limpeza).

## Metodologia (2 passes independentes)

1. **Pré-scan determinístico** (sem IA): títulos em branco/genéricos/curtíssimos, duplicatas exatas e quase-duplicatas, contagem por artista.
2. **Passe 1 — classificação por conhecimento** (206 lotes, todas as 18.460 collabs): cada registro → `CONFIRMADA` / `SUSPEITA` / `INVÁLIDA`, com a regra dura *"na dúvida, SUSPEITA; nunca confirmar por palpite"*.
3. **Passe 2 — verificação web adversarial** das candidatas INVÁLIDA: um verificador independente tentou **provar que cada uma é real** via busca na web. Só permanece INVÁLIDA quem os **dois passes** condenam; falso-positivos viram RESGATADA; inconclusivos web viram SUSPEITA.

> A verificação web parou em **1.128 de 1.391** candidatas (limite semanal de uso). As **263** restantes ficam como `INVÁLIDA_PENDENTE` (suspeita de fabricação pelo Passe 1, **ainda sem** confirmação web) — não recomendo removê-las antes de completar o Passe 2.

## Contagem geral

| Status final | Qtd | O que significa |
|---|---:|---|
| ✅ CONFIRMADA | 4,698 | collab real e conhecida — manter |
| ❓ SUSPEITA | 12,564 | incerta (inclui 193 rebaixadas do Passe 1 por web inconclusiva) — manter e revisar |
| ❌ INVÁLIDA (confirmada 2 passes) | 867 | fabricação confirmada por IA **e** web — **candidata a remoção** |
| ⚠️ INVÁLIDA (pendente) | 263 | suspeita forte, sem verificação web ainda — **não remover ainda** |
| ♻️ RESGATADA | 68 | Passe 1 errou; web provou que é real — **manter** |
| **Total** | **18,460** | 18.460 collabs / 5.898 artistas |

**Categorias determinísticas** (sobrepostas ao acima): **632** cópias duplicadas exatas · **249** títulos em branco/genéricos/curtíssimos.

O exemplo que você citou está capturado: **Ivete Sangalo × Ne-Yo — “What You Want”** (#1972).

## ❌ INVÁLIDAS confirmadas (2 passes) — 867 — candidatas a remoção

Fabricações confirmadas pela classificação **e** pela verificação web independente. Ordenadas por id.

- **Bad Bunny × Shakira** — “TQG” [song, 2023] (#107) — _TQG é de Karol G com Shakira, não Bad Bunny_  
    ↳ web: Wikipedia/Spotify: 'TQG' é de Karol G feat. Shakira (2023), Bad Bunny não creditado
- **Kendrick Lamar × Lil Baby** — “N95” [song, 2022] (#118) — _N95 é solo de Kendrick, sem Lil Baby_  
    ↳ web: Wikipedia: 'N95' de Kendrick Lamar tem Baby Keem, não Lil Baby
- **Lil Wayne × 50 Cent** — “Ayo Technology” [song, 2007] (#125) — _Ayo Technology é de 50 Cent com Timberlake, sem Lil Wayne_  
    ↳ web: Wikipedia/Discogs: 'Ayo Technology' é 50 Cent feat. Justin Timberlake & Timbaland, sem Lil Wayne
- **Frank Ocean × Anderson .Paak** — “Solo (Reprise)” [song, 2016] (#166) — _Solo (Reprise) tem André 3000, não Anderson .Paak_  
    ↳ web: Wikipedia: 'Solo (Reprise)' do Blonde é cantada por André 3000, não Anderson .Paak
- **Charlie Puth × Megan Thee Stallion** — “Cry Baby” [song, 2021] (#183) — _Cry Baby não é dueto Charlie Puth/Megan_  
    ↳ web: Wikipedia: 'Cry Baby' (2020/2021) é de Megan Thee Stallion feat. DaBaby, não Charlie Puth
- **Diplo × Major Lazer** — “Major Lazer Project” [album, 2015] (#204) — _não existe álbum chamado Major Lazer Project_  
    ↳ web: Wikipedia: não existe álbum 'Major Lazer Project'; álbum de 2015 do Major Lazer (projeto do Diplo) é 'Peace Is the Mission'
- **David Guetta × Eminem** — “Not Afraid of the Dark” [song, 2011] (#211) — _Not Afraid é solo do Eminem, faixa fabricada_  
    ↳ web: Wikipedia: 'Not Afraid' (2010) é solo do Eminem (Recovery); não existe faixa 'Not Afraid of the Dark' com David Guetta
- **Usher × Lil Wayne** — “OMG” [song, 2010] (#222) — _OMG é com will.i.am, não Lil Wayne_  
    ↳ web: Discogs/IMDb: 'OMG' (2010) de Usher é featuring will.i.am, não Lil Wayne
- **Sia × Dua Lipa** — “Genius (LSD)” [song, 2018] (#227) — _Genius é do LSD; Dua Lipa não participa_  
    ↳ web: Wikipedia/Discogs: 'Genius' do LSD credita Sia, Diplo, Labrinth; remix tem Lil Wayne, nao Dua Lipa
- **Gilberto Gil × Gal Costa** — “Domingo” [album, 1967] (#603) — _Domingo 1967 é de Caetano e Gal, não Gil_  
    ↳ web: Wikipedia: álbum 'Domingo' (1967) é de Gal Costa e Caetano Veloso, não Gilberto Gil
- **Veigh × WIU** — “Largado às Traças” [song, 2022] (#632) — _'Largado às Traças' é de Zé Neto e Cristiano, não Veigh×WIU_  
    ↳ web: Letras.mus.br: 'Largado às Traças' é de Zé Neto & Cristiano (sertanejo), não Veigh x WIU
- **Pitty × Nando Reis** — “Admirável Chip Novo” [album, 2003] (#667) — _Admirável Chip Novo é álbum solo da Pitty, sem Nando Reis_  
    ↳ web: Wikipedia/Discogs: 'Admirável Chip Novo' (2003) é álbum solo da Pitty; Nando Reis não participa (colab só em 2023)
- **Caetano Veloso × Jorge Ben Jor** — “Tropicália 2” [album, 1993] (#669) — _Tropicália 2 é de Caetano e Gil, não Jorge Ben Jor_  
    ↳ web: Wikipedia/Discogs: 'Tropicália 2' (1993) é de Caetano Veloso e Gilberto Gil, não Jorge Ben Jor
- **Kali Uchis × Bad Bunny** — “Telepatía” [feature, 2020] (#848) — _'Telepatía' é solo Kali Uchis, sem Bad Bunny_  
    ↳ web: Wikipedia: 'Telepatía' é solo de Kali Uchis sem feature; só remixes de fãs com Bad Bunny
- **Vampire Weekend × Diplo** — “Hold Up” [song, 2016] (#898) — _'Hold Up' não é colaboração Vampire Weekend/Diplo_  
    ↳ web: Wikipedia: 'Hold Up' é canção da Beyoncé (Lemonade); Ezra Koenig e Diplo só têm crédito de composição, não é colab VW/Diplo
- **Rema × Ruger** — “Calm Down (Remix)” [remix, 2021] (#990) — _remix de Calm Down é com Selena Gomez, não Ruger_  
    ↳ web: Remix de 'Calm Down' é Rema x Selena Gomez, não Ruger (Wikipedia)
- **Rema × Ayra Starr** — “Bloody Samaritan (Remix)” [remix, 2022] (#991) — _Bloody Samaritan é da Ayra Starr, não single do Rema_  
    ↳ web: 'Bloody Samaritan' é da Ayra Starr e o remix é com Kelly Rowland, não Rema (Spotify/Apple Music)
- **Rema × Fireboy DML** — “Bandana” [song, 2019] (#992) — _Bandana é Fireboy×Asake, não Rema×Fireboy_  
    ↳ web: 'Bandana' é Fireboy DML feat. Asake, não Rema (Wikipedia/Spotify)
- **Ayra Starr × Giveon** — “Commas” [song, 2021] (#993) — _Commas é solo da Ayra Starr, sem Giveon_  
    ↳ web: 'Commas' é solo da Ayra Starr, sem Giveon (Wikipedia/Spotify)
- **Ayra Starr × Cardi B** — “Bloody Samaritan (Remix)” [remix, 2022] (#994) — _remix de Bloody Samaritan foi com Kelly Rowland, não Cardi B_  
    ↳ web: Remix de 'Bloody Samaritan' é com Kelly Rowland, não Cardi B (Spotify/Apple Music)
- **Ayra Starr × Olamide** — “Bloody Samaritan” [song, 2021] (#996) — _Bloody Samaritan é solo da Ayra Starr, sem Olamide_  
    ↳ web: 'Bloody Samaritan' original é solo da Ayra Starr, sem Olamide (Wikipedia)
- **Asake × Rema** — “Organise” [song, 2022] (#1010) — _Organise é solo de Asake, sem Rema_  
    ↳ web: 'Organise' é faixa solo de Asake em Mr. Money With The Vibe, sem Rema (Wikipedia/Discogs)
- **Olamide × 2Baba** — “Story for the Gods” [song, 2016] (#1019) — _Story for the Gods é do Davido, não Olamide×2Baba_  
    ↳ web: 'Story for the Gods' é solo do Olamide (prod. Young John, álbum Street OT), sem 2Baba (tooxclusive/audiomack)
- **2Baba × P-Square** — “No One Like You” [song, 2006] (#1024) — _No One Like You é da própria P-Square, sem 2Baba_  
    ↳ web: 'No One Like You' é da própria P-Square (álbum Game Over), sem 2Baba (Wikipedia P-Square)
- **Patoranking × Diamond Platnumz** — “Girlie O (Remix)” [remix, 2015] (#1031) — _remix de Girlie O foi com Tiwa Savage, não Diamond Platnumz_  
    ↳ web: 'Girlie O (Remix)' credita Patoranking ft. Tiwa Savage, não Diamond Platnumz (BellaNaija/Spotify)
- **Niniola × Femi Kuti** — “Fela Kuti Vibes” [song, 2020] (#1049) — _título 'Fela Kuti Vibes' parece fabricado, sem registro_  
    ↳ web: colab real Niniola×Femi Kuti (2020) é 'Fantasy', não 'Fela Kuti Vibes' (OkayAfrica/ChannelsTV)
- **Oxlade × Fireboy DML** — “Ku Lo Sa” [song, 2021] (#1060) — _Ku Lo Sa é solo de Oxlade, sem Fireboy_  
    ↳ web: 'Ku Lo Sa' é solo de Oxlade (feature notável é com Camila Cabello), sem Fireboy DML (Apple Music)
- **Stonebwoy × Burna Boy** — “Activate” [song, 2019] (#1077) — _Activate é de Stonebwoy com Davido, não Burna Boy_  
    ↳ web: 'Activate' (2019) é Stonebwoy ft. Davido, não Burna Boy (Vibe/SoundCloud Stonebwoy)
- **Sho Madjozi × Drake** — “My N*gga (Remix)” [remix, 2019] (#1122) — _remix de Sho Madjozi com Drake é fabricação improvável_  
    ↳ web: Nenhuma evidência de colaboração/remix entre Sho Madjozi e Drake; features reais dela são Stormzy/Burna Boy (spotify, billboard)
- **Tems × Rema** — “Free Mind (Remix)” [remix, 2020] (#1389) — _'Free Mind' é solo da Tems, remix com Rema não documentado_  
    ↳ web: Spotify/Apple: 'Free Mind' é solo de Tems; remixes por outros DJs, sem Rema. Colab real Tems/Rema é remix de 'Bout U'
- **Adekunle Gold × Lucky Dube** — “5 Star” [song, 2022] (#1405) — _Lucky Dube morreu em 2007, colaboração 2022 impossível_  
    ↳ web: BellaNaija/ThatGrapeJuice: '5 Star' (2022) de Adekunle Gold é solo; remix ft. Rick Ross, não Lucky Dube (falecido 2007)
- **Anitta × Snoop Dogg** — “Deixa Ele Sofrer” [song, 2018] (#1412) — _título não corresponde a colaboração real Anitta x Snoop Dogg_  
    ↳ web: Wikipedia: 'Deixa Ele Sofrer' é single solo da Anitta (2015), sem Snoop Dogg; colab real com Snoop é 'Onda Diferente'
- **Dennis DJ × MC Ryan SP** — “Que Tiro Foi Esse” [song, 2018] (#1443) — _Que Tiro Foi Esse é de Jorge Jay/Zé Felipe, não Dennis x Ryan SP_  
    ↳ web: 'Que Tiro Foi Esse' é de Jojo Todynho/Maronttinni (comp. DJ Batata e Pitter Corrêa), não Dennis DJ x MC Ryan SP (pt.wikipedia / open.spotify.com)
- **MC Ryan SP × WC no Beat** — “Que Tiro Foi Esse” [song, 2018] (#1474) — _Que Tiro Foi Esse não é de Ryan SP x WC no Beat_  
    ↳ web: 'Que Tiro Foi Esse' é single solo de Jojo Todynho/Maronttinni, não MC Ryan SP x WC no Beat (letras.mus.br / open.spotify.com)
- **MC Zaac × Sean Paul** — “Bum Bum Tam Tam” [song, 2017] (#1499) — _Sean Paul não está no Bum Bum Tam Tam_  
    ↳ web: 'Bum Bum Tam Tam' é de MC Fioti; remix traz Future/J Balvin/Stefflon Don/Juan Magán, sem Sean Paul nem MC Zaac (en.wikipedia)
- **MC Zaac × Tyga** — “Loka” [song, 2018] (#1502) — _Loka não é colaboração Zaac x Tyga_  
    ↳ web: 'Loka' (2017) é de Simone & Simaria feat. Anitta, não MC Zaac x Tyga (en.wikipedia / discogs.com)
- **Furacão 2000 × MC Doca** — “Rap das Armas” [song, 2008] (#1518) — _MC Doca não é o autor; Rap das Armas é Cidinho & Doca, não Furacão x Doca_  
    ↳ web: 'Rap das Armas' é de MC Júnior & MC Leonardo (original) / Cidinho & Doca (cover), não Furacão 2000 x MC Doca (en.wikipedia / open.spotify.com)
- **Jojo Todynho × Dennis DJ** — “Que Tiro Foi Esse” [song, 2019] (#1523) — _Que Tiro Foi Esse é de Jojo Maronttinni, não feat Dennis DJ_  
    ↳ web: 'Que Tiro Foi Esse' é single solo de Jojo Todynho (=Maronttinni), sem participação de Dennis DJ (pt.wikipedia / cifras.com.br)
- **Alok × Anitta** — “Is It Love (Belo Horizonte)” [song, 2019] (#1544) — _'Is It Love' é Alok com Mathieu Koss, não Anitta_  
    ↳ web: não há faixa 'Is It Love' de Alok; colaboração Alok+Anitta é 'Looking For Love' (2024) (Rolling Stone/Spotify)
- **Alok × Luísa Sonza** — “Terremoto” [song, 2021] (#1546) — _'Terremoto' é Alok com Anitta, não Luísa Sonza_  
    ↳ web: 'Terremoto' é de Anitta & MC Kevinho, não Alok com Luísa Sonza (Spotify/Shazam)
- **Alok × Giulia Be** — “Hear Me Now” [song, 2019] (#1548) — _'Hear Me Now' é Alok/Bruno Martini/Zeeba, não Giulia Be_  
    ↳ web: 'Hear Me Now' é de Alok, Bruno Martini feat. Zeeba (2016), não Giulia Be (Wikipedia/Spotify)
- **Ivete Sangalo × Anitta** — “Ai Se Eu Te Pego (Remix)” [remix, 2022] (#1555) — _'Ai Se Eu Te Pego' é de Michel Teló, não remix Ivete/Anitta_  
    ↳ web: 'Ai Se Eu Te Pego' é de Michel Teló (remix feat. Pitbull); 1ª colab Ivete+Anitta foi 'Lugar Perfeito' (LETRAS/Spotify)
- **Flay × Anitta** — “Modo Turbo” [song, 2021] (#1578) — _'Modo Turbo' é Luísa Sonza/Pabllo/Anitta, não Flay_  
    ↳ web: 'Modo Turbo' é de Luísa Sonza, Pabllo Vittar e Anitta; Flay não participa (pt.wikipedia.org, open.spotify.com)
- **MC Mayara × Anitta** — “Combatchy (Extended)” [song, 2019] (#1628) — _Combatchy é da Anitta com Lexa/Luísa/Rebecca, não MC Mayara_  
    ↳ web: Discogs/IMDb: 'Combatchy' é Anitta, Lexa, Luísa Sonza feat. MC Rebecca; sem MC Mayara
- **MC Morena × Dennis DJ** — “Baile de Favela” [song, 2019] (#1632) — _Baile de Favela é do MC João, não MC Morena/Dennis_  
    ↳ web: WhoSampled/1001Tracklists: 'Baile de Favela' é do MC João (remix Dennis DJ); sem MC Morena
- **Kondzilla × Dennis DJ** — “Baile de Favela” [song, 2016] (#1660) — _Baile de Favela é do MC João, não Kondzilla/Dennis_  
    ↳ web: YouTube/1001Tracklists: 'Baile de Favela' é MC João, Dennis DJ remix; KondZilla é o canal/label, não artista creditado
- **Tainá Costa × Anitta** — “Modo Turbo” [song, 2021] (#1678) — _Modo Turbo é Luísa Sonza/Pabllo/Anitta, não Tainá Costa_  
    ↳ web: Discogs: 'Modo Turbo' é Luísa Sonza & Pabllo Vittar feat. Anitta; sem Tainá Costa
- **Cacau Oliver × Anitta** — “Faz Gostoso” [song, 2020] (#1681) — _Faz Gostoso é Anitta com Blaya, não Cacau Oliver_  
    ↳ web: Wikipedia PT: 'Faz Gostoso' é da Blaya, gravada por Anitta (e Madonna); sem Cacau Oliver
- **MC Duda do Marapé × Anitta** — “Combatchy (Feat.)” [song, 2019] (#1695) — _Combatchy é Anitta/Lexa/Luísa/Rebecca, não MC Duda_  
    ↳ web: Discogs/IMDb: 'Combatchy' é Anitta, Lexa, Luísa Sonza feat. MC Rebecca; sem MC Duda do Marapé
- **Anitta × Nicky Jam** — “Sure Thing” [song, 2019] (#1912) — _'Sure Thing' é cover solo da Anitta, não feat com Nicky Jam_  
    ↳ web: 'Sure Thing' é de Miguel; colaboração real Anitta/Nicky Jam é 'Dançarina Remix' (en.wikipedia.org)
- **MC Kevinho × MC Livinho** — “Baile da Favela” [song, 2019] (#1936) — _'Baile da Favela' é de MC João, não Kevinho/Livinho_  
    ↳ web: 'Baile de Favela' (2015) é de MC João e DJ R7, não Kevinho/Livinho (spotify.com)
- **Dennis DJ × Anitta** — “Funk Rave” [song, 2018] (#1944) — _'Funk Rave' é solo da Anitta (2023), não com Dennis em 2018_  
    ↳ web: 'Funk Rave' é solo da Anitta (2023), sem Dennis DJ (en.wikipedia.org)
- **Criolo × Djavan** — “Nó na Orelha” [song, 2011] (#1961) — _'Nó na Orelha' é álbum do Criolo, não feat com Djavan_  
    ↳ web: 'Nó na Orelha' (2011) é álbum autoral do Criolo, sem Djavan (discogs.com)
- **Ivete Sangalo × Ne-Yo** — “What You Want” [song, 2016] (#1972) — _Ivete Sangalo feat. Ne-Yo é fabricação típica do dataset_  
    ↳ web: Não há música 'What You Want' Ivete/Ne-Yo; Ne-Yo não consta nos feats da Ivete (portalpopline.com.br)
- **Thiaguinho × Sorriso Maroto** — “Ai Se Eu Te Pego” [song, 2019] (#1975) — _'Ai Se Eu Te Pego' é de Michel Teló, não Thiaguinho/Sorriso_  
    ↳ web: 'Ai Se Eu Te Pego' é de Michel Teló (2011), não Thiaguinho/Sorriso (en.wikipedia.org)
- **Naiara Azevedo × Marília Mendonça** — “Malhação” [song, 2019] (#2034) — _título 'Malhação' não é faixa real desse dueto_  
    ↳ web: Purepeople/Metrópoles: dueto real Naiara x Marília é '50%', não 'Malhação'
- **Joelma × Anitta** — “Calypso Pop” [song, 2021] (#2042) — _Joelma feat. Anitta 'Calypso Pop' aparenta fabricação_  
    ↳ web: Letras/Popline: colab real Joelma feat. Anitta é 'Dançando Calypso' (2021), não 'Calypso Pop'
- **Seu Jorge × Zeca Pagodinho** — “Apelido Carinhoso” [song, 2017] (#2100) — _'Apelido Carinhoso' é de Dilsinho/Péricles, não de Seu Jorge e Zeca_  
    ↳ web: 'Apelido Carinhoso' (2017) é de Gusttavo Lima, comp. Junior Angelim (Spotify/IMDb), não Seu Jorge e Zeca
- **Elba Ramalho × Luiz Gonzaga** — “Riacho do Navio” [song, 2012] (#2117) — _Luiz Gonzaga morreu em 1989, impossível gravação em 2012_  
    ↳ web: Dueto real Elba+Gonzaga é 'Sanfoninha Choradeira'; 'Riacho do Navio' em 'Duetos com Mestre Lua' é com Fagner (Vagalume)
- **Caetano Veloso × Elza Soares** — “AmarElo” [song, 2019] (#2227) — _AmarElo é do Emicida; não é parceria Caetano/Elza_  
    ↳ web: LETRAS/amusicade: 'AmarElo' (2019) é do Emicida com Majur e Pabllo Vittar, não parceria Caetano/Elza
- **Luedji Luna × Gilsons** — “Um Corpo no Mundo” [song, 2017] (#2342) — _'Um Corpo no Mundo' é de Luedji Luna sozinha, não com Gilsons_  
    ↳ web: Bandcamp/Spotify: 'Um Corpo no Mundo' (2017) é álbum/faixa solo de Luedji Luna, sem Gilsons
- **Carlinhos Brown × Caetano Veloso** — “Tropicália 2” [album, 1993] (#2349) — _Tropicália 2 é de Caetano e Gil, não de Carlinhos Brown; ano 1993 inconsistente_  
    ↳ web: Wikipedia/Discogs: 'Tropicália 2' (1993) é de Caetano Veloso e Gilberto Gil, não Carlinhos Brown
- **Tim Maia × Gilberto Gil** — “Descobridor dos Sete Mares” [song, 1983] (#2363) — _'Descobridor dos Sete Mares' é de Tim Maia sozinho, não com Gil_  
    ↳ web: Wikipedia/Discogs: 'O Descobridor dos Sete Mares' é solo de Tim Maia (1983), composta por Gilson Mendonça/Michel, sem Gilberto Gil
- **Papatinho × Emicida** — “Deixa Eu Dizer” [song, 2017] (#2382) — _'Deixa Eu Dizer' é clássico dos Racionais; Matuê/Papatinho não cabe no ano_  
    ↳ web: Letras/Discogs: 'Deixa Eu Dizer' é de Cláudia (1973, Ivan Lins); não existe faixa de Papatinho com Emicida com esse título
- **Papatinho × Matuê** — “Deixa Eu Dizer” [song, 2017] (#2383) — _faixa e ano inconsistentes para Matuê com Papatinho_  
    ↳ web: Deezer/Letras: não há faixa 'Deixa Eu Dizer' de Papatinho com Matuê; colaborações reais têm outros títulos
- **Papatinho × MC Cabelinho** — “Deixa Eu Dizer” [song, 2017] (#2384) — _título e ano inconsistentes com MC Cabelinho_  
    ↳ web: Letras/Spotify: nenhuma faixa 'Deixa Eu Dizer' de Papatinho com MC Cabelinho; título pertence a Cláudia/Marcelo D2
- **Papatinho × Filipe Ret** — “Deixa Eu Dizer” [song, 2017] (#2385) — _título e ano inconsistentes com Filipe Ret_  
    ↳ web: Busca web: não existe 'Deixa Eu Dizer' de Papatinho com Filipe Ret; título é de Cláudia (Ivan Lins)
- **Elis Regina × Ivan Lins** — “Elis & Tom” [album, 1974] (#2414) — _'Elis & Tom' é só de Elis e Tom Jobim, não de Ivan Lins_  
    ↳ web: Wikipedia: álbum 'Elis & Tom' (1974) é de Elis Regina e Antônio Carlos Jobim, não Ivan Lins
- **Rodrigo Amarante × Nando Reis** — “Los Hermanos” [album, 2005] (#2431) — _Los Hermanos é a banda, não álbum feito com Nando Reis_  
    ↳ web: Los Hermanos é banda de que Amarante é membro; Nando Reis não integra o grupo nem o álbum homônimo (en.wikipedia.org)
- **Los Hermanos × Rodrigo Amarante** — “Ventura” [album, 2003] (#2433) — _Amarante é membro do Los Hermanos, não colaboração externa_  
    ↳ web: 'Ventura' (2003) é álbum da banda Los Hermanos, da qual Amarante é membro; não é colaboração externa (en.wikipedia.org)
- **Luan Santana × Shakira** — “Yo Te Quiero (feat.)” [song, 2016] (#2501) — _Luan Santana x Shakira é fabricação cross-cultural improvável_  
    ↳ web: Não há canção 'Yo Te Quiero' de Luan Santana com Shakira; duetos de Luan são com Enrique Iglesias, Belinda etc (pt.wikipedia.org)
- **Michel Teló × Anitta** — “Ai Se Eu Te Pego (remix)” [song, 2012] (#2553) — _'Ai Se Eu Te Pego' não tem remix com Anitta, fabricação_  
    ↳ web: Letras/Vagalume: o remix real de 'Ai Se Eu Te Pego' credita Pitbull, não Anitta
- **Paula Fernandes × Shawn Mendes** — “Summer Of Love (PT)” [song, 2016] (#2556) — _cross-país improvável Paula Fernandes x Shawn Mendes, fabricação_  
    ↳ web: Wikipedia/Spotify: 'Summer of Love' é de Shawn Mendes & Tainy; sem versão com Paula Fernandes
- **Pabllo Vittar × Gloria Groove** — “K.O.” [song, 2018] (#2664) — _K.O. é faixa solo de Pabllo Vittar, sem Gloria Groove_  
    ↳ web: 'K.O.' é faixa solo de Pabllo Vittar (álbum Vai Passar Mal), sem Gloria Groove (Wikipedia)
- **Pabllo Vittar × Anitta** — “Triste com T” [song, 2018] (#2665) — _Triste com T é de Pabllo Vittar, sem Anitta_  
    ↳ web: 'Triste com T' é solo de Pabllo Vittar (Batidão Tropical 2021), sem Anitta (pt.wikipedia/spotify)
- **Post Malone × Tim McGraw** — “I Had Some Help” [feature, 2024] (#3004) — _'I Had Some Help' é com Morgan Wallen, não Tim McGraw_  
    ↳ web: Wikipedia/Billboard: 'I Had Some Help' de Post Malone é feat. Morgan Wallen, não Tim McGraw
- **Post Malone × Brad Paisley** — “Guy for That” [song, 2024] (#3005) — _'Guy for That' é com Morgan Wallen, não Brad Paisley_  
    ↳ web: Wikipedia/Spotify: 'Guy for That' de Post Malone é feat. Luke Combs, não Brad Paisley
- **George Strait × Garth Brooks** — “Cowboys and Indians (Live CMA)” [live, 2009] (#3017) — _'Cowboys and Indians' não é faixa conhecida de Strait/Garth_  
    ↳ web: Wikipedia: primeiro dueto Strait/Garth foi 'The Cowboy Rides Away' (48th ACM, 2013); 'Cowboys and Indians' não existe como faixa deles
- **Shania Twain × Lil Durk** — “Giddy Up!” [song, 2023] (#3021) — _par improvável Shania x Lil Durk; título não recordado_  
    ↳ web: Wikipedia/Billboard: 'Giddy Up!' é single solo da Shania Twain (2023), sem Lil Durk
- **HARDY × Florida Georgia Line** — “One Beer” [song, 2019] (#3033) — _'One Beer' é com Lauren Alaina/Devin Dawson, não FGL_  
    ↳ web: Wikipedia/Spotify: 'One Beer' de HARDY é feat. Lauren Alaina & Devin Dawson, não Florida Georgia Line
- **Kelsea Ballerini × Dua Lipa** — “Cowboys Don't Cry (Dua Lipa feature)” [song, 2023] (#3038) — _'Cowboys Don't Cry' não tem feature de Dua Lipa_  
    ↳ web: Rolling Stone/Wikipedia: música da Kelsea 'Cowboys Cry Too' tem feature de Noah Kahan, não Dua Lipa
- **Sam Hunt × Khalid** — “Hard to Forget (Khalid feature)” [feature, 2020] (#3049) — _'Hard to Forget' é solo de Sam Hunt, sem Khalid_  
    ↳ web: Wikipedia: 'Hard to Forget' é solo de Sam Hunt com sample de Webb Pierce, sem Khalid
- **Zach Bryan × Lainey Wilson** — “Something in the Orange” [feature, 2023] (#3080) — _'Something in the Orange' e solo Zach Bryan_  
    ↳ web: Wikipedia: 'Something in the Orange' é solo de Zach Bryan, sem feat de Lainey Wilson
- **Rihanna × Bob Marley** — “Lift Up” [remix, 2003] (#3187) — _Rihanna/Bob Marley remix 2003 impossível, fabricação_  
    ↳ web: Rihanna estreou em 2005; nenhum remix 'Lift Up' com Bob Marley em 2003 (en.wikipedia.org)
- **pb_rocco × Sean Paul** — “Everyday We Lit” [song, 2017] (#3245) — _Everyday We Lit é PnB Rock ft YFN Lucci, não Sean Paul_  
    ↳ web: Wikipedia/Songfacts: 'Everyday We Lit' é YFN Lucci feat. PnB Rock, sem Sean Paul
- **Jessie J × Popcaan** — “Who You Are” [song, 2018] (#3260) — _Who You Are é solo de Jessie J, sem Popcaan_  
    ↳ web: Wikipedia: 'Who You Are' é solo de Jessie J (Toby Gad/Shelly Peiken), sem Popcaan; nenhuma colab Jessie J x Popcaan encontrada
- **DJ Khaled × Beyoncé** — “Sticky” [song, 2022] (#3275) — _Sticky não tem participação de Beyoncé_  
    ↳ web: Spotify/Grammy: colabs DJ Khaled x Beyoncé são 'Shining' e 'Top Off'; não existe 'Sticky' (Drake, 2022)
- **David Guetta × will.i.am** — “Just a Little More Love” [song, 2002] (#3283) — _Just a Little More Love é com Chris Willis, não will.i.am_  
    ↳ web: Wikipedia: 'Just a Little More Love' de David Guetta tem vocais de Chris Willis, não will.i.am
- **Calvin Harris × Justin Timberlake** — “Drinking from the Bottle” [song, 2012] (#3310) — _Drinking from the Bottle é com Tinie Tempah, não JT_  
    ↳ web: Wikipedia/Spotify: 'Drinking from the Bottle' é Calvin Harris feat. Tinie Tempah, não Justin Timberlake
- **Marshmello × Tyga** — “Faded” [song, 2015] (#3318) — _Faded é de Alan Walker, não Marshmello/Tyga_  
    ↳ web: Spotify/Wikipedia: 'Faded' (2015) é de Alan Walker; sem faixa Marshmello x Tyga com esse título
- **The Chainsmokers × Ryan Tedder** — “Something Just Like This” [song, 2017] (#3324) — _Something Just Like This é com Coldplay, não Ryan Tedder_  
    ↳ web: Wikipedia: 'Something Just Like This' é The Chainsmokers x Coldplay; compositores são Taggart e membros do Coldplay, não Ryan Tedder
- **Tiësto × Demi Lovato** — “Don't Be Shy” [song, 2021] (#3342) — _Don't Be Shy é com Karol G, não Demi Lovato_  
    ↳ web: 'Don't Be Shy' (2021) é de Tiësto & Karol G, não Demi Lovato (en.wikipedia.org)
- **Skrillex × Chance the Rapper** — “BLUE (Da Ba Dee)” [song, 2016] (#3364) — _BLUE (Da Ba Dee) é Eiffel 65; não Skrillex x Chance_  
    ↳ web: 'BLUE (Da Ba Dee)' é do Eiffel 65; colab real Skrillex x Chance é 'Show Me Love' (en.wikipedia.org, complex.com)
- **Daft Punk × Stevie Wonder** — “Too Long” [song, 2001] (#3432) — _Too Long traz Romanthony, não Stevie Wonder_  
    ↳ web: Daft Wiki/Wikipedia: 'Too Long' (Discovery) traz vocais de Romanthony, não Stevie Wonder
- **Fred again.. × UK Garage** — “Delilah” [song, 2022] (#3517) — _'UK Garage' é gênero, não artista; par fabricado_  
    ↳ web: 'Delilah (pull me out of this)' é de Fred again.. feat. Delilah Montagu; 'UK Garage' é gênero (discogs.com/songfacts.com)
- **Zedd × Botnek** — “Clarity (Zedd feat. Botnek)” [song, 2013] (#3558) — _Clarity é com Foxes, não Botnek_  
    ↳ web: 'Clarity' credita Zedd feat. Foxes, não Botnek (en.wikipedia.org/discogs.com)
- **Alan Walker × Hans Zimmer** — “Live and Let Die (Remix)” [remix, 2021] (#3573) — _par implausível Alan Walker e Hans Zimmer_  
    ↳ web: Colab Alan Walker/Hans Zimmer é o remix de 'Time', não 'Live and Let Die' (edm.com/facebook.com Hans Zimmer)
- **Jul × niro** — “Bande organisée” [song, 2020] (#3703) — _niro não consta no 'Bande organisée'_  
    ↳ web: Spotify/IMDb: 'Bande organisée' credita Jul, SCH, Kofs, Naps, Soso Maness, Elams, Solda, Houari; niro não consta
- **Jul × prolongeau** — “Bande organisée” [song, 2020] (#3706) — _prolongeau não consta no 'Bande organisée'_  
    ↳ web: Spotify/IMDb: 'Bande organisée' credita Jul, SCH, Kofs, Naps, Soso Maness, Elams, Solda, Houari; prolongeau não consta
- **Sexion d'Assaut × jR_o_level** — “Sexion d'Assaut - L'Apogée” [album, 2013] (#3740) — _jR_o_level não é membro do Sexion d'Assaut_  
    ↳ web: fr.wikipedia: membro real é 'JR O Crom' (Karim Ballo); 'jR_o_level' não existe e L'Apogée é álbum do grupo Sexion d'Assaut
- **Soolking × nicky_minaj_fr** — “Ciao Bella” [song, 2019] (#3783) — _parceiro 'nicky_minaj_fr' é handle fabricado_  
    ↳ web: 'nicky_minaj_fr' é handle fabricado; discografia de Soolking (Wikipedia/Discogs) não tem 'Ciao Bella'
- **Aya Nakamura × ninos_africa** — “Jolie nana (remix)” [remix, 2020] (#3816) — _parceiro 'ninos_africa' é handle fabricado_  
    ↳ web: 'ninos_africa' é handle fabricado; Jolie Nana oficial de Aya Nakamura é solo, sem esse feat (Wikipedia)
- **Orelsan × big_fmly** — “Superstar” [song, 2021] (#3829) — _parceiro 'big_fmly' é handle fabricado_  
    ↳ web: 'big_fmly' é handle fabricado; album Civilisation de Orelsan não tem faixa 'Superstar' (Wikipedia)
- **Gims × Pharrell Williams** — “Corazon (feat. Pharrell)” [song, 2016] (#3839) — _'Corazon' tem Lil Wayne e French Montana, não Pharrell_  
    ↳ web: 'Corazón' de GIMS credita Lil Wayne e French Montana, não Pharrell (Spotify/Discogs/IMDb)
- **Gims × Kungs** — “Bohemian Rhapsody (remix)” [remix, 2016] (#3871) — _Bohemian Rhapsody remix por Gims/Kungs não existe_  
    ↳ web: Busca (Spotify/Deezer/Apple): não existe remix de 'Bohemian Rhapsody' por Gims/Kungs
- **La Fouine × Rohff** — “La Fouine x Rohff” [song, 2010] (#3923) — _La Fouine e Rohff tiveram rixa, colab improvável; título genérico_  
    ↳ web: Spotify/booska-p: colabs reais La Fouine/Rohff são 'Passe leur le salam' e 'On peut pas tout avoir'; título 'La Fouine x Rohff' não existe
- **Rohff × La Fouine** — “Le toit du monde (feat. La Fouine)” [song, 2011] (#3924) — _Rohff e La Fouine eram inimigos, colab inexistente_  
    ↳ web: Mediatheque/Spotify: 'Le toit du monde' é álbum de Sinik; colab Rohff/La Fouine real é 'On peut pas tout avoir'
- **Sido × Sarah Connor** — “Ich und meine Maske” [song, 2004] (#3951) — _'Ich und meine Maske' é solo Sido; Sarah Connor não participa_  
    ↳ web: Wikipedia/laut.de: 'Ich und meine Maske' é álbum/faixa solo de Sido; Sarah Connor não participa
- **Sido × Peter Fox** — “Beweg dein Arsch” [song, 2008] (#3952) — _'Beweg dein Arsch' é solo Sido, não feat. Peter Fox_  
    ↳ web: Wikipedia/Spotify: 'Beweg dein Arsch' credita Scooter, Kitty Kat, Tony D — não Peter Fox (esse é 'Rodeo')
- **Armin van Buuren × Hardwell** — “Blah Blah Blah” [song, 2011] (#4062) — _'Blah Blah Blah' é solo de Armin (2018), não dueto com Hardwell_  
    ↳ web: Wikipedia: 'Blah Blah Blah' (2018) é solo de Armin van Buuren, vocais de Aidan Bullimore, sem Hardwell
- **Olivia Rodrigo × Zedd** — “Deja Vu” [song, 2021] (#4087) — _'Deja Vu' é solo de Olivia Rodrigo, não feat Zedd_  
    ↳ web: Wikipedia/Billboard: 'Deja Vu' é de Olivia Rodrigo com Dan Nigro, sem Zedd
- **DJ Snake × Bad Bunny** — “Taki Taki” [song, 2018] (#4104) — _'Taki Taki' é com Selena/Ozuna/Cardi B, não Bad Bunny_  
    ↳ web: Discogs/IMDb: 'Taki Taki' credita DJ Snake, Selena Gomez, Ozuna e Cardi B, não Bad Bunny
- **AP Dhillon × Dua Lipa** — “Insane” [song, 2023] (#4233) — _não existe colaboração AP Dhillon com Dua Lipa_  
    ↳ web: 'Insane' de AP Dhillon credita Shinda Kahlon, Gurinder Gill, Gminxr; sem Dua Lipa (spotify.com, en.wikipedia.org)
- **AP Dhillon × Nick Jonas** — “Summer High” [song, 2022] (#4235) — _'Summer High' não tem Nick Jonas; fabricação cross-genre_  
    ↳ web: 'Summer High' (2022) é solo de AP Dhillon, sem artista convidado; sem Nick Jonas (imdb.com, spotify.com)
- **Guru Randhawa × Hardy Sandhu** — “Kya Baat Ay” [song, 2019] (#4250) — _'Kya Baat Ay' é de Hardy Sandhu, não dueto com Guru Randhawa_  
    ↳ web: 'Kya Baat Ay' é de Harrdy Sandhu (Jaani/B Praak), não dueto com Guru Randhawa (spotify.com, lyricsmint.com)
- **Vishal-Shekhar × ankit_tiwari** — “Galliyan” [song, 2014] (#4261) — _'Galliyan' é de Ankit Tiwari, não composição Vishal-Shekhar_  
    ↳ web: 'Galliyan' (Ek Villain) é composta e cantada por Ankit Tiwari, não Vishal-Shekhar (en.wikipedia.org, spotify.com)
- **Diljit Dosanjh × The Weeknd** — “Here We Go” [feature, 2024] (#4301) — _não existe feature Diljit Dosanjh com The Weeknd_  
    ↳ web: 'Here We Go... Again' é The Weeknd feat. Tyler, the Creator (Dawn FM 2022); não há colab Diljit Dosanjh/Weeknd (Wikipedia/Spotify)
- **Diljit Dosanjh × Sia** — “Lover (Remix)” [remix, 2021] (#4302) — _remix Diljit com Sia não existe, fabricação_  
    ↳ web: 'Lover (Remix)' de Diljit é remix Punjabi (MoonChild Era/Intense/Raj Ranjodh), sem Sia; colabs Sia dele são 'Hass Hass' e 'Ranjha' (Spotify/Billboard)
- **Jasmine Sandlas × Garry Sandhu** — “Nikle Currant” [song, 2018] (#4317) — _'Nikle Currant' é de Jassi Gill e Neha Kakkar, não esses dois_  
    ↳ web: 'Nikle Currant' (2018) é de Jassi Gill e Neha Kakkar, não Jasmine Sandlas/Garry Sandhu (Wikipedia/Spotify)
- **Guru Randhawa × nikkie_bella** — “Lagdi Lahore Di” [song, 2019] (#4336) — _Nikki Bella é wrestler; fabricação_  
    ↳ web: Spotify/Apple Music: 'Lagdi Lahore Di' credita Guru Randhawa e Tulsi Kumar, não Nikki Bella
- **Lata Mangeshkar × A.R. Rahman** — “Pyar Kiya Toh Darna Kya” [song, 1998] (#4457) — _Pyar Kiya Toh Darna Kya (Mughal-e-Azam) é de Lata; Rahman não envolvido, ano/atribuição fabricados_  
    ↳ web: Wikipedia: 'Pyar Kiya To Darna Kya' (Mughal-e-Azam 1960) cantada por Lata, composta por Naushad; sem A.R. Rahman
- **Lata Mangeshkar × Asha Bhosle** — “Aaj Phir Tum Pe” [song, 1981] (#4459) — _Aaj Phir Tum Pe (Hate Story 3) é solo; dueto Lata/Asha em 1981 fabricado_  
    ↳ web: JioSaavn/lyricsmint: 'Aaj Phir Tum Pe' original de Dayavan 1988 (Pankaj Udhas/Anuradha Paudwal) e Hate Story 2 (Arijit); não dueto Lata/Asha 1981
- **Diljit Dosanjh × The Weeknd** — “GOAT (Greatest of All Time)” [song, 2024] (#4489) — _GOAT é de Diljit Dosanjh (2020); colaboração com The Weeknd em 2024 fabricada_  
    ↳ web: Wikipedia: 'G.O.A.T.' é de Diljit Dosanjh (2020, prod. G-Funk); sem The Weeknd, só mashups de fãs
- **AP Dhillon × arjan_dhillon** — “Heart on My Sleeve” [song, 2022] (#4500) — _título 'Heart on My Sleeve' não é faixa real de AP Dhillon/Arjan Dhillon_  
    ↳ web: Wikipedia/Spotify: 'Heart on My Sleeve' (2023) é o track AI de Drake/Weeknd; sem colab AP Dhillon+Arjan Dhillon
- **Tiziano Ferro × Biagio Antonacci** — “Strani amori” [song, 2003] (#4800) — _'Strani amori' é de Laura Pausini, não de Ferro/Antonacci_  
    ↳ web: 'Strani amori' é de Laura Pausini (Sanremo 1994), não de Ferro/Antonacci (en.wikipedia.org)
- **Tiziano Ferro × Jovanotti** — “Il regalo più grande” [song, 2013] (#4803) — _'Il regalo più grande' é de Tiziano Ferro, não com Jovanotti_  
    ↳ web: 'Il regalo più grande' é de Tiziano Ferro solo; versões com convidados são RBD e Amaia Montero, não Jovanotti (en.wikipedia.org)
- **C. Tangana × omar_montes** — “Yung Beef” [song, 2021] (#4833) — _'Yung Beef' não é faixa de Tangana com Omar Montes; confuso_  
    ↳ web: 'Yung Beef' é nome de artista, não faixa de Tangana com Omar Montes; colab real deles é 'Una y Mil Veces' (youtube.com)
- **Lola Indigo × Miriam Doblas** — “El Mismo Sol” [song, 2020] (#4855) — _Miriam Doblas é o nome real de Lola Indigo; par redundante_  
    ↳ web: 'El Mismo Sol' é de Álvaro Soler (feat. Jennifer Lopez), não de Lola Indigo/Miriam Doblas (en.wikipedia.org)
- **Nathy Peluso × Becky G** — “La Noche de Anoche” [song, 2022] (#4859) — _'La Noche de Anoche' é de Bad Bunny/Rosalía, não Nathy/Becky G_  
    ↳ web: 'La Noche de Anoche' é de Bad Bunny e Rosalía, não Nathy Peluso/Becky G (en.wikipedia.org)
- **Marco Mengoni × Elodie** — “Mille” [song, 2021] (#4894) — _'Mille' é de Fedez/Achille Lauro/Orietta Berti, não Mengoni×Elodie_  
    ↳ web: Wikipedia/IMDb: 'Mille' (2021) é de Fedez/Achille Lauro/Orietta Berti; Mengoni×Elodie é 'Pazza musica' (2023)
- **Sangiovanni × Elodie** — “Mille” [feature, 2022] (#4900) — _'Mille' não é feature de Sangiovanni×Elodie_  
    ↳ web: Wikipedia: 'Mille' é de Fedez/Achille Lauro/Orietta Berti, não feature Sangiovanni×Elodie
- **Jovanotti × Eros Ramazzotti** — “L'estate addosso” [song, 2018] (#4911) — _'L'estate addosso' é solo de Jovanotti, não dueto com Eros_  
    ↳ web: Wikipedia/Spotify: 'L'estate addosso' é solo de Jovanotti (2015), sem dueto com Eros Ramazzotti
- **Enrique Iglesias × Ricky Martin** — “Súbeme la Radio remix” [remix, 2017] (#4916) — _'Súbeme la Radio' é com Zion&Lennox, não Ricky Martin_  
    ↳ web: Wikipedia: 'Súbeme la Radio' feat. Descemer Bueno & Zion&Lennox; remixes com Sean Paul/CNCO/Jacob Forever, não Ricky Martin
- **Noemi × Fedez** — “Makumba” [song, 2020] (#4926) — _'Makumba' é da Noemi solo, não feature de Fedez_  
    ↳ web: Wikipedia/Spotify: 'Makumba' é Noemi feat. Carl Brave, não Fedez
- **Becky G × David Bisbal** — “Sin Pijama” [song, 2018] (#4940) — _'Sin Pijama' é Becky G×Natti Natasha, não Bisbal_  
    ↳ web: Wikipedia/Billboard: 'Sin Pijama' é Becky G × Natti Natasha, sem David Bisbal
- **Benny Benassi × T-Pain** — “Love Is Gonna Save Us” [song, 2013] (#5011) — _'Love Is Gonna Save Us' é faixa solo de Benassi, sem T-Pain_  
    ↳ web: 'Love Is Gonna Save Us' (2004) é Benny Benassi com The Biz nos vocais, sem T-Pain (Spotify/Dork)
- **Psy × Wiz Khalifa** — “Gangnam Style” [feature, 2013] (#5040) — _Gangnam Style é só do Psy, sem Wiz Khalifa_  
    ↳ web: Wikipedia/Discogs: 'Gangnam Style' é solo do Psy, sem Wiz Khalifa
- **Jackson Wang × Flo Rida** — “Just Hold On” [feature, 2018] (#5049) — _Just Hold On é Steve Aoki x Louis Tomlinson, não Jackson Wang/Flo Rida_  
    ↳ web: Wikipedia: 'Just Hold On' é de Steve Aoki & Louis Tomlinson, não Jackson Wang/Flo Rida
- **Suga × Lil Wayne** — “Haiku” [song, 2023] (#5059) — _Haiku com Lil Wayne não existe_  
    ↳ web: Wikipedia D-Day tracklist: não existe faixa 'Haiku'; sem Lil Wayne
- **Suga × Eminem** — “Amygdala” [feature, 2023] (#5060) — _Amygdala é solo de Agust D/Suga, sem Eminem_  
    ↳ web: Wikipedia/Spotify: 'AMYGDALA' é solo do Agust D no D-Day, sem Eminem
- **RM × Anderson .Paak** — “Forever Rain” [song, 2018] (#5066) — _Forever Rain é solo do RM no mono, sem Anderson .Paak_  
    ↳ web: Wikipedia Mono: 'Forever Rain' é solo do RM; Anderson .Paak está em 'Still Life', não nesta
- **G-Dragon × Diplo** — “Who You” [song, 2013] (#5077) — _Who You é solo do G-Dragon, sem Diplo_  
    ↳ web: Billboard/Wikipedia: Diplo produziu a faixa-título 'Coup d'Etat', não 'Who You?'; 'Who You?' é solo do G-Dragon
- **Super Junior × Henry Lau** — “Bonamana” [feature, 2010] (#5080) — _Bonamana é single do Super Junior, não feature com Henry Lau_  
    ↳ web: Wikipedia: Henry compôs 'All My Heart' no repackage, não é feature no single 'Bonamana' do Super Junior
- **Taeyeon × Crush** — “Some” [feature, 2017] (#5094) — _Some é Soyou x Junggigo, não Taeyeon x Crush_  
    ↳ web: Wikipedia: 'Some' é Soyou x Junggigo feat. Lil Boi, não Taeyeon x Crush
- **Moonbyul × Loco** — “BAAM” [feature, 2018] (#5118) — _BAAM é do MOMOLAND, não Moonbyul x Loco_  
    ↳ web: Wikipedia/Spotify: 'BAAM' é single do MOMOLAND, não Moonbyul x Loco
- **Sunmi × Lauv** — “Pporappippam” [song, 2020] (#5119) — _Pporappippam é solo da Sunmi, sem Lauv_  
    ↳ web: Wikipedia: 'Pporappippam' é solo da Sunmi (com Frants), sem Lauv
- **TXT × Anitta** — “0X1=LOVESONG” [feature, 2021] (#5134) — _música do TXT sem Anitta, par improvável_  
    ↳ web: '0X1=LOVESONG' do TXT feat. Seori (e remixes pH-1/Mod Sun), não Anitta (TXT Fandom)
- **TXT × Coi Leray** — “Good Boy Gone Bad” [feature, 2022] (#5136) — _título é faixa solo do TXT, sem Coi Leray_  
    ↳ web: 'Good Boy Gone Bad' é faixa solo do TXT; Coi Leray está em outra música ('Happy Fools') (TXT Fandom)
- **ENHYPEN × JVKE** — “Drunk-Dazed” [feature, 2022] (#5137) — _Drunk-Dazed é do ENHYPEN sem JVKE_  
    ↳ web: 'Drunk-Dazed' é faixa do ENHYPEN sem feat.; JVKE não consta (Spotify/ENHYPEN Fandom)
- **Dok2 × The Quiett** — “No Flex Zone” [song, 2014] (#5163) — _No Flex Zone é dos Rae Sremmurd, não Dok2_  
    ↳ web: 'No Flex Zone' é single de estreia do Rae Sremmurd (2014), não Dok2/The Quiett (Wikipedia)
- **Giriboy × Babylon** — “Kiss Me More” [song, 2020] (#5176) — _Kiss Me More é da Doja Cat, não Giriboy_  
    ↳ web: 'Kiss Me More' é da Doja Cat feat. SZA; sem faixa Giriboy/Babylon com esse título (busca web)
- **Jolin Tsai × G-Dragon** — “Play” [feature, 2010] (#5193) — _par improvável Jolin Tsai x G-Dragon não documentado_  
    ↳ web: Wikipedia: 'Play' (2014) é solo de Jolin Tsai; colaboração com G-Dragon nunca ocorreu (allkpop apenas cita desejo de colaborar em 2012)
- **Jay Chou × Alicia Keys** — “Mojito” [feature, 2020] (#5194) — _Mojito é solo de Jay Chou sem Alicia Keys_  
    ↳ web: Wikipedia: 'Mojito' (2020) é single solo de Jay Chou, sem Alicia Keys nos créditos
- **ONE OK ROCK × Miley Cyrus** — “Heartache” [feature, 2017] (#5213) — _Heartache é do ONE OK ROCK sem Miley Cyrus_  
    ↳ web: Fandom/Spotify: 'Heartache' é do álbum 35xxxv de ONE OK ROCK, sem Miley Cyrus
- **Kenshi Yonezu × Eve** — “Pale Blue” [feature, 2021] (#5214) — _Pale Blue é solo de Kenshi Yonezu sem Eve_  
    ↳ web: Wikipedia: 'Pale Blue' (2021) é single solo de Kenshi Yonezu, sem Eve
- **Ado × Vaundy** — “New Genesis” [feature, 2023] (#5215) — _New Genesis é da Ado sem Vaundy_  
    ↳ web: Wikipedia: 'New Genesis' é escrita e produzida por Yasutaka Nakata; Vaundy fez 'Backlight', não este tema
- **Ado × Fujii Kaze** — “Hana” [feature, 2022] (#5216) — _Hana atribuída erroneamente, par não documentado_  
    ↳ web: Wikipedia: 'Hana' (2023) é single solo de Fujii Kaze, não da Ado; par não existe
- **Peso Pluma × Xavi** — “La Diabla” [song, 2023] (#5260) — _La Diabla é de Xavi solo; Peso Pluma não participa_  
    ↳ web: Wikipedia: 'La Diabla' é solo de Xavi (Interscope), sem Peso Pluma
- **Peso Pluma × Karol G** — “Mi Ex Tenía Razón” [song, 2024] (#5261) — _Mi Ex Tenía Razón é da Karol G solo, sem Peso Pluma_  
    ↳ web: Wikipedia/Spotify: 'Mi Ex Tenía Razón' é solo de Karol G, sem Peso Pluma
- **Peso Pluma × Ángela Aguilar** — “Dime Cómo Quieres” [song, 2024] (#5263) — _Dime Cómo Quieres é de Christian Nodal x Ángela Aguilar, não Peso Pluma_  
    ↳ web: Wikipedia: 'Dime Cómo Quieres' é Christian Nodal & Ángela Aguilar, não Peso Pluma
- **Natanael Cano × Bad Bunny** — “Tumbado y Relajado” [song, 2023] (#5288) — _Tumbado y Relajado Natanael x Bad Bunny fabricada_  
    ↳ web: Last.fm: 'Tumbado y Relajado' é Decalifornia feat Jay R; colab real Natanael x Bad Bunny é 'Soy El Diablo'
- **Alejandro Fernández × Vicente Fernández** — “Amor Eterno” [song, 2019] (#5362) — _Amor Eterno é de Juan Gabriel/Rocío Dúrcal, não dueto entre estes em 2019_  
    ↳ web: AllMusic/Spotify: 'Amor Eterno' é solo de Vicente Fernández (comp. Juan Gabriel); duetos com Alejandro são outros títulos
- **Marco Antonio Solís × Juan Gabriel** — “Hasta Que Te Conocí” [song, 1992] (#5367) — _Hasta Que Te Conocí é de Juan Gabriel, não dueto com Solís_  
    ↳ web: Wikipedia: 'Hasta Que Te Conocí' é de Juan Gabriel (dueto 2015 c/ Joy), não com Marco Antonio Solís
- **Maná × Shakira** — “¿Dónde Jugarán los Niños?” [song, 2011] (#5383) — _¿Dónde Jugarán los Niños? é álbum de Maná, não dueto com Shakira_  
    ↳ web: Spotify/Letras: '¿Dónde Jugarán los Niños?' é álbum/canção solo de Maná; colaboração real com Shakira é 'Mi Verdad'
- **Maná × Alejandro Sanz** — “Corazón Espinado (Dueto)” [song, 1999] (#5385) — _Corazón Espinado é Santana/Maná, não com Alejandro Sanz_  
    ↳ web: Discogs/Wikipedia: 'Corazón Espinado' credita Santana feat. Maná, não Alejandro Sanz
- **Babo × Dharius** — “Barrio Fino” [song, 2021] (#5478) — _Barrio Fino é álbum de Daddy Yankee, não faixa Babo/Dharius_  
    ↳ web: Wikipedia/Discogs: 'Barrio Fino' é álbum de Daddy Yankee (2004), não faixa de Babo/Dharius
- **Dua Lipa × Silk Sonic** — “Fever” [song, 2022] (#5514) — _Fever é com Angèle, não Silk Sonic_  
    ↳ web: Wikipedia: 'Fever' é Dua Lipa feat. Angèle, não Silk Sonic
- **The Weeknd × Madonna** — “Ghosttown” [song, 2015] (#5518) — _Ghosttown da Madonna não traz The Weeknd_  
    ↳ web: Wikipedia: 'Ghosttown' (Madonna, 2015) escrita por Madonna/Evigan/Bogart/Douglas, sem The Weeknd
- **Chris Brown × Khalid** — “Call You Mine” [song, 2019] (#5554) — _Call You Mine é Chainsmokers/Bebe Rexha_  
    ↳ web: Wikipedia: 'Call You Mine' (2019) é The Chainsmokers feat. Bebe Rexha, não Chris Brown/Khalid
- **Christina Aguilera × Nicki Minaj** — “Stupid Hoe (uncredited)” [song, 2012] (#5576) — _Stupid Hoe é solo da Nicki, feature inventada_  
    ↳ web: Wikipedia: 'Stupid Hoe' tem vocal só da Nicki Minaj, sem Christina Aguilera
- **Drake × SZA** — “All the Stars” [song, 2018] (#5637) — _All the Stars é SZA com Kendrick, não Drake_  
    ↳ web: Wikipedia/Spotify: 'All the Stars' (2018) credita Kendrick Lamar e SZA, não Drake
- **Kendrick Lamar × Drake** — “Forever” [song, 2009] (#5645) — _Forever (2009) não inclui Kendrick Lamar_  
    ↳ web: Wikipedia: 'Forever' (2009) é Drake, Kanye West, Lil Wayne e Eminem; sem Kendrick Lamar
- **Anne-Marie × Cardi B** — “Cardi B Anne-Marie Collab” [song, 2021] (#5654) — _título genérico placeholder, sem música real_  
    ↳ web: Billboard/Ranker: Anne-Marie citou Cardi B como sonho de colab, mas nenhuma música lançada juntas; título é placeholder
- **Karol G × Maluma** — “Creep” [song, 2019] (#5703) — _'Creep' não é colaboração Karol G x Maluma_  
    ↳ web: Música real Karol G x Maluma é 'Créeme' (2018), não existe 'Creep' entre eles (en.wikipedia.org)
- **Sebastián Yatra × Camila Cabello** — “Tutu” [song, 2022] (#5707) — _'Tutu' é Camilo/Pedro Capó, não Yatra/Camila_  
    ↳ web: 'Tutu' (2019) é de Camilo e Pedro Capó (remix add Shakira), não Yatra x Camila Cabello (en.wikipedia.org)
- **Harry Styles × Shawn Mendes** — “What a Feeling” [song, 2023] (#5712) — _'What a Feeling' não existe Harry x Shawn Mendes_  
    ↳ web: Não existe 'What a Feeling' Harry Styles x Shawn Mendes; título é faixa do One Direction/Flashdance (harrystyles.fandom/wikipedia)
- **6LACK × Khalid** — “Know Your Worth” [song, 2020] (#5722) — _'Know Your Worth' é Khalid x Disclosure, não 6LACK_  
    ↳ web: 'Know Your Worth' (2020) é Khalid x Disclosure (remix Davido/Tems), não 6LACK; 6LACK está em 'OTW' (en.wikipedia.org)
- **Kelly Clarkson × Jason Derulo** — “Already Gone” [song, 2009] (#5741) — _'Already Gone' é Kelly Clarkson solo, sem Derulo_  
    ↳ web: 'Already Gone' (2009) é solo de Kelly Clarkson coescrita com Ryan Tedder, sem Jason Derulo (en.wikipedia.org)
- **Karol G × Feid** — “Juntos (album)” [album, 2023] (#5860) — _álbum conjunto Karol G e Feid 'Juntos' não existe_  
    ↳ web: Billboard/Letras: não existe álbum conjunto 'Juntos' de Karol G e Feid; colaboraram só em faixas ('Friki','Verano Rosa')
- **Anuel AA × Jhay Cortez** — “Safaera (remix)” [remix, 2020] (#5887) — _Safaera é Bad Bunny, remix com Anuel/Jhay não existe_  
    ↳ web: Spotify: 'Safaera' é de Bad Bunny com Jowell & Randy e Ñengo Flow; remix com Anuel AA/Jhay Cortez não existe
- **Myke Towers × Jhay Cortez** — “Yhlqmdlg (remix)” [remix, 2020] (#5907) — _YHLQMDLG é álbum de Bad Bunny, não remix Myke/Jhay_  
    ↳ web: YHLQMDLG é título do álbum de Bad Bunny (2020), não remix de Myke Towers/Jhay Cortez; faixa inexistente
- **Feid × Bad Bunny** — “Un Verano Sin Ti (feature)” [feature, 2022] (#5918) — _Un Verano Sin Ti é álbum solo Bad Bunny, Feid não participa_  
    ↳ web: Wikipedia/Rolling Stone: tracklist de 'Un Verano Sin Ti' (Bad Bunny) não inclui Feid
- **Sebastián Yatra × Rosalía** — “Cristian Y Rosalía” [song, 2019] (#5923) — _título 'Cristian Y Rosalía' Yatra/Rosalía não existe_  
    ↳ web: Letras/Spotify: não existe faixa 'Cristian Y Rosalía' nem colaboração Yatra/Rosalía; 'Cristina' de Yatra é solo
- **Sebastián Yatra × Myke Towers** — “Cristina” [song, 2020] (#5925) — _'Cristina' Yatra e Myke Towers não existe_  
    ↳ web: Wikipedia/Spotify: a colaboração real Yatra + Myke Towers é 'Pareja del Año' (2021), não 'Cristina'
- **Grupo Frontera × Bad Bunny** — “Un Verano Sin Ti (feature)” [feature, 2022] (#5977) — _'Un Verano Sin Ti' é álbum de Bad Bunny, não feature com Grupo Frontera_  
    ↳ web: 'Un Verano Sin Ti' é álbum de Bad Bunny; convidados são Rauw Alejandro, Chencho, Jhayco etc, não Grupo Frontera (en.wikipedia.org)
- **Young Miko × Bad Bunny** — “Un Verano Sin Ti (feature)” [feature, 2022] (#6025) — _'Un Verano Sin Ti' é álbum de Bad Bunny, não feature com Young Miko_  
    ↳ web: 'Un Verano Sin Ti' (Bad Bunny) não tem Young Miko entre os convidados listados (billboard.com/en.wikipedia.org)
- **Burna Boy × J. Balvin** — “Anybody” [song, 2020] (#6040) — _'Anybody' é single solo de Burna Boy, sem J Balvin_  
    ↳ web: Spotify/OkayAfrica: 'Anybody' é solo de Burna Boy; colab com J Balvin é 'Rollercoaster'
- **Lenny Tavárez × Maluma** — “La Canción” [song, 2019] (#6046) — _'La Canción' é de J Balvin e Bad Bunny, não Lenny Tavárez/Maluma_  
    ↳ web: lahiguera/Billboard: colabs Maluma+Lenny Tavárez são 'Parce'/'Sornero'; 'La Canción' é de J Balvin e Bad Bunny
- **Imagine Dragons × Kendrick Lamar** — “Warriors” [song, 2014] (#6075) — _'Warriors' é solo do Imagine Dragons, sem Kendrick Lamar_  
    ↳ web: Wikipedia: 'Warriors' (2014) é do Imagine Dragons solo p/ League of Legends, sem Kendrick Lamar
- **Aretha Franklin × Stevie Wonder** — “Rock Steady” [feature, 1971] (#6321) — _'Rock Steady' é da própria Aretha; Stevie Wonder não é feature_  
    ↳ web: Wikipedia: 'Rock Steady' é de Aretha Franklin; personnel inclui Donny Hathaway/Purdie/Dr John, sem Stevie Wonder
- **Earth, Wind & Fire × Daft Punk** — “Let's Groove Tonight” [feature, 2013] (#6373) — _'Let's Groove' é de EWF; feature com Daft Punk em 2013 é fabricação_  
    ↳ web: Discogs/YouTube: 'Let's Groove' é single de Earth, Wind & Fire de 1981; não há colaboração oficial com Daft Punk em 2013
- **DJ Khaled × Tinie Tempah** — “Hold You Down” [song, 2014] (#6662) — _Tinie Tempah não consta no elenco de Hold You Down do DJ Khaled_  
    ↳ web: Wikipedia/Spotify: 'Hold You Down' credita Chris Brown, August Alsina, Future e Jeremih, não Tinie Tempah
- **Tiësto × Anne-Marie** — “BOOM!” [song, 2017] (#6671) — _Anne-Marie não consta em BOOM! do Tiësto_  
    ↳ web: Discogs/Spotify: Tiësto 'BOOM' (2017) é com Sevenn (e versão Gucci Mane), não Anne-Marie
- **Gorillaz × Noel Gallagher** — “Fading Like a Flower” [song, 2010] (#6675) — _Fading Like a Flower é dos Roxette; não é faixa Gorillaz x Noel Gallagher_  
    ↳ web: Wikipedia: 'Fading Like a Flower' é dos Roxette; colab Gorillaz x Noel Gallagher é 'We Got the Power'
- **Skepta × Drake** — “Drake x Skepta Together” [song, 2016] (#6724) — _título genérico fabricado 'Drake x Skepta Together'; não é faixa real_  
    ↳ web: Last.fm/Spotify: colabs reais Drake x Skepta são 'Skepta Interlude'/'Ojuelegba Remix'; título 'Drake x Skepta Together' inexistente
- **Dave × Cardi B** — “Funky Friday (Remix)” [remix, 2018] (#6754) — _Cardi B não participa de 'Funky Friday'_  
    ↳ web: 'Funky Friday' é de Dave feat. Fredo (2018), prod. 169; Cardi B não participa (en.wikipedia.org)
- **Metro Boomin × Gunna** — “Drip Too Hard” [song, 2018] (#6812) — _'Drip Too Hard' é Lil Baby & Gunna prod. Turbo, não Metro_  
    ↳ web: 'Drip Too Hard' é de Lil Baby & Gunna, prod. Turbo; Metro Boomin não creditado (en.wikipedia.org)
- **Metro Boomin × Young Thug** — “Drip Too Hard” [song, 2018] (#6813) — _'Drip Too Hard' não é produção Metro×Young Thug_  
    ↳ web: 'Drip Too Hard' é Lil Baby & Gunna prod. Turbo; nem Metro Boomin nem Young Thug participam (en.wikipedia.org)
- **Migos × Drake** — “Motorsport” [song, 2017] (#6833) — _'Motorsport' não tem Drake_  
    ↳ web: 'MotorSport' é Migos feat. Nicki Minaj e Cardi B, sem Drake (en.wikipedia.org)
- **Migos × Lil Baby** — “Motorsport” [song, 2017] (#6834) — _'Motorsport' não tem Lil Baby_  
    ↳ web: 'MotorSport' credita Migos, Nicki Minaj e Cardi B, sem Lil Baby (discogs.com)
- **Quavo × Future** — “Low Life” [song, 2016] (#6839) — _'Low Life' é Future feat. The Weeknd, não Quavo_  
    ↳ web: 'Low Life' (2016) é Future feat. The Weeknd, não Quavo (en.wikipedia.org)
- **Lil Baby × 4pf** — “Forever” [song, 2020] (#6849) — _4pf é gravadora, não artista; pareamento inválido_  
    ↳ web: 'Forever' 2020 (My Turn) de Lil Baby traz Lil Wayne; 4pf é a gravadora, não artista (Wikipedia/Spotify)
- **Young Thug × Wiz Khalifa** — “Lifestyle” [song, 2014] (#6862) — _Lifestyle é Rich Gang/Thug/Rich Homie Quan, não Wiz Khalifa_  
    ↳ web: 'Lifestyle' 2014 é Rich Gang feat. Young Thug & Rich Homie Quan; sem Wiz Khalifa (Wikipedia/Spotify)
- **DJ Khaled × Lil Wayne** — “Every Chance I Get” [song, 2021] (#6889) — _Every Chance I Get tem Lil Baby/Durk, não Lil Wayne_  
    ↳ web: 'Every Chance I Get' 2021 traz Lil Baby & Lil Durk, não Lil Wayne (Wikipedia/Spotify)
- **DJ Khaled × Rick Ross** — “Every Chance I Get” [song, 2021] (#6890) — _Every Chance I Get não tem Rick Ross_  
    ↳ web: 'Every Chance I Get' traz apenas Lil Baby & Lil Durk; sem Rick Ross (Wikipedia/Spotify)
- **DJ Khaled × Post Malone** — “Top Off” [song, 2019] (#6895) — _Top Off tem Jay-Z/Future/Beyoncé, não Post Malone_  
    ↳ web: 'Top Off' traz Jay-Z, Future & Beyoncé; sem Post Malone (Wikipedia/Discogs/Grammy.com)
- **DJ Khaled × Cardi B** — “Top Off” [song, 2019] (#6896) — _Top Off não tem Cardi B_  
    ↳ web: 'Top Off' traz Jay-Z, Future & Beyoncé; sem Cardi B (Wikipedia/Spotify)
- **DJ Khaled × 21 Savage** — “Top Off” [song, 2019] (#6897) — _Top Off não tem 21 Savage_  
    ↳ web: 'Top Off' traz Jay-Z, Future & Beyoncé; sem 21 Savage (Wikipedia/Spotify)
- **DJ Khaled × Nicki Minaj** — “Top Off” [song, 2019] (#6898) — _Top Off não tem Nicki Minaj_  
    ↳ web: 'Top Off' traz Jay-Z, Future & Beyoncé; sem Nicki Minaj (Wikipedia/Spotify)
- **DJ Khaled × Travis Scott** — “Top Off” [song, 2019] (#6899) — _Top Off não tem Travis Scott_  
    ↳ web: 'Top Off' traz Jay-Z, Future & Beyoncé; sem Travis Scott (Wikipedia/Spotify)
- **DJ Khaled × Nicki Minaj** — “Suffering from Success” [song, 2013] (#6900) — _Suffering from Success título de álbum, não tem Nicki nessa faixa-título_  
    ↳ web: Faixa-título 'Suffering from Success' traz Ace Hood & Future, não Nicki Minaj (Wikipedia/hiphopsince1987)
- **DJ Khaled × Jay-Z** — “Higher” [song, 2019] (#6904) — _Higher tem Nipsey Hussle e John Legend, não Jay-Z_  
    ↳ web: 'Higher' 2019 traz Nipsey Hussle & John Legend; sem Jay-Z (Wikipedia/Spotify/NPR)
- **Cardi B × J. Cole** — “Wish Wish” [song, 2019] (#6910) — _Wish Wish não tem J. Cole_  
    ↳ web: 'Wish Wish' é do DJ Khaled feat. Cardi B & 21 Savage, sem J. Cole (Wikipedia/Spotify)
- **Cardi B × Swae Lee** — “Someone Like U” [song, 2019] (#6912) — _título inventado entre Cardi B e Swae Lee_  
    ↳ web: não existe faixa 'Someone Like U' de Cardi B com Swae Lee; nenhuma colaboração entre eles (buscas Spotify/Genius)
- **Megan Thee Stallion × Tyga** — “Freak Nasty” [song, 2019] (#6913) — _Freak Nasty é solo de Megan, não com Tyga_  
    ↳ web: 'Freak Nasty' é solo de Megan Thee Stallion (álbum Tina Snow), sem Tyga (Spotify/IMDb)
- **Megan Thee Stallion × Lil Durk** — “Pressurelicious” [song, 2022] (#6914) — _Pressurelicious é com Future, não Lil Durk_  
    ↳ web: 'Pressurelicious' de Megan é feat. Future, não Lil Durk (Wikipedia/Spotify)
- **Nicki Minaj × Lil Wayne** — “a milli (Remix)” [song, 2010] (#6920) — _A Milli é faixa solo de Lil Wayne_  
    ↳ web: remix oficial de 'A Milli' é o 'Freemix' solo de Lil Wayne, sem Nicki Minaj (Wikipedia)
- **Nicki Minaj × Post Malone** — “Rich Sex” [song, 2018] (#6921) — _Rich Sex de Nicki é com Lil Wayne, não Post Malone_  
    ↳ web: 'Rich Sex' de Nicki Minaj é feat. Lil Wayne, não Post Malone (Wikipedia/Spotify)
- **Jack Harlow × Lil Wayne** — “Nail Tech” [song, 2022] (#6927) — _Nail Tech é single solo de Jack Harlow, sem Lil Wayne_  
    ↳ web: 'Nail Tech' é solo de Jack Harlow; Lil Wayne está em 'Poison', não em Nail Tech (Wikipedia/Variety)
- **Jack Harlow × Justin Timberlake** — “What's Up (Feat. Lil Baby)” [song, 2022] (#6929) — _faixa de Jack Harlow feat Lil Baby, não Justin Timberlake_  
    ↳ web: álbum de Jack Harlow tem 'Parent Trap' feat. Justin Timberlake; não existe 'What's Up feat. Lil Baby' (Rolling Stone/Wikipedia)
- **Jack Harlow × Lil Wayne** — “Common Ground” [song, 2022] (#6930) — _sem faixa 'Common Ground' de Jack Harlow com Lil Wayne_  
    ↳ web: Wikipedia (Jackman): 'Common Ground' é faixa solo de Jack Harlow, álbum sem features; não Lil Wayne
- **Jack Harlow × Lil Baby** — “Common Ground” [song, 2022] (#6931) — _sem faixa 'Common Ground' de Jack Harlow com Lil Baby_  
    ↳ web: Wikipedia (Jackman): 'Common Ground' é solo de Jack Harlow, álbum sem features; não Lil Baby
- **J. Cole × Kendrick Lamar** — “All the Stars (Remix)” [song, 2018] (#6945) — _All the Stars é Kendrick com SZA, sem remix com J. Cole_  
    ↳ web: Wikipedia: 'All the Stars' é Kendrick Lamar × SZA; não há remix oficial com J. Cole
- **J. Cole × Drake** — “All the Stars (Remix)” [song, 2018] (#6946) — _All the Stars não tem remix com Drake_  
    ↳ web: Wikipedia: 'All the Stars' é Kendrick Lamar × SZA; não há remix oficial com Drake
- **ASAP Rocky × Kanye West** — “Phone Home” [song, 2019] (#6952) — _sem faixa 'Phone Home' de ASAP Rocky com Kanye_  
    ↳ web: Wikipedia/YouTube: colab real Rocky+Kanye é 'Jukebox Joints', não existe 'Phone Home'
- **ASAP Rocky × Lil Wayne** — “Electric Body” [song, 2015] (#6954) — _Electric Body não tem Lil Wayne_  
    ↳ web: WhoSampled/Wikipedia: 'Electric Body' feat. ScHoolboy Q, não Lil Wayne
- **Pusha T × Rick Ross** — “Drug Dealers Anonymous” [song, 2016] (#6971) — _Drug Dealers Anonymous é com Jay-Z, não Rick Ross_  
    ↳ web: Wikipedia/Discogs: 'Drug Dealers Anonymous' feat. Jay-Z, não Rick Ross
- **Lil Uzi Vert × Travis Scott** — “No More Parties in LA (Remix)” [song, 2016] (#6994) — _No More Parties in LA é Kanye/Kendrick, sem remix com Lil Uzi_  
    ↳ web: Wikipedia/WhoSampled: 'No More Parties in LA' é Kanye feat. Kendrick; sem remix com Lil Uzi
- **Lil Uzi Vert × 21 Savage** — “No More Parties in LA (Remix)” [song, 2016] (#6995) — _No More Parties in LA sem remix com 21 Savage_  
    ↳ web: Wikipedia: 'No More Parties in LA' é Kanye feat. Kendrick; sem remix com 21 Savage
- **Pop Smoke × Gunna** — “Demeanor” [song, 2020] (#7043) — _Demeanor não tem Gunna, é com Dua Lipa_  
    ↳ web: 'Demeanor' do Pop Smoke é com Dua Lipa, não Gunna (wikipedia/rollingstone)
- **Pop Smoke × Future** — “For the Night” [song, 2020] (#7046) — _For the Night é com Lil Baby e DaBaby, não Future_  
    ↳ web: 'For the Night' do Pop Smoke tem Lil Baby e DaBaby, não Future (wikipedia/songfacts)
- **youngboy_nba × NBA YoungBoy** — “Sincerely, Kentrell” [album, 2021] (#7056) — _mesmo artista duplicado, não é colaboração_  
    ↳ web: 'Sincerely, Kentrell' é álbum solo do NBA YoungBoy sem participações; artistas duplicados (wikipedia)
- **2 Chainz × Travis Scott** — “MFN Right” [song, 2012] (#7068) — _MFN Right não tem Travis Scott; ano errado_  
    ↳ web: 'MFN Right' de 2 Chainz é solo (2016); remix com Lil Wayne, não Travis Scott; ano 2012 errado (discogs/allmusic)
- **Rick Ross × Future** — “Bag of Money” [song, 2012] (#7074) — _Bag of Money não tem Future_  
    ↳ web: 'Bag of Money' é do Wale c/ Rick Ross, Meek Mill e T-Pain; não tem Future (wikipedia/appleMusic)
- **Rick Ross × Drake** — “Bag of Money” [song, 2012] (#7075) — _Bag of Money não tem Drake_  
    ↳ web: 'Bag of Money' (Wale/Rick Ross/Meek Mill/T-Pain) não tem Drake (wikipedia/appleMusic)
- **Mustard × Travis Scott** — “100 Bands” [song, 2019] (#7087) — _100 Bands não inclui Travis Scott_  
    ↳ web: '100 Bands' do Mustard é com Quavo, 21 Savage, YG e Meek Mill; sem Travis Scott (wikipedia/hypebeast)
- **Mike WiLL Made-It × Kendrick Lamar** — “Tequila” [song, 2017] (#7094) — _Humble/Tequila não bate; Tequila não é Mike WiLL/Kendrick_  
    ↳ web: Não existe 'Tequila' de Mike WiLL/Kendrick; colabs deles são Perfect Pint, Humble, DNA (wikipedia/npr)
- **French Montana × Lil Baby** — “Best Believe” [song, 2021] (#7097) — _Best Believe de French é com Drake, não Lil Baby_  
    ↳ web: Não há 'Best Believe' de French Montana; 1ª colab French+Lil Baby foi 'Okay' em 2023 (uproxx/thesource)
- **French Montana × Future** — “Best Believe” [song, 2021] (#7098) — _Best Believe é com Drake, não Future_  
    ↳ web: Não existe 'Best Believe' de French Montana; álbum 2021 é 'They Got Amnesia', sem Future nesse título (hiphopdx/wikipedia)
- **Gucci Mane × Post Malone** — “Pick Up the Phone” [song, 2016] (#7100) — _Pick Up the Phone não tem Post Malone_  
    ↳ web: 'Pick Up the Phone' é de Young Thug e Travis Scott c/ Quavo; não tem Gucci Mane nem Post Malone (grokipedia)
- **Gucci Mane × Big Sean** — “Beamer, Benz, or Bentley” [song, 2010] (#7102) — _Beamer Benz Bentley é Lloyd Banks, não Gucci/Big Sean_  
    ↳ web: 'Beamer, Benz, or Bentley' é de Lloyd Banks feat. Juelz Santana (2010), não Gucci Mane/Big Sean (en.wikipedia.org)
- **DBN Gogo × Kamo Mphela** — “Tshwala Bam” [song, 2023] (#7297) — _Tshwala Bam é de TitoM & Yuppe, não DBN Gogo/Kamo_  
    ↳ web: Wikipedia: 'Tshwala Bam' é de TitoM & Yuppe feat. S.N.E/EeQue, não DBN Gogo/Kamo Mphela
- **Mellow & Sleazy × Kabza De Small** — “John Vuli Gate” [song, 2020] (#7322) — _John Vuli Gate é de Mapara A Jazz, não Mellow&Sleazy/Kabza_  
    ↳ web: AllMusic/Deezer: 'John Vuli Gate' é de Mapara A Jazz feat. Ntosh Gazi & Colano, não Mellow&Sleazy/Kabza
- **Mellow & Sleazy × Focalistic** — “Ke Star 2.0” [song, 2022] (#7324) — _Ke Star é de Focalistic/Vigro Deep, não Mellow&Sleazy_  
    ↳ web: Spotify/Wikipedia: 'Ke Star' é de Focalistic feat. Vigro Deep (remix c/ Davido); não existe 'Ke Star 2.0' c/ Mellow&Sleazy
- **Stino Le Thwenny × Mr JazziQ** — “Club Controller” [song, 2021] (#7355) — _Club Controller é de TimAideo/Lady Du, não Stino/Mr JazziQ_  
    ↳ web: Shazam/Spotify: 'Club Controller' é de Prince Kaybee & LaSoulMates ft TNS/Zanda Zakuza, não Stino/Mr JazziQ
- **TKZee × Mandoza** — “Shibobo” [song, 1999] (#7372) — _Shibobo é só do TKZee, não com Mandoza_  
    ↳ web: Discogs/Wikipedia: 'Shibobo' é de TKZee & Benni McCarthy, não com Mandoza
- **Zola 7 × Mandoza** — “Nkalakatha” [song, 2000] (#7375) — _Nkalakatha é só do Mandoza, não feat. Zola 7_  
    ↳ web: Discogs/Spotify: 'Nkalakatha' (2000) é solo de Mandoza, sem Zola 7
- **Lava Lava × Zuchu** — “Tetema” [song, 2022] (#7396) — _Tetema é de Rayvanny com Diamond, não Lava Lava com Zuchu_  
    ↳ web: Wikipedia/Shazam: 'Tetema' é de Rayvanny feat. Diamond Platnumz; Lava Lava e Zuchu colaboram em 'Cherie' (2025)
- **Aya Nakamura × Gims** — “Pookie” [song, 2019] (#7443) — _Pookie é solo de Aya Nakamura; remix tem Lil Pump, não Gims_  
    ↳ web: Discogs/Qobuz: remixes de 'Pookie' (Aya Nakamura) têm Lil Pump e Capo Plaza, não Gims
- **Aya Nakamura × Tayc** — “Jolie” [song, 2021] (#7444) — _Jolie é colaboração de Tayc, mas par com Aya Nakamura não existe_  
    ↳ web: YouTube/Shazam: colaboração Tayc + Aya Nakamura é 'VA LOIN'; 'Jolie madame' de Tayc é feat. Ronisia, não Aya
- **Vegedream × Aya Nakamura** — “Ramenez la Coupe” [song, 2018] (#7461) — _Ramenez la Coupe à la Maison é solo de Vegedream, sem Aya Nakamura_  
    ↳ web: Wikipedia: 'Ramenez la coupe à la maison' (2018) é single solo de Vegedream, sem Aya Nakamura
- **Sidiki Diabate × Dadju** — “Joli Bébé” [song, 2020] (#7467) — _Joli Bébé é hit solo de Naza, não de Sidiki Diabate com Dadju_  
    ↳ web: Wikipedia/Shazam: 'Joli bébé' (2020) é de Naza e Niska, não Sidiki Diabaté com Dadju
- **Stromae × Black Coffee** — “Quelqu'un M'a Dit Remix” [song, 2022] (#7475) — _Quelqu'un M'a Dit é de Carla Bruni, não Stromae_  
    ↳ web: Spotify/Wikipedia: 'Quelqu'un m'a dit' é canção de Carla Bruni (2002), não de Stromae; sem remix de Black Coffee
- **Khaled × Cheb Mami** — “Aicha” [song, 1996] (#7477) — _Aïcha é solo de Khaled, não feat Cheb Mami_  
    ↳ web: Wikipedia/Discogs: 'Aïcha' (1996) é solo de Khaled (composta por Goldman); Cheb Mami não está na gravação original (só em remix Soolking 2025)
- **Focalistic × Drake** — “Ke Star (Toronto Edit)” [song, 2021] (#7572) — _edição 'Toronto Edit' fabricada, sem feat real Focalistic×Drake_  
    ↳ web: Spotify/TrendyBeatz: 'Ke Star (Remix)' credita Focalistic, Davido e Vigro Deep, não Drake; sem 'Toronto Edit'
- **Brenda Fassie × Arthur Mafokate** — “Vuli Ndlela Remix” [song, 2001] (#7579) — _'Vuli Ndlela' é de Brenda Fassie sozinha, remix com Arthur fabricado_  
    ↳ web: WhoSampled/Discogs: remix de 'Vuli Ndlela' (1998) produzido por Sello Twala; remixes conhecidos são Master KG/Gregor Salto, não Arthur Mafokate
- **Oliver Mtukudzi × Angélique Kidjo** — “Neria Remix” [song, 2008] (#7587) — _'Neria' é de Tuku, remix com Kidjo fabricado_  
    ↳ web: zimlive.com: remix de 'Neria' foi com Ladysmith Black Mambazo, não Angélique Kidjo
- **Justin Bieber × DJ Khaled** — “I Believe” [song, 2018] (#7625) — _'I Believe' não é colaboração documentada Bieber×DJ Khaled_  
    ↳ web: Wikipedia/Grammy: 'I Believe' (2018) é DJ Khaled feat. Demi Lovato, sem Justin Bieber
- **Future × Travis Scott** — “Beibs in the Trap” [song, 2017] (#7656) — _'Beibs in the Trap' tem NAV, não Future_  
    ↳ web: Wikipedia/Spotify: 'Beibs in the Trap' é Travis Scott feat. NAV, não Future
- **Khalid × Swae Lee** — “Know Your Worth” [song, 2020] (#7665) — _'Know Your Worth' remix tem Davido e Tems, não Swae Lee_  
    ↳ web: Wikipedia/Spotify: 'Know Your Worth' é Khalid & Disclosure (remix c/ Davido e Tems), sem Swae Lee
- **DJ Khaled × SZA** — “Higher” [song, 2019] (#7672) — _'Higher' tem Nipsey Hussle e John Legend, não SZA_  
    ↳ web: Wikipedia/Spotify: 'Higher' é DJ Khaled feat. Nipsey Hussle e John Legend, não SZA
- **Jack Harlow × Quavo** — “Way Out” [song, 2021] (#7688) — _'Way Out' de Jack Harlow tem Big Sean, não Quavo_  
    ↳ web: Wikipedia/Spotify: 'Way Out' é Jack Harlow feat. Big Sean, não Quavo
- **Calvin Harris × Pharrell Williams** — “Rollin” [song, 2016] (#7689) — _'Rollin' de Calvin Harris tem Future e Khalid, não Pharrell_  
    ↳ web: Wikipedia/Discogs: 'Rollin' é Calvin Harris feat. Future e Khalid, não Pharrell
- **Juice WRLD × Lil Uzi Vert** — “Feline” [song, 2019] (#7693) — _'Feline' tem Polo G e Trippie Redd, não Lil Uzi Vert_  
    ↳ web: Spotify/Amazon: 'Feline' é Juice WRLD com Polo G e Trippie Redd, não Lil Uzi Vert
- **Ty Dolla $ign × Future** — “Bang” [song, 2018] (#7699) — _colab Ty Dolla/Future/Swae é 'Don't Judge Me', não 'Bang'_  
    ↳ web: Spotify/Discogs: colab Ty Dolla/Future/Swae é 'Don't Judge Me', não existe 'Bang'
- **Ty Dolla $ign × Swae Lee** — “Bang” [song, 2018] (#7700) — _colab Ty Dolla/Swae/Future é 'Don't Judge Me', não 'Bang'_  
    ↳ web: Spotify/Discogs: colab Ty Dolla/Swae/Future é 'Don't Judge Me', não existe 'Bang'
- **Gorillaz × Beck** — “Hollywood” [song, 2018] (#7701) — _'Hollywood' do Gorillaz tem Snoop Dogg, não Beck_  
    ↳ web: Wikipedia/Spotify: 'Hollywood' do Gorillaz é feat. Snoop Dogg e Jamie Principle, não Beck
- **Tierry × Wesley Safadão** — “Só Quer Vrau” [feature, 2018] (#7831) — _'Só Quer Vrau' é de MC MM/DJ RD, não Tierry com Safadão_  
    ↳ web: Cifra Club/letras/Spotify: 'Só Quer Vrau' é de MC MM & DJ RD, não Tierry com Wesley Safadão
- **Aldair Playboy × Garota Safada** — “Piseiro Antigo” [song, 2012] (#7871) — _Aldair Playboy não atuava em 2012; cronologia inconsistente_  
    ↳ web: Wikipedia: Aldair Playboy (nasc.1996) só iniciou carreira em 2017; em 2012 não atuava, colab com Garota Safada impossível
- **Léo Santana × Ivete Sangalo** — “Que Tiro Foi Esse” [feature, 2018] (#7887) — _'Que Tiro Foi Esse' é de Jojo Todynho, não Léo Santana feat Ivete_  
    ↳ web: Wikipedia/LETRAS: 'Que Tiro Foi Esse' é single de Jojo Maronttinni (Todynho) 2017-18, não Léo Santana feat Ivete
- **Ximbinha × Joelma** — “Eletroaxé” [album, 2005] (#7890) — _Ximbinha e Joelma são da Banda Calypso; álbum 'Eletroaxé' inventado_  
    ↳ web: Wikipedia (Discografia Banda Calypso): não existe álbum 'Eletroaxé'; Ximbinha e Joelma são a própria Banda Calypso (gênero calypso, não axé)
- **Ximbinha × Banda Calypso** — “Calypso e Arrocha” [live, 2009] (#7891) — _Ximbinha É da Banda Calypso; colaboração consigo mesmo inventada_  
    ↳ web: Wikipedia/Archive: DVD Banda Calypso de 2009 é '10 Anos Ao Vivo Em Recife', não 'Calypso e Arrocha'; Ximbinha é membro da própria banda
- **Claudia Leitte × Anitta** — “Largadinho” [song, 2013] (#7901) — _'Largadinho' é solo de Claudia Leitte, sem Anitta_  
    ↳ web: Spotify/Discogs: 'Largadinho' (2013) é de Claudia Leitte solo (versão feat. Anselmo Ralph), sem Anitta
- **Rastapé × Luiz Gonzaga** — “Pé de Serra” [live, 2002] (#8035) — _Luiz Gonzaga morreu em 1989, live 2002 impossível_  
    ↳ web: Luiz Gonzaga morreu em 1989 e Rastapé só surgiu em 1999; live conjunta em 2002 impossível, sem registro (pt.wikipedia / letras.mus.br)
- **Jammil × Claudia Leitte** — “Lepo Lepo” [song, 2013] (#8232) — _Lepo Lepo é do Psirico, não Jammil com Claudia Leitte_  
    ↳ web: 'Lepo Lepo' é do Psirico (Márcio Victor), não Jammil com Claudia Leitte (last.fm/spotify)
- **Irmão do Jorel × Clarice Falcão** — “Mundo dos Desenhos” [song, 2015] (#8293) — _Irmão do Jorel é desenho animado, não artista musical_  
    ↳ web: Fandom Irmão do Jorel: músicas do desenho compostas pelos criadores (Furlan/Chico Cuica), sem colaboração com Clarice Falcão nem faixa 'Mundo dos Desenhos'
- **Irmão do Jorel × Anavitória** — “Animação Ao Vivo” [live, 2016] (#8294) — _Irmão do Jorel não é artista musical_  
    ↳ web: Fandom Irmão do Jorel: é desenho animado, não artista; sem colaboração com Anavitória
- **Angra × Sepultura** — “Metal Brasil Festival” [live, 2002] (#8377) — _festival fictício, não é colaboração documentada_  
    ↳ web: evento conjunto Sepultura×Angra foi Carnaval de Salvador em 2016, não 'Metal Brasil Festival' 2002 (Blabbermouth/Ligado à Música)
- **Cartola × Zeca Pagodinho** — “Samba Clássico (Tributo)” [live, 1999] (#8378) — _Cartola morreu em 1980; impossível live 1999_  
    ↳ web: Cartola morreu em 1980; Zeca fez tributo cobrindo Cartola, mas live 1999 com Cartola é impossível (Gazeta do Povo)
- **Lukas Graham (BR) × Anavitória** — “Acoustic Session” [ep, 2019] (#8380) — _'Lukas Graham (BR)' fictício, fabricação_  
    ↳ web: 'Lukas Graham (BR)' inexistente; nenhum EP acústico com Anavitória documentado (Wikipedia Lukas Graham)
- **Lukas Graham (BR) × Jovem Dionisio** — “Pop Novo BR” [song, 2022] (#8382) — _'Lukas Graham (BR)' fictício, fabricação_  
    ↳ web: 'Lukas Graham (BR)' inexistente; nenhuma colab 'Pop Novo BR' com Jovem Dionisio documentada (Wikipedia/CNN Brasil)
- **DJ Snake × -M-** — “Lean On” [song, 2015] (#8384) — _Lean On é Major Lazer/DJ Snake/MØ, não -M-_  
    ↳ web: 'Lean On' (2015) é Major Lazer x DJ Snake feat. MØ, não -M- (Discogs/Wikipedia)
- **Nicky Jam × Becky G** — “Sin Pijama” [song, 2018] (#8406) — _Sin Pijama é Becky G & Natti Natasha, não Nicky Jam_  
    ↳ web: 'Sin Pijama' (2018) é Becky G & Natti Natasha, sem Nicky Jam (Wikipedia/Discogs)
- **Peso Pluma × Bad Bunny** — “Tití Me Preguntó (Remix)” [song, 2023] (#8424) — _Tití Me Preguntó não tem remix com Peso Pluma_  
    ↳ web: Só existem remixes de fãs (SoundCloud/Bandcamp); não há remix oficial de 'Tití Me Preguntó' com Peso Pluma
- **Peso Pluma × Nicki Minaj** — “Teka” [song, 2023] (#8425) — _Teka é Peso Pluma & DJ Snake, não Nicki Minaj_  
    ↳ web: RateYourMusic/Spotify: 'Teka' é DJ Snake & Peso Pluma, não Nicki Minaj
- **G-Dragon × Jennie** — “That XX” [song, 2012] (#8439) — _That XX é solo de G-Dragon, não feat Jennie_  
    ↳ web: Wikipedia: 'That XX' é solo de G-Dragon; Jennie só atua no clipe, não canta
- **Dolly Parton × Whitney Houston** — “I Will Always Love You” [song, 1992] (#8456) — _I Will Always Love You é solo de Whitney, não dueto com Dolly_  
    ↳ web: Wikipedia: versão de 1992 de 'I Will Always Love You' é solo de Whitney; nunca houve dueto com Dolly Parton
- **Kacey Musgraves × Zedd** — “Beautiful Noise” [song, 2022] (#8464) — _Beautiful Noise é de Zedd com Alessia Cara/Khalid, não Musgraves_  
    ↳ web: Wikipedia: não existe 'Beautiful Noise' de Kacey Musgraves x Zedd; Zedd tem 'Beautiful Now' feat. Jon Bellion (2015), sem Musgraves
- **Morgan Wallen × Jason Aldean** — “Up Down” [song, 2017] (#8467) — _Up Down é de Morgan Wallen com Florida Georgia Line, não Jason Aldean_  
    ↳ web: Wikipedia/Spotify: 'Up Down' (2017) é de Morgan Wallen feat. Florida Georgia Line, não Jason Aldean
- **Morgan Wallen × HARDY** — “WASTED ON YOU” [song, 2021] (#8468) — _Wasted on You é solo de Morgan Wallen, sem HARDY_  
    ↳ web: Wikipedia/Billboard: 'Wasted on You' credita Wallen, Vojtesak, Ernest e Josh Thompson, sem HARDY
- **Tim McGraw × Taylor Swift** — “Tim McGraw” [song, 2006] (#8480) — _Tim McGraw é canção de Taylor Swift sobre ele, não dueto_  
    ↳ web: Wikipedia: 'Tim McGraw' é single solo de Taylor Swift (2006) sobre ele, não dueto com Tim McGraw
- **Mano Brown × Criolo** — “Não Existe Amor em SP” [song, 2011] (#8514) — _Não Existe Amor em SP é de Criolo solo (2011), sem Mano Brown_  
    ↳ web: Spotify/Letras: 'Não Existe Amor em SP' é composição solo de Criolo (2011); Mano Brown não consta na faixa
- **MC Livinho × Anitta** — “Funk Rave” [song, 2019] (#8542) — _Funk Rave é de Anitta solo (2023); MC Livinho não é feature_  
    ↳ web: IMDb/Spotify: 'Funk Rave' é solo de Anitta (2023); MC Livinho colabora em outra faixa ('Sem Freio'), não nesta
- **Prince × Beyoncé** — “Why Don't You Love Me” [song, 2012] (#8564) — _música solo da Beyoncé, sem Prince_  
    ↳ web: 'Why Don't You Love Me' é solo de Beyoncé, escrito por Beyoncé/Solange/Beyincé, sem Prince (en.wikipedia.org)
- **Romeo Santos × Nicki Minaj** — “Fútbol y Rumba” [song, 2021] (#8579) — _Fútbol y Rumba é com Anuel AA, não Nicki_  
    ↳ web: 'Fútbol y Rumba' é de Enrique Iglesias com Anuel AA; não é de Romeo Santos nem Nicki Minaj (letras.com)
- **Maiara & Maraisa × Henrique & Juliano** — “Que Tiro Foi Esse (Remix)” [song, 2019] (#8587) — _Que Tiro Foi Esse é da Jojo Maronttinni_  
    ↳ web: 'Que Tiro Foi Esse' é de Jojo Maronttinni; sem remix de Maiara & Maraisa com Henrique & Juliano (letras.mus.br, open.spotify.com)
- **Pitty × Charlie Brown Jr.** — “Pit Bull Meets Charlie” [song, 2005] (#8593) — _título fabricado, sem registro_  
    ↳ web: Nenhum registro de faixa 'Pit Bull Meets Charlie' de Pitty com Charlie Brown Jr.; título inexistente (open.spotify.com)
- **Lauren Daigle × Hillsong United** — “Open Up the Heavens” [song, 2018] (#8651) — _Open Up the Heavens é do Vertical, não Daigle/Hillsong_  
    ↳ web: Spotify/Wikipedia: 'Open Up the Heavens' é do Vertical Worship feat. Andi Rozier & Meredith Andrews, não Daigle/Hillsong
- **TobyMac × Justin Bieber** — “Love Never Fails” [feature, 2012] (#8698) — _TobyMac feat. Justin Bieber inexistente, fabricação_  
    ↳ web: Wikipedia: 'Love Never Fails' é canção do Brandon Heath (2009); colaboração TobyMac feat. Justin Bieber inexistente
- **for KING & COUNTRY × Casting Crowns** — “Proof of Your Love” [song, 2014] (#8711) — _Proof of Your Love é for KING & COUNTRY sozinho, sem Casting Crowns_  
    ↳ web: Wikipedia: 'The Proof of Your Love' é do for KING & COUNTRY (versão feat. Rebecca St. James), sem Casting Crowns
- **Switchfoot × Relient K** — “The Beautiful Letdown” [live, 2004] (#8723) — _The Beautiful Letdown é álbum solo do Switchfoot, sem Relient K_  
    ↳ web: Wikipedia: 'The Beautiful Letdown' (2003) é álbum solo do Switchfoot; Relient K só participou de faixa 'Ammunition' na regravação de 2023, não 2004
- **Jars of Clay × Switchfoot** — “Flood” [live, 2000] (#8734) — _'Flood' é de Jars of Clay; Switchfoot não participa dessa música_  
    ↳ web: Wikipedia: 'Flood' é single de estreia de Jars of Clay (1996); Switchfoot não participa da gravação
- **Paul Baloche × Don Moen** — “Your Grace Is Enough” [live, 2007] (#8749) — _'Your Grace Is Enough' é de Matt Maher/Tomlin, não de Baloche x Moen_  
    ↳ web: umcdiscipleship.org: 'Your Grace Is Enough' foi escrita por Matt Maher; não é composição/gravação de Baloche x Moen
- **Israel Houghton × William McDowell** — “I Give Myself Away” [live, 2013] (#8754) — _'I Give Myself Away' é de William McDowell; Houghton não é coautor dessa_  
    ↳ web: christiantoday: 'I Give Myself Away' é de William McDowell e Sam Hinn; Houghton fez cover mas não é coautor/creditado na faixa de McDowell
- **Mary Mary × Tasha Cobbs Leonard** — “Go Get It” [song, 2013] (#8762) — _'Go Get It' é das Mary Mary; não é colaboração com Tasha Cobbs_  
    ↳ web: Wikipedia/Discogs: single 'Go Get It' é solo das Mary Mary; Tasha Cobbs não é creditada como feature na faixa
- **Marvin Sapp × Fred Hammond** — “Never Would Have Made It” [song, 2007] (#8764) — _'Never Would Have Made It' é de Marvin Sapp; não é colaboração com Fred Hammond_  
    ↳ web: Discogs/CBN: 'Never Would Have Made It' é single solo de Marvin Sapp (2007); Fred Hammond não é feature na música
- **Jekalyn Carr × Tasha Cobbs Leonard** — “Greater Is Coming” [song, 2016] (#8787) — _'Greater Is Coming' é de Jekalyn Carr; não é colaboração com Tasha Cobbs_  
    ↳ web: Wikipedia: 'Greater Is Coming' é single de estreia solo de Jekalyn Carr; Tasha Cobbs não participa dessa faixa
- **Koryn Hawthorne × Lecrae** — “Won't He Do It” [song, 2017] (#8788) — _'Won't He Do It' é de Koryn Hawthorne; não é colaboração com Lecrae_  
    ↳ web: RCA Inspiration/Shazam: 'Won't He Do It' é estreia solo de Koryn Hawthorne (remix c/ Roshon Fegan); Lecrae aparece só em 'Unstoppable' (2019)
- **Propaganda × Sho Baraka** — “Precious Puritans” [song, 2012] (#8808) — _'Precious Puritans' é solo de Propaganda; Sho Baraka não participa_  
    ↳ web: Discogs: em 'Precious Puritans' o feature é Kevin 'K.O.' Olusola (cello); Sho Baraka aparece em outra faixa do álbum, não nessa
- **Mercy Chinwo × Sinach** — “Excess Love” [song, 2019] (#8820) — _Excess Love é de Mercy Chinwo sozinha, não colab com Sinach_  
    ↳ web: Spotify: 'Excess Love' é de Mercy Chinwo solo; versão feat. é JJ Hairston, não Sinach
- **Flyleaf × Skillet** — “All Around Me” [song, 2007] (#8845) — _All Around Me é do Flyleaf sozinho, não colab com Skillet_  
    ↳ web: Wikipedia: 'All Around Me' é do Flyleaf (Lacey Mosley et al.); Skillet apenas turnê, sem crédito
- **Relient K × Switchfoot** — “Sadie Hawkins Dance” [live, 2004] (#8846) — _Sadie Hawkins Dance é do Relient K, não colab com Switchfoot_  
    ↳ web: Spotify/Wikipedia: 'Sadie Hawkins Dance' é do Relient K solo, sem Switchfoot na faixa
- **Twila Paris × Michael W. Smith** — “How Beautiful” [song, 1992] (#8872) — _How Beautiful é de Twila Paris, não colab com Michael W. Smith_  
    ↳ web: Wikipedia (Cry for the Desert): 'How Beautiful' escrita e cantada por Twila Paris solo, sem duet com Michael W. Smith
- **Clairo × Lorde** — “Scene Collaboration” [song, 2021] (#8931) — _título genérico 'Scene Collaboration'; sem colaboração real Clairo×Lorde_  
    ↳ web: Rolling Stone/NME: colabs reais Clairo×Lorde são 'Blouse' e 'Solar Power'; não existe faixa 'Scene Collaboration'
- **beabadoobee × PinkPantheress** — “Indie UK Scene” [song, 2022] (#8936) — _título genérico 'Indie UK Scene'; fabricação_  
    ↳ web: Rolling Stone/Spotify: colab real beabadoobee×PinkPantheress é 'tinkerbell is overrated' (Beatopia 2022), não 'Indie UK Scene'
- **Rex Orange County × Conan Gray** — “Scene Friends Feature” [song, 2020] (#8938) — _título genérico 'Scene Friends Feature'; fabricação_  
    ↳ web: Wikipedia lista de colabs de Conan Gray e Rex Orange County não mostra faixa conjunta; 'Scene Friends Feature' é título genérico inexistente
- **Omar Apollo × Kali Uchis** — “Scene Pairing” [song, 2021] (#8943) — _título genérico 'Scene Pairing'; fabricação_  
    ↳ web: Rolling Stone/FADER: colabs reais Omar Apollo×Kali Uchis são 'Bad Life' e 'Hey Boy', não 'Scene Pairing'
- **Dominic Fike × Lorde** — “Good Days (Feature)” [song, 2021] (#8945) — _'Good Days' é da SZA; feature Dominic Fike×Lorde inexistente_  
    ↳ web: Wikipedia/Billboard: 'Good Days' é da SZA com Jacob Collier no refrão, não Dominic Fike×Lorde
- **Girl in Red × Clairo** — “Teenage Scene” [song, 2020] (#8948) — _título genérico 'Teenage Scene'; fabricação_  
    ↳ web: Nenhum registro de faixa 'Teenage Scene' com Girl in Red e Clairo; só playlists de fãs (Spotify/Fandom)
- **Girl in Red × boygenius** — “Queer Folk Feature” [live, 2022] (#8950) — _título genérico 'Queer Folk Feature'; fabricação_  
    ↳ web: Wikipedia/Rolling Stone: girl in red nunca integrou/gravou com boygenius; não existe 'Queer Folk Feature'
- **Gus Dapperton × beabadoobee** — “Indie Pop Collab” [song, 2021] (#8951) — _título genérico 'Indie Pop Collab'; fabricação_  
    ↳ web: Wikipedia/DIY: colabs de Gus Dapperton são com BENEE/Surf Mesa etc., nenhuma com beabadoobee
- **Bon Iver × Caroline Polachek** — “Bon Iver Collab” [song, 2019] (#8957) — _título genérico 'Bon Iver Collab'; sem colab documentada com Caroline Polachek_  
    ↳ web: Wikipedia/Brooklyn Vegan: sem colab Bon Iver x Caroline Polachek; só ambos no remix album da Charli XCX
- **Sylvan Esso × Wye Oak** — “Electronic Folk Feature” [song, 2018] (#8958) — _título genérico 'Electronic Folk Feature'; fabricação_  
    ↳ web: Exclaim/NPR: colab Sylvan Esso x Wye Oak é 'Echo Mountain Sessions' 2017, não 'Electronic Folk Feature'
- **Sylvan Esso × Flock of Dimes** — “Mountain Sessions” [live, 2019] (#8959) — _título genérico 'Mountain Sessions'; fabricação_  
    ↳ web: Brooklyn Vegan: colab ao vivo com Flock of Dimes é a turnê/álbum 'WITH' (2019), não 'Mountain Sessions'
- **100 gecs × SOPHIE** — “Hyperpop Feature” [song, 2020] (#8961) — _título genérico 'Hyperpop Feature'; fabricação_  
    ↳ web: Wikipedia tracklist 'Tree of Clues' 2020 lista Hannah Diamond/A.G. Cook, não SOPHIE; sem 'Hyperpop Feature'
- **100 gecs × Slayyyter** — “Hyperpop Scene” [song, 2021] (#8964) — _título genérico 'Hyperpop Scene'; fabricação_  
    ↳ web: Album of the Year/Wikipedia: discografia 100 gecs sem faixa com Slayyyter chamada 'Hyperpop Scene'
- **SOPHIE × A. G. Cook** — “Hyperpop Collab” [song, 2018] (#8970) — _título genérico 'Hyperpop Collab'; fabricação_  
    ↳ web: Wikipedia: colab SOPHIE x A.G. Cook é 'Hey QT' (2014, projeto QT), não 'Hyperpop Collab' 2018
- **SOPHIE × Hannah Diamond** — “PC Music Feature” [song, 2015] (#8972) — _título genérico 'PC Music Feature'; fabricação_  
    ↳ web: Wikipedia/Face: faixa SOPHIE+Hannah Diamond é 'Paradise' (Charli XCX, 2016); não existe 'PC Music Feature' 2015
- **A. G. Cook × Slayyyter** — “Hyperpop Feature” [song, 2021] (#8974) — _título genérico 'Hyperpop Feature'; fabricação_  
    ↳ web: Last.fm/Beatport: A.G. Cook fez remix de 'Click' da Slayyyter, sem faixa creditada 'Hyperpop Feature'
- **Japanese Breakfast × Sufjan Stevens** — “Folk Pop Scene” [live, 2021] (#8982) — _título genérico 'Folk Pop Scene'; fabricação_  
    ↳ web: Japanese Breakfast so fez cover de 'Romulus' de Sufjan em 2021, nao show conjunto 'Folk Pop Scene' (consequence.net)
- **Snail Mail × Soccer Mommy** — “Indie Rock Feature” [song, 2020] (#8984) — _título genérico 'Indie Rock Feature'; fabricação_  
    ↳ web: Colaboracao real foi cover de 'Iris' do Goo Goo Dolls ao vivo, nao musica 'Indie Rock Feature' (stereogum.com)
- **Soccer Mommy × Jay Som** — “Bedroom Pop Collab” [song, 2019] (#8986) — _título genérico 'Bedroom Pop Collab'; fabricação_  
    ↳ web: Soccer Mommy e Jay Som trocaram covers na Singles Series, nao musica 'Bedroom Pop Collab' (exclaim.ca)
- **Mitski × Sharon Van Etten** — “Always Forever” [song, 2019] (#8988) — _'Always Forever' não é dueto Mitski×Sharon Van Etten; fabricação_  
    ↳ web: 'Always Forever' e de Cults/Bryson Tiller/Romy, nao dueto Mitski x Sharon Van Etten (wikipedia.org)
- **Angel Olsen × Sharon Van Etten** — “Lark (Remix)” [song, 2021] (#8995) — _'Lark' é da Angel Olsen; remix com Sharon Van Etten inexistente_  
    ↳ web: 'Lark' e solo da Angel Olsen; colab real com SVE e 'Like I Used To', remix inexistente (rollingstone.com)
- **Lorde × Bon Iver** — “Liability (Feature)” [song, 2017] (#9117) — _'Liability' é solo da Lorde, não feature do Bon Iver_  
    ↳ web: Wikipedia: 'Liability' (Melodrama) é faixa solo da Lorde, sem feat. de Bon Iver
- **Rels B × Quevedo** — “Safaera” [song, 2022] (#9291) — _'Safaera' é de Bad Bunny/Jowell&Randy, não Rels B/Quevedo_  
    ↳ web: Wikipedia: 'Safaera' é de Bad Bunny com Jowell & Randy e Ñengo Flow, não Rels B/Quevedo
- **Rels B × Recycled J** — “Con Calma” [song, 2020] (#9293) — _'Con Calma' é de Daddy Yankee/Snow, não Rels B/Recycled J_  
    ↳ web: Wikipedia/Discogs: 'Con Calma' é de Daddy Yankee feat. Snow, não Rels B/Recycled J
- **Feid × Justin Quiles** — “Yandel 150” [song, 2023] (#9299) — _'Yandel 150' é de Yandel/Feid, não Feid/Justin Quiles_  
    ↳ web: Wikipedia: 'Yandel 150' credita Yandel e Feid (remix c/ Daddy Yankee), não Justin Quiles
- **Peso Pluma × Ke Personajes** — “El Tóxico” [song, 2023] (#9308) — _'El Tóxico' é de Grupo Firme; não Peso Pluma/Ke Personajes_  
    ↳ web: Spotify/IMDb: 'El Tóxico' é de Grupo Firme feat. Carín León, não Peso Pluma/Ke Personajes
- **Peso Pluma × Marca MP** — “Grupo Firme y Peso” [song, 2023] (#9311) — _título fabricado 'Grupo Firme y Peso', não é faixa real_  
    ↳ web: Nenhuma faixa 'Grupo Firme y Peso' de Peso Pluma/Marca MP encontrada; título fabricado (letras.com/Spotify)
- **Natanael Cano × Junior H** — “Con Altura” [song, 2021] (#9312) — _'Con Altura' é de Rosalía/J Balvin, não Natanael/Junior H_  
    ↳ web: Wikipedia: 'Con Altura' é de Rosalía, J Balvin e El Guincho, não Natanael Cano/Junior H
- **Natanael Cano × Ke Personajes** — “El Color de Tus Ojos” [song, 2022] (#9314) — _'El Color de Tus Ojos' é de Banda MS; não Natanael/Ke Personajes_  
    ↳ web: Wikipedia: 'El Color de Tus Ojos' é de Octubre Doce/Banda MS (versão c/ Natalia Jiménez), não Natanael/Ke Personajes
- **Rauw Alejandro × Farruko** — “La Nota” [song, 2021] (#9346) — _'La Nota' é de Manuel Turizo/Rauw/Myke; não Rauw/Farruko_  
    ↳ web: Wikipedia: 'La Nota' é de Manuel Turizo, Rauw Alejandro e Myke Towers, não Farruko
- **Lunay × Sech** — “Soltera” [song, 2019] (#9348) — _'Soltera' é de Lunay/Daddy Yankee/Bad Bunny, não Lunay/Sech_  
    ↳ web: Spotify/letras.com: 'Soltera (Remix)' é de Lunay, Daddy Yankee e Bad Bunny, não Sech
- **Lunay × Dalex** — “Cuatro Babys” [song, 2019] (#9349) — _'Cuatro Babys' é de Maluma, não Lunay/Dalex_  
    ↳ web: Wikipedia: 'Cuatro Babys' é de Maluma feat. Noriel, Bryant Myers e Juhn, não Lunay/Dalex
- **Dalex × Lenny Tavárez** — “Adán y Eva” [song, 2019] (#9353) — _'Adán y Eva' é de Paulo Londra, não Dalex/Lenny Tavárez_  
    ↳ web: Wikipedia: 'Adán y Eva' é solo de Paulo Londra, não Dalex/Lenny Tavárez
- **Sebastián Yatra × Camilo** — “Tutu” [song, 2019] (#9424) — _'Tutu' é Camilo & Pedro Capó (e Shakira remix), não Yatra_  
    ↳ web: Spotify/Wikipedia: 'Tutu' é Camilo & Pedro Capó (remix Shakira), não Yatra
- **Arcángel × Jhay Cortez** — “Mamiii” [song, 2022] (#9484) — _Mamiii é de Becky G e Karol G, não Arcángel e Jhay Cortez_  
    ↳ web: Wikipedia/Spotify: 'Mamiii' (2022) é de Becky G & Karol G, não Arcángel e Jhay Cortez
- **Villano Antillano × Bad Bunny** — “Quevedo Remix” [song, 2022] (#9640) — _Quevedo Remix não existe entre Villano e Bad Bunny_  
    ↳ web: Colab de Villano Antillano é BZRP Sessions #51 com Bizarrap; 'Quevedo Remix' com Bad Bunny não existe
- **Manuel Turizo × Karol G** — “El Makinon” [song, 2022] (#9644) — _El Makinon é Karol G/Mariah Angeliq, não Turizo_  
    ↳ web: Wikipedia/Spotify: 'El Makinón' é de KAROL G e Mariah Angeliq, não Manuel Turizo
- **Mora × Anuel AA** — “Secreto” [song, 2021] (#9646) — _Secreto é de Anuel/Karol G, não Mora_  
    ↳ web: Discogs/Spotify: 'Secreto' é de Anuel AA e KAROL G, não Mora
- **Lunay × Anuel AA** — “Adán y Eva” [song, 2019] (#9647) — _Adán y Eva é de Paulo Londra, não Lunay/Anuel_  
    ↳ web: Wikipedia: 'Adán y Eva' é solo de Paulo Londra, não Lunay/Anuel
- **Plan B × Nicky Jam** — “Algo Me Gusta de Ti” [song, 2018] (#9659) — _Algo Me Gusta de Ti é Wisin & Yandel, não Plan B/Nicky_  
    ↳ web: Wikipedia/Spotify: 'Algo Me Gusta de Ti' é de Wisin & Yandel feat. Chris Brown e T-Pain, não Plan B/Nicky Jam
- **Paulo FG × Lasso** — “La Vida Es Buena” [song, 2022] (#9673) — _título genérico, colaboração improvável_  
    ↳ web: 'La Vida Es Buena' conhecida é de Descemer Bueno feat. Issac Delgado, não Paulo FG+Lasso (letras.com/spotify)
- **Taburete × Carlos Rivera** — “Valerie” [song, 2023] (#9675) — _Valerie não é canção de Taburete/Carlos Rivera_  
    ↳ web: 'Valerie' é canção famosa de The Zutons/Amy Winehouse; sem versão Taburete+Carlos Rivera (letras.com)
- **Amr Diab × Tarkan** — “Tamally Maak” [song, 2001] (#9682) — _Tamally Maak é solo de Amr Diab, não dueto com Tarkan_  
    ↳ web: Wikipedia: 'Tamally Maak' é solo de Amr Diab (2000), não dueto com Tarkan
- **Balti × Flenn** — “Ya Lili” [song, 2017] (#9702) — _Ya Lili é Balti feat. Hamouda, não Flenn_  
    ↳ web: 'Ya Lili' credita Balti feat. Hamouda, não Flenn (Wikipedia/Spotify/IMDb)
- **Static & Ben El × DJ Snake** — “Taki Taki Remix” [song, 2019] (#9728) — _Taki Taki é Selena/Cardi/Ozuna, não Static & Ben El_  
    ↳ web: Wikipedia/Spotify: 'Taki Taki' é DJ Snake feat. Selena, Ozuna, Cardi B; sem Static & Ben El
- **Kathem Al Saher × Kadim Al Saher** — “Sotak Aghla” [song, 2007] (#9744) — _Kathem e Kadim Al Saher são o mesmo artista_  
    ↳ web: Wikipedia/Encyclopedia: Kathem e Kadim Al Saher são o mesmo artista (transliterações de Kazem Al-Saher)
- **Cheb Khaled × Saad Lamjarred** — “Maghrebi Spirit” [song, 2017] (#9758) — _título fabricado tipo 'Maghrebi Spirit'_  
    ↳ web: Spotify/Amazon: colab real Khaled x Saad Lamjarred é 'Aicha'; título 'Maghrebi Spirit' não existe
- **Rachid Taha × Cheb Akil** — “Rock El Casbah” [song, 2004] (#9761) — _Rock El Casbah é de Rachid Taha solo, dueto fabricado_  
    ↳ web: Discogs/SecondHandSongs: 'Rock El Casbah' (2004) é single solo de Rachid Taha (cover do Clash), sem Cheb Akil
- **Noa Kirel × Netta Barzilai** — “Israel Power” [song, 2021] (#9783) — _título fabricado 'Israel Power'_  
    ↳ web: Jerusalem Post/Times of Israel: Kirel e Netta só fizeram remix viral de 'Unicorn/Toy' no Eurovision 2023; faixa 'Israel Power' inexistente
- **Infected Mushroom × Marshmello** — “Saeed EDM” [song, 2019] (#9797) — _título fabricado 'Saeed EDM' Infected x Marshmello_  
    ↳ web: Spotify/Wikipedia: 'Saeed' é faixa solo do Infected Mushroom (álbum 2009 Black Shawarma), sem Marshmello
- **Shahram Nazeri × Ebi** — “Persian Heritage” [song, 2009] (#9924) — _título 'Persian Heritage' descritivo fabricado_  
    ↳ web: Shahram Nazeri e Ebi colaboraram em 'Royay e Ma'/'A Dream' (2012), não em 'Persian Heritage' (Wikipedia)
- **French Montana × Massari** — “All The Way Up Arabic” [song, 2016] (#9933) — _'All The Way Up Arabic' fabricação de remix_  
    ↳ web: Colaboração real French Montana+Massari é remix de 'Nour El Ein' (2019); 'All The Way Up' é de Fat Joe/Remy Ma (thenationalnews/Spotify)
- **DJ Snake × Marshmello** — “Taki Taki” [song, 2018] (#9934) — _Taki Taki é DJ Snake feat Selena/Ozuna/Cardi, não Marshmello_  
    ↳ web: 'Taki Taki' credita DJ Snake ft. Selena Gomez, Ozuna e Cardi B; Marshmello não consta (Discogs/IMDb)
- **Marshmello × Massari** — “Happier Nights” [song, 2019] (#9935) — _'Happier Nights' fabricação, par improvável_  
    ↳ web: 'Happier' é de Marshmello ft. Bastille; não existe 'Happier Nights' com Massari (Wikipedia/Spotify)
- **Gims × Balti** — “Ya Lili Remix” [song, 2018] (#9941) — _'Ya Lili Remix' atribuição fabricada_  
    ↳ web: 'Ya Lili' é de Balti ft. Hamouda; remixes por Cyril M etc., não por Gims (Spotify/musicme)
- **Gal Gadot × Noa Kirel** — “Israeli Icons” [song, 2017] (#9950) — _Gal Gadot é atriz, não cantora; título fabricado_  
    ↳ web: Wikipedia: Gal Gadot é atriz, não cantora; nenhum song 'Israeli Icons' com Noa Kirel
- **Gal Gadot × Dana International** — “Wonder Woman Collab” [song, 2018] (#9951) — _'Wonder Woman Collab' fabricação óbvia_  
    ↳ web: IMDb soundtrack: trilha de Wonder Woman é instrumental (Gregson-Williams); sem 'Wonder Woman Collab' Gadot/Dana International
- **Hayedeh × Googoosh** — “Zan Iran Classic” [song, 2001] (#9952) — _Hayedeh faleceu 1990; data e título impossíveis_  
    ↳ web: Spotify/Wikipedia: Hayedeh faleceu em 1990; ano 2001 impossível; sem dueto real 'Zan Iran Classic'
- **Hayedeh × Dariush** — “Golha” [song, 1999] (#9953) — _Hayedeh faleceu 1990; ano 1999 impossível_  
    ↳ web: Last.fm: 'Golha' era programa de rádio de Hayedeh, não dueto com Dariush; ela morreu em 1990 (ano 1999 impossível)
- **Noa Kirel × Shiri Maimon** — “Israeli Stars” [song, 2021] (#9967) — _título 'Israeli Stars' descritivo fabricado_  
    ↳ web: Last.fm/Crownnote: colab real Kirel/Maimon é 'היא בדיוק כמוני', não 'Israeli Stars'
- **Netta Barzilai × Omer Adam** — “Israeli Pride” [song, 2020] (#9970) — _título 'Israeli Pride' descritivo fabricado_  
    ↳ web: Apple Music/Wikipedia: dueto real Netta/Omer Adam é 'Beg' (2019), não 'Israeli Pride'
- **Fairuz × Fayrouz** — “Lebanese Classics” [album, 2003] (#9975) — _Fairuz e Fayrouz são a mesma artista_  
    ↳ web: Fairuz e Fayrouz são a mesma artista (transliterações); álbum-colaboração impossível (en.wikipedia)
- **Fayrouz × Wael Kfoury** — “Liban El Akhdar” [song, 2006] (#9977) — _Fayrouz=Fairuz, dueto improvável; título fabricado_  
    ↳ web: 'Lebnan El Akhdar' é solo de Fairuz, escrito pelos Rahbani, não dueto com Wael Kfoury (youtube/hibamusic)
- **Khaled × Cheb Khaled** — “Didi Extended” [song, 2000] (#9978) — _Khaled e Cheb Khaled são o mesmo artista_  
    ↳ web: Khaled = Cheb Khaled (mesmo artista); 'Didi' é solo dele de 1992 (en.wikipedia Didi song)
- **Ofra Haza × Idan Raichel** — “Im Nin Alu” [song, 2001] (#9984) — _'Im Nin Alu' é solo de Ofra Haza, não dueto com Idan Raichel_  
    ↳ web: 'Im Nin'alu' é solo de Ofra Haza; sem gravação com Idan Raichel; Haza morreu em 2000 (en.wikipedia Im Nin'alu/Ofra Haza)
- **Arik Einstein × Yehuda Poliker** — “Israel Forever” [song, 2005] (#9992) — _título patriótico genérico improvável; não existe_  
    ↳ web: Nenhuma música 'Israel Forever' de Arik Einstein/Yehuda Poliker nas discografias (en.wikipedia Arik Einstein discography)
- **Arik Einstein × Achinoam Nini** — “Hebrew Songs” [album, 2007] (#9993) — _álbum genérico inventado entre os dois_  
    ↳ web: Álbum de Arik Einstein em 2007 foi 'Kol Hatov Shebaolam' com Guy Bukati (en.wikipedia); não 'Hebrew Songs' com Achinoam Nini
- **Zara Larsson × Tiësto** — “So Good” [song, 2018] (#9998) — _'So Good' é com Ty Dolla $ign, não Tiësto_  
    ↳ web: 'So Good' da Zara Larsson (2017) tem feat. Ty Dolla $ign (en.wikipedia/discogs), não Tiësto
- **Inna × David Guetta** — “Sun Is Up” [song, 2010] (#10047) — _'Sun Is Up' é solo da Inna, não com Guetta_  
    ↳ web: 'Sun Is Up' é single solo da Inna escrito por Play & Win, sem David Guetta (wikipedia/discogs)
- **Helena Paparizou × Sakis Rouvas** — “Greece Eurovision” [live, 2008] (#10071) — _título de show genérico fabricado_  
    ↳ web: Grécia no Eurovision 2008 foi Kalomira 'Secret Combination', não Paparizou+Rouvas; duo real deles só em 2020 (wikipedia/eurovisionworld)
- **Helena Paparizou × Sarbel** — “Eurovision Greece 2007” [live, 2007] (#10075) — _título de show genérico fabricado_  
    ↳ web: Eurovision 2007 foi de Sarbel ('Yassou Maria'); Paparizou só convidada, sem gravação em dupla (wikipedia.org)
- **Helena Paparizou × Demy** — “Greece Eurovision 2017” [live, 2017] (#10076) — _título de show genérico fabricado_  
    ↳ web: Demy representou a Grécia em 2017 sozinha; não há dueto/gravação Paparizou x Demy (wikipedia.org, esctoday.com)
- **Kayah × Brodka** — “Polish Women” [live, 2018] (#10172) — _título descritivo 'Polish Women', não é música real_  
    ↳ web: Nenhum dueto Kayah/Brodka; título 'Polish Women' não existe como gravação (en.wikipedia.org, spotify)
- **Brodka × Organek** — “Polish Alt Rock” [live, 2017] (#10174) — _título descritivo 'Polish Alt Rock', fabricado_  
    ↳ web: Brodka e Organek gravaram juntos em Męskie Granie 2017, mas a faixa é 'Nieboskłon'; não existe track 'Polish Alt Rock' (open.spotify.com, wirtualnemedia.pl)
- **Organek × Mrozu** — “Polskie Radio Session” [song, 2018] (#10175) — _título descritivo 'Polskie Radio Session', fabricado_  
    ↳ web: Sem evidência de gravação Organek/Mrozu intitulada 'Polskie Radio Session' (spotify, wikipedia)
- **Mrozu × Ralph Kaminski** — “Pop Alternatywa” [song, 2022] (#10177) — _título descritivo 'Pop Alternatywa', fabricado_  
    ↳ web: Sem registro de colaboração Mrozu/Ralph Kaminski chamada 'Pop Alternatywa' (spotify, en.wikipedia.org)
- **Margaret × Blanka** — “Polish Pop Girls” [song, 2023] (#10178) — _título descritivo 'Polish Pop Girls', fabricado_  
    ↳ web: Nenhuma música 'Polish Pop Girls' de Margaret/Blanka; discografias não a listam (en.wikipedia.org)
- **Margaret × Roksana Węgiel** — “Pop Power” [song, 2022] (#10179) — _título descritivo 'Pop Power', fabricado_  
    ↳ web: Sem faixa 'Pop Power' de Margaret/Roksana Węgiel nas discografias (music.apple.com, wikipedia)
- **Margaret × Doda** — “Polskie Ikony” [live, 2017] (#10180) — _título descritivo 'Polskie Ikony', fabricado_  
    ↳ web: Nenhuma gravação 'Polskie Ikony' de Margaret/Doda; só menções a eventos conjuntos (en.wikipedia.org)
- **Blanka × Ochman** — “Eurovision Poland” [live, 2023] (#10181) — _título descritivo 'Eurovision Poland', fabricado_  
    ↳ web: Blanka e Ochman foram entradas Eurovision separadas (2023 e 2022); não há dueto 'Eurovision Poland' (en.wikipedia.org, eurovision.com)
- **Blanka × Viki Gabor** — “Young Polish Pop” [song, 2022] (#10182) — _título descritivo 'Young Polish Pop', fabricado_  
    ↳ web: Sem faixa 'Young Polish Pop' de Blanka/Viki Gabor nas discografias (en.wikipedia.org)
- **Ochman × Roksana Węgiel** — “Polish Stars” [song, 2022] (#10183) — _título descritivo 'Polish Stars', fabricado_  
    ↳ web: Ochman e Roksana Węgiel foram atos de intervalo na Eurovision 2023, mas não existe faixa 'Polish Stars' (en.wikipedia.org)
- **Viki Gabor × Roksana Węgiel** — “Polskie Eurovision” [live, 2021] (#10184) — _título descritivo 'Polskie Eurovision', fabricado_  
    ↳ web: Viki Gabor e Roksana Węgiel cantaram 'Arcade' juntas no Junior Eurovision 2020; não há track 'Polskie Eurovision' (en.wikipedia.org, wprost.pl)
- **Sokół × Pezet** — “Klasyczne Brzmienia” [album, 2010] (#10194) — _álbum 'Klasyczne Brzmienia' inexistente entre os dois_  
    ↳ web: Álbum conjunto Sokół/Pezet foi anunciado/especulado por anos mas nunca lançado; 'Klasyczne Brzmienia' 2010 inexistente (glamrap.pl / cgm.pl)
- **Quebonafide × Mata** — “Polish Hip-Hop Session” [song, 2020] (#10198) — _título descritivo 'Polish Hip-Hop Session', fabricado_  
    ↳ web: Nenhum tema 'Polish Hip-Hop Session' de Quebonafide+Mata; discografias bem documentadas não o listam (en.wikipedia.org/Quebonafide, spotify)
- **Mata × Otsochodzi** — “Ulica Polska” [song, 2022] (#10201) — _título descritivo 'Ulica Polska', fabricado_  
    ↳ web: Nenhum 'Ulica Polska' de Mata+Otsochodzi; buscas em tekstowo.pl e last.fm não retornam a faixa
- **Otsochodzi × Lil Masti** — “Trap Polska” [song, 2021] (#10203) — _título descritivo 'Trap Polska', fabricado_  
    ↳ web: Nenhum 'Trap Polska' de Otsochodzi+Lil Masti; buscas em tekstowo.pl e spotify não retornam tal faixa
- **Alina Pash × Jamala** — “Ukrainian Queens” [song, 2022] (#10204) — _título descritivo 'Ukrainian Queens', fabricado_  
    ↳ web: Nenhum 'Ukrainian Queens' Alina Pash+Jamala; existe 'Ukrainian Girls' só de Alina Pash (spotify, en.wikipedia.org)
- **Alina Pash × Kalush Orchestra** — “Ukrainian Style” [song, 2022] (#10205) — _título descritivo 'Ukrainian Style', fabricado_  
    ↳ web: Nenhuma colaboração 'Ukrainian Style' Alina Pash+Kalush Orchestra; foram rivais no Vidbir 2022 (en.wikipedia.org, eurovisionworld.com)
- **Jamala × Ruslana** — “Ukraine Eurovision Legend” [live, 2016] (#10208) — _título descritivo 'Ukraine Eurovision Legend', fabricado_  
    ↳ web: Sem performance conjunta 'Ukraine Eurovision Legend' Jamala+Ruslana em 2016; Ruslana só apresentou o sorteio (en.wikipedia.org/Ukraine_ESC_2016)
- **Jamala × Tina Karol** — “Ukraine Night” [song, 2019] (#10210) — _título descritivo 'Ukraine Night', fabricado_  
    ↳ web: Nenhuma música 'Ukraine Night' Jamala+Tina Karol 2019; discografias não a listam (en.wikipedia.org/Jamala, Tina_Karol)
- **Onuka × Go_A** — “Ukrainian Electronic” [song, 2021] (#10213) — _título descritivo 'Ukrainian Electronic', fabricado_  
    ↳ web: Nenhuma faixa 'Ukrainian Electronic' Onuka+Go_A 2021; álbum KOLIR da Onuka não a inclui (en.wikipedia.org/Onuka, onuka.ua)
- **MELOVIN × Go_A** — “Eurovision Ukraine” [live, 2019] (#10221) — _título descritivo 'Eurovision Ukraine', fabricado_  
    ↳ web: Ucrânia não participou do Eurovision 2019 e Go_A só venceu seleção em 2020; live conjunta impossível (wikipedia/eurovoix)
- **Dima Bilan × Philipp Kirkorov** — “Russia My Country” [live, 2009] (#10233) — _título descritivo 'Russia My Country', fabricado_  
    ↳ web: a música real 'Россия' é de Kirkorov com Masha Rasputina; sem dueto lançado Bilan+Kirkorov (search/ru.wikipedia)
- **Dima Bilan × t.A.T.u.** — “Russian Legends” [live, 2010] (#10234) — _título descritivo 'Russian Legends', fabricado_  
    ↳ web: não existe faixa 'Russian Legends'; Bilan colaborou com Yulia Volkova (t.A.T.u.) em 'Back to Her Future' (en.wikipedia.org)
- **Dima Bilan × Polina Gagarina** — “Russian Eurovision Duo” [live, 2015] (#10235) — _título descritivo 'Russian Eurovision Duo', fabricado_  
    ↳ web: dueto real Bilan/Gagarina é 'Души'/'Dushi', título 'Russian Eurovision Duo' inexistente (music.apple.com, esccovers.com)
- **Philipp Kirkorov × Alsou** — “Estrada Rossii” [live, 2008] (#10236) — _título descritivo 'Estrada Rossii', fabricado_  
    ↳ web: 'Estrada Rossii' é gênero, não faixa; dueto real de Alsou é 'Дуэт' com A. Shevchenko, nenhum registro com Kirkorov (zvuk.com)
- **Philipp Kirkorov × Dimash Kudaibergen** — “Voice of Kazakhstan Russia” [song, 2019] (#10237) — _título descritivo 'Voice of Kazakhstan Russia', fabricado_  
    ↳ web: apenas jams informais em shows de Krutoy, sem dueto oficial 'Voice of Kazakhstan Russia' (en.dimashnews.com)
- **Artik & Asti × NILETTO** — “Russian Pop Collab” [song, 2021] (#10241) — _título descritivo 'Russian Pop Collab', fabricado_  
    ↳ web: colab real Artik&Asti/NILETTO é 'Худи' (2024, c/ GeeGun); 'Russian Pop Collab' inexistente (music.apple.com)
- **Jony × Egor Kreed** — “Modern Russian Pop” [song, 2021] (#10244) — _título descritivo 'Modern Russian Pop', fabricado_  
    ↳ web: colab real Jony/Egor Kreed é 'Дым'/'Smoke' (2024); 'Modern Russian Pop' inexistente (music.apple.com, tophit.com)
- **Monetochka × Bi-2** — “Russian Indie” [live, 2020] (#10253) — _título descritivo 'Russian Indie', fabricado_  
    ↳ web: Colab real Monetochka x Bi-2 é 'Нити ДНК/DNA Threads' (2018) e 'Мой рок-н-ролл', não 'Russian Indie' (wikipedia/allmusic)
- **Bi-2 × Kino** — “Russian Rock Legends” [live, 2010] (#10255) — _Kino dissolvido em 1990, colaboração impossível em 2010_  
    ↳ web: Kino dissolveu em 1990 após morte de Viktor Tsoi; live com Bi-2 em 2010 impossível (en.wikipedia.org)
- **Kino × Ariya** — “Soviet Rock” [live, 2005] (#10256) — _Kino acabou em 1990, live 2005 impossível_  
    ↳ web: Kino terminou em 1990 após morte de Tsoi; colaboração live 2005 com Ariya impossível (en.wikipedia.org)
- **Keisya Levronka × Tiara Andini** — “Akad” [song, 2022] (#10441) — _'Akad' é música do Payung Teduh, não colaboração Keisya/Tiara_  
    ↳ web: 'Akad' é do Payung Teduh; colabs Keisya/Tiara são 'Cantik' e '365', não 'Akad' (youtube.com/tiktok.com)
- **Fourtwnty × Nadin Amizah** — “Zona Nyaman” [song, 2021] (#10449) — _'Zona Nyaman' é música solo do Fourtwnty, não colab com Nadin_  
    ↳ web: 'Zona Nyaman' é faixa solo do Fourtwnty (OST Filosofi Kopi 2), sem Nadin Amizah (kapanlagi.com/eventori.id)
- **Payung Teduh × Kunto Aji** — “Resah” [song, 2017] (#10453) — _'Resah' é música solo do Payung Teduh, não colab com Kunto Aji_  
    ↳ web: 'Resah' é música solo do Payung Teduh (2010); Kunto Aji só colaborou no álbum de 2019, não nessa faixa (tempo.co/liputan6.com)
- **Armand Maulana × Gigi** — “Naif” [song, 2002] (#10465) — _'Naif' é nome de banda, não música Armand/Gigi_  
    ↳ web: 'Naif' é nome de banda indonésia (id.wikipedia.org Naif grup musik), não há música 'Naif' de Armand Maulana/Gigi
- **Milli × Phum Viphurit** — “Mango Sticky Rice” [song, 2022] (#10476) — _'Mango Sticky Rice' é solo da Milli (Coachella), não colab com Phum_  
    ↳ web: 'Mango Sticky Rice' é single solo da MILLI, 2022 (open.spotify.com/tpop.fandom); sem Phum Viphurit
- **Sơn Tùng M-TP × Đen Vâu** — “Chạy Ngay Đi” [feature, 2020] (#10503) — _'Chạy Ngay Đi' é solo do Sơn Tùng M-TP, não feature com Đen Vâu_  
    ↳ web: 'Chạy Ngay Đi' é single solo de Sơn Tùng M-TP com atriz Davika no MV (open.spotify.com); sem Đen Vâu
- **Karik × Rhymastic** — “Việt Nam Tôi Đâu” [song, 2017] (#10508) — _'Việt Nam Tôi Đâu' é música do Việt Khang, não Karik/Rhymastic_  
    ↳ web: 'Việt Nam Tôi Đâu' é música de Việt Khang (antiwarsongs.org/loibaihatviet), não de Karik/Rhymastic
- **Rhymastic × Binz** — “Người Lạ Ơi” [song, 2017] (#10509) — _'Người Lạ Ơi' é de Karik & Orange/Superbrothers, não Rhymastic/Binz_  
    ↳ web: 'Người Lạ Ơi' credita Karik, Orange e Superbrothers (nhac.vn/zingmp3.vn), não Rhymastic/Binz
- **Mono × Sơn Tùng M-TP** — “Nắng Ấm Xa Dần” [song, 2022] (#10516) — _'Nắng Ấm Xa Dần' é solo do Sơn Tùng M-TP, não colab com Mono_  
    ↳ web: 'Nắng Ấm Xa Dần' é solo de Sơn Tùng M-TP, 2013 (vi.wikipedia/open.spotify); sem Mono
- **Min × Sơn Tùng M-TP** — “Em Của Ngày Hôm Qua” [song, 2016] (#10519) — _'Em Của Ngày Hôm Qua' é solo do Sơn Tùng M-TP, não colab com Min_  
    ↳ web: 'Em Của Ngày Hôm Qua' é single solo de Sơn Tùng M-TP, 2014 (vi.wikipedia/open.spotify); sem Min
- **Ái Phương × Hà Anh Tuấn** — “Nơi Tình Yêu Bắt Đầu” [song, 2018] (#10524) — _'Nơi Tình Yêu Bắt Đầu' é música do Bằng Kiều, não Ái Phương/Hà Anh Tuấn_  
    ↳ web: 'Nơi Tình Yêu Bắt Đầu' é de Bằng Kiều/Lam Anh e Bùi Anh Tuấn (open.spotify/nhac.vn), não Ái Phương/Hà Anh Tuấn
- **Pamungkas × Yura Yunita** — “Cinta Luar Biasa” [feature, 2021] (#10570) — _Cinta Luar Biasa é solo de Andmesh, não esse dueto_  
    ↳ web: Spotify/lagujuara: 'Cinta Luar Biasa' é solo de Andmesh (2018); hit de Yura Yunita é 'Cinta Dan Rahasia', não dueto com Pamungkas
- **Sơn Tùng M-TP × LiSA** — “Make It Right” [feature, 2020] (#10575) — _Make It Right é do BTS, não Son Tung x LiSA_  
    ↳ web: Wikipedia: 'Make It Right' é do BTS (feat. Lauv/Ed Sheeran); Sơn Tùng apenas manifestou desejo de colaborar com Lisa (laodong.vn)
- **Ariel Rivera × Martin Nievera** — “How Did You Know” [song, 1997] (#10606) — _How Did You Know é de Gary V, não esse dueto_  
    ↳ web: Spotify/Apple Music: 'How Did You Know' é de Gary Valenciano (comp. Cecile Azarcon), não dueto Ariel Rivera x Martin Nievera
- **Ryan Cayabyab × Sharon Cuneta** — “Total Eclipse of the Heart” [song, 1997] (#10610) — _Total Eclipse é cover de Bonnie Tyler, dueto fabricado_  
    ↳ web: Spotify/whosampled: 'Total Eclipse of the Heart' creditada a Sharon Cuneta sozinha (cover de Bonnie Tyler/Jim Steinman), sem Ryan Cayabyab como intérprete
- **John Roa × Arthur Nery** — “Uhaw” [song, 2022] (#10623) — _'Uhaw' é de Dilaw, não de John Roa com Arthur Nery_  
    ↳ web: Wikipedia/Spotify: 'Uhaw' é da banda Dilaw, não John Roa com Arthur Nery
- **Maja Salvador × Julie Anne San Jose** — “Pusong Bato” [song, 2016] (#10626) — _'Pusong Bato' é de Jovit Baldivino, não esse dueto_  
    ↳ web: Wikipedia: 'Pusong Bato' é de Aimee Torres, cover de Jovit Baldivino; não dueto Maja/Julie Anne
- **IV of Spades × SB19** — “Pare Ko” [feature, 2021] (#10639) — _'Pare Ko' é dos Eraserheads, não feature IV of Spades x SB19_  
    ↳ web: Wikipedia/Spotify: 'Pare Ko' é dos Eraserheads, não colab IV of Spades x SB19
- **Up Dharma Down × Ben&Ben** — “Tadhana” [live, 2020] (#10640) — _'Tadhana' é de Up Dharma Down sozinha, não com Ben&Ben_  
    ↳ web: Spotify/Wish1075: 'Tadhana' é de Up Dharma Down sozinha (álbum Capacities 2012), sem Ben&Ben
- **Marisa Monte × Gilberto Gil** — “Tribalistas” [album, 2002] (#10839) — _Tribalistas (2002) é com Arnaldo Antunes e Carlinhos Brown, não Gilberto Gil_  
    ↳ web: Álbum 'Tribalistas' (2002) é Marisa Monte, Arnaldo Antunes e Carlinhos Brown, não Gilberto Gil (Wikipedia)
- **Legião Urbana × Cazuza** — “Dois Caras do Rock Nacional” [song, 1987] (#10894) — _título inventado, parceria não existe_  
    ↳ web: Legião Urbana e Cazuza nunca gravaram juntos; 'Dois Caras do Rock Nacional' é título inventado (Wikipedia/medium)
- **Cazuza × Barão Vermelho** — “Pro Dia Nascer Feliz” [album, 1984] (#10895) — _Pro Dia Nascer Feliz é do Barão, não álbum conjunto_  
    ↳ web: Wikipedia/Discogs: 'Pro Dia Nascer Feliz' é música/single do Barão Vermelho (Cazuza era o vocalista), não álbum conjunto
- **Barão Vermelho × Frejat** — “Barão de Frejat” [live, 2005] (#10896) — _Frejat é vocalista do próprio Barão, título inventado_  
    ↳ web: Discogs/Wikipedia: DVD ao vivo 2005 é 'MTV Ao Vivo' do Barão Vermelho; Frejat é o vocalista da banda, 'Barão de Frejat' não existe
- **Xand Avião × Anitta** — “Sua Cara” [song, 2018] (#10916) — _Sua Cara é Major Lazer/Anitta/Pabllo, não Xand Avião_  
    ↳ web: Wikipedia/Spotify: 'Sua Cara' é Major Lazer feat. Anitta & Pabllo Vittar; Xand Avião não é creditado
- **Valentina Monetta × Jimmy Jump** — “The Social Network Song (Oh Oh - Uh - Oh Oh)” [song, 2012] (#11027) — _Valentina Monetta cantou solo; Jimmy Jump é invasor de palco, não músico_  
    ↳ web: Wikipedia: 'The Social Network Song' é solo de Valentina Monetta (Eurovision 2012, Ralph Siegel); Jimmy Jump não participa
- **Alcazar × ABBA** — “Crying at the Discoteque (ABBA tribute medley)” [live, 2004] (#11046) — _'Crying at the Discoteque' é música do Alcazar; ABBA não colaborou nela_  
    ↳ web: Wikipedia/Discogs: 'Crying at the Discoteque' é do Alcazar samplando 'Spacer' de Sheila B. Devotion, sem ABBA
- **ASAP Blacc × Aloe Blacc** — “Wake Me Up (ASAP Blacc remix feature)” [song, 2014] (#11048) — _'ASAP Blacc' inventado; 'Wake Me Up' é Avicii feat. Aloe Blacc_  
    ↳ web: Wikipedia/Discogs: 'Wake Me Up' é Avicii feat. Aloe Blacc; 'ASAP Blacc' não existe
- **Interpol × The Strokes** — “NYC Punk scene compilation” [album, 2002] (#11067) — _coletânea 'NYC Punk' fabricada, sem colaboração real entre as bandas_  
    ↳ web: Coletânea real de 2002 com Interpol e Strokes é 'Yes New York' (Vice), não 'NYC Punk'
- **Nick Drake × John Cale** — “Five Leaves Left” [album, 1969] (#11165) — _Cale tocou em Bryter Layter, não em Five Leaves Left_  
    ↳ web: John Cale tocou em 'Bryter Layter' (1971), não no álbum 'Five Leaves Left' (1969) (Wikipedia)
- **After School × Psy** — “Rania” [song, 2011] (#11171) — _Rania é grupo, não colab com Psy_  
    ↳ web: 'Rania'/'Dr. Feel Good' é do grupo RaNia produzido por Teddy Riley; não é colab After School/Psy (allkpop/Seoulbeats)
- **YOASOBI × Ado** — “Oshi no Ko theme collaboration” [song, 2023] (#11212) — _YOASOBI fez Idol sozinha, não com Ado_  
    ↳ web: 'Idol' do Oshi no Ko é da YOASOBI sozinha (com shouts do Real Akiba Boyz), sem Ado (en.wikipedia.org)
- **Ayaka × Jason Mraz** — “Flavor of Life” [feature, 2009] (#11220) — _Flavor of Life é da Utada Hikaru, não Ayaka/Mraz_  
    ↳ web: 'Flavor of Life' é composição/gravação da Utada Hikaru, não Ayaka nem Jason Mraz (en.wikipedia.org, discogs.com)
- **Dave Coulier × Alanis Morissette** — “You Oughta Know” [feature, 1995] (#11225) — _Coulier é tema rumoreado, não colaborador_  
    ↳ web: 'You Oughta Know' é creditada a Morissette e Glen Ballard; Coulier é só o suposto tema, não colaborador (en.wikipedia.org)
- **In Flames × Arch Enemy** — “Dead End” [feature, 2002] (#11229) — _Dead End é do In Flames feat Miskovsky, não Arch Enemy_  
    ↳ web: 'Dead End' é do In Flames feat. Lisa Miskovsky (Come Clarity 2006), não Arch Enemy (last.fm, en.wikipedia.org)
- **Flo Milli × Mulatto** — “In the Party” [feature, 2020] (#11249) — _In the Party é da Flo Milli, sem Mulatto_  
    ↳ web: 'In the Party' é faixa solo da Flo Milli, sem feature de Mulatto/Latto (en.wikipedia.org, spotify.com)
- **Sly & the Family Stone × Miles Davis** — “A Tribute to Jack Johnson” [album, 1971] (#11254) — _A Tribute to Jack Johnson é álbum solo de Miles Davis, não colaboração com Sly_  
    ↳ web: 'A Tribute to Jack Johnson' (1971) é álbum solo de Miles Davis; apenas referencia temas de Sly Stone, sem colaboração (en.wikipedia.org, milesdavis.com)
- **Hoshino Gen × Aimyon** — “Koi” [song, 2016] (#11271) — _Koi é solo de Hoshino Gen, não colaboração com Aimyon_  
    ↳ web: 'Koi' (2016) é single solo de Gen Hoshino, sem Aimyon (en.wikipedia.org, generasia.com)
- **Hoshino Gen × Kenshi Yonezu** — “Nandemo Naiya” [song, 2016] (#11272) — _Nandemo Naiya é solo de Hoshino Gen, sem Kenshi Yonezu_  
    ↳ web: 'Nandemonaiya' (2016) é de RADWIMPS (Your Name), escrita por Yojiro Noda; não é Hoshino/Yonezu (open.spotify.com, kiminonawa.fandom.com)
- **Zahara × Lira** — “Loliwe” [song, 2011] (#11273) — _Loliwe é solo da Zahara, não dueto com Lira_  
    ↳ web: Loliwe é solo da Zahara, sem Lira creditada (Wikipedia/Spotify)
- **Radiohead × Björk** — “I've Seen It All” [song, 2000] (#11280) — _I've Seen It All é de Björk com Thom Yorke (Dancer in the Dark), não Radiohead banda_  
    ↳ web: I've Seen It All é Björk feat. Thom Yorke, não a banda Radiohead (Wikipedia)
- **Radiohead × Paul McCartney** — “Nothing” [song, 2012] (#11281) — _colaboração Radiohead/Paul McCartney não existe_  
    ↳ web: Não existe colaboração Radiohead/Paul McCartney 'Nothing'; McCartney só sonhou trabalhar com Yorke (faroutmagazine/NME)
- **Big & Rich × Kenny Chesney** — “Lost in This Moment” [song, 2006] (#11290) — _Lost in This Moment é de Big & Rich, não com Kenny Chesney_  
    ↳ web: Lost in This Moment é do duo Big & Rich, sem Kenny Chesney (Wikipedia/Songfacts)
- **SEVENTEEN × BTS** — “IDEAL CUT” [live, 2018] (#11295) — _IDEAL CUT é tour do SEVENTEEN, não live com BTS_  
    ↳ web: IDEAL CUT é a turnê/concerto próprio do SEVENTEEN, sem BTS (carat.fandom/musickorea)
- **SEVENTEEN × Marshmello** — “Darl+ing” [song, 2022] (#11296) — _Darl+ing é do SEVENTEEN solo, não com Marshmello_  
    ↳ web: Darl+ing é do SEVENTEEN solo (Woozi/Bumzu/Shannon), sem Marshmello (Wikipedia)
- **Joe Mettle × Mercy Chinwo** — “Bo Noo Ni” [song, 2019] (#11303) — _Bo Noo Ni é de Joe Mettle solo, Mercy Chinwo incompatível_  
    ↳ web: Bo Noo Ni é de Joe Mettle feat. Luigi Maclean, não Mercy Chinwo (Spotify/africangospellyrics)
- **Trivium × Dave Mustaine** — “Entrance of the Conflagration” [song, 2006] (#11321) — _Entrance of the Conflagration é do Trivium solo, sem Mustaine_  
    ↳ web: Entrance of the Conflagration é do Trivium solo; único convidado do álbum The Crusade foi Jason Suecof, sem Mustaine (Wikipedia/metal.fandom)
- **Asa × Nneka** — “African Queen” [song, 2012] (#11332) — _African Queen é solo da Asa, não dueto com Nneka_  
    ↳ web: African Queen é do 2Baba/2Face Idibia; Asa não tem essa música nem dueto com Nneka (Wikipedia)
- **Asa × Salif Keita** — “Jailer” [song, 2014] (#11333) — _Jailer é solo da Asa, sem Salif Keita_  
    ↳ web: Jailer é solo da Asa (álbum Asha 2007, escrita por Cobhams Asuquo), sem Salif Keita (Spotify/TrendyBeatz)
- **Eagles × Linda Ronstadt** — “Desperado” [song, 1973] (#11336) — _Desperado é dos Eagles, não dueto com Linda Ronstadt_  
    ↳ web: 'Desperado' é dos Eagles; Ronstadt gravou cover solo em 1973, não dueto (en.wikipedia.org)
- **IVE × Coldplay** — “MY UNIVERSE (Remix)” [song, 2023] (#11381) — _'My Universe' é Coldplay x BTS, não IVE; remix fabricado_  
    ↳ web: 'My Universe' e seus remixes (SUGA, Galantis, Guetta) são Coldplay x BTS, não IVE (en.wikipedia.org)
- **After School × Dara** — “Nu ABO” [song, 2011] (#11385) — _'Nu ABO' é da f(x), não After School; Dara é 2NE1_  
    ↳ web: 'Nu ABO' é do f(x) (SM, 2010), não After School; Dara é do 2NE1 (en.wikipedia.org)
- **VIXX × EXO** — “KCON Stage” [live, 2014] (#11388) — _título de palco genérico KCON, sem colaboração documentada_  
    ↳ web: EXO nem estava no lineup do KCON 2014; sem palco conjunto VIXX x EXO documentado (billboard.com, en.wikipedia.org)
- **DAY6 × BTS** — “JYP Nation Concert” [live, 2018] (#11390) — _título de concerto genérico, sem colaboração documentada_  
    ↳ web: BTS não é artista da JYP; 'JYP Nation Concert' 2018 não reúne DAY6 e BTS (soompi/wikipedia)
- **LOONA × K/DA** — “More” [song, 2020] (#11391) — _'More' (K/DA) não é da LOONA; fabricação_  
    ↳ web: 'More' é da K/DA com (G)I-dle e Madison Beer, sem LOONA (en.wikipedia More K/DA song)
- **LOONA × EXID** — “Hi High” [live, 2019] (#11392) — _'Hi High' é da LOONA; EXID não participa, palco fabricado_  
    ↳ web: 'Hi High' é debut da própria LOONA (M Countdown 2018), EXID não participa (youtube/kpopreviewed)
- **AOA × Block B** — “MAMA Stage” [live, 2014] (#11394) — _título de palco MAMA genérico, sem colaboração documentada_  
    ↳ web: Palco 2014 MAMA foi BTS vs Block B, não AOA x Block B (koreaboo/wikipedia 2014 MAMA)
- **Dreamcatcher × SHINee** — “InSomnia” [live, 2019] (#11395) — _'InSomnia' é da Dreamcatcher; SHINee não participa_  
    ↳ web: 'InSomnia' é o nome do fandom da Dreamcatcher, não colab com SHINee (wikipedia Dreamcatcher)
- **Dreamcatcher × Gaho** — “BOCA” [song, 2020] (#11396) — _'BOCA' é da Dreamcatcher; Gaho não participa_  
    ↳ web: 'BOCA' é faixa-título própria da Dreamcatcher (Dystopia), sem Gaho (dreamcatcher.fandom/spotify)
- **King Gnu × Millennium Parade** — “Samsung” [song, 2020] (#11399) — _'Samsung' não é faixa; King Gnu e Millennium Parade mesmo líder, fabricado_  
    ↳ web: Não existe faixa 'Samsung'; King Gnu e Millennium Parade são projetos de Daiki Tsuneta (wikipedia King Gnu)
- **King Gnu × Masego** — “Hakujitsu” [song, 2019] (#11400) — _'Hakujitsu' é do King Gnu; Masego não participa_  
    ↳ web: 'Hakujitsu' (2019) é do King Gnu, tema de drama, sem Masego (en.wikipedia Hakujitsu)
- **Sakanaction × Polyphia** — “Mikazuki Ni Nare” [live, 2017] (#11401) — _'Mikazuki' é da Sakanaction; Polyphia não participa, palco fabricado_  
    ↳ web: A faixa é 'Mikazuki Sunset' da Sakanaction, não 'Mikazuki ni Nare' nem colab Polyphia (wikipedia Sakanaction)
- **Bezerra da Silva × Caetano Veloso** — “Haiti” [song, 1993] (#11412) — _'Haiti' é de Caetano e Gilberto Gil; Bezerra da Silva não participa_  
    ↳ web: 'Haiti' (1993, Tropicália 2) é de Caetano Veloso e Gilberto Gil, sem Bezerra da Silva (en.wikipedia/spotify)
- **Hadiya George × Moby** — “Natural Blues (remake)” [song, 2021] (#11429) — _'Natural Blues' é do Moby; remake c/ Hadiya George fabricado_  
    ↳ web: Remakes de 'Natural Blues' de Moby são com Gregory Porter e Amythyst Kiah (Reprise 2021), não Hadiya George (wikipedia/deutschegrammophon)
- **Juanes × Aterciopelados** — “Estoy Aquí” [song, 2003] (#11579) — _Estoy Aquí é de Shakira, não colaboração Juanes/Aterciopelados_  
    ↳ web: 'Estoy Aquí' é de Shakira (Pies Descalzos 1995), não Juanes/Aterciopelados (Wikipedia)
- **Alejandro Sanz × Jesse & Joy** — “Don't Stop the Music” [song, 2010] (#11599) — _Don't Stop the Music é da Rihanna, fabricação_  
    ↳ web: Spotify/AppleMusic: colaboração real Jesse & Joy x Alejandro Sanz é 'No Soy Una de Esas', não 'Don't Stop the Music' (da Rihanna)
- **Chayanne × Paulina Rubio** — “Dejaría Todo” [song, 2002] (#11612) — _'Dejaría Todo' é solo de Chayanne, não dueto com Paulina_  
    ↳ web: 'Dejaría Todo' (1998) é canção solo de Chayanne, sem Paulina Rubio (wikipedia, discogs)
- **Luis Miguel × Thalía** — “Tu y Yo” [song, 1993] (#11617) — _não há dueto documentado Luis Miguel/Thalía_  
    ↳ web: 'Tú y Yo' (1993, álbum Aries) é solo de Luis Miguel; não há dueto com Thalía (wikipedia, discogs)
- **Luis Miguel × Benny Moré** — “La Historia de un Amor (Tributo)” [song, 1991] (#11619) — _Benny Moré morreu em 1963; tributo como dueto é fabricação_  
    ↳ web: Benny Moré morreu em 1963; 'Historia de un Amor' de Luis Miguel é solo, dueto é impossível (wikipedia)
- **Enrique Iglesias × Jennifer Lopez** — “Ayer” [song, 1998] (#11627) — _'Ayer' é solo posterior; dueto Enrique/JLo em 1998 não existe_  
    ↳ web: Não existe dueto Enrique Iglesias/Jennifer Lopez chamado 'Ayer'; colaborações reais são 'Physical' (wikipedia, spotify)
- **Maluma × Carlos Rivera** — “Pienso en Tu Mirá” [song, 2017] (#11657) — _'Pienso en Tu Mirá' é de Rosalía, não Maluma/Carlos Rivera_  
    ↳ web: 'Pienso en Tu Mirá' é de Rosalía (El Mal Querer), escrita com C. Tangana; não Maluma/Carlos Rivera (wikipedia)
- **Karol G × Nicki Jam** — “Tusa” [song, 2019] (#11674) — _'Tusa' é Karol G com Nicki Minaj, não 'Nicki Jam'_  
    ↳ web: 'Tusa' é Karol G com Nicki Minaj, não 'Nicki Jam' (wikipedia, discogs)
- **Romeo Santos × Monchy & Alexandra** — “Dos Locos” [song, 2008] (#11683) — _'Dos Locos' é de Monchy & Alexandra, não dueto com Romeo Santos_  
    ↳ web: 'Dos Locos' é original de Monchy & Alexandra (álbum Confesiones); não é dueto com Romeo Santos (wikipedia, spotify)
- **Kinito Méndez × Eddy Herrera** — “El Baile del Perrito” [song, 1997] (#11718) — _El Baile del Perrito é de Wilfrido Vargas, não dueto Kinito/Eddy_  
    ↳ web: 'El Baile del Perrito' é de Wilfrido Vargas, não dueto Kinito Méndez/Eddy Herrera (letras.com, spotify.com)
- **La India × India** — “Salseras (Live)” [live, 2001] (#11722) — _La India e India são a mesma artista, dueto impossível_  
    ↳ web: La India e 'India' são a mesma artista; dueto consigo mesma é impossível (en.wikipedia.org)
- **Héctor Lavoe × Johnny Pacheco** — “El Malo” [song, 1975] (#11740) — _El Malo é de Willie Colón com Lavoe, não Pacheco_  
    ↳ web: 'El Malo' (1967) é de Willie Colón & Héctor Lavoe, não Johnny Pacheco (discogs.com, es.wikipedia.org)
- **Nacho × Chino & Nacho** — “Me Voy Enamorando (Remix)” [song, 2011] (#11770) — _Nacho integra Chino & Nacho; dueto consigo mesmo_  
    ↳ web: 'Me Voy Enamorando (Remix)' é Chino & Nacho ft. Farruko; Nacho integra Chino & Nacho, par consigo mesmo (discogs.com, en.wikipedia.org)
- **Ricardo Montaner × Carlos Rivera** — “Me Va a Extrañar” [song, 2019] (#11774) — _Me Va a Extrañar é de Montaner solo, não dueto com Carlos Rivera_  
    ↳ web: 'Me Va a Extrañar - Versión Montaner' (2019) é solo de Ricardo Montaner; dueto com Carlos Rivera é 'Yo No Fumo' 2023 (spotify.com, informador.mx)
- **Luis Fonsi × Natti Natasha** — “No Me Queda Más” [song, 2019] (#11924) — _'No Me Queda Más' é de Selena, não de Fonsi e Natti_  
    ↳ web: Wikipedia: 'No Me Queda Más' é de Selena (álbum Amor Prohibido 1994), escrita por Ricky Vela, não Fonsi/Natti
- **Lucenzo × Pitbull** — “Pump It (Remix)” [song, 2012] (#11927) — _'Pump It' é dos Black Eyed Peas, não Lucenzo e Pitbull_  
    ↳ web: Wikipedia: 'Pump It' é dos Black Eyed Peas (Monkey Business 2005); Lucenzo/Pitbull colaboram em 'Danza Kuduro'
- **Paul Simon × Bob Dylan** — “The Concert in Central Park” [live, 1981] (#11970) — _Concert in Central Park foi de Simon & Garfunkel, não Dylan_  
    ↳ web: Wikipedia: 'The Concert in Central Park' (1981) é álbum ao vivo de Simon & Garfunkel (Paul Simon e Art Garfunkel), não Bob Dylan
- **Sam Cooke × Ray Charles** — “Night Beat” [feature, 1963] (#12062) — _'Night Beat' é álbum de Sam Cooke; Ray Charles não participou_  
    ↳ web: Wikipedia: 'Night Beat' (1963) é álbum solo de Sam Cooke; pianista era Ray Johnson, Ray Charles não participou
- **Elton John × Paul McCartney** — “Friends of Mr. Cairo” [feature, 1981] (#12076) — _'Friends of Mr. Cairo' é do Jon & Vangelis, não Elton/McCartney_  
    ↳ web: Wikipedia: 'The Friends of Mr Cairo' (1981) é de Jon & Vangelis (Jon Anderson + Vangelis), não Elton John/McCartney
- **Stevie Wonder × Michael Jackson** — “Girl Friend” [song, 1979] (#12078) — _'Girl Friend' não é colaboração documentada Stevie Wonder/Michael Jackson_  
    ↳ web: Wikipedia: 'Girlfriend' (Off the Wall 1979) foi escrita por Paul McCartney e cantada por Michael Jackson solo; Stevie Wonder não participa
- **Stevie Wonder × Diana Ross** — “My Cherie Amour” [feature, 1969] (#12079) — _'My Cherie Amour' é solo de Stevie Wonder; Diana Ross não participa_  
    ↳ web: Wikipedia: 'My Cherie Amour' (1969) é single solo de Stevie Wonder; Diana Ross não aparece
- **John Fogerty × Bob Dylan** — “Change in the Weather” [feature, 1986] (#12126) — _'Change in the Weather' é de John Fogerty solo; Dylan não participa_  
    ↳ web: Discogs/Wikipedia: 'Change in the Weather' é de John Fogerty solo (álbum 'Eye of the Zombie' 1986); Bob Dylan não participa
- **Bobby Byrd × Maceo Parker** — “I Know You Got Soul” [song, 1971] (#12148) — _'I Know You Got Soul' é de Bobby Byrd 1971, mas Maceo Parker não creditado como artista_  
    ↳ web: Funkatropolis/trombonealex: no sax da faixa original de Bobby Byrd (1971) consta Jimmy Parker, não Maceo Parker
- **Van Morrison × Mick Jagger** — “The Last Waltz” [live, 1976] (#12167) — _Mick Jagger não participou do Last Waltz; fabricação_  
    ↳ web: Wikipedia (The Last Waltz): Van Morrison participou, mas Mick Jagger nao esteve no evento
- **David Crosby × Paul McCartney** — “Too Much Rock and Roll” [feature, 1993] (#12189) — _título inexistente; colaboração Crosby/McCartney fabricada_  
    ↳ web: the-paulmccartney-project/Wikipedia: Crosby e McCartney nunca gravaram dueto; 'Too Much Rock and Roll' inexistente
- **Peter Gabriel × David Bowie** — “I Have Been Here Before” [feature, 1987] (#12190) — _I Have Been Here Before não é colaboração Gabriel/Bowie_  
    ↳ web: davidbowie.com/petergabriel.com: Bowie e Gabriel nunca gravaram juntos (Bowie recusou 'Scratch My Back'); musica inexistente
- **Mark Knopfler × Stevie Wonder** — “Ebony and Ivory Sessions” [feature, 1985] (#12192) — _Ebony and Ivory é McCartney/Wonder; Knopfler fabricado_  
    ↳ web: Wikipedia: 'Ebony and Ivory' e de McCartney/Stevie Wonder; nenhuma colaboracao Knopfler/Wonder documentada
- **Michael Jackson × Stevie Wonder** — “Happy Birthday” [feature, 1981] (#12199) — _Happy Birthday Stevie Wonder não tem feature Michael Jackson_  
    ↳ web: Wikipedia: 'Happy Birthday' de Stevie Wonder (Hotter than July, 1980) e solo, sem feature de Michael Jackson
- **Queen × John Lennon** — “Bohemian Rhapsody” [feature, 1977] (#12202) — _Bohemian Rhapsody do Queen não tem John Lennon_  
    ↳ web: Wikipedia: 'Bohemian Rhapsody' e composicao/gravacao apenas do Queen, sem John Lennon
- **Neil Diamond × Elvis Presley** — “Sweet Caroline” [feature, 1969] (#12223) — _Sweet Caroline é só de Neil Diamond; feature Elvis fabricado_  
    ↳ web: Wikipedia/ultimateclassicrock: 'Sweet Caroline' e solo de Neil Diamond; Elvis apenas fez cover ao vivo, sem feature conjunto
- **Elvis Presley × Neil Diamond** — “Holly Holy” [feature, 1970] (#12227) — _Holly Holy é de Neil Diamond; feature Elvis fabricado_  
    ↳ web: Wikipedia (Holly Holy): musica solo de Neil Diamond; Elvis cantou so uma linha ao vivo, sem gravacao conjunta
- **Ed Sheeran × Chance the Rapper** — “Chuck D” [song, 2019] (#12232) — _Chuck D não é música de Sheeran com Chance; fabricação_  
    ↳ web: Wikipedia (No.6 Collaborations Project): colab Sheeran/Chance e 'Cross Me' feat. PnB Rock, nao existe faixa 'Chuck D'
- **Taylor Swift × Bon Iver** — “both of us” [song, 2012] (#12233) — _both of us é de B.o.B com Taylor Swift, não Bon Iver_  
    ↳ web: Wikipedia/Spotify: 'Both of Us' é de B.o.B feat. Taylor Swift, Bon Iver não participa
- **Gunna × Post Malone** — “One Right Now” [song, 2021] (#12365) — _One Right Now é de Post Malone com The Weeknd, não Gunna_  
    ↳ web: Wikipedia: 'One Right Now' é de Post Malone com The Weeknd, sem participação de Gunna
- **Roddy Ricch × The Weeknd** — “Lost in the Fire” [feature, 2019] (#12369) — _Lost in the Fire é de Gesaffelstein com The Weeknd, não Roddy Ricch_  
    ↳ web: Wikipedia/Spotify: 'Lost in the Fire' é de Gesaffelstein com The Weeknd, não Roddy Ricch
- **Gorillaz × Mavis Staples** — “Hallelujah Money” [song, 2017] (#12386) — _Hallelujah Money é de Gorillaz com Benjamin Clementine, não Mavis Staples_  
    ↳ web: Wikipedia/Songfacts: 'Hallelujah Money' credita Gorillaz feat. Benjamin Clementine, não Mavis Staples
- **Gorillaz × Little Simz** — “Momentary Bliss” [song, 2020] (#12387) — _Momentary Bliss é de Gorillaz com slowthai e Slaves, não Little Simz_  
    ↳ web: Wikipedia/Spotify: 'Momentary Bliss' credita Gorillaz feat. slowthai e Slaves, não Little Simz
- **Jhené Aiko × Chris Brown** — “None of Your Concern” [song, 2020] (#12410) — _None of Your Concern é de Jhené Aiko com Big Sean, não Chris Brown_  
    ↳ web: Wikipedia/Billboard: 'None of Your Concern' credita Jhené Aiko feat. Big Sean, não Chris Brown
- **Jung Kook × Major Lazer** — “We Don't Talk About Bruno (Remix)” [song, 2022] (#12532) — _remix de 'Bruno' (Encanto) por Jung Kook & Major Lazer não existe_  
    ↳ web: Spotify/busca: não existe remix de 'We Don't Talk About Bruno' por Jung Kook & Major Lazer
- **Jung Kook × DJ Snake** — “Oh La La” [song, 2022] (#12533) — _'Oh La La' é de NewJeans; Jung Kook & DJ Snake não fizeram esta_  
    ↳ web: Spotify: colaboração Jung Kook/DJ Snake é 'Please Don't Change' (GOLDEN 2023); não há faixa 'Oh La La' dos dois
- **Jason Derulo × Adam Levine** — “Try Me” [song, 2019] (#12538) — _'Try Me' de Jason Derulo é com Jennifer Lopez/Matoma, não Adam Levine_  
    ↳ web: what-song: 'Try Me' de Jason Derulo é feat. Jennifer Lopez e Matoma; colab com Adam Levine é 'Lifestyle'
- **OneRepublic × Demi Lovato** — “What I've Done (Linkin Park Cover)” [song, 2018] (#12579) — _cover de Linkin Park por OneRepublic & Demi Lovato não existe_  
    ↳ web: WhoSampled/busca: não existe cover de 'What I've Done' (Linkin Park) por OneRepublic & Demi Lovato
- **Nas × Jay-Z** — “Dead Presidents II” [song, 1996] (#12592) — _'Dead Presidents II' é de Jay-Z; Nas não participa (samplea voz de Nas)_  
    ↳ web: Wikipedia/WhoSampled: 'Dead Presidents II' é solo do Jay-Z (prod. Ski), apenas samplea a voz de Nas de 'The World Is Yours'
- **Nas × Kanye West** — “ULTRAlite Beam (Remix)” [song, 2016] (#12596) — _'Ultralight Beam' é de Kanye; remix com Nas não existe_  
    ↳ web: WhoSampled: 'Ultralight Beam' credita Chance/Kirk Franklin/The-Dream/Kelly Price; nenhum remix com Nas documentado
- **2 Pac × Roger Troutman** — “I'll Be Missing You” [song, 1996] (#12624) — _I'll Be Missing You é de Puff Daddy, não 2Pac/Troutman_  
    ↳ web: 'I'll Be Missing You' é de Puff Daddy & Faith Evans feat. 112, não 2Pac/Roger Troutman (en.wikipedia.org/discogs.com)
- **Method Man × Lauryn Hill** — “How Many Mics” [song, 1996] (#12636) — _How Many Mics é Fugees/Lauryn, não Method Man_  
    ↳ web: 'How Many Mics' é dos Fugees (Lauryn Hill, Wyclef, Pras), sem Method Man (spotify.com/en.wikipedia.org)
- **Mary J. Blige × Common** — “Come On Eileen” [song, 2014] (#12671) — _Come On Eileen não é faixa de Mary J. Blige/Common_  
    ↳ web: 'Come On Eileen' é dos Dexys Midnight Runners; não existe versão Mary J. Blige/Common (en.wikipedia.org)
- **Erykah Badu × D'Angelo** — “The Root” [song, 1999] (#12672) — _The Root é faixa só de D'Angelo, sem Erykah Badu_  
    ↳ web: 'The Root' é faixa solo de D'Angelo (guit/baixo de Charlie Hunter), sem Erykah Badu (en.wikipedia.org)
- **The 1975 × Taylor Swift** — “Anti-Hero (Remix)” [song, 2022] (#12692) — _Anti-Hero é da Taylor, não há remix com The 1975_  
    ↳ web: Não existe remix oficial de 'Anti-Hero' com The 1975; remixes são de Roosevelt, Jayda G, Kungs, ILLENIUM (en.wikipedia.org, last.fm)
- **Beck × Cat Power** — “Sea Change (Remix)” [song, 2002] (#12712) — _Sea Change é álbum solo do Beck, não remix com Cat Power_  
    ↳ web: 'Sea Change' é álbum solo do Beck (2002, prod. Nigel Godrich), sem remix/colaboração de Cat Power (en.wikipedia.org, discogs.com)
- **Pharrell × Nelly** — “Hot in Herre” [song, 2002] (#12718) — _Hot in Herre é do Nelly produzido pelos Neptunes; não é feat de Pharrell_  
    ↳ web: 'Hot in Herre' é do Nelly produzida pelos Neptunes (Pharrell é produtor, não feature); vocais extras de Dani Stevenson (en.wikipedia.org, songfacts.com)
- **Heuss L'Enfoiré × Ninho** — “Bande Organisée” [song, 2020] (#12764) — _Bande Organisée é dos rappers de Marselha, não de Heuss e Ninho_  
    ↳ web: 'Bande organisée' (13 Organisé) traz Jul, SCH, Kofs, Naps, Soso Maness, Elams, Solda, Houari; nem Heuss nem Ninho estão nela (en.wikipedia.org, spotify.com)
- **Heuss L'Enfoiré × Jul** — “Bande Organisée” [song, 2020] (#12765) — _Bande Organisée é de Jul e companhia, sem Heuss L'Enfoiré_  
    ↳ web: Jul está em 'Bande organisée', mas Heuss L'Enfoiré não é creditado; elenco é do coletivo marselhês 13 Organisé (en.wikipedia.org, spotify.com)
- **Heuss L'Enfoiré × Alonzo** — “Bande Organisée” [song, 2020] (#12766) — _Bande Organisée não inclui Heuss L'Enfoiré_  
    ↳ web: 'Bande Organisée' (13 Organisé, 2020) traz SCH, Kofs, Jul, Naps, Soso Maness, Elams, Solda, Houari; Heuss L'Enfoiré não consta (en.wikipedia.org)
- **Heuss L'Enfoiré × SCH** — “Bande Organisée” [song, 2020] (#12767) — _Bande Organisée não inclui Heuss L'Enfoiré_  
    ↳ web: Créditos de 'Bande Organisée' 2020 não incluem Heuss L'Enfoiré, apenas SCH/Kofs/Jul/Naps/Soso Maness/Elams/Solda/Houari (shazam.com)
- **Heuss L'Enfoiré × Soso Maness** — “Bande Organisée” [song, 2020] (#12768) — _Bande Organisée não inclui Heuss L'Enfoiré_  
    ↳ web: 'Bande Organisée' 2020 é do coletivo 13 Organisé sem Heuss L'Enfoiré nos créditos (en.wikipedia.org)
- **Tanya Stephens × Anthony B** — “Gangsta Blues” [album, 2004] (#12907) — _Gangsta Blues é álbum solo de Tanya Stephens, não com Anthony B_  
    ↳ web: 'Gangsta Blues' (2004) é álbum de Tanya Stephens com feats de Wyclef Jean e Spragga Benz, sem Anthony B (discogs/wikipedia)
- **Diana King × Shaggy** — “Shy Guy” [song, 1995] (#12908) — _Shy Guy é de Diana King solo, não feat. Shaggy_  
    ↳ web: 'Shy Guy' (1995) é creditada só a Diana King, escrita por King/Gardner/Marvel, sem Shaggy (wikipedia/discogs)
- **Ali Campbell × ASTRO** — “That Look in Your Eye” [song, 1995] (#12913) — _ASTRO marcado K-Pop; cruzamento improvável com Ali Campbell em 1995_  
    ↳ web: 'That Look in Your Eye' (1995) é solo de Ali Campbell com Pamela Starks; Astro não participa dessa faixa de 1995 (wikipedia/discogs)
- **Lee 'Scratch' Perry × The Clash** — “Complete Control” [song, 1977] (#12918) — _Complete Control é do The Clash; Lee Perry produziu mas não é colaboração creditada_  
    ↳ web: 'Complete Control' (1977) é música do The Clash apenas produzida por Lee Perry, não colaboração creditada dos dois (wikipedia/songfacts)
- **Mad Cobra × Shabba Ranks** — “Flex” [song, 1992] (#12956) — _Flex é de Mad Cobra solo, não com Shabba Ranks_  
    ↳ web: 'Flex' (1992) é de Mad Cobra solo; Shabba Ranks só aparece em single dividido com outra faixa ('Ting-A-Ling'), não em 'Flex' (discogs/wikipedia)
- **Grupo Niche × Celia Cruz** — “La Rebelión” [song, 1989] (#13015) — _La Rebelión é de Joe Arroyo, não Grupo Niche com Celia_  
    ↳ web: Wikipedia/salserisimoperu: 'La Rebelión' é de Joe Arroyo y La Verdad, não Grupo Niche com Celia Cruz
- **Rubén Blades × Celia Cruz** — “La Vida Es Un Carnaval” [song, 1998] (#13040) — _La Vida Es Un Carnaval é solo de Celia Cruz, não com Blades_  
    ↳ web: Wikipedia: 'La Vida Es Un Carnaval' é solo de Celia Cruz (autor Victor Daniel), sem Rubén Blades
- **The Beatles × Peter Sellers** — “A Hard Day's Night” [song, 1965] (#13047) — _A Hard Day's Night não é colaboração Beatles-Peter Sellers_  
    ↳ web: Discogs/openculture: Peter Sellers gravou cover cômico separado; não é colaboração conjunta com The Beatles
- **Blink-182 × Lil Wayne** — “A Letter to Elise” [song, 2011] (#13052) — _'A Letter to Elise' é do The Cure, não Blink-182 feat Lil Wayne_  
    ↳ web: 'A Letter to Elise' é do The Cure, coverizada pelo Blink-182, sem Lil Wayne (letras.com, youtube.com)
- **Blink-182 × Nicki Minaj** — “Up All Night” [song, 2011] (#13053) — _'Up All Night' do Blink-182 não tem Nicki Minaj_  
    ↳ web: 'Up All Night' do Blink-182 (2011) não tem Nicki Minaj; a versão com Nicki é do Drake (en.wikipedia.org)
- **Simple Plan × Rivers Cuomo** — “What's New Scooby-Doo?” [song, 2003] (#13056) — _Rivers Cuomo não participa do tema Scooby-Doo do Simple Plan_  
    ↳ web: Tema 'What's New Scooby-Doo?' do Simple Plan foi escrito por Rich Dickerson, sem Rivers Cuomo (scoobydoo.fandom.com, open.spotify.com)
- **Shinedown × Eminem** — “Dream” [song, 2022] (#13059) — _Shinedown feat Eminem implausível e inexistente_  
    ↳ web: Nenhuma faixa 'Dream' de Shinedown com Eminem em 2022; ligação Eminem/Dream On é Aerosmith/Steven Tyler (en.wikipedia.org)
- **Alphabeat × Robyn** — “Boyfriend” [song, 2007] (#13233) — _Boyfriend não é dueto Alphabeat/Robyn_  
    ↳ web: Wikipedia/Discogs: 'Boyfriend' é single solo do Alphabeat (prod. Mike Spencer), sem Robyn
- **NSYNC × Michael Jackson** — “Celebrity” [song, 2001] (#13247) — _Celebrity é álbum/faixa NSYNC, não dueto com MJ_  
    ↳ web: Wikipedia: 'Celebrity' é álbum/faixa do NSYNC; o dueto cogitado com MJ era 'Gone' e nunca saiu
- **Spice Girls × Elton John** — “Are You Man Enough?” [song, 1997] (#13249) — _título não é colaboração Spice Girls/Elton John_  
    ↳ web: Wikipedia: 'Are You Man Enough?' é dos Four Tops (1973); Spice/Elton fizeram 'Don't Go Breaking My Heart'
- **Spice Girls × Bryan Adams** — “When You're Gone” [song, 1998] (#13250) — _When You're Gone é Bryan Adams com Mel C, não Spice Girls_  
    ↳ web: Wikipedia/Discogs: 'When You're Gone' (1998) é Bryan Adams feat. Melanie C (solo), não Spice Girls
- **Luis Miguel × Mariah Carey** — “When I Fall in Love” [song, 1995] (#13268) — _When I Fall in Love é dueto Luis Miguel não é com Mariah_  
    ↳ web: Mariahcareynetwork/Remezcla: único dueto Luis Miguel/Mariah foi 'After Tonight' (não lançado); não há 'When I Fall in Love'
- **Fabrizio De André × Premiata Forneria Marconi** — “La buona novella” [album, 1970] (#13277) — _La buona novella é álbum solo De André, não colab PFM_  
    ↳ web: Wikipedia: 'La buona novella' (1970) é álbum solo De André, tocado por 'I Quelli' (só viraria PFM em 1971)
- **Café Quijano × Boney M.** — “La Quiero a Morir” [song, 2001] (#13292) — _La Quiero a Morir é de Sabina/Café Quijano, não Boney M._  
    ↳ web: Spotify/SecondHandSongs: 'La Quiero a Morir' é de Cabrel; versão Café Quijano é com Alejandro Sanz, sem Boney M.
- **MC Daniel × Lexa** — “Envolvimento (Remix)” [song, 2022] (#13297) — _Envolvimento é de MC Loma, não MC Daniel/Lexa_  
    ↳ web: Spotify/Wikipedia: 'Envolvimento' é de MC Loma e As Gêmeas Lacração; sem versão MC Daniel/Lexa
- **D Double E × Skepta** — “Rolex Sweep” [song, 2009] (#13531) — _Rolex Sweep é do DJ Q/Skepta, não de D Double E_  
    ↳ web: Wikipedia/Discogs: 'Rolex Sweep' (2008) é solo de Skepta, prod. Bless Beats; sem D Double E
- **Manga Saint Hilare × Ghetts** — “Talking the Hardest” [song, 2016] (#13544) — _Talking the Hardest é de Giggs, não Manga/Ghetts_  
    ↳ web: RateYourMusic/Spotify: 'Talkin da Hardest' é de Giggs, não Manga Saint Hilare/Ghetts
- **Travis × Paul McCartney** — “Baby One More Time” [live, 2002] (#13555) — _Baby One More Time live Travis com McCartney implausível e fabricado_  
    ↳ web: Spotify/YouTube: 'Baby One More Time' ao vivo é cover solo do Travis (VH1 Storytellers); sem McCartney nessa faixa
- **Ali Zafar × Aditi Singh Sharma** — “London Thumakda” [song, 2014] (#13577) — _London Thumakda é de Queen, não de Ali Zafar/Aditi_  
    ↳ web: Wikipedia/Amazon Music: 'London Thumakda' (Queen) é de Labh Janjua, Sonu & Neha Kakkar, não Ali Zafar/Aditi
- **Malkit Singh × Daler Mehndi** — “Tunak Tunak Tun” [song, 1998] (#13592) — _Tunak Tunak Tun é solo de Daler Mehndi, não dueto_  
    ↳ web: 'Tunak Tunak Tun' e solo de Daler Mehndi (1998), sem dueto com Malkit Singh (en.wikipedia.org)
- **Nooran Sisters × Javed Ali** — “Patakha Guddi” [song, 2014] (#13595) — _Patakha Guddi é das Nooran Sisters, sem Javed Ali_  
    ↳ web: 'Patakha Guddi' e das Nooran Sisters (versao masculina do proprio A.R. Rahman), sem Javed Ali (en.wikipedia.org/spotify.com)
- **Sunanda Sharma × Jassie Gill** — “Akh Lad Jaave” [song, 2018] (#13599) — _Akh Lad Jaave é de Badshah (Gentleman), não Sunanda/Jassie_  
    ↳ web: 'Akh Lad Jaave' (Loveyatri) e de Badshah, Asees Kaur e Jubin Nautiyal, nao Sunanda/Jassie (imdb.com)
- **Imran Khan × Snoop Dogg** — “Satisfya” [song, 2012] (#13625) — _Satisfya é solo de Imran Khan, sem Snoop Dogg_  
    ↳ web: 'Satisfya' e solo de Imran Khan, sem Snoop Dogg (en.wikipedia.org/open.spotify.com)
- **Barbie Maan × Sidhu Moose Wala** — “Jine Mera Dil Luteya” [song, 2020] (#13651) — _Jine Mera Dil Luteya é de Gippy Grewal, não Barbie/Sidhu_  
    ↳ web: 'Jine Mera Dil Luteya' e de Jazzy B; Barbie Maan e Sidhu fizeram 'Ajj Kal Ve', titulo diferente (open.spotify.com/imdb.com)
- **Barbie Maan × Gurnam Bhullar** — “Rabb Ne Banaiyan Jodiyan” [song, 2019] (#13652) — _Rabb Ne Banaiyan Jodiyan é de Akhil/B Praak, não Barbie/Gurnam_  
    ↳ web: 'Rabb Ne Banaiyan Jodiyan' e de Babbu Maan/Gurdas Maan; sem colaboracao Barbie Maan + Gurnam Bhullar (en.wikipedia.org/jiosaavn.com)
- **Navv Inder × Mista Baaz** — “Lak 28 Kudi Da” [song, 2013] (#13654) — _Lak 28 Kudi Da é de Diljit Dosanjh/Yo Yo Honey Singh_  
    ↳ web: 'Lak 28 Kudi Da' é de Diljit Dosanjh/Yo Yo Honey Singh, sem Navv Inder nem Mista Baaz (open.spotify.com, jiosaavn.com)
- **Antara Mitra × Arijit Singh** — “Tum Hi Ho” [song, 2013] (#13656) — _Tum Hi Ho é de Arijit solo, sem Antara Mitra_  
    ↳ web: 'Tum Hi Ho' (Aashiqui 2) é Arijit Singh solo; nenhuma versão oficial credita Antara Mitra (en.wikipedia.org, open.spotify.com)
- **Ilaiyaraaja × Harris Jayaraj** — “Mellisai Mannan” [song, 2006] (#13657) — _Ilaiyaraaja e Harris Jayaraj nunca fizeram música juntos_  
    ↳ web: 'Mellisai Mannan' é alcunha do compositor M. S. Viswanathan, não uma faixa colaborativa Ilaiyaraaja/Harris Jayaraj (en.wikipedia.org)
- **Dan + Shay × Reba McEntire** — “I Remember Everything” [song, 2022] (#13667) — _I Remember Everything é de Zach Bryan/Kacey, não Dan+Shay/Reba_  
    ↳ web: 'I Remember Everything' (2023) é de Zach Bryan feat. Kacey Musgraves, não Dan+Shay/Reba (en.wikipedia.org, open.spotify.com)
- **Brooks & Dunn × Kenny Rogers** — “If You See Her Tonight” [song, 1995] (#13669) — _título inventado a partir da música real de Brooks&Dunn/Reba_  
    ↳ web: Título inexistente; a faixa real de Brooks & Dunn é 'If You See Him/If You See Her' (1998) com Reba, sem Kenny Rogers (open.spotify.com, songfacts.com)
- **Toby Keith × Krystal Keith** — “Drink on It” [song, 2013] (#13672) — _Drink on It é de Blake Shelton, não Toby/Krystal Keith_  
    ↳ web: 'Drink on It' (2012) é de Blake Shelton, não Toby/Krystal Keith (en.wikipedia.org, theboot.com)
- **Big & Rich × Gretchen Wilson** — “Redneck Woman” [song, 2004] (#13701) — _Redneck Woman é música solo de Gretchen Wilson_  
    ↳ web: Wikipedia: 'Redneck Woman' é single solo de Gretchen Wilson; Big & Rich só co-escreveram/aparecem no clipe, não creditados como intérpretes
- **SEVENTEEN × Fallin' Flower** — “Fallin' Flower” [song, 2020] (#13750) — _b é título de música, não artista_  
    ↳ web: Wikipedia: 'Fallin' Flower' é single só do SEVENTEEN; 'b' é o título da música, não um artista
- **SEVENTEEN × Ailee** — “Call Call Call!” [song, 2017] (#13751) — _Call Call Call é do SEVENTEEN sem Ailee_  
    ↳ web: carat.fandom/soompi: 'Call Call Call!' tem os 13 membros do SEVENTEEN; Ailee só colaborou em 'Q&A' (2015), não nesta faixa
- **aespa × Black Mamba featuring AI avatar** — “Black Mamba” [song, 2020] (#13754) — _b é descrição inventada; Black Mamba é da aespa_  
    ↳ web: Wikipedia: 'Black Mamba' é estreia solo da aespa; 'b' ('featuring AI avatar') é descrição inventada, não artista
- **Big Bang × Epik High** — “Black Swan Art (2 of them)” [song, 2022] (#13759) — _título sem sentido, colaboração inexistente_  
    ↳ web: Nenhuma fonte mostra 'Black Swan Art (2 of them)'; colabs Epik High/Big Bang são Tablo com Taeyang ('Rich'/'Tomorrow'), título inexistente
- **Xiumin × Jimin (BTS)** — “We Don't Talk Together (SM x BH event)” [live, 2019] (#13767) — _We Don't Talk Together é de Heize/Giriboy_  
    ↳ web: Apple Music/kpop.fandom: 'We Don't Talk Together' (2019) é de Heize feat. Giriboy (prod. SUGA), não Xiumin e Jimin
- **Suho × Chen** — “EXO CBX - Hey Mama!” [album, 2016] (#13768) — _Suho não integra o EXO-CBX_  
    ↳ web: Wikipedia: EXO-CBX = Xiumin, Baekhyun e Chen; Suho não integra o subgrupo 'Hey Mama!'
- **Vico C × Calle 13** — “Pa'l Norte” [song, 2010] (#13898) — _'Pa'l Norte' é Calle 13 com Orishas, não Vico C_  
    ↳ web: Discogs/Spotify: 'Pa'l Norte' é Calle 13 feat. Orishas; Vico C é só influência, não crédito
- **Sonora Santanera × Luis Miguel** — “La Media Vuelta” [song, 1996] (#13915) — _'La Media Vuelta' é Luis Miguel, sem Sonora_  
    ↳ web: Wikipedia: 'La Media Vuelta' de Luis Miguel (álbum Segundo Romance) é solo, sem Sonora Santanera
- **Matthieu Chedid × Sting** — “Desert Rose (French version)” [feature, 2000] (#13922) — _'Desert Rose' é Sting x Cheb Mami, não -M-_  
    ↳ web: Wikipedia/WhoSampled: 'Desert Rose' é Sting feat. Cheb Mami, não Matthieu Chedid
- **Sigur Rós × Radiohead** — “Ára bátur (live with Radiohead)” [live, 2003] (#13927) — _ao vivo Sigur Rós x Radiohead fabricado_  
    ↳ web: NME/Wikipedia: 'Ára bátur' gravada em 2008 e tocada ao vivo pela 1ª vez em 2025 no Royal Albert Hall; live 2003 c/ Radiohead impossível
- **Adam Levine × Stevie Wonder** — “Just a Fool” [song, 2012] (#13943) — _'Just a Fool' é Aguilera x Blake Shelton_  
    ↳ web: Wikipedia/Spotify: 'Just a Fool' (2012) é Christina Aguilera feat. Blake Shelton, não Adam Levine x Stevie Wonder
- **DMX × Eve** — “What These Bitches Want” [song, 1999] (#14036) — _Eve é rapper de Filadélfia, não J-Pop; gênero fabricado, mas faixa existe - rótulo errado_  
    ↳ web: Wikipedia/Spotify: 'What These Bitches Want' de DMX feat. Sisqó (Dru Hill), não Eve
- **Arafat Abou-Chaker × Bushido** — “Sonnenbank Flavour” [song, 2006] (#14086) — _Arafat Abou-Chaker não é artista/rapper, não gravou faixa_  
    ↳ web: Wikipedia/Discogs: 'Sonnenbank Flavour' é single solo de Bushido; Arafat Abou-Chaker era manager, não artista
- **Woodkid × Lykke Li** — “Heart of Courage” [song, 2013] (#14095) — _Heart of Courage é instrumental de Woodkid, não feat Lykke Li_  
    ↳ web: Spotify/SPIN: colaboração Woodkid & Lykke Li é 'Never Let You Down', não 'Heart of Courage'
- **José González × Nick Drake** — “Heartbeats” [song, 2003] (#14103) — _Heartbeats é cover de The Knife, Nick Drake morto em 1974_  
    ↳ web: Wikipedia/WhoSampled: 'Heartbeats' de José González é cover solo de The Knife (Dreijer); Nick Drake não participa
- **American Authors × fun.** — “Go Big or Go Home” [song, 2014] (#14110) — _Go Big or Go Home é de American Authors solo, sem fun._  
    ↳ web: Wikipedia/Spotify: 'Go Big or Go Home' é solo de American Authors (2015), sem fun.
- **Styles P × Nas** — “Nas Is Like (remix)” [song, 1999] (#14156) — _'Nas Is Like' é de Nas, sem remix com Styles P_  
    ↳ web: Wikipedia/WhoSampled: 'Nas Is Like' e de Nas prod. DJ Premier; nao existe remix oficial com Styles P
- **Sheek Louch × DMX** — “What These Bitches Want” [song, 2000] (#14161) — _'What These Bitches Want' é DMX feat Sisqo, não Sheek Louch_  
    ↳ web: Wikipedia: 'What These Bitches Want' e DMX feat. Sisqo, nao Sheek Louch
- **S.H.E × Jay Chou** — “珊瑚海 (Coral Sea)” [song, 2006] (#14175) — _'Coral Sea' é de Jay Chou feat Lara Liang, não S.H.E_  
    ↳ web: WhoSampled/JpopAsia: 'Coral Sea (珊瑚海)' e dueto de Jay Chou com Lara Liang/Veronin, nao S.H.E
- **Ed Sheeran × Yelamos** — “Celestial” [song, 2022] (#14197) — _'Celestial' é só de Ed Sheeran (Pokemon); Yelamos inexistente_  
    ↳ web: Wikipedia: 'Celestial' e de Ed Sheeran (co-escrito com Steve Mac/Johnny McDaid) para Pokemon; 'Yelamos' inexistente
- **Ed Sheeran × Pharrell Williams** — “Feels” [song, 2017] (#14199) — _'Feels' é Calvin Harris feat Pharrell/Katy/Big Sean, sem Ed_  
    ↳ web: Wikipedia: 'Feels' e Calvin Harris feat. Pharrell/Katy Perry/Big Sean; sem Ed Sheeran
- **Sabrina Carpenter × Olivia Rodrigo** — “Skin” [song, 2021] (#14216) — _'Skin' de Sabrina é resposta a Olivia, não colab_  
    ↳ web: BuzzFeed/HollywoodLife: 'Skin' e solo de Sabrina Carpenter, resposta a Olivia Rodrigo, nao colaboracao
- **SZA × Beyoncé** — “SZA on Lemonade” [song, 2016] (#14225) — _título 'SZA on Lemonade' não é uma faixa real_  
    ↳ web: Feats de Lemonade (2016) são Jack White, The Weeknd, James Blake e Kendrick Lamar; SZA não consta e 'SZA on Lemonade' não é faixa real (wikipedia/thefader)
- **Troye Sivan × Years & Years** — “Take Yourself Home” [song, 2020] (#14251) — _'Take Yourself Home' é solo do Troye Sivan, sem Years & Years_  
    ↳ web: 'Take Yourself Home' (2020) é single solo de Troye Sivan, escrito por Leland/Oscar Görres, sem Years & Years (wikipedia/discogs)
- **David Guetta × Eminem** — “Little Bad Girl” [song, 2011] (#14257) — _'Little Bad Girl' é Guetta feat Taio Cruz/Ludacris, não Eminem_  
    ↳ web: 'Little Bad Girl' (2011) é de David Guetta feat. Taio Cruz e Ludacris, sem Eminem (wikipedia/discogs)
- **Future × Gunna** — “Drip Too Hard” [song, 2018] (#14286) — _'Drip Too Hard' é Lil Baby e Gunna, sem Future_  
    ↳ web: 'Drip Too Hard' (2018) é de Lil Baby e Gunna, sem Future (wikipedia/spotify)
- **21 Savage × Cardi B** — “Money Bag” [song, 2018] (#14287) — _'Money Bag' é solo da Cardi B, sem 21 Savage_  
    ↳ web: 'Money Bag' é solo da Cardi B (Invasion of Privacy), sem 21 Savage; colaboração real deles é 'Bartier Cardi' (en.wikipedia.org)
- **21 Savage × Nicki Minaj** — “Bed” [song, 2018] (#14290) — _'Bed' é Nicki Minaj feat Ariana Grande, sem 21 Savage_  
    ↳ web: 'Bed' é Nicki Minaj feat. Ariana Grande (álbum Queen 2018), sem 21 Savage (en.wikipedia.org)
- **Snoop Dogg × Warren G** — “Regulate” [song, 1994] (#14293) — _'Regulate' é Warren G feat Nate Dogg, sem Snoop Dogg_  
    ↳ web: 'Regulate' é Warren G & Nate Dogg 1994, Snoop Dogg não é creditado na faixa (en.wikipedia.org, discogs.com)
- **Snoop Dogg × Lil Jon** — “Drop It Like It's Hot” [song, 2004] (#14294) — _'Drop It Like It's Hot' é Snoop feat Pharrell, sem Lil Jon_  
    ↳ web: 'Drop It Like It's Hot' é Snoop Dogg feat. Pharrell/Neptunes; Lil Jon só no remix, não creditado na original (en.wikipedia.org, discogs.com)
- **Metro Boomin × Cardi B** — “Ric Flair Drip” [song, 2018] (#14301) — _'Ric Flair Drip' é Offset e Metro Boomin, sem Cardi B_  
    ↳ web: 'Ric Flair Drip' é Offset & Metro Boomin (Without Warning 2017), sem Cardi B (en.wikipedia.org, spotify.com)
- **Roddy Ricch × Polo G** — “Pop Out” [song, 2019] (#14307) — _'Pop Out' é Polo G feat Lil Tjay, sem Roddy Ricch_  
    ↳ web: 'Pop Out' é Polo G feat. Lil Tjay 2019, sem Roddy Ricch (en.wikipedia.org, discogs.com)
- **Pharrell Williams × Missy Elliott** — “Pass That Dutch” [song, 2003] (#14317) — _'Pass That Dutch' é da Missy Elliott solo (Timbaland)_  
    ↳ web: 'Pass That Dutch' é solo da Missy Elliott, produzida por Timbaland, sem Pharrell (Wikipedia/Discogs)
- **Marc Anthony × Will Smith** — “Gettin' Jiggy Wit It” [song, 1998] (#14383) — _'Gettin' Jiggy Wit It' é do Will Smith solo, sem Marc Anthony_  
    ↳ web: 'Gettin' Jiggy wit It' é solo de Will Smith, produzida por Poke & Tone, sem Marc Anthony (Wikipedia)
- **Nicki Nicole × Jhay Cortez** — “Ahora Dice” [song, 2022] (#14392) — _'Ahora Dice' é Chris Jeday/Balvin/Ozuna/Arcángel, não Nicki/Jhay_  
    ↳ web: 'Ahora Dice' é de Chris Jeday feat. J Balvin/Ozuna/Arcángel (remix add Anuel/Cardi/Offset), sem Nicki Nicole nem Jhay Cortez (Spotify/letras.com)
- **Emicida × Seu Jorge** — “AmarElo” [song, 2019] (#14404) — _AmarElo tem Majur e Pabllo, não Seu Jorge_  
    ↳ web: 'AmarElo' de Emicida traz Majur e Pabllo Vittar, não Seu Jorge (emicida.bandcamp.com)
- **Caetano Veloso × Gilberto Gil** — “Expresso 2222” [album, 1972] (#14410) — _Expresso 2222 é álbum solo de Gilberto Gil_  
    ↳ web: 'Expresso 2222' é álbum solo de Gilberto Gil (1972), não parceria com Caetano (en.wikipedia.org)
- **Caetano Veloso × David Byrne** — “Nothing Is Going to Stop Us Now” [song, 1989] (#14413) — _título é música do Starship, não Caetano/Byrne_  
    ↳ web: 'Nothing Is Going to Stop Us Now' é do Starship; não existe faixa Caetano/Byrne com esse título (en.wikipedia.org)
- **BTS × Sia** — “Dream Glow” [song, 2019] (#14428) — _Dream Glow é com Charli XCX, não Sia_  
    ↳ web: 'Dream Glow' (BTS World) é com Charli XCX, não Sia (en.wikipedia.org)
- **BTS × Desiigner** — “DNA” [song, 2017] (#14430) — _DNA não tem feat de Desiigner_  
    ↳ web: 'DNA' do BTS não tem Desiigner; ele participou do remix de 'Mic Drop' (en.wikipedia.org)
- **LiSA × Cardi B** — “Money” [song, 2022] (#14432) — _'Money' é da Cardi B; LiSA J-Pop confundida com Lisa Blackpink_  
    ↳ web: 'Money' de Lisa (Blackpink) é solo; Cardi B só citou como favorita, não participa (en.wikipedia.org)
- **LiSA × Doja Cat** — “SG” [song, 2021] (#14433) — _'SG' é single Doja/Ozuna/Lisa Blackpink; LiSA errada_  
    ↳ web: 'SG' é de DJ Snake, Ozuna, Megan Thee Stallion e LISA/Blackpink; sem Doja Cat (en.wikipedia.org)
- **LiSA × Megan Thee Stallion** — “LALISA” [song, 2021] (#14434) — _'LALISA' é da Lisa Blackpink, não LiSA J-Pop_  
    ↳ web: 'LALISA' é single solo de Lisa/Blackpink; feat com Megan é em 'Rapunzel', não LALISA (en.wikipedia.org)
- **Imagine Dragons × Khalid** — “Enemy” [song, 2021] (#14448) — _'Enemy' é com J.I.D, não Khalid_  
    ↳ web: 'Enemy' (2021) é do Imagine Dragons com JID, não Khalid (en.wikipedia.org)
- **Imagine Dragons × Kygo** — “Whatever It Takes” [song, 2017] (#14451) — _'Whatever It Takes' é solo do Imagine Dragons_  
    ↳ web: 'Whatever It Takes' é solo do Imagine Dragons; nenhum remix/colab com Kygo (en.wikipedia.org)
- **Imagine Dragons × Avicii** — “Levels” [song, 2021] (#14452) — _'Levels' é música do Avicii, não colaboração_  
    ↳ web: 'Levels' é single solo do Avicii (2011), sem Imagine Dragons (en.wikipedia.org)
- **Linkin Park × Paul McCartney** — “New Divide” [song, 2009] (#14453) — _'New Divide' é solo do Linkin Park; McCartney absurdo_  
    ↳ web: 'New Divide' (2009) escrita/gravada só pelo Linkin Park, produzida por Mike Shinoda, sem McCartney (en.wikipedia.org)
- **Linkin Park × Steven Tyler** — “Iridescent” [song, 2011] (#14455) — _'Iridescent' é solo do Linkin Park_  
    ↳ web: 'Iridescent' é faixa solo do Linkin Park em A Thousand Suns, sem Steven Tyler (en.wikipedia.org)
- **Fall Out Boy × Elton John** — “Young and Menace” [song, 2017] (#14456) — _'Young and Menace' é solo do Fall Out Boy_  
    ↳ web: 'Young and Menace' (2017) escrita/performada só pelo Fall Out Boy, sem Elton John (en.wikipedia.org)
- **Fall Out Boy × Sirah** — “My Songs Know What You Did in the Dark” [song, 2013] (#14461) — _'My Songs Know...' é solo; Sirah é ligada a Skrillex_  
    ↳ web: 'My Songs Know...' original é solo do Fall Out Boy; remix tem 2 Chainz, não Sirah (en.wikipedia.org)
- **Måneskin × Damiano David** — “Beggin'” [song, 2021] (#14466) — _Damiano David é o próprio vocalista do Måneskin_  
    ↳ web: Damiano David é o próprio vocalista do Måneskin; 'Beggin'' é da banda, não colab (en.wikipedia.org)
- **Don Omar × J. Balvin** — “Ella y Yo” [song, 2011] (#14714) — _Ella y Yo é de Don Omar com Aventura, não J Balvin_  
    ↳ web: Wikipedia/Spotify: 'Ella y Yo' é de Aventura feat. Don Omar (2004-05), J. Balvin não participa
- **Christina Aguilera × Nicki Minaj** — “Primadonna (Remix)” [song, 2012] (#14724) — _Primadonna é de Marina; remix com Aguilera/Nicki não existe_  
    ↳ web: Apple/Spotify: 'Primadonna' é de Marina and The Diamonds; não existe remix com Christina Aguilera/Nicki Minaj
- **Christina Aguilera × Cardi B** — “Sault” [song, 2019] (#14730) — _'Sault' não é faixa de Aguilera com Cardi B; fabricação_  
    ↳ web: Wikipedia (Liberation): Aguilera lamentou não ter tido Cardi B no álbum; não existe faixa 'Sault' entre elas
- **Léo Santana × Parangolé** — “Galinha Pintadinha” [song, 2019] (#14758) — _Galinha Pintadinha não é faixa de Léo Santana com Parangolé_  
    ↳ web: Wikipedia: 'Galinha Pintadinha' é marca infantil de Juliano Prado/Marcos Luporini (voz Vera Fuzaro), não faixa de Léo Santana com Parangolé
- **Seu Jorge × David Bowie** — “Rebel Rebel” [song, 2004] (#15026) — _cover solo de Bowie, não colaboração real_  
    ↳ web: Wikipedia/Rolling Stone: 'Rebel Rebel' é cover solo de Seu Jorge (Life Aquatic, 2004); Bowie não participa da gravação
- **Rosé × The Weeknd** — “One of the Girls” [song, 2023] (#15050) — _'One of the Girls' é The Weeknd/JENNIE/Lily-Rose Depp, não Rosé_  
    ↳ web: 'One of the Girls' é The Weeknd com JENNIE e Lily-Rose Depp; Rosé não participa (Wikipedia/Discogs)
- **Rosé × Pharrell Williams** — “ROSÉ and Bruno Mars album” [song, 2024] (#15052) — _título genérico fabricado, não é música real_  
    ↳ web: Colab Rosé/Bruno Mars é 'APT.' (2024); título é fabricado e Pharrell não é colaborador da faixa (Wikipedia/Billboard)
- **Green Day × Fall Out Boy** — “Punk Rock Almanac” [song, 2022] (#15075) — _título fabricado, não é música real com Fall Out Boy_  
    ↳ web: Nenhuma música 'Punk Rock Almanac' de Green Day com Fall Out Boy existe; título fabricado (busca web/Wikipedia)
- **Wizkid × Swae Lee** — “Ginger” [song, 2020] (#15082) — _'Ginger' é Wizkid feat. Burna Boy, não Swae Lee_  
    ↳ web: 'Ginger' (Made in Lagos) é Wizkid feat. Burna Boy, não Swae Lee (Wikipedia/Spotify)
- **Shawn Mendes × Teddy Swims** — “Summer of Love” [song, 2021] (#15116) — _'Summer of Love' é Shawn Mendes e Tainy, não Teddy Swims_  
    ↳ web: 'Summer of Love' (2021) é Shawn Mendes e Tainy, não Teddy Swims (Wikipedia/Spotify)
- **Demi Lovato × will.i.am** — “That Power” [song, 2013] (#15121) — _#thatPOWER é do will.i.am com Justin Bieber, não Demi_  
    ↳ web: '#thatPOWER' é will.i.am feat. Justin Bieber 2013, sem Demi Lovato (en.wikipedia.org, spotify.com)
- **Frank Ocean × Kanye West** — “New Magic Wand” [song, 2013] (#15138) — _'New Magic Wand' é do Tyler, não Frank/Kanye_  
    ↳ web: 'New Magic Wand' é de Tyler, the Creator feat. A$AP Rocky/Santigold (IGOR 2019); Frank/Kanye em outras faixas, não nesta (en.wikipedia.org)
- **Frank Ocean × Drake** — “Thinking About You (feat. Drake)” [song, 2016] (#15140) — _'Thinking Bout You' não tem feature de Drake_  
    ↳ web: 'Thinkin Bout You' é solo de Frank Ocean (Channel Orange 2012), sem feature de Drake (en.wikipedia.org)
- **Frank Ocean × Kendrick Lamar** — “Complexion (A Zulu Love)” [song, 2015] (#15142) — _'Complexion' é do Kendrick, não Frank_  
    ↳ web: 'Complexion (A Zulu Love)' é Kendrick Lamar feat. Rapsody (To Pimp a Butterfly 2015), não Frank Ocean (spotify.com, music.apple.com)
- **Calvin Harris × Halsey** — “Pray to God” [song, 2015] (#15165) — _'Pray to God' é com HAIM, não Halsey_  
    ↳ web: 'Pray to God' é Calvin Harris feat. HAIM 2015, não Halsey (en.wikipedia.org, discogs.com)
- **Major Lazer × Beyoncé** — “Run the World (Girls) Remix” [song, 2011] (#15171) — _remix de 'Run the World' por Major Lazer não existe_  
    ↳ web: 'Run the World (Girls)' apenas faz sample de 'Pon de Floor' do Major Lazer; não existe remix oficial em colaboração (whosampled.com, wikipedia)
- **Tiësto × Bia** — “Jackie Chan” [song, 2018] (#15185) — _Bia não participa de 'Jackie Chan'_  
    ↳ web: 'Jackie Chan' é creditada a Tiësto, Dzeko, Preme e Post Malone; Bia não participa (wikipedia, spotify)
- **Travis Scott × Cardi B** — “Beibs in the Trap” [song, 2017] (#15205) — _'Beibs in the Trap' é com Nav, não Cardi B_  
    ↳ web: 'Beibs in the Trap' de Travis Scott é feat. NAV, não Cardi B (wikipedia, whosampled)
- **Lil Durk × SZA** — “TIKE” [song, 2023] (#15213) — _música inexistente entre os dois_  
    ↳ web: HipHopDX/Wikipedia: Durk pediu SZA publicamente; sem colab lançada, 'TIKE' inexistente
- **Eminem × 50 Cent** — “Jimmy, Brian and Mike” [song, 2018] (#15222) — _música inexistente_  
    ↳ web: eminem.com/Songfacts: 'Jimmy, Brian and Mike' é solo do Eminem, sem 50 Cent
- **A$AP Rocky × Florence Welch** — “M's” [song, 2015] (#15225) — _M'$ é solo do Rocky, sem Florence_  
    ↳ web: Wikipedia: 'M'$' feat. Lil Wayne; colab Rocky+Florence Welch é 'I Come Apart'
- **DaBaby × Future** — “Jumpin on a Jet” [song, 2019] (#15236) — _Jumpin on a Jet é solo do Future_  
    ↳ web: Wikipedia: 'Jumpin on a Jet' é single solo do Future (The Wizrd), sem DaBaby
- **Wiz Khalifa × Amber Rose** — “No Sleep” [song, 2011] (#15251) — _No Sleep é solo do Wiz_  
    ↳ web: Wikipedia: 'No Sleep' é solo do Wiz Khalifa; Amber Rose só aparece no videoclipe, não é artista
- **Wiz Khalifa × Abra** — “Bad Together” [song, 2018] (#15252) — _fabricação cross-cultural_  
    ↳ web: Dua Lipa Wiki: único 'Bad Together' é da Dua Lipa; sem colaboração Wiz Khalifa x Abra
- **Wiz Khalifa × IZ*ONE** — “Feel Special” [song, 2019] (#15253) — _Feel Special é do TWICE_  
    ↳ web: Wikipedia: 'Feel Special' é single do TWICE (2019), não Wiz Khalifa/IZ*ONE
- **Rick Ross × Usher** — “Sanctified” [song, 2014] (#15257) — _Sanctified é com Kanye/Big Sean_  
    ↳ web: Wikipedia/Spotify: 'Sanctified' credita Rick Ross ft Kanye West & Big Sean, não Usher
- **Rick Ross × Foxy Brown** — “The Devil Is a Lie” [song, 2014] (#15260) — _Devil Is a Lie é com Jay-Z_  
    ↳ web: Wikipedia/Spotify: 'The Devil Is a Lie' é Rick Ross ft Jay-Z, não Foxy Brown
- **Rick Ross × Wale** — “Lotus Flower Bomb” [song, 2012] (#15263) — _Lotus Flower Bomb é Wale ft Miguel_  
    ↳ web: Wikipedia/Spotify: 'Lotus Flower Bomb' é Wale ft Miguel, não Rick Ross
- **Daddy Yankee × Wisin** — “Noche de Sexo” [song, 2007] (#15275) — _Noche de Sexo é Wisin & Yandel/Aventura_  
    ↳ web: AllMusic: 'Noche de Sexo' é Wisin & Yandel ft Aventura, não Daddy Yankee
- **Daddy Yankee × Bad Bunny** — “MIA” [song, 2018] (#15277) — _MIA é Bad Bunny ft Drake_  
    ↳ web: Wikipedia/Spotify: 'MIA' é Bad Bunny ft Drake, não Daddy Yankee
- **Daddy Yankee × Becky G** — “Sin Pijama” [song, 2018] (#15281) — _Sin Pijama é Becky G x Natti Natasha_  
    ↳ web: Wikipedia: 'Sin Pijama' é Becky G & Natti Natasha; Daddy Yankee só produziu/co-escreveu, não é intérprete
- **Feid × J. Balvin** — “Unforgettable” [song, 2021] (#15283) — _Unforgettable é French Montana_  
    ↳ web: Wikipedia/Spotify: 'Unforgettable' é French Montana ft Swae Lee, não Feid/J. Balvin
- **Feid × Paulo Londra** — “Adan y Eva” [song, 2023] (#15285) — _Adán y Eva é solo do Paulo Londra_  
    ↳ web: Wikipedia/Spotify: 'Adán y Eva' é solo de Paulo Londra (2018); colab real Feid x Londra é 'A Veces'
- **Ricky Martin × Jennifer Lopez** — “No Me Ames” [song, 1999] (#15299) — _No Me Ames é Marc Anthony x JLo_  
    ↳ web: Wikipedia/Discogs: 'No Me Ames' é dueto Jennifer Lopez com Marc Anthony (1999), sem Ricky Martin
- **Ricky Martin × Pitbull** — “Rain Over Me” [song, 2011] (#15302) — _Rain Over Me é Pitbull feat. Marc Anthony, não Ricky Martin_  
    ↳ web: 'Rain Over Me' (2011) é Pitbull feat. Marc Anthony, não Ricky Martin (en.wikipedia.org/discogs)
- **Matuê × L7nnon** — “Deu Onda” [song, 2021] (#15326) — _Deu Onda é Matuê solo, não colab com L7nnon_  
    ↳ web: 'Deu Onda' é de MC G15 (2017); colab real Matuê x L7nnon é 'Sem Dó' (2021), não 'Deu Onda' (spotify/apple music)
- **Racionais MC's × NX Zero** — “Não Deixe o Samba Morrer” [song, 2006] (#15351) — _Não Deixe o Samba Morrer não é colab Racionais x NX Zero_  
    ↳ web: 'Não Deixe o Samba Morrer' é samba de Edson Conceição/Aloísio Silva gravado por Alcione (1975), não colab Racionais x NX Zero (pt.wikipedia.org)
- **Coldplay × Kylie Minogue** — “Somewhere Only We Know” [song, 2003] (#15366) — _Somewhere Only We Know é Keane, não Coldplay x Kylie_  
    ↳ web: 'Somewhere Only We Know' (2004) é do Keane, não Coldplay x Kylie Minogue (en.wikipedia.org/discogs)
- **Coldplay × Kanye West** — “Homecoming” [song, 2007] (#15369) — _Homecoming é Kanye feat. Chris Martin, não crédito a Coldplay_  
    ↳ web: 'Homecoming' é creditada como Kanye West feat. Chris Martin (individual), não à banda Coldplay (en.wikipedia.org)
- **Gorillaz × Anthony Hamilton** — “Hallelujah Money” [song, 2017] (#15379) — _Hallelujah Money é com Benjamin Clementine, não Anthony Hamilton_  
    ↳ web: 'Hallelujah Money' dos Gorillaz é feat. Benjamin Clementine, não Anthony Hamilton (en.wikipedia.org)
- **Davido × Summer Walker** — “Know Yourself” [song, 2020] (#15390) — _'Know Yourself' é do Drake; não há colaboração Davido feat. Summer Walker com esse título_  
    ↳ web: Spotify/YouTube: colab real Davido+Summer Walker e 'D & G'; 'Know Yourself' e do Drake
- **Luke Combs × Ray Charles** — “Better Together (Remix)” [song, 2021] (#15404) — _Ray Charles morreu em 2004; remix 2021 com Luke Combs impossível_  
    ↳ web: Wikipedia: 'Better Together' e solo de Luke Combs (2020); nao existe remix/dueto com Ray Charles
- **Billie Eilish × Lil Nas X** — “Kid Laroi, Juice WRLD type” [song, 2019] (#15419) — _título placeholder 'type' fabricado; não é música real Eilish/Lil Nas X_  
    ↳ web: Busca: titulo 'Kid Laroi, Juice WRLD type' e placeholder; nao ha colaboracao Billie Eilish/Lil Nas X documentada
- **Billie Eilish × Childish Gambino** — “Waiting for a Girl Like You” [song, 2017] (#15422) — _'Waiting for a Girl Like You' é do Foreigner; não há dueto Eilish/Gambino_  
    ↳ web: 'Waiting for a Girl Like You' é do Foreigner; sem dueto Eilish/Gambino (Billboard/NME)
- **Camila Cabello × Madonna** — “Bitch I'm Loca” [song, 2019] (#15437) — _'Bitch I'm Madonna' é da Madonna com Nicki Minaj, não Camila Cabello_  
    ↳ web: 'Bitch I'm Loca' é da Madonna feat. Maluma, não Camila Cabello (Spotify/Madonna.com)
- **SZA × FEAR.** — “20 Min” [song, 2017] (#15454) — _'20 Min' é faixa solo da SZA no Ctrl; 'FEAR.' não é artista_  
    ↳ web: '20 Min' é faixa solo da SZA no Ctrl; 'FEAR.' é música do Kendrick, não artista (Wikipedia)
- **SZA × Bob Dylan** — “When I Get Home” [song, 2019] (#15458) — _'When I Get Home' é álbum de Solange, não colaboração SZA/Bob Dylan_  
    ↳ web: 'When I Get Home' é álbum da Solange (2019); sem colaboração SZA/Bob Dylan (Wikipedia)
- **Usher × Gunna** — “Standing Next to You (Remix)” [song, 2024] (#15472) — _'Standing Next to You' é do Jungkook (BTS); remix Usher/Gunna fabricado_  
    ↳ web: 'Standing Next to You (Remix)' é do Jungkook feat. Usher, sem Gunna (Rolling Stone/NME)
- **Alicia Keys × Pharrell Williams** — “100 Days 100 Nights” [song, 2007] (#15474) — _'100 Days 100 Nights' é de Sharon Jones; não é dueto Alicia Keys/Pharrell_  
    ↳ web: '100 Days, 100 Nights' é da Sharon Jones & The Dap-Kings (2007), não Alicia Keys/Pharrell (Wikipedia)
- **Nicki Nicole × Peso Pluma** — “La Bebe (Remix)” [song, 2023] (#15664) — _La Bebe Remix é de Peso Pluma com Yng Lvcas, não Nicki Nicole_  
    ↳ web: 'La Bebe (Remix)' é de Yng Lvcas com Peso Pluma, sem Nicki Nicole (spotify, billboard)
- **Nicki Nicole × Myke Towers** — “Rae Sremmurd (Remix)” [song, 2021] (#15666) — _título 'Rae Sremmurd (Remix)' não é faixa desses artistas_  
    ↳ web: Colab real Nicki Nicole+Myke Towers é 'Ella No Es Tuya (Remix)' com Rochy RD; 'Rae Sremmurd (Remix)' não existe deles (billboard, apple music)
- **Caetano Veloso × Chet Baker** — “My Funny Valentine (Live)” [live, 1987] (#15683) — _dueto ao vivo com Chet Baker improvável e não documentado_  
    ↳ web: Caetano admirava Chet Baker como influência, mas não há dueto/gravação 'My Funny Valentine' juntos (allmusic, worldmusiccentral)
- **MC Kevinho × Gloria Groove** — “Olha a Explosão” [song, 2018] (#15688) — _Olha a Explosão é de MC Kevinho sozinho, não com Gloria Groove_  
    ↳ web: 'Olha a Explosão' é solo de MC Kevinho; remix oficial tem 2 Chainz/French Montana/Nacho, sem Gloria Groove (spotify, umusicbrazil)
- **LiSA × LALISA** — “Money” [song, 2021] (#15701) — _confunde LiSA com LALISA; Money é de Lisa do BLACKPINK, não LiSA J-Pop_  
    ↳ web: 'Money' é faixa solo de Lisa (BLACKPINK) do álbum LALISA; não é colab de dois artistas distintos, LiSA J-Pop não envolvida (en.wikipedia Money Lisa song)
- **LiSA × Tyga** — “1+1” [song, 2022] (#15702) — _colaboração LiSA J-Pop com Tyga improvável e não documentada_  
    ↳ web: Não existe colab '1+1' de nenhuma LiSA com Tyga; Tyga tem '1 of 1' solo de 2016 (wikipedia, hotnewhiphop)
- **LiSA × Cardi B** — “Money (Remix)” [song, 2022] (#15703) — _Money Remix é de Lisa BLACKPINK; atribuição a LiSA J-Pop é fabricação_  
    ↳ web: 'Money' é solo de Lisa (BLACKPINK); remix com Cardi B só existe em mashups fanmade, não oficial com LiSA J-Pop (youtube fan edits, wikipedia)
- **LiSA × Fred again..** — “ROCKSTAR” [song, 2023] (#15704) — _ROCKSTAR é de Lisa BLACKPINK; confusão com LiSA J-Pop_  
    ↳ web: 'Rockstar' é solo de Lisa (BLACKPINK), escrita por Lisa/Ryan Tedder/Sam Homaee etc., sem Fred again.. (en.wikipedia Rockstar Lisa song)
- **LiSA × Rema** — “LALISA” [song, 2024] (#15706) — _LALISA é de Lisa BLACKPINK; título e artista trocados_  
    ↳ web: 'LALISA' é single solo de Lisa (2021) sem Rema; colab real Lisa+Rema é 'Goals' 2026 com Anitta (wikipedia Goals song, billboard)
- **Jackson Wang × Internet Money** — “100 Ways” [song, 2022] (#15710) — _100 Ways é de Jackson Wang sozinho, não com Internet Money_  
    ↳ web: '100 Ways' é single solo de Jackson Wang (2020); a colab dele com Internet Money é 'Drive You Home' (nme.com/spotify)
- **Agust D × HYBE** — “Amygdala” [song, 2023] (#15713) — _HYBE é gravadora, não artista; não é colaboração_  
    ↳ web: 'Amygdala' de Agust D (D-DAY 2023) credita EL CAPITXN, não HYBE, que é a gravadora, não artista (discogs/albumoftheyear)
- **Linkin Park × Nas** — “Collision Course” [album, 2004] (#15722) — _Collision Course é com Jay-Z, não Nas_  
    ↳ web: 'Collision Course' (2004) é EP de Linkin Park com Jay-Z, não Nas (en.wikipedia.org/discogs)
- **Linkin Park × Eminem** — “Collision Course (Track)” [song, 2004] (#15723) — _Collision Course é com Jay-Z, não Eminem_  
    ↳ web: 'Collision Course' (2004) é mash-up de Linkin Park com Jay-Z, não Eminem (en.wikipedia.org/discogs)
- **Linkin Park × Frank Zappa** — “Drawbar” [song, 2010] (#15724) — _Drawbar é instrumental de Linkin Park com Tom Morello, não Frank Zappa_  
    ↳ web: 'Drawbar' (The Hunting Party 2014) é instrumental de Linkin Park feat. Tom Morello, não Frank Zappa (linkinpedia/spotify)
- **Fall Out Boy × Machine Gun Kelly** — “My Body Is a Cage” [song, 2020] (#15729) — _My Body Is a Cage é do Arcade Fire, não faixa Fall Out Boy com MGK_  
    ↳ web: 'My Body Is a Cage' é do Arcade Fire (Neon Bible 2007); não há faixa Fall Out Boy com MGK com esse título (spotify/wikipedia)
- **Måneskin × Post Malone** — “If I Can Dream” [song, 2021] (#15737) — _If I Can Dream é cover de Elvis; colab Måneskin com Post Malone improvável_  
    ↳ web: 'If I Can Dream' (Elvis soundtrack) é cover solo do Måneskin, sem Post Malone (loudersound/spotify)
- **Carrie Underwood × Sam Hunt** — “If I Didn't Love You” [song, 2021] (#15761) — _a música é com Jason Aldean, não Sam Hunt_  
    ↳ web: Wikipedia: 'If I Didn't Love You' é dueto de Jason Aldean e Carrie Underwood, não Sam Hunt
- **Beyoncé × Tems** — “ALREADY” [song, 2020] (#15770) — _ALREADY é com Shatta Wale, não Tems_  
    ↳ web: Wikipedia: 'ALREADY' credita Beyoncé, Shatta Wale e Major Lazer, não Tems
- **Beyoncé × Childish Gambino** — “ALREADY” [song, 2020] (#15771) — _ALREADY não é com Childish Gambino_  
    ↳ web: Wikipedia: 'ALREADY' credita Beyoncé, Shatta Wale e Major Lazer, não Childish Gambino
- **Bruno Mars × Hozier** — “Too Good at Goodbyes (Live)” [live, 2018] (#15792) — _música é de Sam Smith, não de Bruno Mars_  
    ↳ web: 'Too Good at Goodbyes' é de Sam Smith; sem registro de versão ao vivo Bruno Mars/Hozier
- **Meghan Trainor × Nicki Minaj** — “Better When I'm Dancin'” [song, 2015] (#15813) — _Better When I'm Dancin' não é feat de Nicki Minaj_  
    ↳ web: Wikipedia: 'Better When I'm Dancin'' é solo de Meghan Trainor, sem feat de Nicki Minaj
- **Meghan Trainor × Earth, Wind & Fire** — “Can't Stop the Feeling (Remix)” [song, 2016] (#15814) — _Can't Stop the Feeling é de Justin Timberlake_  
    ↳ web: Wikipedia: 'Can't Stop the Feeling!' é de Justin Timberlake, não remix Meghan Trainor/EWF
- **Skrillex × Porter Robinson** — “Sad Machine” [song, 2014] (#15892) — _'Sad Machine' é solo de Porter Robinson, sem Skrillex_  
    ↳ web: Wikipedia/RateYourMusic: 'Sad Machine' é solo de Porter Robinson (com vocal Avanna), sem Skrillex nos créditos
- **Alan Walker × Martin Garrix** — “Tired” [song, 2017] (#15896) — _'Tired' é com Gavin James, não Martin Garrix_  
    ↳ web: Wikipedia/Discogs: 'Tired' (2017) é Alan Walker feat. Gavin James, não Martin Garrix
- **Kendrick Lamar × Swizz Beatz** — “Pray for Me” [song, 2022] (#15905) — _'Pray for Me' é com The Weeknd, não Swizz Beatz_  
    ↳ web: Wikipedia/Spotify: 'Pray for Me' é The Weeknd com Kendrick Lamar (Black Panther), Swizz Beatz não participa
- **Lil Wayne × Big Sean** — “My Last” [song, 2011] (#15925) — _'My Last' é com Chris Brown, não Lil Wayne_  
    ↳ web: Discogs/Wikipedia: 'My Last' (2011) é Big Sean feat. Chris Brown, não Lil Wayne
- **Offset × Gunna** — “Drip Season 3” [album, 2018] (#15967) — _Drip Season 3 é mixtape solo de Gunna, não com Offset_  
    ↳ web: Wikipedia/HipHopDX: 'Drip Season 3' é mixtape solo de Gunna (feats: Lil Durk, Nav, Yachty), sem Offset
- **BLACKPINK × Halsey** — “The Album (feature)” [feature, 2020] (#16112) — _Halsey não participa de The Album da BLACKPINK_  
    ↳ web: Wikipedia/Consequence: The Album traz Selena Gomez e Cardi B como convidadas, nao Halsey
- **BLACKPINK × Tyga** — “Taste (Remix)” [song, 2018] (#16113) — _Taste é de Tyga solo, sem BLACKPINK_  
    ↳ web: Spotify/YouTube: 'Taste' de Tyga tem feat. Offset, sem BLACKPINK
- **BLACKPINK × David Guetta** — “Boom” [song, 2020] (#16115) — _Boom não é colaboração BLACKPINK x David Guetta_  
    ↳ web: Dancing Astronaut/We Rave You: colaboracao BLACKPINK x David Guetta foi 'Lovesick Girls', nao existe 'Boom'
- **Jennie × FKA twigs** — “One of the Girls” [song, 2023] (#16121) — _One of the Girls não tem FKA twigs_  
    ↳ web: Wikipedia/Rolling Stone: 'One of the Girls' credita The Weeknd, Jennie e Lily-Rose Depp, sem FKA twigs
- **Jennie × Caroline Polachek** — “Mantra” [song, 2024] (#16123) — _Mantra é de Jennie solo, sem Caroline Polachek_  
    ↳ web: Wikipedia: 'Mantra' e single solo de Jennie (comp. Jennie, Claudia Valentina, Zikai), sem Caroline Polachek
- **J-Hope × Nicki Minaj** — “Killin It (Remix)” [song, 2022] (#16134) — _remix Killin It com Nicki Minaj inexistente_  
    ↳ web: Spotify/Weverse: single de j-hope e 'Killin' It Girl' feat. GloRilla, remix com Nicki Minaj inexistente
- **J-Hope × Lil Nas X** — “Old Town Road (Live)” [live, 2019] (#16136) — _J-Hope não fez Old Town Road ao vivo com Lil Nas X_  
    ↳ web: Spotify/NPR: remix 'Seoul Town Road' de Old Town Road tem RM do BTS, nao J-Hope
- **J-Hope × MAX** — “Chicken Noodle Soup” [song, 2019] (#16137) — _Chicken Noodle Soup é com Becky G, não MAX_  
    ↳ web: Wikipedia/Billboard: 'Chicken Noodle Soup' de j-hope traz feat. Becky G, nao MAX
- **Maroon 5 × Kid Cudi** — “Beautiful Goodbye” [song, 2012] (#16141) — _Beautiful Goodbye é Maroon 5 solo, sem Kid Cudi_  
    ↳ web: AllMusic/WhoSampled: 'Beautiful Goodbye' e do Maroon 5 (Overexposed), escrita por Levine/Malik/Blanco, sem Kid Cudi
- **Red Hot Chili Peppers × Neil Young** — “Give Me One Reason (Live)” [live, 2014] (#16144) — _Give Me One Reason é de Tracy Chapman, não RHCP/Neil Young_  
    ↳ web: Wikipedia/Hollywood Reporter: 'Give Me One Reason' e de Tracy Chapman; RHCP e Neil Young tocaram 'Everybody Knows This Is Nowhere' no benefit
- **Red Hot Chili Peppers × Danger Mouse** — “Blood Sugar Sex Magik (Remix)” [song, 2007] (#16146) — _remix de Blood Sugar Sex Magik com Danger Mouse inexistente_  
    ↳ web: Wikipedia/readdork: Danger Mouse produziu 'The Getaway' (2016); 'Blood Sugar Sex Magik' (1991) foi produzido por Rick Rubin, remix inexistente
- **Panic! at the Disco × Weezer** — “Death of a Bachelor (Live)” [live, 2017] (#16152) — _Death of a Bachelor ao vivo com Weezer improvável_  
    ↳ web: Wikipedia/Discogs: 'Death of a Bachelor' e faixa solo do Panic!; gravacao ao vivo do tour e solo, sem Weezer
- **Panic! at the Disco × Lil Wayne** — “Emperor's New Clothes (Live)” [live, 2018] (#16153) — _Emperor's New Clothes ao vivo com Lil Wayne inexistente_  
    ↳ web: Sem colaboração oficial Panic!/Lil Wayne; só mashups de fãs (spin.com, youtube)
- **The 1975 × Greta Van Fleet** — “The Sound (Live)” [live, 2019] (#16155) — _The Sound ao vivo com Greta Van Fleet improvável_  
    ↳ web: 'The Sound' é do The 1975 solo (live MSG 2022); sem colab com Greta Van Fleet (só line-up de festival, wikipedia)
- **Burna Boy × Coldplay** — “My Universe (Remix)” [song, 2021] (#16160) — _My Universe é Coldplay x BTS, não Burna Boy_  
    ↳ web: 'My Universe' é Coldplay x BTS; remixes são SUGA/Galantis/Guetta, não Burna Boy (Wikipedia/Spotify)
- **Burna Boy × Diddy** — “Act Now” [song, 2019] (#16164) — _Act Now com Diddy improvável/inexistente_  
    ↳ web: Colab real Diddy/Burna Boy é 'Act Like You Got It' (2023), não 'Act Now' 2019 (Spotify/Apple Music)
- **Asake × Ludmilla** — “Dance (Remix)” [song, 2023] (#16179) — _remix Dance com Ludmilla cruzando gêneros improvável_  
    ↳ web: Colab real Asake x Ludmilla é 'Whine' (2024), não 'Dance' 2023 (Spotify/YouTube)
- **Rihanna × Ne-Yo** — “Barbados Girl” [song, 2008] (#16184) — _Barbados Girl não é música conhecida de Rihanna x Ne-Yo_  
    ↳ web: Não existe 'Barbados Girl'; Ne-Yo escreveu 'Unfaithful' para Rihanna (Wikipedia)
- **Rihanna × Slash** — “Mother Nature” [song, 2010] (#16187) — _Mother Nature com Slash não é música de Rihanna_  
    ↳ web: Colab real Rihanna x Slash é 'Rockstar 101' (2010), não 'Mother Nature' (Wikipedia/Spotify)
- **The Weeknd × DaBaby** — “Heartless” [song, 2019] (#16190) — _Heartless é The Weeknd solo, sem DaBaby_  
    ↳ web: 'Heartless' é The Weeknd solo; remix feat. Lil Uzi Vert, não DaBaby (Wikipedia/Spotify)
- **The Weeknd × J. Cole** — “The Zone” [song, 2011] (#16191) — _The Zone é The Weeknd com Drake, não J. Cole_  
    ↳ web: 'The Zone' é The Weeknd feat. Drake (2011), não J. Cole (Wikipedia/Spotify)
- **The Weeknd × Young Thug** — “Wanderlust” [song, 2021] (#16192) — _Wanderlust é The Weeknd solo, sem Young Thug_  
    ↳ web: 'Wanderlust' é The Weeknd solo (2013, remix feat. Pharrell); colab com Young Thug é 'Better Believe' (Wikipedia)
- **Lady Gaga × Akon** — “Just Dance” [song, 2008] (#16193) — _Just Dance é com Colby O'Donis, não Akon como par creditado_  
    ↳ web: 'Just Dance' credita feat. Colby O'Donis; Akon foi co-autor/vocais não creditados, não o par creditado (Wikipedia)
- **Lady Gaga × Celine Dion** — “I'll Never Love Again” [song, 2018] (#16197) — _I'll Never Love Again é Lady Gaga solo, sem Celine Dion_  
    ↳ web: 'I'll Never Love Again' é Lady Gaga (e Bradley Cooper no filme); Celine Dion não participou (Wikipedia)
- **Charlie Puth × Danielle** — “That's Hilarious” [song, 2021] (#16199) — _That's Hilarious é Charlie Puth solo; Danielle não é colaboradora_  
    ↳ web: Wikipedia/Songfacts: 'That's Hilarious' é solo de Charlie Puth, sem Danielle
- **Sam Smith × Lay** — “Thunder” [song, 2020] (#16211) — _par improvável, feature Sam Smith x Lay não existe_  
    ↳ web: Nenhuma faixa 'Thunder' de Sam Smith 2020 nem feature com Lay Zhang; inexistente (wikipedia.org)
- **J. Cole × TLC** — “Crocodile Toothpaste” [song, 2017] (#16260) — _'Crocodile Toothpaste' não é faixa real de J. Cole x TLC_  
    ↳ web: A faixa real é 'Crocodile Tearz' de J. Cole (solo, 2024); não existe 'Crocodile Toothpaste' com TLC (wikipedia.org)
- **J. Cole × Young Thug** — “Thotiana (Remix)” [song, 2019] (#16262) — _'Thotiana Remix' é Blueface/Cardi, não J. Cole x Young Thug_  
    ↳ web: 'Thotiana (Remix)' é de Blueface feat. Cardi B & YG, não J. Cole x Young Thug (spotify.com, music.apple.com)
- **Cardi B × Chance the Rapper** — “Best Part” [song, 2018] (#16264) — _'Best Part' é Daniel Caesar feat. H.E.R., não Cardi x Chance_  
    ↳ web: 'Best Part' é de Daniel Caesar feat. H.E.R. (2017), não Cardi B x Chance (wikipedia.org)
- **Post Malone × Halsee** — “Only Wanna Be With You” [song, 2019] (#16274) — _'Only Wanna Be With You' é solo de Post Malone; 'Halsee' fabricado_  
    ↳ web: 'Only Wanna Be With You (Pokémon 25)' é cover solo de Post Malone, sem feature; 'Halsee' inexistente (bulbapedia.bulbagarden.net)
- **Post Malone × Young Thug** — “Scared to Be Lonely (Remix)” [song, 2017] (#16275) — _'Scared to Be Lonely' é Martin Garrix/Dua Lipa, não Post x Thug_  
    ↳ web: 'Scared to Be Lonely' é de Martin Garrix feat. Dua Lipa, não Post Malone x Young Thug (wikipedia.org)
- **Marcelo D2 × Racionais MC's** — “Sobrevivendo no Inferno (Clipe)” [song, 2017] (#16444) — _'Sobrevivendo no Inferno' é álbum dos Racionais, não colab com D2_  
    ↳ web: Discogs/YouTube: 'Sobrevivendo no Inferno' (1997) é álbum solo do Racionais MC's, não clipe/colab com Marcelo D2 (havia até desavença)
- **Jung Kook × Major Lazer** — “We Don't Talk About That” [song, 2023] (#16448) — _faixa Jung Kook-Major Lazer inexistente_  
    ↳ web: Spotify/Rolling Stone: colab real Jung Kook x Major Lazer é 'Closer to You' (Golden, 2023); 'We Don't Talk About That' inexistente
- **Rosé × Lady Gaga** — “FLOWER” [song, 2024] (#16451) — _'FLOWER' é solo da Rosé, não colab com Lady Gaga_  
    ↳ web: Wikipedia: 'FLOWER' (2023) é single solo de Jisoo (não Rosé) e sem Lady Gaga
- **Rosé × Jennie** — “BLACKPINK 2024 Collab” [song, 2024] (#16452) — _título genérico fabricado 'BLACKPINK 2024 Collab'_  
    ↳ web: Billboard/Wikipedia: em 2024 Rosé ('rosie') e Jennie ('Mantra') só lançaram solos; nenhuma faixa conjunta 'BLACKPINK 2024 Collab'
- **NIKI × Jackson Wang** — “Drive (Remix)” [song, 2021] (#16455) — _'Drive' remix NIKI-Jackson Wang inexistente_  
    ↳ web: Spotify/NME: colab real NIKI x Jackson Wang é 'California (Remix)' (2021); nenhum 'Drive (Remix)' entre eles
- **RM × Erykah Badu** — “Bicycle” [song, 2022] (#16458) — _'Bicycle' é single solo de RM, não colab com Erykah Badu_  
    ↳ web: Wikipedia/Billboard: 'Bicycle' é RM solo; Erykah Badu aparece em 'Yun' do Indigo, não em 'Bicycle'
- **RM × Anderson .Paak** — “POP/STARS” [song, 2019] (#16459) — _'POP/STARS' é K/DA, não colab RM-Anderson .Paak_  
    ↳ web: Wikipedia/Discogs: 'POP/STARS' é K/DA feat. Madison Beer, (G)I-DLE, Jaira Burns; sem RM/Anderson .Paak
- **OneRepublic × Katy Perry** — “Wild@Heart” [song, 2021] (#16464) — _colaboração OneRepublic-Katy Perry inexistente_  
    ↳ web: Wikipedia (Human): OneRepublic tem 'Wild Life', não 'Wild@Heart'; nenhuma colab OneRepublic-Katy Perry existe
- **OneRepublic × DJ Shadow** — “I'll Be Missing You” [song, 2019] (#16465) — _'I'll Be Missing You' é Puff Daddy, não OneRepublic-DJ Shadow_  
    ↳ web: Wikipedia/Discogs: 'I'll Be Missing You' é Puff Daddy & Faith Evans feat. 112; sem OneRepublic/DJ Shadow
- **Mariah Carey × Bryan Adams** — “When You Believe” [song, 1998] (#16561) — _'When You Believe' foi com Whitney Houston, não Bryan Adams_  
    ↳ web: Wikipedia/whitneyhouston.com: 'When You Believe' (1998) é dueto Mariah Carey & Whitney Houston, não Bryan Adams
- **Kanye West × Kid Cudi** — “Everybody Wants to Be My Enemy” [song, 2018] (#16591) — _'Everybody Wants to Be My Enemy' é de Studio Killers, não Kanye/Cudi_  
    ↳ web: Wikipedia: tracklist de Kids See Ghosts (Kanye/Cudi) não tem 'Everybody Wants to Be My Enemy'; é verso de 'Enemy' de Imagine Dragons/J.I.D
- **Lil Durk × Young Thug** — “Rich Flex” [song, 2022] (#16616) — _'Rich Flex' é Drake & 21 Savage, não Lil Durk/Young Thug_  
    ↳ web: Wikipedia: 'Rich Flex' (Her Loss, 2022) é de Drake & 21 Savage, não Lil Durk/Young Thug
- **Migos × Meek Mill** — “Oodles O' Noodles Babies” [song, 2021] (#16653) — _faixa é do Meek Mill, sem Migos_  
    ↳ web: 'Oodles O' Noodles Babies' é solo do Meek Mill (Championships 2018), produção Butter Beats/Kendxll, sem Migos (en.wikipedia.org)
- **Wiz Khalifa × Bruno Mars** — “See You Again” [song, 2015] (#16660) — _See You Again é com Charlie Puth, não Bruno Mars_  
    ↳ web: 'See You Again' é Wiz Khalifa feat. Charlie Puth (Furious 7, 2015), sem Bruno Mars (en.wikipedia.org)
- **Rick Ross × Future** — “Purple Lamborghini” [song, 2016] (#16663) — _Purple Lamborghini é Skrillex & Rick Ross, sem Future_  
    ↳ web: 'Purple Lamborghini' é Skrillex & Rick Ross (Suicide Squad, 2016), sem Future (en.wikipedia.org, billboard.com)
- **Ice Spice × Latto** — “Bikini Bottom” [song, 2023] (#16677) — _Bikini Bottom é Ice Spice sozinha, sem Latto_  
    ↳ web: 'Bikini Bottom' é solo da Ice Spice (2022); Latto só ligada por momento viral de entrevista, sem colab (en.wikipedia.org)
- **Ice Spice × Kali Uchis** — “Deli” [song, 2023] (#16678) — _Deli é Ice Spice sozinha, sem Kali Uchis_  
    ↳ web: 'Deli' é single solo da Ice Spice (EP Like..?), sem Kali Uchis (en.wikipedia.org)
- **J. Balvin × Bad Bunny** — “Un Verano Sin Ti (collaboration)” [song, 2022] (#16679) — _Un Verano Sin Ti é álbum do Bad Bunny, não colab_  
    ↳ web: 'Un Verano Sin Ti' é álbum solo do Bad Bunny; J Balvin não aparece nele (en.wikipedia.org)
- **J. Balvin × Bad Bunny** — “UN VERANO SIN TI” [album, 2022] (#16682) — _álbum é do Bad Bunny solo, não J. Balvin_  
    ↳ web: Álbum 'Un Verano Sin Ti' (2022) é solo do Bad Bunny, não colab com J Balvin (en.wikipedia.org)
- **J. Balvin × Khalid** — “Wild Thoughts” [song, 2017] (#16684) — _Wild Thoughts é DJ Khaled/Rihanna, não Balvin/Khalid_  
    ↳ web: 'Wild Thoughts' é de DJ Khaled feat. Rihanna e Bryson Tiller; Balvin/Khalid gravaram 'Otra Noche Sin Ti' (en.wikipedia.org)
- **Feid × Bad Bunny** — “Monaco” [song, 2023] (#16692) — _Monaco é Bad Bunny solo, sem Feid_  
    ↳ web: 'Monaco' é faixa solo do Bad Bunny (álbum Nadie Sabe...), sem Feid (en.wikipedia.org)
- **Feid × Quevedo** — “Beso” [song, 2023] (#16695) — _Beso é Rosalía & Rauw Alejandro, não Feid/Quevedo_  
    ↳ web: 'Beso' (2023) é de Rosalía & Rauw Alejandro, não Feid/Quevedo (en.wikipedia.org)
- **Wisin × Ricky Martin** — “Hasta el Amanecer” [song, 2017] (#16702) — _Hasta el Amanecer é Nicky Jam, não Wisin/Ricky Martin_  
    ↳ web: 'Hasta el Amanecer' é do Nicky Jam; Ricky Martin não consta (en.wikipedia.org)
- **Wisin × Enrique Iglesias** — “Move to Miami” [song, 2018] (#16703) — _Move to Miami é Enrique Iglesias feat. Pitbull_  
    ↳ web: 'Move to Miami' é Enrique Iglesias feat. Pitbull; Wisin não participa (en.wikipedia.org)
- **Ricky Martin × Paloma Faith** — “Wherever I Go” [song, 2015] (#16717) — _Wherever I Go é OneRepublic, não Ricky/Paloma_  
    ↳ web: 'Wherever I Go' (2016) é do OneRepublic, não Ricky Martin/Paloma Faith (en.wikipedia.org)
- **Alok × System of a Down** — “BYOB (Remix)” [song, 2018] (#16760) — _remix fabricado com banda de metal_  
    ↳ web: Beatport/Spotify: 'BYOB' é de Alok & Sevenn samplando System of a Down; SOAD não é colaborador creditado
- **Racionais MC's × MV Bill** — “Soldado do Morro” [song, 2006] (#16775) — _Soldado do Morro é solo do MV Bill_  
    ↳ web: Spotify: 'Soldado do Morro' é de MV Bill (1999) com DJ Luciano, sem Racionais MC's
- **Gorillaz × Slow Thai** — “The Valley of The Pagans” [song, 2020] (#16813) — _Valley of the Pagans é com Beck, não Slowthai_  
    ↳ web: Spotify/Wikipedia: 'The Valley of The Pagans' é Gorillaz feat. Beck, não Slowthai
- **Davido × Nicki Minaj** — “If” [song, 2017] (#16826) — _If é hit solo do Davido, sem Nicki_  
    ↳ web: Wikipedia: 'If' é solo de Davido (prod. Tekno, 2017); remix tem R. Kelly, não Nicki Minaj
- **Davido × SZA** — “So Crazy” [song, 2021] (#16829) — _So Crazy é com Lil Baby, não SZA_  
    ↳ web: Spotify: 'So Crazy' de Davido é feat. Lil Baby, não SZA
- **The Weeknd × Madonna** — “Die For You” [song, 2023] (#16994) — _Die For You remix é com Ariana Grande, não Madonna_  
    ↳ web: Wikipedia/Apple Music: remix de 'Die For You' (2023) é com Ariana Grande, não Madonna
- **The Weeknd × Republic** — “Creepin'” [song, 2022] (#16996) — _Creepin' é Metro Boomin com Weeknd e 21; Republic é gravadora, não artista_  
    ↳ web: Wikipedia/Spotify: 'Creepin'' credita Metro Boomin, The Weeknd e 21 Savage; Republic é gravadora, não artista
- **Bad Bunny × Post Malone** — “Sensationail” [song, 2021] (#17005) — _Sensationail não é música real de Bad Bunny e Post Malone_  
    ↳ web: Sem registro de música 'Sensationail'; Bad Bunny e Post Malone só fizeram dueto ao vivo em Coachella (NME), sem faixa de estúdio
- **Bad Bunny × Nesi** — “Andrea” [song, 2022] (#17009) — _Andrea é com Buscabulla, não com Nesi_  
    ↳ web: Spotify/WhoSampled: 'Andrea' de Un Verano Sin Ti é Bad Bunny feat. Buscabulla, não Nesi
- **Ed Sheeran × Nicki Minaj** — “Beautiful People” [song, 2019] (#17017) — _'Beautiful People' é com Khalid, não Nicki Minaj_  
    ↳ web: Discogs/Songfacts: 'Beautiful People' é Ed Sheeran feat. Khalid, não Nicki Minaj
- **Ed Sheeran × Elton John** — “Cold Heart” [song, 2021] (#17019) — _'Cold Heart' é de Elton John e Dua Lipa, não Ed Sheeran_  
    ↳ web: Wikipedia: 'Cold Heart (Pnau remix)' é Elton John & Dua Lipa, não Ed Sheeran
- **Justin Bieber × Lil Dicky** — “Freaky Friday” [song, 2018] (#17028) — _'Freaky Friday' de Lil Dicky é com Chris Brown, não Bieber_  
    ↳ web: Wikipedia: 'Freaky Friday' é Lil Dicky feat. Chris Brown, não Justin Bieber
- **Justin Bieber × Kehlani** — “Already” [song, 2020] (#17029) — _'Already' é Beyoncé/Shatta Wale, não Bieber/Kehlani_  
    ↳ web: Wikipedia/Spotify: 'Already' é Beyoncé, Shatta Wale & Major Lazer, não Bieber/Kehlani
- **Ariana Grande × Ty Dolla $ign** — “Rule the World” [song, 2017] (#17035) — _'Rule the World' é de 2 Chainz, não Ty Dolla $ign_  
    ↳ web: Wikipedia: 'Rule the World' é 2 Chainz feat. Ariana Grande, não Ty Dolla $ign
- **Beyoncé × Kanye West** — “Everything Is Love” [song, 2018] (#17045) — _'Everything Is Love' é álbum de Beyoncé e Jay-Z, não Kanye_  
    ↳ web: Wikipedia: 'Everything Is Love' é álbum de The Carters (Beyoncé e Jay-Z), não colab com Kanye
- **Post Malone × Doja Cat** — “Enemies” [song, 2021] (#17068) — _'Enemies' de Post Malone é com DaBaby, não Doja Cat_  
    ↳ web: Wikipedia/Spotify: 'Enemies' de Post Malone é feat. DaBaby, não Doja Cat
- **Post Malone × Future** — “Cooped Up” [song, 2022] (#17071) — _'Cooped Up' é Post Malone com Roddy Ricch, não Future_  
    ↳ web: Wikipedia/Spotify: 'Cooped Up' é Post Malone feat. Roddy Ricch, não Future
- **Post Malone × Future** — “Spoil My Night” [song, 2018] (#17072) — _'Spoil My Night' é Post Malone com Swae Lee, não Future_  
    ↳ web: Spotify/Songfacts: 'Spoil My Night' é Post Malone feat. Swae Lee, não Future
- **Dua Lipa × Anitta** — “Boom” [song, 2021] (#17079) — _'Boom' não é colab conhecida Dua Lipa/Anitta_  
    ↳ web: Popline/Terra: colab Dua Lipa/Anitta nunca saiu (só tentativa 2017); nenhum 'Boom' existe
- **Dua Lipa × Hozier** — “Love Wins” [song, 2020] (#17081) — _'Love Wins' não é colaboração Dua Lipa/Hozier_  
    ↳ web: Busca (Wikipedia/Spotify): não existe 'Love Wins' com Dua Lipa e Hozier
- **Travis Scott × 21 Savage** — “Out West” [song, 2020] (#17086) — _'Out West' é Travis Scott com Young Thug, não 21 Savage_  
    ↳ web: Wikipedia/Spotify: 'Out West' é JACKBOYS/Travis Scott feat. Young Thug, não 21 Savage
- **Kendrick Lamar × SZA** — “From the D 2 the LBC” [song, 2022] (#17095) — _'From the D 2 the LBC' é Eminem/Snoop, não Kendrick/SZA_  
    ↳ web: Wikipedia/eminem.com: 'From the D 2 the LBC' é Eminem com Snoop Dogg, não Kendrick/SZA
- **Kendrick Lamar × Lil Nas X** — “INDUSTRY BABY” [song, 2021] (#17097) — _'INDUSTRY BABY' é Lil Nas X com Jack Harlow, não Kendrick_  
    ↳ web: Wikipedia/Billboard: 'INDUSTRY BABY' é Lil Nas X feat. Jack Harlow, Kendrick não participa
- **Nicki Minaj × Cardi B** — “Twerk” [song, 2018] (#17108) — _Twerk é City Girls feat. Cardi B, não Nicki_  
    ↳ web: 'Twerk' é City Girls feat. Cardi B, sem Nicki Minaj (en.wikipedia.org)
- **Cardi B × Drake** — “Get It Together” [song, 2017] (#17114) — _Get It Together é Drake feat. Jorja Smith, não Cardi_  
    ↳ web: 'Get It Together' é Drake feat. Jorja Smith e Black Coffee, sem Cardi B (whosampled.com)
- **Cardi B × Benson Boone** — “Beautiful Things (Remix)” [song, 2024] (#17116) — _remix improvável, não existe_  
    ↳ web: Só existem remixes de fãs/produtores (Henri PFR etc) de 'Beautiful Things'; nenhum remix oficial com Cardi B (soundcloud)
- **Lil Wayne × Drake** — “Back to Back” [song, 2015] (#17118) — _Back to Back é diss solo do Drake_  
    ↳ web: 'Back to Back' é diss solo do Drake contra Meek Mill, sem Lil Wayne (Wikipedia)
- **Lil Wayne × Beyoncé** — “Drunk in Love (Remix)” [song, 2014] (#17122) — _remix inexistente_  
    ↳ web: O remix oficial de 'Drunk in Love' traz JAY-Z e Kanye West, não Lil Wayne (Wikipedia/Spotify)
- **Lil Wayne × Rihanna** — “Lollipop (Remix)” [song, 2008] (#17123) — _Lollipop é feat. Static Major, remix com Rihanna não existe_  
    ↳ web: 'Lollipop (Remix)' é feat. Static Major e Kanye West, não Rihanna (Apple Music/Discogs)
- **Doja Cat × Eve** — “Who Dat Girl” [song, 2020] (#17127) — _Eve J-Pop com Doja não existe, título fabricado_  
    ↳ web: 'Who Dat Girl' é do Flo Rida feat. Akon; colab real Doja/Eve chama-se 'Tonight' (Wikipedia)
- **Doja Cat × Sam Ock** — “Planet Her (Intro)” [song, 2021] (#17133) — _Planet Her é álbum da Doja, colab improvável_  
    ↳ web: Planet Her não tem faixa 'Intro' e não há colab Doja Cat com Sam Ock (Wikipedia/Spotify)
- **Doja Cat × Khalid** — “Body Count” [song, 2021] (#17134) — _Body Count é faixa solo da Doja_  
    ↳ web: Não há faixa 'Body Count' em Planet Her nem colab Doja/Khalid (Wikipedia/Billboard)
- **SZA × Lil Wayne** — “Low (SZA)” [song, 2023] (#17136) — _Low do SOS é solo da SZA_  
    ↳ web: 'Low' do SOS tem adlibs de Travis Scott, não Lil Wayne (Wikipedia)
- **SZA × Jonas Brothers** — “Hesitate” [song, 2019] (#17140) — _Hesitate é faixa solo dos Jonas Brothers_  
    ↳ web: 'Hesitate' é faixa dos Jonas Brothers (carta de Joe p/ Sophie), sem SZA (Wikipedia/ET)
- **Lady Gaga × Elton John** — “Always Remember Us This Way (duet)” [song, 2020] (#17160) — _Always Remember Us This Way é solo da Gaga, não dueto com Elton_  
    ↳ web: 'Always Remember Us This Way' é solo da Gaga (A Star Is Born), não dueto com Elton John (Wikipedia)
- **Lady Gaga × Florence Welch** — “Heal Me” [song, 2018] (#17162) — _Heal Me é solo da Gaga em Joanne_  
    ↳ web: Não existe 'Heal Me' em Joanne; a colab Gaga/Florence é 'Hey Girl' (Wikipedia)
- **Katy Perry × Kylie Minogue** — “Padam Padam (remix)” [song, 2023] (#17167) — _remix de Padam Padam com Katy não existe_  
    ↳ web: Remixes oficiais de 'Padam Padam' são Jax Jones/HAAi/Absolute; nenhum com Katy Perry (Mixmag/Wikipedia)
- **Katy Perry × Sam Smith** — “When I'm Gone” [song, 2023] (#17168) — _When I'm Gone é com Alesso, não Sam Smith_  
    ↳ web: 'When I'm Gone' e de Alesso e Katy Perry, sem Sam Smith (en.wikipedia.org)
- **Maroon 5 × Juice WRLD** — “Beautiful Mistakes” [song, 2021] (#17173) — _Beautiful Mistakes é com Megan Thee Stallion, não Juice WRLD_  
    ↳ web: 'Beautiful Mistakes' e Maroon 5 feat. Megan Thee Stallion, nao Juice WRLD (en.wikipedia.org)
- **Maroon 5 × Adam Levine** — “Payphone” [song, 2012] (#17176) — _Adam Levine é o próprio vocalista do Maroon 5_  
    ↳ web: 'Payphone' e Maroon 5 feat. Wiz Khalifa; Adam Levine e o proprio vocalista do Maroon 5, nao colaboracao (en.wikipedia.org)
- **Coldplay × Noel Gallagher** — “Talk (original collaboration)” [song, 2005] (#17179) — _Talk baseia-se em Kraftwerk, não Noel Gallagher_  
    ↳ web: 'Talk' e baseada em 'Computer Love' do Kraftwerk, sem Noel Gallagher (en.wikipedia.org)
- **Calvin Harris × Stormzy** — “How Deep Is Your Love” [song, 2015] (#17288) — _How Deep Is Your Love é com Disciples, não com Stormzy_  
    ↳ web: 'How Deep Is Your Love' é de Calvin Harris & Disciples ft. Ina Wroldsen; nenhum Stormzy nos créditos (en.wikipedia.org, discogs.com)
- **21 Savage × Travis Scott** — “Highest in the Room (remix)” [song, 2019] (#17381) — _Highest in the Room remix é com Rosalía/Lil Baby, não 21 Savage_  
    ↳ web: O remix de 'Highest in the Room' é feat. Rosalía e Lil Baby, não 21 Savage (Wikipedia/Spotify)
- **J. Cole × Kendrick Lamar** — “Alright (remix)” [song, 2015] (#17411) — _Alright de Kendrick não tem remix oficial com J. Cole_  
    ↳ web: O remix 'Black Friday' de 'Alright' é freestyle solo de J. Cole sobre a base; Kendrick não aparece na faixa (Vibe/WhoSampled)
- **J. Cole × Kodak Black** — “Super Bowl Shuffle” [song, 2019] (#17417) — _Super Bowl Shuffle não é colab J. Cole/Kodak_  
    ↳ web: 'The Super Bowl Shuffle' é dos Chicago Bears Shufflin' Crew (1985); não existe colab J. Cole/Kodak Black (Wikipedia)
- **Pharrell Williams × SZA** — “Paramedic!” [song, 2018] (#17433) — _Paramedic! é dos SOB x RBE/Kendrick, não Pharrell/SZA_  
    ↳ web: 'Paramedic!' (Black Panther) é de SOB x RBE & Kendrick Lamar, sem Pharrell nem SZA (Spotify/Last.fm)
- **Pharrell Williams × Usher** — “Yeah! (production)” [song, 2004] (#17434) — _Yeah! de Usher produzida por Lil Jon, não Pharrell_  
    ↳ web: 'Yeah!' de Usher (feat. Lil Jon & Ludacris) foi produzida por Lil Jon; Pharrell não é autor nem produtor (Wikipedia/Discogs)
- **Timbaland × Rihanna** — “SOS (remix)” [song, 2006] (#17448) — _SOS de Rihanna prod. J.R. Rotem, não Timbaland_  
    ↳ web: 'SOS' de Rihanna foi produzida por J.R. Rotem; remixes por Digital Dog etc., sem Timbaland (Wikipedia/WhoSampled)
- **Timbaland × Chris Brown** — “Say Aah (remix)” [song, 2009] (#17451) — _Say Aah é de Trey Songz, não Chris Brown/Timbaland_  
    ↳ web: 'Say Aah' é de Trey Songz feat. Fabolous, não Chris Brown/Timbaland (en.wikipedia.org/whosampled.com)
- **Timbaland × Usher** — “Burn” [song, 2004] (#17457) — _Burn de Usher prod. Jam & Lewis, não Timbaland_  
    ↳ web: 'Burn' de Usher foi produzida por Jermaine Dupri e Bryan-Michael Cox, sem Timbaland/Usher-colab (en.wikipedia.org)
- **Justin Timberlake × Kirk Franklin** — “My Body Is a Cage (remix)” [song, 2007] (#17467) — _'My Body Is a Cage' é do Arcade Fire, remix gospel fabricado_  
    ↳ web: Spotify: 'My Body Is a Cage' é do Arcade Fire (2007); nenhum remix gospel JT/Kirk Franklin documentado
- **Justin Timberlake × DJ Khaled** — “INSHA'ALLAH” [song, 2021] (#17469) — _título 'INSHA'ALLAH' JT x DJ Khaled fabricado_  
    ↳ web: Billboard/Spotify: colab JT x DJ Khaled é 'JUST BE' (2021); nenhuma faixa 'INSHA'ALLAH' existe
- **Anitta × Lexa** — “Loka” [song, 2016] (#17496) — _'Loka' é Simone e Simaria feat Anitta, não Lexa_  
    ↳ web: Wikipedia/Discogs: 'Loka' (2016) é Simone & Simaria feat. Anitta, não Lexa
- **Anitta × Hitmaker** — “Grip” [song, 2022] (#17507) — _'Hitmaker' não é artista, título fabricado_  
    ↳ web: Rolling Stone/Spotify: 'Grip' (Funk Generation, Anitta) é solo; 'Hitmaker' não é artista
- **Anitta × Diplo** — “Kiss Me Thru the Phone (Remix)” [song, 2022] (#17509) — _'Kiss Me Thru the Phone' é Soulja Boy, remix Anitta x Diplo fabricado_  
    ↳ web: Spotify: 'Kiss Me Thru the Phone' é de Soulja Boy; Anitta e Diplo colaboraram em Sua Cara/Make It Hot, não nesse remix
- **Ludmilla × Nicki Minaj** — “Nem Vem (feat.)” [feature, 2017] (#17524) — _Ludmilla x Nicki Minaj 'Nem Vem' não existe_  
    ↳ web: Nenhuma colaboração Ludmilla x Nicki Minaj 'Nem Vem' existe (Wikipedia/lista de músicas de Nicki Minaj)
- **Luísa Sonza × Gloria Groove** — “Parado No Bailão” [song, 2022] (#17552) — _'Parado No Bailão' é do MC L da Vinte, não de Sonza/Groove_  
    ↳ web: Spotify/Apple Music: 'Parado No Bailão' é de MC L da Vinte & MC Gury, não Luísa Sonza/Gloria Groove
- **Luísa Sonza × Lil Nas X** — “Toma (feat.)” [feature, 2022] (#17555) — _cross-cultural improvável; sem registro de Sonza com Lil Nas X_  
    ↳ web: Spotify/Letras: 'TOMA' de Luísa Sonza tem part. de ZAAC, não Lil Nas X
- **Luísa Sonza × Dua Lipa** — “Levitando (feat.)” [feature, 2021] (#17557) — _'Levitating' é de Dua Lipa; não há versão com Luísa Sonza_  
    ↳ web: WhoSampled: 'Levitating' é de Dua Lipa (remix ft. DaBaby); não há versão com Luísa Sonza
- **Luísa Sonza × Benson Boone** — “Beautiful Things (feat.)” [feature, 2024] (#17559) — _'Beautiful Things' é solo de Benson Boone; sem Luísa Sonza_  
    ↳ web: Wikipedia: 'Beautiful Things' é solo de Benson Boone (2024), sem Luísa Sonza
- **Pabllo Vittar × Sam Smith** — “Unholy (feat.)” [feature, 2023] (#17571) — _'Unholy' é Sam Smith/Kim Petras, sem Pabllo Vittar_  
    ↳ web: Spotify/Tunebat: 'Unholy' é Sam Smith feat. Kim Petras; sem versão com Pabllo Vittar
- **Pabllo Vittar × Kim Petras** — “Unholy (feat.)” [feature, 2023] (#17572) — _'Unholy' é Sam Smith/Kim Petras, sem Pabllo Vittar_  
    ↳ web: Spotify: 'Unholy' credita Sam Smith & Kim Petras, mas Pabllo Vittar não participa (dupla claimed é falsa)
- **Gusttavo Lima × Kauan & Matheus** — “Caneta Azul (feat.)” [feature, 2019] (#17643) — _Caneta Azul é de Nog, não parceria destes_  
    ↳ web: 'Caneta Azul' é de Manoel Gomes; não é parceria de Gusttavo Lima com Kauan & Matheus (en.wikipedia.org, open.spotify.com)
- **Gusttavo Lima × Naiara Azevedo** — “50 Reais (ao vivo)” [live, 2021] (#17645) — _50 Reais é de Naiara com Maiara & Maraisa, não Gusttavo_  
    ↳ web: '50 Reais' (inclusive ao vivo) é de Naiara Azevedo com Maiara & Maraisa, não com Gusttavo Lima (pt.wikipedia.org, open.spotify.com)
- **Jorge & Mateus × Naiara Azevedo** — “50 Reais (ao vivo)” [live, 2021] (#17668) — _50 Reais não é de Jorge & Mateus_  
    ↳ web: '50 Reais' é de Naiara Azevedo com Maiara & Maraisa; Jorge & Mateus não participam (letras.mus.br, open.spotify.com)
- **Matuê × Djonga** — “Máquina do Tempo (feat.)” [feature, 2020] (#17700) — _Máquina do Tempo não é feat de Djonga_  
    ↳ web: 'Máquina do Tempo' é faixa solo de Matuê (prod. WIU/Celo); álbum tem Teto, WIU, Brandão85, Predella, não Djonga (pt.wikipedia.org, letras.mus.br)
- **Matuê × MC Kevin** — “Máquina do Tempo (feat.)” [feature, 2020] (#17702) — _Máquina do Tempo não é feat de MC Kevin_  
    ↳ web: 'Máquina do Tempo' é solo de Matuê; convidados do álbum são Teto/WIU/Brandão85/Predella, sem MC Kevin (pt.wikipedia.org, letras.mus.br)
- **Matuê × Anitta** — “Joga Pra Lua (feat.)” [feature, 2021] (#17705) — _Joga Pra Lua é de Anitta 2024, não feat Matuê 2021_  
    ↳ web: 'Joga Pra Lua' é de Anitta com DENNIS e Pedro Sampaio (2023/2024), sem Matuê (rollingstone.com, open.spotify.com)
- **Matuê × Borges** — “Máquina do Tempo (feat.)” [feature, 2020] (#17710) — _Máquina do Tempo não é feat de Borges_  
    ↳ web: 'Máquina do Tempo' é faixa-título/álbum solo de Matuê (7 faixas), sem feat de Borges (pt.wikipedia.org, vagalume)
- **Emicida × Rico Dalasam** — “AmarElo (feat.)” [feature, 2019] (#17723) — _AmarElo é feat Majur e Pabllo Vittar, não Rico Dalasam_  
    ↳ web: 'AmarElo' de Emicida é feat Majur e Pabllo Vittar, não Rico Dalasam (spotify, tenhomaisdiscosqueamigos)
- **Alok × Dennis DJ** — “Baile de Favela (feat.)” [song, 2020] (#17758) — _'Baile de Favela' é de MC João, não de Alok x Dennis_  
    ↳ web: 'Baile de Favela' é de MC João (prod. DJ R7), remixes de Alok e Dennis são separados (Spotify/1001tracklists)
- **Alok × Bali Baby** — “Never Let Me Go (feat.)” [feature, 2019] (#17764) — _'Never Let Me Go' é com Zeeba/Bruno Martini, não Bali Baby_  
    ↳ web: 'Never Let Me Go' é Alok, Bruno Martini e Zeeba (2017), não Bali Baby (Spotify/Spinnin')
- **Alok × Benson Boone** — “In The Name Of Love (feat.)” [feature, 2023] (#17767) — _'In The Name Of Love' é Bebe Rexha/Martin Garrix, não Alok x Benson Boone_  
    ↳ web: 'In the Name of Love' é Martin Garrix & Bebe Rexha (2016), não Alok x Benson Boone (Wikipedia)
- **Luan Santana × Jão** — “Amor de Verdade (feat.)” [feature, 2023] (#17796) — _'Amor de Verdade' é Pedro Sampaio/Wesley Safadão, não Luan x Jão_  
    ↳ web: 'Amor de Verdade' (2018) é MC Kekel e MC Rita, não Luan Santana x Jão (As Super Listas/Letras)
- **Pedro Sampaio × Dennis DJ** — “Baile de Favela (feat.)” [song, 2020] (#17812) — _'Baile de Favela' é de MC João, não de Pedro Sampaio x Dennis_  
    ↳ web: Spotify/Letras: 'Baile de Favela' é de MC João e DJ R7; Pedro Sampaio apenas remixou, não colab com Dennis
- **Pedro Sampaio × Luísa Sonza** — “CAFÉ DA MANHÃ (feat.)” [song, 2023] (#17823) — _CAFÉ DA MANHÃ é de Luísa Sonza; não é feat com Pedro Sampaio_  
    ↳ web: 'CAFÉ DA MANHÃ ;P' é de Luísa Sonza x Ludmilla, não feat com Pedro Sampaio (spotify.com, letras.com)
- **Veigh × Anitta** — “Funk Generation (feat.)” [feature, 2024] (#17861) — _Funk Generation é álbum da Anitta, não feat com Veigh_  
    ↳ web: 'Funk Generation' é álbum da Anitta; features são Brray, Bad Gyal, Dennis, Pedro Sampaio, Sam Smith, sem Veigh (wikipedia.org)
- **Alicia Keys × Drake** — “Enough Said” [song, 2012] (#17900) — _Enough Said é de Aaliyah feat Drake, não de Alicia Keys_  
    ↳ web: 'Enough Said' (2012) é de Aaliyah feat. Drake, não Alicia Keys (wikipedia.org)
- **Alicia Keys × Lil Wayne** — “Unbreakable” [song, 2007] (#17901) — _Unbreakable é single solo de Alicia Keys, sem feat de Lil Wayne_  
    ↳ web: 'Unbreakable' é single solo de Alicia Keys (2005), escrito por Keys/Kanye West/Harold Lilly, sem Lil Wayne (en.wikipedia.org)
- **Selena Gomez × Camila Cabello** — “Feel Me” [song, 2023] (#17944) — _não existe colaboração Feel Me com Camila_  
    ↳ web: Wikipedia: 'Feel Me' é solo de Selena Gomez (álbum Rare), sem Camila Cabello nos créditos
- **Camila Cabello × Young Thug** — “Him & I” [song, 2018] (#17956) — _Him & I é de G-Eazy e Halsey, não Camila/Young Thug_  
    ↳ web: Wikipedia: 'Him & I' é de G-Eazy e Halsey, não Camila Cabello/Young Thug
- **Camila Cabello × Cardi B** — “Crown” [song, 2020] (#17959) — _Crown é de Camila com Grey, não Cardi B_  
    ↳ web: Spotify/Wikipedia: 'Crown' é Camila Cabello & Grey (trilha Bright), sem Cardi B
- **The Chainsmokers × Bryce Vine** — “Do You Mean” [song, 2017] (#18004) — _'Do You Mean' é com Ty Dolla e bülow, não Bryce Vine_  
    ↳ web: Discogs/Spotify: 'Do You Mean' credita Ty Dolla $ign & bülow, não Bryce Vine
- **Jack Harlow × Bryson Tiller** — “They Don't Love It” [song, 2022] (#18009) — _'They Don't Love It' é solo, não com Bryson Tiller_  
    ↳ web: Wikipedia: 'They Don't Love It' é faixa solo de Jack Harlow (Jackman), sem Bryson Tiller
- **Jack Harlow × Saweetie** — “Whats Poppin (remix)” [song, 2020] (#18013) — _remix de Whats Poppin não inclui Saweetie_  
    ↳ web: Wikipedia/Spotify: remix de 'Whats Poppin' tem DaBaby, Tory Lanez & Lil Wayne, não Saweetie
- **Jack Harlow × 2 Chainz** — “Way Out” [song, 2020] (#18016) — _'Way Out' é com Big Sean, não 2 Chainz_  
    ↳ web: Wikipedia: 'Way Out' de Jack Harlow feat. Big Sean, não 2 Chainz
- **Jack Harlow × Pharrell Williams** — “Neverita” [song, 2023] (#18017) — _'Neverita' é do Bad Bunny, não Jack Harlow_  
    ↳ web: Wikipedia: 'Neverita' é do Bad Bunny (Un Verano Sin Ti), produção Tainy; sem Jack Harlow/Pharrell
- **Jack Harlow × Chris Brown** — “No Idea” [feature, 2021] (#18021) — _'No Idea' é do Don Toliver, não colab desses_  
    ↳ web: Wikipedia: 'No Idea' é single solo de Don Toliver, não colab Jack Harlow/Chris Brown
- **Jack Harlow × Bia** — “WHATS POPPIN (remix)” [song, 2020] (#18022) — _Bia não está no remix de Whats Poppin_  
    ↳ web: Wikipedia/Spotify: remix de 'Whats Poppin' tem DaBaby, Tory Lanez & Lil Wayne, não Bia
- **Jack Harlow × Lil Baby** — “Nail Tech” [feature, 2022] (#18023) — _'Nail Tech' é solo, não feat Lil Baby_  
    ↳ web: Wikipedia: 'Nail Tech' é single solo de Jack Harlow, sem feat Lil Baby
- **Lil Nas X × Ben Affleck** — “Holiday (skit)” [feature, 2023] (#18036) — _fabricação, sem faixa com Ben Affleck_  
    ↳ web: Wikipedia: 'Holiday' de Lil Nas X é single standalone; sem skit/feat com Ben Affleck
- **Tyler, The Creator × Kendrick Lamar** — “Tamale” [song, 2013] (#18038) — _'Tamale' é solo do Wolf, sem Kendrick_  
    ↳ web: Wikipedia: 'Tamale' (Wolf) escrita e produzida só por Tyler; sem Kendrick Lamar
- **Tyler, The Creator × Pharrell Williams** — “SMUCKERS” [song, 2015] (#18039) — _SMUCKERS é com Kanye e Lil Wayne, não Pharrell_  
    ↳ web: Wikipedia: 'Smuckers' (Cherry Bomb) feat. Kanye West & Lil Wayne, não Pharrell
- **Tyler, The Creator × Lil Uzi Vert** — “GONE, GONE / THANK YOU” [song, 2019] (#18040) — _'GONE, GONE' é solo do IGOR_  
    ↳ web: Wikipedia/HotNewHipHop: 'GONE, GONE / THANK YOU' traz CeeLo Green e La Roux, nao Lil Uzi Vert
- **Tyler, The Creator × Charlie Wilson** — “RUNNING OUT OF TIME” [song, 2021] (#18042) — _faixa solo, sem Charlie Wilson_  
    ↳ web: Fandom/RYM: Charlie Wilson canta em 'EARFQUAKE'; 'RUNNING OUT OF TIME' tem vocais de Jessy Wilson
- **Tyler, The Creator × Jaden Smith** — “Where This Flower Blooms” [song, 2017] (#18045) — _faixa tem Frank Ocean, não Jaden Smith_  
    ↳ web: Spotify/thefader: 'Where This Flower Blooms' e feat. Frank Ocean, nao Jaden Smith
- **Tyler, The Creator × Solange** — “SWEET / I THOUGHT YOU WANTED TO DANCE” [song, 2021] (#18047) — _faixa tem Brent Faiyaz e Fana Hues, não Solange_  
    ↳ web: Spotify/Wikipedia: 'SWEET / I THOUGHT YOU WANTED TO DANCE' feat. Brent Faiyaz & Fana Hues, nao Solange
- **Tyler, The Creator × Lil Uzi Vert** — “WHAT IT IS” [song, 2023] (#18049) — _'WHAT IT IS' é da Doechii, não Tyler_  
    ↳ web: Wikipedia: 'What It Is (Block Boy)' e single da Doechii feat. Kodak Black; nao existe faixa Tyler+Lil Uzi com esse titulo
- **Tyler, The Creator × Teezo Touchdown** — “WHARF TALK” [song, 2023] (#18054) — _WHARF TALK é com A$AP Rocky, não Teezo_  
    ↳ web: NME/Spotify: 'WHARF TALK' e feat. A$AP Rocky (add. vocals DJ Drama), nao Teezo Touchdown
- **Tyler, The Creator × ScHoolboy Q** — “WHARF TALK” [song, 2023] (#18055) — _WHARF TALK é com A$AP Rocky, não ScHoolboy Q_  
    ↳ web: NME/Spotify: 'WHARF TALK' e feat. A$AP Rocky, nao ScHoolboy Q
- **Tyler, The Creator × LaFame** — “See You Again” [song, 2017] (#18056) — _'See You Again' é com Kali Uchis, não LaFame_  
    ↳ web: Spotify/Wikipedia: 'See You Again' e feat. Kali Uchis, nao LaFame
- **Tyler, The Creator × Daniel Caesar** — “ARE WE STILL FRIENDS?” [song, 2019] (#18057) — _'ARE WE STILL FRIENDS?' é solo do IGOR_  
    ↳ web: RYM/AnalogPlanet: 'ARE WE STILL FRIENDS?' tem background vocals de Pharrell Williams, nao Daniel Caesar
- **A$AP Rocky × Wale** — “1Train” [song, 2012] (#18063) — _Wale não está em '1Train'_  
    ↳ web: Wikipedia/Spotify: '1Train' feat. Kendrick, Joey Bada$$, Yelawolf, Danny Brown, Action Bronson, Big K.R.I.T.; sem Wale
- **A$AP Rocky × Gunplay** — “1Train” [song, 2012] (#18067) — _Gunplay não está em '1Train'_  
    ↳ web: Wikipedia/Spotify: lineup de '1Train' nao inclui Gunplay
- **Sabrina Carpenter × Rema** — “Busy Woman” [song, 2025] (#18076) — _'Busy Woman' é solo, não com Rema_  
    ↳ web: Wikipedia: 'Busy Woman' é solo de Sabrina Carpenter (Carpenter/Amy Allen/Jack Antonoff), sem Rema
- **Sabrina Carpenter × Pharrell Williams** — “Slim Pickins” [feature, 2024] (#18078) — _'Slim Pickins' é solo, não feat Pharrell_  
    ↳ web: Wikipedia: 'Slim Pickins' creditada a Carpenter/Amy Allen/Jack Antonoff, sem Pharrell
- **Lil Uzi Vert × The Weeknd** — “Unforgettable” [song, 2017] (#18085) — _'Unforgettable' é do French Montana, não desses_  
    ↳ web: Wikipedia: 'Unforgettable' (2017) é de French Montana feat. Swae Lee; The Weeknd apenas sampleado, sem Lil Uzi Vert
- **J. Balvin × Myke Towers** — “XO Tour Life (Remix)” [song, 2023] (#18203) — _'XO Tour Life' é de Lil Uzi Vert; remix fabricado_  
    ↳ web: 'XO Tour Llif3' é de Lil Uzi Vert; nenhum remix J Balvin+Myke Towers encontrado (Spotify)
- **Karol G × Maluma** — “Mía” [song, 2018] (#18222) — _'Mía' é Bad Bunny/Drake, não Karol G/Maluma_  
    ↳ web: Wikipedia/Spotify: colab real Karol G+Maluma é 'Créeme'; 'Mía' não existe entre eles
- **Maluma × Luis Fonsi** — “Échame la Culpa” [song, 2017] (#18243) — _'Échame la Culpa' é Fonsi & Demi Lovato, não Maluma_  
    ↳ web: Wikipedia: 'Échame la Culpa' é Luis Fonsi & Demi Lovato, sem Maluma
- **Daddy Yankee × El Alfa** — “Rompe” [song, 2022] (#18267) — _'Rompe' é de 2005 sem El Alfa; remix fabricado_  
    ↳ web: Letras/Apple Music: 'Rompe (Remix)' feat. G-Unit (Lloyd Banks/Young Buck), não El Alfa
- **Ozuna × Anuel AA** — “Yonaguni” [song, 2021] (#18298) — _Yonaguni é de Bad Bunny solo, não Ozuna/Anuel_  
    ↳ web: 'Yonaguni' é single solo de Bad Bunny (2021), sem Ozuna nem Anuel AA (en.wikipedia.org, open.spotify.com)

## ♻️ RESGATADAS — 68 — o sistema se corrigiu (MANTER)

O Passe 1 marcou como inválidas, mas a web provou que são reais. **Prova de que o filtro não é cego** — não remover.

- **Doja Cat × Megan Thee Stallion** — “34+35 (Remix)” [song, 2021] (#123) — _34+35 Remix é de Ariana Grande, não dueto Doja x Megan_  
    ↳ web: Spotify/Discogs: '34+35 Remix' tem Doja Cat e Megan Thee Stallion juntas (versos), feat. de Ariana Grande
- **Imagine Dragons × Lil Wayne** — “Believer (Remix)” [song, 2017] (#239) — _remix de Believer com Lil Wayne não existe_  
    ↳ web: whosampled/lilwaynehq: 'Believer (Remix)' feat. Lil Wayne (Imagine Dragons + Lil Wayne, jan/2019) existe
- **Chance the Rapper × Justin Bieber** — “Confident (Remix)” [song, 2017] (#249) — _remix de Confident com Bieber não existe_  
    ↳ web: Wikipedia/Spotify: 'Confident' de Justin Bieber feat. Chance the Rapper (Journals) credita os dois juntos
- **Sabrina Carpenter × Dolly Parton** — “Please Please Please” [song, 2024] (#363) — _'Please Please Please' é solo de Sabrina Carpenter, sem Dolly Parton_  
    ↳ web: Existe 'Please Please Please (feat. Dolly Parton)' remix no deluxe de Short n' Sweet com Sabrina e Dolly (open.spotify.com/en.wikipedia.org)
- **Jack White × Beck** — “Jack White produced sessions” [live, 2012] (#460) — _título genérico/fabricado de sessões_  
    ↳ web: Billboard/American Songwriter: Beck gravou com Jack White no Third Man (~2011-12), releases 'I Just Started Hating Some People Today'/'Blue Randy'
- **Troye Sivan × Charli XCX** — “Talk Talk (Troye Sivan)” [song, 2024] (#815) — _'Talk Talk' é solo do Troye Sivan, sem Charli_  
    ↳ web: Apple Music/Spotify: 'Talk talk featuring Troye Sivan' creditado a Charli XCX & Troye Sivan (2024)
- **Kid Cudi × Skrillex** — “Ignite the Love” [album, 2022] (#897) — _título fabricado, sem álbum Kid Cudi/Skrillex_  
    ↳ web: Wikipedia/edm.com: 'Ignite the Love' de Kid Cudi (Entergalactic 2022) tem Skrillex creditado na produção
- **AKA × Burna Boy** — “All Eyes on Me” [song, 2016] (#1127) — _'All Eyes on Me' AKA com Burna Boy não existe; atribuição falsa_  
    ↳ web: 'All Eyes on Me' de AKA é feat. Burna Boy, Da L.E.S. e JR; Burna Boy consta creditado (wikipedia, spotify, audiomack)
- **Alok × Ellie Goulding** — “All by Myself” [song, 2020] (#1926) — _'All by Myself' não consta entre Alok e Ellie Goulding_  
    ↳ web: 'All by Myself' (2022) é de Alok, Sigala e Ellie Goulding, ambos creditados (en.wikipedia.org)
- **Post Malone × Blake Shelton** — “Pour Me a Drink (feat. Blake Shelton)” [song, 2024] (#3008) — _'Pour Me a Drink' é com Luke Combs, não Blake Shelton_  
    ↳ web: Wikipedia/Spotify: 'Pour Me a Drink' de Post Malone é feat. Blake Shelton (2024) confirmado; motivo original errado
- **Martin Garrix × David Guetta** — “So Far Away” [song, 2017] (#3331) — _So Far Away é com Goulding/Vassy, não David Guetta_  
    ↳ web: 'So Far Away' (2017) é de Martin Garrix & David Guetta feat. Jamie Scott & Romy Dya (en.wikipedia.org/Discogs)
- **Tiësto × Karol G** — “Don't Be Shy” [song, 2021] (#3341) — _Don't Be Shy é Tiësto x Karol G — confere Karol G na verdade_  
    ↳ web: 'Don't Be Shy' (2021) é de Tiësto & Karol G, ambos creditados (en.wikipedia.org)
- **Tiësto × Jonas Blue** — “Rita Ora” [song, 2020] (#3344) — _título 'Rita Ora' não é música; confusão de dados_  
    ↳ web: Tiësto e Jonas Blue gravaram juntos 'Ritual' (com Rita Ora) em 2019/2020; 'Rita Ora' no título é o 3º artista (en.wikipedia.org)
- **Rahat Fateh Ali Khan × Pritam** — “Teri Ore” [song, 2008] (#4273) — _'Teri Ore' é de Salim-Sulaiman, não Pritam_  
    ↳ web: 'Teri Ore' (Singh Is Kinng 2008) composta por Pritam e cantada por Rahat Fateh Ali Khan; ambos creditados (spotify.com, shazam.com)
- **Badshah × Neha Kakkar** — “Kala Chashma” [song, 2016] (#4282) — _'Kala Chashma' é de Amar Arshi/Badshah; não tem Neha Kakkar_  
    ↳ web: 'Kala Chashma' (Baar Baar Dekho, 2016) credita Badshah e Neha Kakkar juntos (Spotify/Apple Music)
- **Badshah × varun_dhawan** — “Garmi” [song, 2019] (#4608) — _Varun Dhawan é ator, não cantor da faixa_  
    ↳ web: Spotify/Apple Music: 'Garmi' de Street Dancer 3D é creditada Badshah feat. Varun Dhawan (e Neha Kakkar)
- **Marracash × Gué** — “Santeria” [album, 2011] (#4712) — _Santeria é álbum de Marracash & Gué (2016), não 2011_  
    ↳ web: Wikipedia: 'Santeria' é álbum colaborativo real de Marracash & Guè (junho de 2016; ano do dataset 2011 está errado, mas a dupla é correta)
- **Jonghyun × Taeyeon** — “Lonely” [song, 2016] (#5085) — _Lonely de 2016 é Jonghyun feat. Taeyeon? duvidoso; canção Lonely é de Jonghyun solo_  
    ↳ web: Wikipedia/Spotify: 'Lonely' é Jonghyun feat. Taeyeon (Story Op.2, 2017)
- **Davichi × T-ara** — “We Were In Love” [song, 2012] (#5180) — _We Were In Love é T-ara x Davichi? título atribuído errado_  
    ↳ web: 'We Were In Love' é colaboração creditada de T-ara e Davichi (2011/2012) (Wikipedia/CCL)
- **Gloria Trevi × Karol G** — “Hijoepu#@ el Momento” [song, 2021] (#5376) — _título real é '160' de Gloria Trevi, não com Karol G_  
    ↳ web: Spotify/Milenio: 'Hijoepu*#' é track de Gloria Trevi feat. Karol G no álbum Diosa de la Noche; motivo sobre '160' é incorreto
- **Marc Anthony × Gloria Estefan** — “Mi Tierra” [song, 2001] (#5482) — _Mi Tierra é álbum/música solo de Gloria Estefan, não dueto com Marc Anthony_  
    ↳ web: YouTube/Facebook: dueto ao vivo de Gloria Estefan & Marc Anthony cantando 'Mi Tierra' (Live in Atlantis / Latin Billboard)
- **Celia Cruz × Marc Anthony** — “Quimbara” [song, 2000] (#5483) — _Quimbara é de Celia Cruz; não dueto com Marc Anthony_  
    ↳ web: Vimeo/Instagram: Celia Cruz & Marc Anthony interpretam 'Quimbara' ao vivo (Divas Live 2001)
- **Juan Gabriel × Rocío Dúrcal** — “Amor Eterno” [song, 1984] (#5487) — _Amor Eterno é canção de Juan Gabriel gravada por Rocío Dúrcal, não dueto_  
    ↳ web: Wikipedia: 'Amor Eterno' gravada por Rocío Dúrcal com Juan Gabriel no álbum 'Canta a Juan Gabriel Vol.6' (1984), há versão em dueto
- **James Arthur × Anne-Marie** — “Rewrite the Stars” [song, 2017] (#5745) — _'Rewrite the Stars' é trilha Greatest Showman, não James Arthur x Anne-Marie_  
    ↳ web: James Arthur & Anne-Marie gravaram cover 'Rewrite The Stars' juntos (The Greatest Showman: Reimagined), confirmado por Spotify/Wikipedia
- **Camilo × Shakira** — “Tutu” [song, 2019] (#5939) — _Tutu é Camilo e Pedro Capó, não Shakira_  
    ↳ web: Spotify/Discogs: 'Tutu (Remix)' 2019 credita Camilo, Shakira e Pedro Capó juntos
- **Sauti Sol × Bien Aime** — “Midnight Train” [song, 2022] (#7408) — _Bien Aime é membro do Sauti Sol, não feature separado; Midnight Train é solo do grupo_  
    ↳ web: Wikipedia: Bien-Aimé Baraza é o vocalista principal do Sauti Sol, que gravou 'Midnight Train' (2020); ambos performam na faixa
- **Chris Stapleton × Justin Timberlake** — “Tennessee Whiskey” [song, 2015] (#8460) — _Tennessee Whiskey é de Stapleton; gravou ao vivo com JT no CMA mas não é single conjunto creditado_  
    ↳ web: Billboard/Rolling Stone: Stapleton e Justin Timberlake fizeram dueto documentado de 'Tennessee Whiskey' no CMA 2015 (04/11/2015)
- **Tasha Cobbs Leonard × Nicki Minaj** — “I'm Getting Ready” [song, 2017] (#8705) — _Tasha Cobbs feat. Nicki Minaj inexistente, fabricação_  
    ↳ web: Billboard/Spotify: 'I'm Getting Ready' de Tasha Cobbs Leonard feat. Nicki Minaj (2017) confirmada
- **beabadoobee × Powfu** — “Death Bed (Coffee for Your Head)” [song, 2020] (#8935) — _'Death Bed' é de Powfu com Beabadoobee (sample), mas crédito incerto e provável confusão; sem feature real desse formato_  
    ↳ web: Discogs/Wikipedia/IMDb: 'death bed (coffee for your head)' creditada 'Powfu Feat. beabadoobee'
- **Weyes Blood × Father John Misty** — “God's Favorite Customer Feature” [song, 2018] (#8996) — _'God's Favorite Customer' é álbum do Father John Misty; feature de Weyes Blood inexistente_  
    ↳ web: Under the Radar/Wikipedia: faixa-título 'God's Favorite Customer' de Father John Misty tem feat. Weyes Blood
- **F.HERO × Milli** — “Mirror Mirror” [song, 2022] (#10474) — _'Mirror Mirror' é solo da Milli, não colab com F.HERO_  
    ↳ web: 'Mirror Mirror' credita F.HERO, MILLI e Changbin juntos (open.spotify.com/letras.com)
- **Chico Buarque × Milton Nascimento** — “Clube da Esquina 2” [album, 1978] (#10847) — _Clube da Esquina 2 (1978) é de Milton; Chico não é co-autor do álbum_  
    ↳ web: Chico Buarque canta em 'Clube da Esquina 2' (1978) de Milton, faixa 'Canción por la Unidad de Latino America' (Wikipedia)
- **Tom Jobim × João Gilberto** — “Chega de Saudade” [album, 1975] (#10856) — _'Chega de Saudade' (1959) é álbum solo de João Gilberto, não dupla com Tom em 1975_  
    ↳ web: 'Chega de Saudade' (1959) é álbum de João Gilberto com Tom Jobim como diretor/arranjador/pianista (Wikipedia/AllMusic)
- **Freddie Stone × Sly Stone** — “Thank You (Falettinme Be Mice Elf Agin)” [song, 1969] (#11256) — _Thank You é do Sly & the Family Stone, não dueto Freddie/Sly_  
    ↳ web: 'Thank You (Falettinme Be Mice Elf Agin)' credita Sly Stone e Freddie Stone na mesma gravação da Family Stone (en.wikipedia.org)
- **Tom Jones × Robbie Williams** — “Are You Gonna Go My Way” [song, 1998] (#11285) — _Are You Gonna Go My Way é de Lenny Kravitz, não Tom Jones/Robbie_  
    ↳ web: 'Are You Gonna Go My Way' é cover de Tom Jones com Robbie Williams no álbum Reload 1999 (Wikipedia/WhoSampled)
- **The Skatalites × Bob Marley** — “Simmer Down” [song, 1964] (#11304) — _Simmer Down é dos Wailers/Bob Marley com Skatalites como backing, não dueto Marley_  
    ↳ web: Simmer Down (1964) creditado como The Skatalites feat. Bob Marley & the Wailers (Wikipedia/theskatalites.bandcamp)
- **Marvin Gaye × Diana Ross** — “You Are Everything” [song, 1974] (#12063) — _'You Are Everything' é dueto Diana Ross & Marvin Gaye, mas não desse ano/forma confiável_  
    ↳ web: Wikipedia/uDiscover: 'You Are Everything' é dueto Diana Ross & Marvin Gaye do álbum 'Diana & Marvin' (single UK #5 abril 1974)
- **The Four Tops × The Supremes** — “The Magnificent 7” [album, 1970] (#12070) — _'The Magnificent 7' é álbum Supremes & Four Tops mas título/atribuição duvidosa_  
    ↳ web: Wikipedia: 'The Magnificent 7' (1970, Motown) é álbum colaborativo de The Supremes & The Four Tops
- **Maren Morris × Hozier** — “The Bones” [song, 2019] (#12510) — _The Bones é de Maren Morris sozinha; Hozier não participa_  
    ↳ web: Rolling Stone/Spotify: existe versão oficial 'The Bones (with Hozier)' lançada em out/2019 creditando ambos
- **Pharrell × Kanye West** — “Number One” [song, 2005] (#12720) — _Number One é Pharrell com Kanye? título não confere_  
    ↳ web: 'Number One' é de Pharrell Williams feat. Kanye West, do álbum In My Mind (en.wikipedia.org, spotify.com)
- **Ivano Fossati × Fabrizio De André** — “Le nuvole” [album, 1990] (#13280) — _Le nuvole é álbum solo De André, não colab Fossati_  
    ↳ web: Wikipedia it: em 'Le nuvole' (1990) Fossati co-escreve 'Mégu megún' e ''Â çímma' com De André
- **Craig David TS5 × Sigala** — “Ain't Giving Up” [song, 2016] (#13562) — _Ain't Giving Up é Craig David com Sigala mas não TS5 set; crédito incerto_  
    ↳ web: Wikipedia/Discogs: 'Ain't Giving Up' (2016) é de Craig David & Sigala juntos
- **Dan + Shay × Kelly Clarkson** — “Keeping Score” [song, 2018] (#13666) — _Keeping Score é de Dan+Shay feat. Kelly mas título/parceria não confirmo solidamente; troca dúbia_  
    ↳ web: 'Keeping Score' (2018) é de Dan + Shay feat. Kelly Clarkson, ambos creditados (en.wikipedia.org, open.spotify.com)
- **Toby Keith × Sting** — “I'm So Happy I Can't Stop Crying” [song, 1997] (#13671) — _I'm So Happy é de Sting solo, não dueto com Toby Keith_  
    ↳ web: 'I'm So Happy I Can't Stop Crying' (1997, Dream Walkin') é dueto Toby Keith com Sting, ambos cantam (en.wikipedia.org, songfacts.com)
- **Block B × Bastarz** — “Conduct Zero” [album, 2015] (#13776) — _Conduct Zero nao é album Block B x Bastarz_  
    ↳ web: Wikipedia/Spotify: EP 'Conduct Zero' (2015) creditado a 'Block B - BASTARZ' (sub-unidade do Block B)
- **Jon Secada × Gloria Estefan** — “Just Another Day” [song, 1992] (#13912) — _'Just Another Day' é solo de Jon Secada_  
    ↳ web: Discogs/Wikipedia: Gloria Estefan faz backing vocals em 'Just Another Day' de Jon Secada (creditada, cortesia Epic)
- **Sheek Louch × The LOX** — “Money, Power & Respect” [album, 1998] (#14160) — _'Money Power Respect' é single, álbum é do The LOX 1998_  
    ↳ web: Wikipedia: album 'Money, Power & Respect' (1998) e do The LOX, grupo do qual Sheek Louch e membro
- **Usher × Nicki Minaj** — “Little Freak” [song, 2010] (#14237) — _'Little Freak' é de Steve Lacy, não Usher x Nicki Minaj_  
    ↳ web: 'Lil Freak' (2010) de Usher traz feat. de Nicki Minaj, single de Raymond v. Raymond (wikipedia/spotify)
- **21 Savage × Childish Gambino** — “Monster” [song, 2017] (#14289) — _'Monster' 21 Savage x Childish Gambino não é faixa real_  
    ↳ web: 'Monster' é faixa real de 21 Savage feat. Childish Gambino do álbum I Am > I Was 2018 (en.wikipedia.org, rollingstone.com)
- **Lil Nas X × Nas** — “Rodeo” [song, 2019] (#14310) — _'Rodeo' do Lil Nas X é com Cardi B, não com Nas_  
    ↳ web: Existe remix oficial de 'Rodeo' de Lil Nas X com Nas, lançado em 27/01/2020 (Spotify credita 'Rodeo - feat. Nas'; Wikipedia)
- **BTS × Fall Out Boy** — “Champion” [song, 2017] (#14431) — _'Champion' é música do Fall Out Boy, não feat BTS_  
    ↳ web: remix de 'Champion' do Fall Out Boy traz RM do BTS (2017) (billboard.com)
- **LiSA × DJ Snake** — “SG” [song, 2021] (#14436) — _'SG' é single Lisa Blackpink; título ultracurto e LiSA errada_  
    ↳ web: 'SG' (2021) credita DJ Snake e LISA de Blackpink juntos (en.wikipedia.org)
- **LiSA × Ozuna** — “SG” [song, 2021] (#14437) — _'SG' é single Lisa Blackpink; título ultracurto e LiSA errada_  
    ↳ web: 'SG' (2021) de DJ Snake credita Ozuna e LISA juntos na mesma faixa (en.wikipedia.org/Spotify)
- **Taylor Swift × Paula Fernandes** — “Long Live” [song, 2012] (#15407) — _par improvável Taylor Swift/Paula Fernandes; 'Long Live' é solo de Taylor_  
    ↳ web: Wikipedia/Apple Music: versao 2012 de 'Long Live' feat. Paula Fernandes com versos em portugues
- **LiSA × Rosalía** — “New Woman” [song, 2024] (#15705) — _New Woman é de Lisa BLACKPINK com Rosalía, não LiSA J-Pop_  
    ↳ web: 'New Woman' (2024) é de Lisa feat. Rosalía, ambas creditadas juntas na faixa (en.wikipedia New Woman song, spotify)
- **Imagine Dragons × Arcane** — “Enemy” [song, 2021] (#15718) — _Arcane é série/trilha, não artista; Enemy é Imagine Dragons com JID_  
    ↳ web: Spotify credita a faixa 'Enemy' como Imagine Dragons, JID, Arcane, League of Legends; 'Arcane' aparece como artista creditado (open.spotify.com)
- **Lana Del Rey × Billie Eilish** — “Ocean Eyes (Remix)” [song, 2019] (#15866) — _remix cruzado fabricado, 'Ocean Eyes' é da Billie_  
    ↳ web: iHeartRadio/YouTube: Lana Del Rey e Billie Eilish cantaram 'Ocean Eyes' juntas ao vivo (Coachella 2024)
- **Megan Thee Stallion × Dua Lipa** — “Sweetest Pie (BTS live)” [live, 2022] (#15931) — _título confuso mistura BTS e Dua Lipa, live improvável_  
    ↳ web: Wikipedia/Spotify: 'Sweetest Pie' (2022) é dueto oficial de Megan Thee Stallion e Dua Lipa
- **Juice WRLD × Suga** — “Girl of My Dreams (Remix)” [song, 2020] (#15960) — _cross-cultural improvável Juice WRLD/Suga BTS remix fabricado_  
    ↳ web: Wikipedia/Spotify: 'Girl of My Dreams' credita Juice WRLD com SUGA do BTS (lançada 2021)
- **RM × Lil Nas X** — “Seoul Town Road” [song, 2019] (#16457) — _'Seoul Town Road' é RM com Lil Nas X, mas título/atribuição confusa_  
    ↳ web: Spotify/Billboard: 'Old Town Road (feat. RM of BTS) [Seoul Town Road Remix]' (2019) credita Lil Nas X e RM juntos
- **Wiz Khalifa × Fall Out Boy** — “Uma Thurman” [song, 2015] (#16659) — _Uma Thurman é do Fall Out Boy sozinho_  
    ↳ web: Existe 'Uma Thurman (Remix)' do Fall Out Boy feat. Wiz Khalifa (Boys of Zummer, 2015) (music.apple.com, open.spotify.com)
- **Justin Bieber × Jeff Bridges** — “We Are the World” [song, 2010] (#16931) — _Jeff Bridges é ator, não vocalista do coletivo_  
    ↳ web: Wikipedia/Songfacts: Jeff Bridges e Justin Bieber estão entre os ~100 artistas de 'We Are the World 25 for Haiti' (2010)
- **Justin Bieber × Rashida Jones** — “We Are the World” [song, 2010] (#16949) — _Rashida Jones é atriz, não vocalista do coletivo_  
    ↳ web: Wikipedia/IMDb: Rashida Jones e Justin Bieber constam no coletivo 'We Are the World 25 for Haiti' (2010)
- **Justin Bieber × Jimmy Jean-Louis** — “We Are the World” [song, 2010] (#16950) — _Jimmy Jean-Louis é ator, não vocalista_  
    ↳ web: Songfacts: Jimmy Jean-Louis (ator haitiano) aparece no coro de 'We Are the World 25 for Haiti' com Justin Bieber
- **Justin Bieber × Nicole Richie** — “We Are the World” [song, 2010] (#16959) — _Nicole Richie não é vocalista do coletivo_  
    ↳ web: Wikipedia/IMDb: Nicole Richie e Justin Bieber constam na lista de vocalistas de 'We Are the World 25 for Haiti' (2010)
- **Justin Bieber × Vince Vaughn** — “We Are the World” [song, 2010] (#16966) — _Vince Vaughn é ator, não vocalista do coletivo_  
    ↳ web: Wikipedia/IMDb: Vince Vaughn e Justin Bieber aparecem entre os participantes de 'We Are the World 25 for Haiti' (2010)
- **Pharrell Williams × Nelly** — “Hot in Herre” [song, 2002] (#17421) — _Hot in Herre é só de Nelly, Pharrell não participa_  
    ↳ web: 'Hot in Herre' de Nelly foi produzida e co-escrita por Pharrell (The Neptunes) (Wikipedia/uDiscover)
- **Tyler, The Creator × Slow Thai** — “WHAT'S GOOD” [song, 2019] (#18046) — _'WHAT'S GOOD' é solo do IGOR_  
    ↳ web: crackmagazine/YouTube: 'WHAT'S GOOD (feat. slowthai & Jerrod Carmichael)', slowthai nos backing vocals

## ⚠️ INVÁLIDAS pendentes de verificação web — 263 (NÃO remover ainda)

Suspeita forte do Passe 1, mas o Passe 2 (web) não rodou nelas por causa do limite semanal. Quando o limite resetar, completo a verificação e movo cada uma para *confirmada* ou *resgatada*.

- **Wizkid × Davido** — “Ondo State Vice President” [song, 2013] (#924) — _título absurdo, fabricação provável_
- **Burna Boy × Coldplay** — “Moon Music” [song, 2024] (#927) — _Moon Music é álbum Coldplay, não feat com Burna_
- **Davido × Future** — “Risky” [song, 2018] (#956) — _Risky é com Popcaan, não Future_
- **Yemi Alade × Funke Akindele** — “Oga Oh” [song, 2021] (#978) — _Funke Akindele é atriz, não cantora; provável fabricação_
- **Ivete Sangalo × David Guetta** — “Mad Love” [song, 2018] (#1713) — _par improvável Axé x EDM; 'Mad Love' não é dela_
- **Claudia Leitte × Pitbull** — “We Are One (Ole Ola)” [song, 2014] (#1714) — _'We Are One' é Pitbull/J.Lo/Claudia Leitte; não esse par bilateral assim_
- **Pabllo Vittar × Gloria Groove** — “Que Tiro Foi Esse?” [song, 2018] (#1719) — _'Que Tiro Foi Esse?' é Jojo Maronttinni, não Pabllo x Gloria_
- **Ivete Sangalo × Claudia Leitte** — “Largadinho” [song, 2014] (#1759) — _'Largadinho' é só da Claudia Leitte, não dueto com Ivete_
- **Ivete Sangalo × Léo Santana** — “Galinha Pintadinha” [song, 2019] (#1761) — _'Galinha Pintadinha' não é colaboração Ivete x Léo Santana_
- **Chico Buarque × Elis Regina** — “Elis & Tom” [album, 1974] (#2304) — _Elis & Tom é com Tom Jobim, não Chico Buarque_
- **Ivete Sangalo × Anitta** — “Esse Cara Sou Eu” [song, 2014] (#2308) — _Esse Cara Sou Eu é de Roberto Carlos, não dessa dupla_
- **Anitta × Bad Bunny** — “Ojitos Lindos” [song, 2022] (#2313) — _Ojitos Lindos é Bad Bunny com Bomba Estéreo, não Anitta_
- **Froid × Criolo** — “Convoque Seu Buda” [album, 2014] (#2333) — _Convoque Seu Buda é álbum de Criolo, não parceria com Froid_
- **Marisa Monte × Anitta** — “Ao Vivo” [live, 2019] (#2784) — _título genérico; Marisa Monte x Anitta improvável ao vivo_
- **Gzuz × Haftbefehl** — “Stress ohne Grund” [song, 2017] (#3963) — _'Stress ohne Grund' é de Shindy/Bushido, não Gzuz×Haftbefehl_
- **Apache 207 × RAF Camora** — “Komet” [song, 2022] (#3972) — _'Komet' é Apache 207 com Udo Lindenberg, não RAF Camora_
- **Casper × Marteria** — “Mosaik” [album, 2017] (#3987) — _'Mosaik' é álbum solo de Marteria, não dueto com Casper_
- **Haftbefehl × Kollegah** — “Nur ein Wort” [song, 2009] (#3992) — _'Nur ein Wort' é de Wir sind Helden, não Haftbefehl×Kollegah_
- **Aurora × Guns N' Roses** — “Sweet Child of Mine” [song, 2016] (#4171) — _cover/cross improvável Aurora x Guns N' Roses_
- **Lenny Kravitz × Jay-Z** — “Guns and Roses” [song, 2001] (#5760) — _não existe música 'Guns and Roses' entre Kravitz e Jay-Z_
- **Polo G × Lil Baby** — “Pop Out” [song, 2019] (#5780) — _'Pop Out' é de Polo G com Lil Tjay, não Lil Baby_
- **Surfaces × Kid Cudi** — “Learn to Fly” [song, 2020] (#5781) — _'Learn to Fly' é dos Foo Fighters, não Surfaces/Kid Cudi_
- **George Ezra × Dua Lipa** — “Hold My Girl (Live)” [live, 2019] (#5786) — _'Hold My Girl' é solo de George Ezra, sem Dua Lipa_
- **Bad Bunny × The Weeknd** — “Caro” [song, 2020] (#5795) — _'Caro' não é colaboração com The Weeknd_
- **Bad Bunny × Myke Towers** — “Si Veo a Tu Mamá” [song, 2020] (#5800) — _'Si Veo a Tu Mamá' é solo de Bad Bunny, sem Myke Towers_
- **Daddy Yankee × Don Omar** — “Conteo” [song, 2004] (#5820) — _'Conteo' é solo de Don Omar, sem Daddy Yankee_
- **Daddy Yankee × Psy** — “Gangnam Style (remix)” [remix, 2012] (#5825) — _'Gangnam Style Remix' não existe com Daddy Yankee_
- **Maluma × Nicki Minaj** — “Pitbull” [song, 2018] (#5846) — _'Pitbull' não é música de Maluma com Nicki Minaj_
- **Maluma × Marc Anthony** — “El Perdedor” [song, 2021] (#5847) — _'El Perdedor' é solo de Maluma, sem Marc Anthony_
- **Big Thief × Adrianne Lenker** — “Two Hands” [album, 2019] (#6224) — _Adrianne Lenker é membro do Big Thief, não colaboração entre pares_
- **The Mars Volta × At the Drive-In** — “Acrobatic Tenement (predecessor band)” [album, 1996] (#6228) — _Acrobatic Tenement é álbum do At the Drive-In, não colab entre bandas_
- **Eagles of Death Metal × Josh Homme** — “Peace Love Death Metal” [album, 2004] (#6230) — _Josh Homme é membro do Eagles of Death Metal, não colab entre pares_
- **La Femme × Gorillaz** — “Saturnz Barz (shared tourline Europe)” [live, 2017] (#6233) — _par improvável; Saturnz Barz é faixa do Gorillaz, não colab com La Femme_
- **Paramore × Zac Farro** — “After Laughter” [album, 2017] (#6236) — _Zac Farro é baterista do Paramore, não colab entre pares_
- **Twenty One Pilots × Stressed Out collab with Kygo** — “Never Let You Go” [song, 2015] (#6237) — _colaboração Twenty One Pilots com Kygo inexistente; título fabricado_
- **Fall Out Boy × Courtney Love** — “Beat It (Mike Shinoda remix) era connection” [feature, 2008] (#6238) — _conexão fabricada entre Fall Out Boy e Courtney Love_
- **Panic! at the Disco × Brendon Urie** — “Vices & Virtues” [album, 2011] (#6239) — _Brendon Urie é o Panic! at the Disco, não colab entre pares_
- **My Chemical Romance × Gerard Way** — “The Black Parade” [album, 2006] (#6240) — _Gerard Way é vocalista do MCR, não colab entre pares_
- **Tom Morello × Rage Against the Machine** — “Evil Empire” [album, 1996] (#6248) — _Tom Morello é membro do RATM; Evil Empire é álbum da banda_
- **Tom Morello × Audioslave** — “Revelations” [album, 2006] (#6249) — _Tom Morello é membro do Audioslave; Revelations é álbum da banda_
- **Oasis × Noel Gallagher** — “(What's the Story) Morning Glory?” [album, 1995] (#6253) — _Noel Gallagher é membro do Oasis; álbum da própria banda_
- **Radiohead × Portishead** — “Atoms for Peace co-inspiration / Glastonbury shared bill” [live, 2013] (#6255) — _rótulo fabricado; Atoms for Peace é projeto de Thom Yorke, não colab Radiohead/Portishead_
- **Waxahatchee × Katie Crutchfield** — “Saint Cloud” [album, 2020] (#6257) — _Katie Crutchfield é a Waxahatchee; Saint Cloud é álbum dela_
- **Hand Habits × Meg Duffy** — “Fun House” [album, 2019] (#6258) — _Meg Duffy é a Hand Habits; álbum do mesmo projeto_
- **Cat Power × Chan Marshall** — “You Are Free” [album, 2003] (#6259) — _Chan Marshall é a Cat Power; You Are Free é álbum dela_
- **Led Zeppelin × The Black Crowes** — “No Quarter: Jimmy Page and Robert Plant Unledded” [album, 1994] (#6267) — _Unledded é projeto de Page e Plant, não colab com The Black Crowes_
- **Carlos Santana × Evander Grillo** — “Maria Maria” [song, 2000] (#6295) — _Maria Maria foi com The Product G&B/Wyclef, não Evander Grillo (nome fabricado)_
- **Barry White × Quincy Jones** — “Soul Bossa Nova” [feature, 1969] (#6534) — _Soul Bossa Nova é de Quincy Jones, Barry White não participa_
- **Curtis Mayfield × Wyclef Jean** — “Ghetto Superstar” [feature, 1998] (#6536) — _Ghetto Superstar é de Pras/ODB/Mýa; Mayfield não participa_
- **Oséias de Paula × Ozéias de Paula** — “Glória e Louvor” [album, 2001] (#7750) — _Oséias e Ozéias de Paula são a mesma pessoa, duplicação artificial_
- **Solange Almeida × Aviões do Forró** — “Largado às Traças” [song, 2012] (#7805) — _Largado às Traças é de Zé Neto & Cristiano, não dessa parceria_
- **Geraldo Azevedo × Alceu Valença** — “Anunciação” [song, 1997] (#7807) — _Anunciação é hit solo de Alceu Valença, não parceria com Geraldo_
- **Geraldo Azevedo × Dominguinhos** — “Asa Branca” [live, 2000] (#7808) — _Asa Branca é de Luiz Gonzaga; live atribuído indevidamente_
- **Alceu Valença × Dominguinhos** — “Xote das Meninas” [live, 1998] (#7810) — _Xote das Meninas é de Luiz Gonzaga, não parceria Alceu/Dominguinhos_
- **Calcinha Preta × Xand Avião** — “Show das Poderosas” [live, 2017] (#7824) — _Show das Poderosas é da Anitta, não parceria Calcinha Preta/Xand_
- **Emicida × Gloria Groove** — “Libre Soy (feat. Gloria Groove)” [feature, 2020] (#8121) — _Libre Soy é versão Frozen de Gloria Groove, sem Emicida_
- **Anitta × Pabllo Vittar** — “Sua Cara (feat. J Balvin)” [feature, 2017] (#8127) — _Sua Cara é Major Lazer feat Anitta e Pabllo, não feat J Balvin_
- **Mahmundi × Letrux** — “Vaporwave Tropical” [song, 2018] (#8138) — _título Vaporwave Tropical com Letrux parece fabricado_
- **Nação Zumbi × Raimundos** — “Manguebeat Ao Vivo” [live, 1999] (#8155) — _live Manguebeat de Nação Zumbi com Raimundos parece fabricada_
- **Jota Quest × Capital Inicial** — “Rock Brasileiro Hoje” [live, 2008] (#8159) — _título genérico Rock Brasileiro Hoje parece fabricado_
- **Paralamas do Sucesso × Engenheiros do Hawaii** — “Rock Clássico Brasileiro” [live, 2009] (#8162) — _título genérico Rock Clássico Brasileiro parece fabricado_
- **Engenheiros do Hawaii × Capital Inicial** — “Anos 80 Ao Vivo” [live, 2005] (#8164) — _título genérico Anos 80 Ao Vivo parece fabricado_
- **Barão Vermelho × Titãs** — “Rock Brasileiro Anos 80” [live, 1997] (#8165) — _título genérico Rock Brasileiro Anos 80 parece fabricado_
- **Titãs × Engenheiros do Hawaii** — “Titãs e Engenheiros” [live, 1999] (#8166) — _título genérico Titãs e Engenheiros parece fabricado_
- **Zeca Baleiro × Lenine** — “Nordeste Ao Vivo” [live, 2007] (#8176) — _título genérico Nordeste Ao Vivo parece fabricado_
- **Cássia Eller × Paralamas do Sucesso** — “Ao Vivo Cássia” [live, 1997] (#8178) — _título genérico Ao Vivo Cássia parece fabricado_
- **Cidade Negra × Natiruts** — “Reggae no Brasil” [live, 2002] (#8181) — _título genérico Reggae no Brasil parece fabricado_
- **Natiruts × Ponto de Equilíbrio** — “Natiruts e Ponto” [live, 2006] (#8182) — _título genérico Natiruts e Ponto parece fabricado_
- **Ponto de Equilíbrio × Planta e Raiz** — “Reggae Roots Brasil” [song, 2008] (#8183) — _título genérico Reggae Roots Brasil parece fabricado_
- **Marcelo Falcão × Charlie Brown Jr.** — “CBJ e Marcelo” [live, 2013] (#8186) — _título genérico CBJ e Marcelo parece fabricado_
- **William Onyeabor × Sufjan Stevens** — “African Festival Feature” [live, 2013] (#9201) — _Onyeabor não tocava ao vivo; par implausível com Sufjan_
- **Bizarrap × WOS** — “WOS: Bzrp Music Sessions, Vol. 98” [song, 2018] (#9246) — _WOS Vol. 98 não existe (real é Vol. 12); ano errado_
- **Linn da Quebrada × Luísa Sonza** — “Corpo Sensual” [song, 2022] (#9554) — _Corpo Sensual é de Pabllo Vittar, não dessa dupla_
- **Juanes × Carlos Rivera** — “Tu Falta de Querer” [song, 2020] (#9567) — _Tu Falta de Querer é de Mon Laferte, não dessa dupla_
- **Ricky Martin × Maluma** — “No Me Conoce” [song, 2018] (#9571) — _No Me Conoce é de Jhay Cortez/Bad Bunny, não Ricky Martin_
- **Oruam × MC Cabelinho** — “Poesia Acústica” [song, 2022] (#9619) — _Poesia Acústica é série do Pineapple, não dessa dupla isolada_
- **Peso Pluma × Bad Bunny** — “La Comunidad” [song, 2023] (#9629) — _não existe colaboração documentada Peso Pluma com Bad Bunny_
- **Basshunter × Alan Walker** — “Scandinavia Bass” [song, 2019] (#10080) — _título genérico, sem colaboração documentada Basshunter/Alan Walker_
- **Basshunter × Kygo** — “Bass Drive” [song, 2018] (#10081) — _sem música real Basshunter/Kygo, título genérico_
- **Basshunter × Swedish House Mafia** — “Nordic Rave” [live, 2010] (#10082) — _show fabricado, título genérico_
- **Avicii × Kygo** — “Norwegian Forest” [song, 2015] (#10084) — _sem música real Avicii/Kygo_
- **Ace of Base × Roxette** — “Swedish Pop Legends Tour” [live, 2002] (#10085) — _turnê fabricada com título genérico_
- **Ace of Base × ABBA** — “Swedish Pop History” [live, 2000] (#10086) — _ABBA inativa em 2000, show fabricado_
- **ABBA × Roxette** — “Scandinavian Pop Icons” [live, 1998] (#10087) — _ABBA inativa em 1998, evento fabricado_
- **ABBA × Robyn** — “Swedish Generations” [live, 2010] (#10088) — _colaboração ao vivo fabricada_
- **Roxette × Robyn** — “Swedish Divas” [live, 2008] (#10089) — _título genérico, show inexistente_
- **Roxette × Ace of Base** — “Retro Sweden Night” [live, 2005] (#10090) — _evento fabricado, título genérico_
- **Björk × Of Monsters and Men** — “Iceland Together” [live, 2015] (#10091) — _show ao vivo fabricado, título genérico_
- **Björk × First Aid Kit** — “Scandinavian Women Unite” [live, 2017] (#10092) — _evento fabricado, título temático genérico_
- **Björk × Sigrid** — “Nordic Women Music” [live, 2019] (#10093) — _colaboração ao vivo fabricada_
- **Röyksopp × Kygo** — “Northern Drift” [song, 2016] (#10100) — _sem música real Röyksopp/Kygo_
- **Ghost × Ariya** — “Metal Connection Europe” [live, 2018] (#10143) — _'Ariya' não é ato reconhecido, colaboração fabricada_
- **Natalia Szroeder × Natalia Kills** — “Natalia Duet” [song, 2020] (#10168) — _Natalia Kills não é polonesa, par improvável fabricado_
- **t.A.T.u. × Serebro** — “Russian Girl Groups” [live, 2010] (#10260) — _título descritivo genérico, show conjunto improvável_
- **Glukoza × Serebro** — “Russian Pop” [live, 2011] (#10261) — _título genérico fabricado, sem registro real_
- **Nyusha × Artik & Asti** — “Russian Divas” [live, 2018] (#10263) — _título descritivo genérico, live fabricada_
- **Nyusha × Polina Gagarina** — “Rossiyskiye Pevitsy” [live, 2017] (#10264) — _título genérico fabricado_
- **Polina Gagarina × Alsou** — “Russia Beautiful Voices” [live, 2017] (#10266) — _título descritivo genérico fabricado_
- **Dimash Kudaibergen × Alina Zagitova** — “Kazakhstan Russia Stars” [live, 2020] (#10267) — _patinadora x cantor, título genérico, improvável_
- **Dimash Kudaibergen × Valentina Monetta** — “International Connection” [live, 2021] (#10268) — _par improvável, título genérico fabricado_
- **Gjon's Tears × Tamta** — “Mediterranean Voices” [live, 2021] (#10269) — _título genérico fabricado, live improvável_
- **Gjon's Tears × Valentina Monetta** — “Eurovision Voices” [live, 2021] (#10270) — _título genérico fabricado_
- **Gjon's Tears × Eleni Foureira** — “Eurovision Stars” [live, 2022] (#10271) — _título genérico fabricado_
- **Valentina Monetta × Naviband** — “Eurovision Connections” [live, 2017] (#10272) — _título genérico fabricado_
- **Valentina Monetta × Efendi** — “Small Countries Eurovision” [live, 2021] (#10273) — _título genérico fabricado_
- **Efendi × Tamta** — “Balkan Pop Stars” [song, 2022] (#10275) — _título genérico fabricado_
- **Naviband × ZENA** — “Belarus Eurovision” [live, 2019] (#10276) — _título genérico fabricado_
- **Andrei Lenitsky × Naviband** — “Belarus Together” [live, 2019] (#10279) — _título genérico fabricado_
- **Ivi Adamou × Helena Paparizou** — “Greek Cypriot Connection” [live, 2012] (#10280) — _título descritivo genérico fabricado_
- **Ivi Adamou × Tamta** — “Cypriot Stars” [song, 2020] (#10282) — _título genérico fabricado_
- **Ivi Adamou × Paola** — “Cyprus Sisters” [song, 2015] (#10283) — _título genérico fabricado_
- **Despina Vandi × Notis Sfakianakis** — “Laïká Night” [live, 2010] (#10285) — _título genérico fabricado_
- **Despina Vandi × Stavros Flatley** — “Hellenic Dance” [live, 2010] (#10287) — _Stavros Flatley é dupla cômica de dança, colaboração fabricada_
- **Sakis Rouvas × Kostas Martakis** — “Greek Boys Pop” [live, 2010] (#10291) — _título genérico fabricado_
- **Sakis Rouvas × Demy** — “Greek Celebrities” [live, 2018] (#10292) — _título genérico fabricado_
- **Eleni Foureira × Tamta** — “Balkan Party” [song, 2019] (#10293) — _título genérico fabricado_
- **Eleni Foureira × Ivi Adamou** — “Balkan Festival” [live, 2021] (#10294) — _título genérico fabricado_
- **Antique × Despina Vandi** — “Greek Night” [live, 2006] (#10295) — _título genérico fabricado_
- **Nikos Vertis × Despina Vandi** — “Greek Love Songs” [live, 2012] (#10296) — _título genérico fabricado_
- **Nikos Vertis × Giorgos Mazonakis** — “Laïká Duet” [song, 2011] (#10297) — _título genérico fabricado_
- **Giorgos Mazonakis × Notis Sfakianakis** — “Greek Night” [live, 2009] (#10298) — _título genérico fabricado_
- **Giorgos Mazonakis × Despina Vandi** — “Greek Summer” [song, 2012] (#10299) — _título genérico fabricado_
- **Paola × Helena Paparizou** — “Cypriot Greek Night” [live, 2013] (#10300) — _título genérico fabricado_
- **Kostas Martakis × Sarbel** — “Greek Boys Eurovision” [live, 2012] (#10301) — _título genérico fabricado_
- **Stereo Mike × Sarbel** — “Greek Boys” [live, 2012] (#10302) — _título genérico fabricado, par improvável_
- **Alexandra Stan × Edward Maya** — “Romanian Night” [song, 2012] (#10304) — _título genérico fabricado_
- **Alexandra Stan × Akcent** — “Romanian Dance Pop” [song, 2013] (#10305) — _título genérico fabricado_
- **Edward Maya × Inna** — “Romanian Vibes” [song, 2010] (#10306) — _título genérico fabricado_
- **Edward Maya × Akcent** — “Romanian Beats” [song, 2011] (#10307) — _título genérico fabricado_
- **Costi × Connect-R** — “Romanian Production” [song, 2013] (#10308) — _título genérico fabricado_
- **Akcent × Inna** — “Balkan Night” [song, 2011] (#10309) — _título genérico fabricado_
- **Smiley × Alex Velea** — “Romanian Pop” [song, 2015] (#10311) — _título genérico fabricado_
- **Lora × Irina Rimes** — “Pop Feminin Romania” [song, 2019] (#10314) — _título genérico fabricado_
- **Lora × What's Up** — “Romanian Pop Duet” [song, 2016] (#10315) — _título genérico fabricado_
- **Alex Velea × Costi** — “Production Collab” [song, 2017] (#10316) — _título genérico fabricado_
- **Vanotek × Carla's Dreams** — “Romanian Electronic” [song, 2018] (#10319) — _título genérico fabricado_
- **Carla's Dreams × Smiley** — “Moldovan Romanian Night” [song, 2018] (#10320) — _título genérico fabricado_
- **Delia × Loredana** — “Romanian Pop Legends” [live, 2018] (#10321) — _título genérico fabricado, gênero bg incoerente_
- **Delia × Costi** — “Romanian Diva Production” [song, 2016] (#10322) — _título genérico fabricado_
- **Loredana × Alex Velea** — “Romania Stage” [live, 2017] (#10323) — _título genérico fabricado_
- **Speak × Smiley** — “Romanian Rap Pop” [song, 2017] (#10324) — _título genérico fabricado_
- **Ioana Ignat × Carla's Dreams** — “Romanian Voices” [song, 2019] (#10325) — _título genérico fabricado_
- **Ioana Ignat × Vanotek** — “Romanian Pop Electronic” [song, 2020] (#10326) — _título genérico fabricado_
- **Ioana Ignat × Smiley** — “Romanian Young Star” [song, 2021] (#10327) — _título genérico fabricado_
- **Jain × -M-** — “European Pop Ladies” [live, 2018] (#10330) — _título genérico fabricado_
- **Jain × Zara Larsson** — “Pop Ladies Europe” [live, 2019] (#10331) — _título genérico fabricado, live improvável_
- **Monika Lewczuk × Dawid Podsiadło** — “Polish Music Scene” [live, 2018] (#10332) — _título genérico fabricado_
- **Stavros Flatley × Antique** — “Greek Heritage Night” [live, 2011] (#10337) — _Stavros Flatley dupla cômica, colaboração fabricada_
- **John Newman × Zara Larsson** — “Pop Night Europe” [live, 2017] (#10339) — _título genérico fabricado_
- **Dua Lipa × Zara Larsson** — “Pop Queens” [live, 2018] (#10342) — _título genérico fabricado, live improvável_
- **Dua Lipa × Sigrid** — “Pop Ladies Tour” [live, 2019] (#10343) — _título genérico fabricado, live improvável_
- **Coldplay × Kygo** — “Festival Stage Collab” [live, 2022] (#10344) — _título genérico fabricado_
- **Alina Zagitova × Polina Gagarina** — “Russian Ice Show” [live, 2019] (#10346) — _patinadora x cantora, título genérico fabricado_
- **Alina Zagitova × Dima Bilan** — “Russian Stars on Ice” [live, 2020] (#10347) — _patinadora x cantor, título genérico fabricado_
- **Ozark Henry × Alan Walker** — “Scandinavian Electronic Link” [song, 2020] (#10348) — _título genérico fabricado, par improvável_
- **Ozark Henry × Kygo** — “Chill Electronic Collab” [song, 2021] (#10349) — _título genérico fabricado, par improvável_
- **Avicii × Sigrid** — “Nordic EDM Pop” [song, 2017] (#10350) — _título genérico inventado, sem colaboração documentada Avicii x Sigrid_
- **Avicii × Alan Walker** — “Scandi Drop” [song, 2016] (#10351) — _título 'Scandi Drop' fabricado, sem música Avicii x Alan Walker_
- **Agnez Mo × BTS** — “Not A Single Word” [feature, 2021] (#10359) — _colaboração Agnez Mo x BTS não existe, título fabricado_
- **Warren Hue × BTS** — “Yet to Come” [feature, 2022] (#10364) — _'Yet to Come' é do BTS sozinho, sem Warren Hue_
- **NIKI × Warren Hue** — “Buzzcut” [song, 2021] (#10366) — _'Buzzcut' é Rich Brian, não NIKI x Warren Hue_
- **Juan Karlos × Moira Dela Torre** — “Buwan” [song, 2020] (#10390) — _'Buwan' é do Juan Karlos sozinho, sem Moira Dela Torre_
- **Gloc-9 × Flow G** — “Upuan” [song, 2010] (#10396) — _'Upuan' é do Gloc-9 feat. Jeazell Grutas, não Flow G_
- **Abra × Gloc-9** — “Magbalik” [song, 2015] (#10400) — _'Magbalik' é do Callalily, não Abra x Gloc-9_
- **BINI × SB19** — “Pantropiko” [feature, 2023] (#10407) — _'Pantropiko' é do BINI sozinho, sem SB19_
- **SunKissed Lola × Ben&Ben** — “Pagtingin” [song, 2022] (#10408) — _'Pagtingin' é do Ben&Ben, não SunKissed Lola_
- **Ebe Dancel × Bamboo** — “Noypi” [song, 2019] (#10411) — _'Noypi' é do Bamboo, não Ebe Dancel_
- **Rizky Febian × Mahalini** — “Adu Rayu” [song, 2023] (#10438) — _'Adu Rayu' é Yovie/Tulus/Glenn, não Rizky Febian x Mahalini_
- **Peter Bjorn and John × Cœur de Pirate** — “Young Folks” [song, 2007] (#11115) — _Young Folks é com Victoria Bergsman, não Cœur de Pirate_
- **dawn_golden × ODESZA** — “Say My Name” [song, 2014] (#11121) — _Say My Name da ODESZA é com Zyra, não dawn golden_
- **Dimmu Borgir × Cradle of Filth** — “Heartwork” [song, 2003] (#11135) — _Heartwork é álbum do Carcass, não desses_
- **The Who × The Rolling Stones** — “The Kids Are Alright” [song, 1965] (#11147) — _The Kids Are Alright é só do The Who_
- **Claptone × Seal** — “No Eyes” [song, 2016] (#11152) — _No Eyes do Claptone é feat Jaw, não Seal_
- **Breakbot × Ed Sheeran** — “Break of Dawn” [song, 2012] (#11157) — _Ed Sheeran em faixa de Breakbot é fabricação cross-genre_
- **Aurora Aksnes × Billie Eilish** — “No Time to Die (AURORA cover, released by Billie Eilish)” [song, 2020] (#11442) — _'No Time to Die' é da Billie Eilish, não colaboração com AURORA_
- **Alanis Morissette × Dave Coulier** — “You Oughta Know (written about)” [song, 1995] (#11458) — _Coulier é inspiração da letra, não colaboração musical_
- **Nirvana × David Bowie** — “The Man Who Sold the World” [song, 1993] (#11462) — _cover do Nirvana de música do Bowie, não colaboração_
- **Tower of Power × Santana** — “Africa Speaks, America Responds” [album, 1972] (#11477) — _título fabricado; não há álbum conjunto Tower of Power x Santana_
- **The Vandellas × Marvin Gaye** — “Dancing in the Street” [song, 1964] (#11478) — _'Dancing in the Street' é de Martha & the Vandellas, não de Marvin Gaye_
- **Snow Patrol × Gary Lightbody** — “Run (covered by Leona Lewis)” [song, 2008] (#11485) — _Lightbody é o vocalista do Snow Patrol, não colaboração externa_
- **Geri Halliwell × Spice Girls** — “Wannabe” [song, 1996] (#11487) — _Geri Halliwell é membro das Spice Girls, não colaboração_
- **Morrissey × Johnny Marr** — “This Charming Man (The Smiths)” [song, 1983] (#11488) — _Morrissey e Marr são The Smiths, não colaboração externa_
- **Post Malone × Travis Scott** — “No Bystanders” [feature, 2018] (#12244) — _'No Bystanders' (Astroworld) tem Juice WRLD e Sheck Wes, não Post Malone_
- **Billie Eilish × Gorillaz** — “The Valley of The Pagans” [feature, 2020] (#12250) — _'The Valley of the Pagans' do Gorillaz é com Beck, não Billie Eilish_
- **Doja Cat × Young Thug** — “The Real Slim Shady” [feature, 2020] (#12256) — _'The Real Slim Shady' é do Eminem, não colaboração Doja x Young Thug_
- **Pharrell Williams × Nelly** — “Hot in Herre” [feature, 2002] (#12276) — _'Hot in Herre' é Nelly produzido por Pharrell/Neptunes, não feature de Pharrell_
- **Pharrell Williams × Gwen Stefani** — “Hollaback Girl” [feature, 2004] (#12277) — _'Hollaback Girl' é Gwen Stefani produzida por Pharrell, não feature dele_
- **50 Cent × Young Buck** — “Wanksta” [feature, 2003] (#12282) — _'Wanksta' é solo de 50 Cent (8 Mile OST), sem Young Buck_
- **DJ Khaled × Beyoncé** — “Hold You Down” [feature, 2015] (#12285) — _'Hold You Down' tem Chris Brown/Alsina/Future/Jeremih, não Beyoncé_
- **Sia × Diplo** — “Elastic Heart” [feature, 2014] (#12301) — _'Elastic Heart' Sia produzida com Diplo/Greg Kurstin, não feature de Diplo_
- **Adele × Beyoncé** — “No Angel” [feature, 2013] (#12314) — _'No Angel' é da Beyoncé (2013) sem Adele; feature fabricado_
- **Metro Boomin × Future** — “Super Slimey” [album, 2017] (#12323) — _'Super Slimey' é mixtape Future x Young Thug, não Metro Boomin_
- **Metro Boomin × Post Malone** — “No Complaints” [song, 2017] (#12324) — _'No Complaints' Metro Boomin tem Offset e Drake, não Post Malone_
- **Waka Flocka Flame × Drake** — “Grove St. Party” [song, 2010] (#13152) — _'Grove St. Party' é Waka Flocka feat. Kebo Gotti, não Drake_
- **Christine and the Queens × Madonna** — “Runway” [song, 2015] (#13205) — _'Runway' Christine and the Queens com Madonna não existe; fabricação_
- **Pulp × Common People** — “Common People” [song, 1995] (#13493) — _Common People não é artista, é a própria música_
- **Beyoncé × Andre 3000** — “Back to Black” [song, 2007] (#14490) — _'Back to Black' é da Amy Winehouse; não é feat Beyoncé/Andre 3000 em 2007_
- **Halsey × Travis Scott** — “11 Minutes” [song, 2019] (#14511) — _'11 Minutes' é com Travis Barker, não Travis Scott_
- **Meghan Trainor × Psy** — “Cheer Up” [song, 2016] (#14517) — _'Cheer Up' é da TWICE; não é feat Meghan Trainor x Psy_
- **Normani × Ty Dolla $ign** — “Nicki & Normani” [song, 2018] (#14530) — _título 'Nicki & Normani' fabricado; não é faixa real deles_
- **H.E.R. × Juice WRLD** — “Juice WRLD & H.E.R.” [feature, 2019] (#14533) — _título 'Juice WRLD & H.E.R.' fabricado; não é faixa real_
- **Lana Del Rey × Sublime with Rome** — “Ride” [song, 2012] (#14558) — _'Ride' é música solo de Lana Del Rey; não feat Sublime with Rome_
- **Avicii × Coldplay** — “A Sky Full of Stars” [song, 2014] (#14560) — _'A Sky Full of Stars' é do Coldplay, produzido por Avicii mas não feat_
- **Skrillex × Porter Robinson** — “Shelter” [song, 2016] (#14571) — _'Shelter' é Porter Robinson & Madeon, não envolve Skrillex_
- **Gunna × Roddy Ricch** — “Dollaz on My Head” [song, 2020] (#14613) — _Dollaz on My Head é Gunna/Young Thug, não Roddy Ricch_
- **Offset × Drake** — “No Heart” [song, 2016] (#14623) — _No Heart é 21 Savage/Metro, não Offset/Drake_
- **Timbaland × Ludacris** — “Do It Like a Dude” [song, 2010] (#14633) — _Do It Like a Dude é da Jessie J, não Timbaland/Ludacris_
- **Timbaland × SZA** — “I Ain't Worried (Remix)” [song, 2022] (#14634) — _I Ain't Worried é OneRepublic; remix Timbaland/SZA fabricado_
- **Big Sean × Chris Brown** — “Beware” [song, 2013] (#14642) — _Beware é Big Sean/Lil Wayne/Jhené, não Chris Brown_
- **Jack Harlow × Lil Wayne** — “Way Out” [song, 2020] (#14652) — _Way Out de Jack Harlow é com Big Sean, não Lil Wayne_
- **Jack Harlow × Lil Baby** — “Drip Hard” [song, 2020] (#14657) — _Drip Hard é Lil Baby/Gunna, não Jack Harlow_
- **Nas × Kelis** — “21 Questions” [song, 2003] (#14668) — _21 Questions é de 50 Cent/Nate Dogg, não Nas/Kelis_
- **BLACKPINK × Sia** — “The Album” [feature, 2020] (#14768) — _'The Album' é álbum, não feature único; título errado_
- **BLACKPINK × Tyga** — “Happy New Year” [song, 2018] (#14769) — _BLACKPINK e Tyga não têm essa música juntos_
- **Jennie × Vince Staples** — “90s Rap (Collab)” [feature, 2023] (#14770) — _título genérico fabricado, colab inexistente_
- **Jennie × Zico** — “Any Song (Remix)” [song, 2020] (#14773) — _'Any Song' é do Zico; remix com Jennie inexistente_
- **J-Hope × BTS** — “Dynamite” [song, 2020] (#14781) — _'Dynamite' é do BTS inteiro, não feat de J-Hope_
- **Red Hot Chili Peppers × Wu-Tang Clan** — “Pure Imagination (Live)” [live, 2022] (#14790) — _RHCP com Wu-Tang ao vivo é fabricação improvável_
- **Red Hot Chili Peppers × Elton John** — “True Blue” [song, 2022] (#14791) — _RHCP com Elton John 'True Blue' inexistente_
- **Panic! at the Disco × Lil Wayne** — “I Write Sins Not Tragedies (Remix)” [song, 2006] (#14793) — _remix de Lil Wayne com Panic! inexistente_
- **Panic! at the Disco × Hayley Williams** — “Victorious (feature)” [feature, 2016] (#14794) — _'Victorious' não tem Hayley Williams_
- **The 1975 × Taylor Swift** — “The 1975 (song)” [feature, 2020] (#14796) — _The 1975 com Taylor Swift feature inexistente_
- **Burna Boy × J. Balvin** — “Tu No Metes Cabra” [song, 2019] (#14805) — _'Tu No Metes Cabra' é de Bad Bunny, não Burna/Balvin_
- **Kacey Musgraves × León Larregui** — “Intercultural (feature)” [feature, 2019] (#14816) — _título genérico 'Intercultural' fabricado_
- **The Weeknd × J. Balvin** — “Miracle” [song, 2023] (#14828) — _'Miracle' é Calvin Harris/Ellie Goulding, não Weeknd/Balvin_
- **The Weeknd × SZA** — “Die for You (Remix)” [song, 2023] (#14829) — _remix de 'Die for You' é com Ariana Grande, não SZA_
- **The Weeknd × Republic Records** — “Moth to a Flame” [song, 2021] (#14834) — _'Republic Records' é gravadora, não artista_
- **Sia × Kylie Minogue** — “A Sky Full of Stars” [song, 2013] (#14839) — _'A Sky Full of Stars' é do Coldplay, não Sia/Kylie_
- **Sia × LSD** — “Audio” [song, 2019] (#14844) — _título 'Audio' genérico; LSD é grupo da própria Sia_
- **Tate McRae × Jeremy Zucker** — “we fell in love in october” [song, 2022] (#14849) — _'october' é de Jeremy Zucker/BENÉE, não Tate McRae_
- **Zedd × Alessia Cara** — “Stay the Night” [song, 2014] (#14872) — _'Stay the Night' é com Hailee/Hayley, não Alessia Cara_
- **Martin Garrix × Usher** — “Tremor” [song, 2014] (#14883) — _'Tremor' é instrumental, sem Usher_
- **Roddy Ricch × Luke Combs** — “Forever After All” [song, 2021] (#15573) — _Forever After All é solo de Luke Combs, sem Roddy Ricch_
- **Bizarrap × J. Balvin** — “Outro (Collab)” [song, 2023] (#15653) — _título genérico Outro Collab não é faixa real_
- **Marc Anthony × Will Smith** — “Gettin' Jiggy Wit It (Latin Remix)” [song, 1998] (#15656) — _remix latino de Will Smith com Marc Anthony inexistente_
- **Marc Anthony × Alejandro Fernández** — “Vivir Mi Vida (Remix)” [song, 2014] (#15657) — _Vivir Mi Vida remix com Alejandro Fernández inexistente_
- **Bad Bunny × Becky G** — “Volví” [song, 2021] (#16341) — _'Volví' é Aventura, não Becky G_
- **Rauw Alejandro × Rosalía** — “Vampire (Remix)” [song, 2021] (#16353) — _'Vampire' é Olivia Rodrigo, Rauw/Rosalía fizeram 'Beso'_
- **Myke Towers × Bad Bunny** — “Gata Only (Remix)” [song, 2023] (#16374) — _'Gata Only' é FloyyMenor/Cris Mj, não estes_
- **Green Day × Norah Jones** — “Love Is for Losers” [song, 2023] (#16472) — _Norah Jones colaborou com Billie Joe (Foreverly), não Green Day_
- **Hozier × Alicia Keys** — “In a Week (feat. Alicia Keys)” [song, 2019] (#16476) — _original tem Karen Cowley, não Alicia Keys_
- **Wizkid × Starboy** — “Manya” [song, 2017] (#16486) — _Starboy é o próprio alias/selo de Wizkid_
- **Ayra Starr × Seyi Vibez** — “Last Heartbreak Song” [song, 2023] (#16489) — _Last Heartbreak Song é com Giveon, não Seyi Vibez_
- **Morgan Wallen × Jason Aldean** — “Long Live Cowgirls (Duet)” [song, 2022] (#16497) — _Long Live Cowgirls é com Ernest, não Aldean_
- **Morgan Wallen × Nelly** — “Wasted on You (Remix)” [song, 2021] (#16498) — _remix com Nelly não existe_
- **J. Balvin × Khalid** — “Ecuador” [song, 2023] (#16500) — _faixa Ecuador com Khalid não existe_
- **Ariana Grande × Childish Gambino** — “Just Look Up” [song, 2021] (#16504) — _Just Look Up é da Ariana com Kid Cudi, não Gambino_
- **Justin Bieber × Blake Shelton** — “10,000 Hours” [song, 2019] (#16517) — _10,000 Hours é do Dan + Shay, não Blake Shelton_
- **Shawn Mendes × Macklemore** — “Growing Pains” [song, 2017] (#16518) — _colaboração inexistente_
- **Demi Lovato × Anitta** — “Mal Acostumbrado” [song, 2022] (#16520) — _provável fabricação cross-cultural_
- **Demi Lovato × Iggy Pop** — “California Sober” [song, 2021] (#16523) — _California Sober é solo da Demi, sem Iggy Pop_
- **Demi Lovato × Sirah** — “Ain't Your Mama” [song, 2013] (#16524) — _colaboração inexistente_
- **Demi Lovato × Kehlani** — “No Promises” [song, 2017] (#16526) — _No Promises é do Cheat Codes, não Kehlani_
- **Adele × Rick Rubin** — “30 (production)” [album, 2021] (#16528) — _Rick Rubin produziu 21, não 30_
- **Doja Cat × Roddy Ricch** — “Streets” [song, 2021] (#16537) — _Streets é solo da Doja Cat_
- **Doja Cat × Maluma** — “El Beso del Final” [song, 2022] (#16539) — _colaboração inexistente_
- **Daniel Caesar × Raphael Saadiq** — “Get You” [song, 2017] (#16548) — _Get You tem Kali Uchis, não Raphael Saadiq_
- **Frank Ocean × John Mayer** — “Slide” [song, 2017] (#16552) — _Slide é do Calvin Harris com Frank e Migos, não Mayer_
- **Gunna × SZA** — “Fortnite” [song, 2023] (#18119) — _título Fortnite improvável entre Gunna e SZA_
- **Wisin & Yandel × Maluma** — “Cuatro Babys (Yandel solo)” [song, 2016] (#18384) — _Cuatro Babys é de Maluma sem Yandel/Wisin_
- **Peso Pluma × Nicki Minaj** — “BZRP x Peso Pluma (remix feature)” [song, 2023] (#18439) — _título confuso BZRP, feature Nicki Minaj inexistente_
- **Peso Pluma × Marshmello** — “El Hombre Que Perdio” [song, 2023] (#18447) — _colaboração com Marshmello, título fabricado_
- **Peso Pluma × El Alfa** — “La Jumpa” [song, 2023] (#18448) — _La Jumpa é Anuel/Bad Bunny, não Peso Pluma/El Alfa_

## ♻️ Duplicatas exatas — 632 cópias redundantes

Mesmo par + mesmo título (normalizado). A primeira ocorrência fica; estas são cópias. Limpeza segura independente de autenticidade. Lista completa em `audit_data/duplicatas_exatas.csv`. Amostra:

- **SZA × Drake** — “Slime You Out” [song, 2023] (#119) — _Slime You Out real porém flag dup_of_11, possível duplicata_
- **Calvin Harris × Pharrell Williams** — “Feels” [live, 2017] (#137) — _versão live com flag dup_of_136, possível duplicata_
- **Metro Boomin × Future** — “Heroes & Villains” [album, 2022] (#151) — _flag dup_of_149, possível duplicata_
- **Cardi B × Bruno Mars** — “Finesse (Remix)” [song, 2018] (#178) — _Finesse Remix real porém flag dup_of_109, possível duplicata_
- **Sia × David Guetta** — “Titanium” [song, 2011] (#229) — _possível duplicata de 212_
- **Swae Lee × Post Malone** — “Sunflower” [song, 2018] (#242) — _possível duplicata de 93_
- **Mac Miller × Anderson .Paak** — “Dang!” [song, 2016] (#246) — _possível duplicata de 154_
- **Chance the Rapper × Kanye West** — “Ultralight Beam” [song, 2016] (#248) — _possível duplicata de 24_
- **Bryson Tiller × Rihanna** — “Wild Thoughts” [song, 2017] (#420) — _possível duplicata (dup_of_418)_
- **DJ Snake × Major Lazer** — “Lean On” [song, 2015] (#477) — _possível duplicata_
- **The 1975 × Phoebe Bridgers** — “Jesus Christ 2005 God Bless America” [song, 2020] (#597) — _possível duplicata (dup_of_452)_
- **Caetano Veloso × Gilberto Gil** — “Dois Amigos, Um Século de Música” [dvd, 2016] (#602) — _possível duplicata (dup_of_584)_
- **Wesley Safadão × Anitta** — “Romance Com Safadeza” [song, 2016] (#619) — _possível duplicata (dup_of_582)_
- **Titãs × Os Paralamas do Sucesso** — “Titãs e Os Paralamas Juntos” [live, 2009] (#655) — _possível duplicata de 654_
- **Caetano Veloso × Maria Bethânia** — “Caetano e Bethânia ao Vivo” [live, 1978] (#683) — _possível duplicata (dup_of_585)_
- **Jorge Ben Jor × Gilberto Gil** — “Gil e Jorge (Ogum, Xangô)” [album, 1975] (#719) — _possível duplicata (dup_of_587)_
- **Anitta × Ludmilla** — “Onda Diferente” [song, 2018] (#781) — _possível duplicata (dup_of_563)_
- **Swedish House Mafia × The Weeknd** — “Moth To A Flame” [song, 2021] (#799) — _possível duplicata (dup_of_465)_
- **Myke Towers × Bad Bunny** — “Estamos Arriba” [song, 2021] (#846) — _possível duplicata (dup_of_502)_
- **SZA × Doja Cat** — “Kiss Me More” [feature, 2021] (#852) — _possível duplicata (dup_of_120)_
- **SZA × Drake** — “Slime You Out” [feature, 2023] (#853) — _possível duplicata (dup_of_11)_
- **Madonna × Nicki Minaj** — “Bitch I'm Madonna” [feature, 2015] (#864) — _possível duplicata (dup_of_546)_
- **Madonna × Maluma** — “Medellín” [feature, 2019] (#865) — _possível duplicata (dup_of_547)_
- **Mariah Carey × Snoop Dogg** — “Crybaby” [feature, 1999] (#867) — _possível duplicata (dup_of_284)_
- **Tems × Future** — “Wait for U” [song, 2022] (#936) — _possível duplicata (dup_of_514)_
- **Fireboy DML × Ed Sheeran** — “Peru (Remix)” [remix, 2021] (#1001) — _possível duplicata (dup_of_526)_
- **Anitta × MC Zaac** — “Desce Pro Play (Pa Pa Pa)” [song, 2017] (#1410) — _possível duplicata (dup_of_566)_
- **MC Kevinho × Léo Santana** — “Encaixa” [song, 2018] (#1450) — _possível duplicata (dup_of_578)_
- **Wesley Safadão × Claudia Leitte** — “Camarote” [song, 2017] (#1791) — _possível duplicata (dup_of_1552)_
- **Anitta × Cardi B** — “Me Gusta” [song, 2021] (#1915) — _possível duplicata (dup_of_315)_
- **Olodum × Daniela Mercury** — “O Canto da Cidade” [song, 2014] (#2047) — _possível duplicata (dup_of_1776)_
- **Emicida × Caetano Veloso** — “AmarElo” [song, 2019] (#2129) — _possível duplicata (dup_of_670)_
- **Anitta × Maluma** — “El Que Espera” [song, 2018] (#2312) — _dup_of_1709 possível duplicata_
- **Jão × Anitta** — “Pilantra” [song, 2020] (#2442) — _possível duplicata (dup_of_915)_
- **MC Fioti × J. Balvin** — “Bum Bum Tam Tam” [song, 2018] (#2449) — _possível duplicata (dup_of_1559)_
- **Gusttavo Lima × Henrique & Juliano** — “Apelido Carinhoso” [song, 2020] (#2479) — _possível duplicata (dup_of_2013)_
- **Anitta × Ludmilla** — “Cheia de Marra” [song, 2015] (#2599) — _possível duplicata (dup_of_1409)_
- **Fundo de Quintal × Zeca Pagodinho** — “Ao Vivo” [live, 2008] (#2772) — _dup_of_2289; possível duplicata_
- **Luke Combs × Miranda Lambert** — “Outrunnin' Your Memory” [song, 2021] (#2891) — _possível duplicata (dup_of_543)_
- **Reba McEntire × brooks_and_dunn_official** — “If You See Him / If You See Her” [album, 1998] (#2935) — _possível duplicata (dup_of_2914)_

## ❓ SUSPEITAS e ✅ CONFIRMADAS

São 12,564 suspeitas e 4,698 confirmadas — grandes demais para listar aqui. Listas completas em:

- `audit_data/suspeitas.csv` — revisar manualmente (mantidas por padrão)
- `audit_data/audit_full.csv` — **tudo** com status final, motivo e evidência
- `audit_data/invalidas_confirmadas.csv` / `invalidas_pendentes.csv` / `resgatadas.csv`

## Recomendação para a FASE 3 (após sua aprovação)

1. Remover as **867** `INVÁLIDA_CONFIRMADA` (fabricações confirmadas 2×).
2. Remover as **632** duplicatas exatas (mantendo 1 de cada).
3. **Não** tocar nas **263** pendentes até completar a verificação web (limite semanal).
4. Manter todas as **12,564** suspeitas sinalizadas para revisão; **manter** as 68 resgatadas.
5. Revalidar conectividade do grafo após remoções (componente único) antes de rebuildar `dataset.js`.
