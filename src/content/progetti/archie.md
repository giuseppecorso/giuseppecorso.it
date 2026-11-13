---
title: Archie — analisi statistica sul calcio
order: 2
summary: Piattaforma che raccoglie dati di decine di competizioni calcistiche e li analizza con modelli statistici, con un assistente AI che risponde alle domande.
problem: I dati sul calcio sono tanti e sparsi su fonti diverse; per trarne qualcosa di affidabile servono raccolta automatica, modelli validati in modo onesto e regole che impediscano di "barare" con dati dal futuro.
tech: [Python, FastAPI, SQLAlchemy, Alembic, SQLite, Angular, API Claude, Docker, pytest, GitHub Actions]
links:
  - { label: App online, url: 'https://archie.giuseppecorso.it' }
  - { label: Codice, url: 'https://github.com/giuseppecorso/archie' }
note: Sviluppato con Claude Code su mie specifiche.
---

- Backend FastAPI con aggiornamenti pianificati dei dati: storico dal 2005 di 10 campionati e 33 competizioni seguite.
- Validazione walk-forward: ogni modello viene provato solo su partite successive ai dati con cui è stato costruito.
- Assistente "Chiedi ad Archie" basato sull'API di Claude, con registro dei costi e tetto di spesa mensile. I numeri li calcola il codice, mai l'AI.
- Frontend Angular installabile come app (PWA).
- Oltre 450 test automatici e integrazione continua con GitHub Actions.
