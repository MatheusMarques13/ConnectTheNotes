import React, { createContext, useContext, useState, useCallback, useMemo, useEffect } from 'react';

// The languages most sites ship; the site auto-starts in the player's browser
// language and remembers a manual choice.
export const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'pt', label: 'Português' },
  { code: 'es', label: 'Español' },
  { code: 'fr', label: 'Français' },
  { code: 'de', label: 'Deutsch' },
  { code: 'it', label: 'Italiano' },
  { code: 'ja', label: '日本語' },
];

// Core user-facing strings. {placeholders} are filled at call time. Anything
// missing in a language falls back to English, so partial translations are safe.
const STRINGS = {
  en: {
    how_to_play: 'How to Play', options: 'Options', light_mode: 'Light mode', dark_mode: 'Dark mode',
    choose_two: 'choose two artists', tagline: 'link any two artists through the songs they share',
    todays_puzzle: "Today's Puzzle", play_today: 'Play Today', or_play_freely: 'or play freely',
    enter_artist: "Enter an artist's name", choose_for_me: 'Choose for me', picking: 'Picking…',
    start_game: 'Start Game', surprise_me: 'Surprise Me', artist_n: 'artist {n}',
    footer_stats: '{artists} artists · {songs} songs', genre: 'Genre',
    back: 'Back', connect: 'connect', and: 'and', hint: 'Hint', undo: 'Undo last song',
    give_up: 'Give up & reveal solution', name_a_song: 'Name a song…', play: 'Play',
    artists_found: 'Artists Found', songs_found: 'Songs Found', best_path: 'My Best Path',
    click_card: 'Click a card for more info', drag_board: 'Drag the board or a card', zoom_hint: 'Zoom in / out',
    connected: 'Connected!', you_linked: 'You linked {a} to {b} in {n} {songs}',
    song: 'song', songs: 'songs', your_trail: 'Your trail', play_again: 'Play Again',
    share: 'Share', copied: 'Copied!', new_game: 'New Game', close: 'Close',
    back_to_board: 'Back to board', view_result: 'Result',
    solution_revealed: 'Solution Revealed', times_up: "Time's Up!", try_again: 'Try Again',
    one_way: 'One way to connect {a} and {b}{par}:', in_n_songs: ' in {n} songs',
    ran_out: 'You ran out of time connecting {a} to {b}.',
    you_best: 'You: {used} · Best possible: {best}',
    did_you_mean: 'Did you mean', use_it: 'Use it',
    no_collab: 'No song called “{q}” by anyone you’ve found. Try another.',
    already_played: 'You already played “{title}”.',
    finding_route: 'Finding a route…', try_song_with: 'Try a song with {name}',
    everyone_found: "You've uncovered everyone on the best route — name the song that links them.",
    artists_on_track: 'Artists on this track', preview: 'Preview', no_preview: 'No preview available',
    rating_perfect: 'Perfect — optimal path!', rating_great: 'Great', rating_nice: 'Nice', rating_connected: 'Connected',
    language: 'Language',
  },
  pt: {
    how_to_play: 'Como Jogar', options: 'Opções', light_mode: 'Modo claro', dark_mode: 'Modo escuro',
    choose_two: 'escolha dois artistas', tagline: 'ligue dois artistas pelas músicas que compartilham',
    todays_puzzle: 'Desafio de Hoje', play_today: 'Jogar Hoje', or_play_freely: 'ou jogue livremente',
    enter_artist: 'Digite o nome de um artista', choose_for_me: 'Escolher por mim', picking: 'Escolhendo…',
    start_game: 'Iniciar Jogo', surprise_me: 'Surpreenda-me', artist_n: 'artista {n}',
    footer_stats: '{artists} artistas · {songs} músicas', genre: 'Gênero',
    back: 'Voltar', connect: 'conecte', and: 'e', hint: 'Dica', undo: 'Desfazer última música',
    give_up: 'Desistir e revelar solução', name_a_song: 'Digite uma música…', play: 'Jogar',
    artists_found: 'Artistas Encontrados', songs_found: 'Músicas Encontradas', best_path: 'Melhor Caminho',
    click_card: 'Clique num card para mais info', drag_board: 'Arraste o tabuleiro ou um card', zoom_hint: 'Mais / menos zoom',
    connected: 'Conectado!', you_linked: 'Você ligou {a} a {b} em {n} {songs}',
    song: 'música', songs: 'músicas', your_trail: 'Sua trilha', play_again: 'Jogar de Novo',
    share: 'Compartilhar', copied: 'Copiado!', new_game: 'Novo Jogo', close: 'Fechar',
    back_to_board: 'Voltar ao gráfico', view_result: 'Resultado',
    solution_revealed: 'Solução Revelada', times_up: 'Tempo Esgotado!', try_again: 'Tentar de Novo',
    one_way: 'Um jeito de conectar {a} e {b}{par}:', in_n_songs: ' em {n} músicas',
    ran_out: 'O tempo acabou ligando {a} a {b}.',
    you_best: 'Você: {used} · Melhor possível: {best}',
    did_you_mean: 'Você quis dizer', use_it: 'Usar',
    no_collab: 'Nenhuma música chamada “{q}” por alguém que você achou. Tente outra.',
    already_played: 'Você já jogou “{title}”.',
    finding_route: 'Procurando uma rota…', try_song_with: 'Tente uma música com {name}',
    everyone_found: 'Você revelou todos da melhor rota — agora diga a música que os liga.',
    artists_on_track: 'Artistas nesta faixa', preview: 'Prévia', no_preview: 'Sem prévia disponível',
    rating_perfect: 'Perfeito — caminho ótimo!', rating_great: 'Ótimo', rating_nice: 'Legal', rating_connected: 'Conectado',
    language: 'Idioma',
  },
  es: {
    how_to_play: 'Cómo Jugar', options: 'Opciones', light_mode: 'Modo claro', dark_mode: 'Modo oscuro',
    choose_two: 'elige dos artistas', tagline: 'conecta dos artistas por las canciones que comparten',
    todays_puzzle: 'Reto de Hoy', play_today: 'Jugar Hoy', or_play_freely: 'o juega libremente',
    enter_artist: 'Escribe el nombre de un artista', choose_for_me: 'Elegir por mí', picking: 'Eligiendo…',
    start_game: 'Empezar', surprise_me: 'Sorpréndeme', artist_n: 'artista {n}',
    footer_stats: '{artists} artistas · {songs} canciones', genre: 'Género',
    back: 'Atrás', connect: 'conecta', and: 'y', hint: 'Pista', undo: 'Deshacer última canción',
    give_up: 'Rendirse y revelar solución', name_a_song: 'Escribe una canción…', play: 'Jugar',
    artists_found: 'Artistas Hallados', songs_found: 'Canciones Halladas', best_path: 'Mejor Camino',
    click_card: 'Haz clic en una tarjeta para más info', drag_board: 'Arrastra el tablero o una tarjeta', zoom_hint: 'Acercar / alejar',
    connected: '¡Conectado!', you_linked: 'Conectaste a {a} con {b} en {n} {songs}',
    song: 'canción', songs: 'canciones', your_trail: 'Tu ruta', play_again: 'Jugar de Nuevo',
    share: 'Compartir', copied: '¡Copiado!', new_game: 'Nuevo Juego', close: 'Cerrar',
    solution_revealed: 'Solución Revelada', times_up: '¡Se acabó el tiempo!', try_again: 'Reintentar',
    one_way: 'Una forma de conectar {a} y {b}{par}:', in_n_songs: ' en {n} canciones',
    ran_out: 'Se te acabó el tiempo conectando {a} con {b}.',
    you_best: 'Tú: {used} · Mejor posible: {best}',
    did_you_mean: '¿Quisiste decir', use_it: 'Usar',
    no_collab: 'Ninguna canción llamada “{q}” de alguien que hallaste. Prueba otra.',
    already_played: 'Ya jugaste “{title}”.',
    finding_route: 'Buscando una ruta…', try_song_with: 'Prueba una canción con {name}',
    everyone_found: 'Revelaste a todos de la mejor ruta — di la canción que los une.',
    artists_on_track: 'Artistas en esta pista', preview: 'Vista previa', no_preview: 'Sin vista previa',
    rating_perfect: '¡Perfecto — ruta óptima!', rating_great: 'Genial', rating_nice: 'Bien', rating_connected: 'Conectado',
    language: 'Idioma',
  },
  fr: {
    how_to_play: 'Comment Jouer', options: 'Options', light_mode: 'Mode clair', dark_mode: 'Mode sombre',
    choose_two: 'choisis deux artistes', tagline: 'relie deux artistes par les chansons qu’ils partagent',
    todays_puzzle: 'Défi du Jour', play_today: 'Jouer Aujourd’hui', or_play_freely: 'ou joue librement',
    enter_artist: 'Saisis le nom d’un artiste', choose_for_me: 'Choisir pour moi', picking: 'Choix…',
    start_game: 'Commencer', surprise_me: 'Surprends-moi', artist_n: 'artiste {n}',
    footer_stats: '{artists} artistes · {songs} chansons', genre: 'Genre',
    back: 'Retour', connect: 'relie', and: 'et', hint: 'Indice', undo: 'Annuler la dernière chanson',
    give_up: 'Abandonner & révéler', name_a_song: 'Nomme une chanson…', play: 'Jouer',
    artists_found: 'Artistes Trouvés', songs_found: 'Chansons Trouvées', best_path: 'Meilleur Chemin',
    click_card: 'Clique une carte pour plus d’infos', drag_board: 'Fais glisser le plateau ou une carte', zoom_hint: 'Zoom + / −',
    connected: 'Connecté !', you_linked: 'Tu as relié {a} à {b} en {n} {songs}',
    song: 'chanson', songs: 'chansons', your_trail: 'Ton parcours', play_again: 'Rejouer',
    share: 'Partager', copied: 'Copié !', new_game: 'Nouvelle Partie', close: 'Fermer',
    solution_revealed: 'Solution Révélée', times_up: 'Temps écoulé !', try_again: 'Réessayer',
    one_way: 'Une façon de relier {a} et {b}{par} :', in_n_songs: ' en {n} chansons',
    ran_out: 'Temps écoulé en reliant {a} à {b}.',
    you_best: 'Toi : {used} · Meilleur possible : {best}',
    did_you_mean: 'Vouliez-vous dire', use_it: 'Utiliser',
    no_collab: 'Aucune chanson nommée « {q} » par quelqu’un que tu as trouvé. Essaie une autre.',
    already_played: 'Tu as déjà joué « {title} ».',
    finding_route: 'Recherche d’une route…', try_song_with: 'Essaie une chanson avec {name}',
    everyone_found: 'Tu as révélé tout le monde sur la meilleure route — nomme la chanson qui les relie.',
    artists_on_track: 'Artistes sur ce titre', preview: 'Aperçu', no_preview: 'Aucun aperçu',
    rating_perfect: 'Parfait — chemin optimal !', rating_great: 'Super', rating_nice: 'Bien', rating_connected: 'Connecté',
    language: 'Langue',
  },
  de: {
    how_to_play: 'Spielanleitung', options: 'Optionen', light_mode: 'Heller Modus', dark_mode: 'Dunkler Modus',
    choose_two: 'wähle zwei Künstler', tagline: 'verbinde zwei Künstler über gemeinsame Songs',
    todays_puzzle: 'Heutiges Rätsel', play_today: 'Heute Spielen', or_play_freely: 'oder frei spielen',
    enter_artist: 'Künstlername eingeben', choose_for_me: 'Für mich wählen', picking: 'Wähle…',
    start_game: 'Spiel Starten', surprise_me: 'Überrasch mich', artist_n: 'Künstler {n}',
    footer_stats: '{artists} Künstler · {songs} Songs', genre: 'Genre',
    back: 'Zurück', connect: 'verbinde', and: 'und', hint: 'Tipp', undo: 'Letzten Song zurück',
    give_up: 'Aufgeben & Lösung zeigen', name_a_song: 'Nenne einen Song…', play: 'Spielen',
    artists_found: 'Künstler Gefunden', songs_found: 'Songs Gefunden', best_path: 'Bester Weg',
    click_card: 'Karte für Infos anklicken', drag_board: 'Brett oder Karte ziehen', zoom_hint: 'Rein / raus zoomen',
    connected: 'Verbunden!', you_linked: 'Du hast {a} mit {b} in {n} {songs} verbunden',
    song: 'Song', songs: 'Songs', your_trail: 'Dein Weg', play_again: 'Nochmal',
    share: 'Teilen', copied: 'Kopiert!', new_game: 'Neues Spiel', close: 'Schließen',
    solution_revealed: 'Lösung Gezeigt', times_up: 'Zeit Um!', try_again: 'Erneut',
    one_way: 'Ein Weg, {a} und {b} zu verbinden{par}:', in_n_songs: ' in {n} Songs',
    ran_out: 'Die Zeit lief ab beim Verbinden von {a} und {b}.',
    you_best: 'Du: {used} · Bestmöglich: {best}',
    did_you_mean: 'Meintest du', use_it: 'Nutzen',
    no_collab: 'Kein Song namens „{q}“ von jemandem, den du fandst. Versuch einen anderen.',
    already_played: 'Du hast „{title}“ schon gespielt.',
    finding_route: 'Suche eine Route…', try_song_with: 'Versuch einen Song mit {name}',
    everyone_found: 'Du hast alle auf der besten Route gefunden — nenne den verbindenden Song.',
    artists_on_track: 'Künstler auf diesem Track', preview: 'Vorschau', no_preview: 'Keine Vorschau',
    rating_perfect: 'Perfekt — optimaler Weg!', rating_great: 'Klasse', rating_nice: 'Gut', rating_connected: 'Verbunden',
    language: 'Sprache',
  },
  it: {
    how_to_play: 'Come Giocare', options: 'Opzioni', light_mode: 'Tema chiaro', dark_mode: 'Tema scuro',
    choose_two: 'scegli due artisti', tagline: 'collega due artisti tramite le canzoni che condividono',
    todays_puzzle: 'Sfida di Oggi', play_today: 'Gioca Oggi', or_play_freely: 'o gioca liberamente',
    enter_artist: 'Inserisci il nome di un artista', choose_for_me: 'Scegli tu', picking: 'Scelgo…',
    start_game: 'Inizia', surprise_me: 'Sorprendimi', artist_n: 'artista {n}',
    footer_stats: '{artists} artisti · {songs} canzoni', genre: 'Genere',
    back: 'Indietro', connect: 'collega', and: 'e', hint: 'Aiuto', undo: 'Annulla ultima canzone',
    give_up: 'Arrenditi e rivela', name_a_song: 'Nomina una canzone…', play: 'Gioca',
    artists_found: 'Artisti Trovati', songs_found: 'Canzoni Trovate', best_path: 'Percorso Migliore',
    click_card: 'Clicca una carta per info', drag_board: 'Trascina il tavolo o una carta', zoom_hint: 'Zoom + / −',
    connected: 'Collegato!', you_linked: 'Hai collegato {a} a {b} in {n} {songs}',
    song: 'canzone', songs: 'canzoni', your_trail: 'Il tuo percorso', play_again: 'Rigioca',
    share: 'Condividi', copied: 'Copiato!', new_game: 'Nuova Partita', close: 'Chiudi',
    solution_revealed: 'Soluzione Rivelata', times_up: 'Tempo Scaduto!', try_again: 'Riprova',
    one_way: 'Un modo per collegare {a} e {b}{par}:', in_n_songs: ' in {n} canzoni',
    ran_out: 'Tempo scaduto collegando {a} a {b}.',
    you_best: 'Tu: {used} · Miglior possibile: {best}',
    did_you_mean: 'Intendevi', use_it: 'Usa',
    no_collab: 'Nessuna canzone “{q}” di qualcuno che hai trovato. Provane un’altra.',
    already_played: 'Hai già giocato “{title}”.',
    finding_route: 'Cerco un percorso…', try_song_with: 'Prova una canzone con {name}',
    everyone_found: 'Hai rivelato tutti sul percorso migliore — nomina la canzone che li unisce.',
    artists_on_track: 'Artisti in questo brano', preview: 'Anteprima', no_preview: 'Nessuna anteprima',
    rating_perfect: 'Perfetto — percorso ottimale!', rating_great: 'Ottimo', rating_nice: 'Bene', rating_connected: 'Collegato',
    language: 'Lingua',
  },
  ja: {
    how_to_play: '遊び方', options: '設定', light_mode: 'ライトモード', dark_mode: 'ダークモード',
    choose_two: 'アーティストを2人選ぶ', tagline: '共有する楽曲で2人のアーティストをつなげよう',
    todays_puzzle: '今日のパズル', play_today: '今日のをプレイ', or_play_freely: 'または自由にプレイ',
    enter_artist: 'アーティスト名を入力', choose_for_me: 'おまかせ', picking: '選択中…',
    start_game: 'ゲーム開始', surprise_me: 'ランダム', artist_n: 'アーティスト{n}',
    footer_stats: '{artists} アーティスト · {songs} 曲', genre: 'ジャンル',
    back: '戻る', connect: 'つなぐ', and: 'と', hint: 'ヒント', undo: '最後の曲を取り消す',
    give_up: 'あきらめて答えを見る', name_a_song: '曲名を入力…', play: '送信',
    artists_found: '見つけたアーティスト', songs_found: '見つけた曲', best_path: '最短ルート',
    click_card: 'カードをクリックで詳細', drag_board: 'ボードやカードをドラッグ', zoom_hint: 'ズーム +／−',
    connected: 'つながった！', you_linked: '{a} と {b} を{n}曲でつなげた',
    song: '曲', songs: '曲', your_trail: 'あなたのルート', play_again: 'もう一度',
    share: 'シェア', copied: 'コピー！', new_game: '新しいゲーム', close: '閉じる',
    solution_revealed: '答えを表示', times_up: '時間切れ！', try_again: '再挑戦',
    one_way: '{a} と {b} をつなぐ一例{par}：', in_n_songs: '（{n}曲）',
    ran_out: '{a} と {b} をつなぐ前に時間切れ。',
    you_best: 'あなた：{used} · 最良：{best}',
    did_you_mean: 'もしかして', use_it: '使う',
    no_collab: '見つけた誰の「{q}」という曲もありません。別の曲を。',
    already_played: '「{title}」はもう使いました。',
    finding_route: 'ルートを探索中…', try_song_with: '{name} の曲を試そう',
    everyone_found: '最短ルートの全員を見つけました — つなぐ曲を入力。',
    artists_on_track: 'この曲のアーティスト', preview: 'プレビュー', no_preview: 'プレビューなし',
    rating_perfect: '完璧 — 最短ルート！', rating_great: 'すごい', rating_nice: 'いいね', rating_connected: 'つながった',
    language: '言語',
  },
};

