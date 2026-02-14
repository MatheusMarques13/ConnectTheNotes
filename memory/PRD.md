# Connect the Notes - PRD

## Overview
A musical artist connection trivia game where players connect two artists through their collaborations (songs, albums, live performances). Inspired by Connect the Stars but for music.

## Tech Stack
- **Frontend**: React + Tailwind CSS
- **Backend**: FastAPI + MongoDB
- **Database**: 459 artists, 834 collaborations across Hip-Hop, Pop, R&B, Rock, EDM, Latin, K-Pop, Afrobeats, Country, Indie

## Features
- Artist search with autocomplete (backed by MongoDB regex)
- Random artist selection
- Game board with collaboration chain-building
- BFS pathfinding for hints
- Step counter, undo, restart
- Victory screen with connection chain display
- How to Play & Options modals
- Animated starry/constellation background with mouse interactivity

## Design
- Diamond/crystal atmosphere: icy blues, silvers, deep navy
- Fonts: Cormorant Garamond (display), Outfit (body), JetBrains Mono (mono)
- Constellation animations with shooting stars
