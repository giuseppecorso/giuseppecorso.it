---
title: Assenze Desk — gestione delle assenze
order: 3
summary: Strumento in Excel/VBA, in uso quotidiano in un team, che automatizza la gestione delle comunicazioni di malattia, ferie e permessi.
problem: Ogni comunicazione di malattia richiedeva passaggi manuali tra posta, portale INPS, gestionale e risposte ai lavoratori. Vincoli — niente da installare, solo strumenti Microsoft, dati sanitari che non escono dall'azienda.
tech: [Excel, VBA, Outlook, Word, Python (prototipo)]
links:
  - { label: Codice del prototipo Python, url: 'https://github.com/giuseppecorso/assenze-desk' }
note: Progetto AI-assisted. Requisiti, regole, collaudi e decisioni sono miei.
---

- Legge le mail, recupera il certificato dal portale INPS, compila il gestionale e prepara le bozze di risposta. L'operatore conferma sempre prima dell'invio.
- Gestisce ferie e permessi anche a partire da testo libero.
- Nato come prototipo in Python, riscritto in Excel/VBA per essere usato senza installazioni.
- Circa 23.000 righe di VBA, oltre 1.800 test automatici e più di 100 decisioni documentate.
- Tempi di gestione ridotti del 70%; una malattia completa si chiude in circa 75 secondi.