function detect() {
  try {
    const saved = localStorage.getItem('ctn_lang');
    if (saved && STRINGS[saved]) return saved;
    const navs = navigator.languages || [navigator.language || 'en'];
    for (const l of navs) { const c = String(l).slice(0, 2).toLowerCase(); if (STRINGS[c]) return c; }
  } catch (e) { /* ignore */ }
  return 'en';
}

const I18nContext = createContext({ lang: 'en', setLang: () => {}, t: (k) => k });

export function I18nProvider({ children }) {
  const [lang, setLangState] = useState(detect);
  const setLang = useCallback((l) => {
    setLangState(STRINGS[l] ? l : 'en');
    try { localStorage.setItem('ctn_lang', l); } catch (e) { /* ignore */ }
  }, []);
  useEffect(() => { try { document.documentElement.lang = lang; } catch (e) { /* ignore */ } }, [lang]);
  const t = useCallback((key, vars) => {
    let s = (STRINGS[lang] && STRINGS[lang][key]) || STRINGS.en[key] || key;
    if (vars) for (const k in vars) s = s.split('{' + k + '}').join(vars[k]);
    return s;
  }, [lang]);
  const value = useMemo(() => ({ lang, setLang, t }), [lang, setLang, t]);
  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export const useI18n = () => useContext(I18nContext);
