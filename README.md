# giuseppecorso.it

Il mio sito personale: portfolio tecnico, pagine dei miei prodotti digitali e assistenza WordPress.
Online su **https://giuseppecorso.it**.

È un sito statico: le pagine vengono generate al momento della build e servite da nginx come semplici file HTML. Nessun database e nessun JavaScript lato client per il sito.

## Stack

| Parte | Scelta |
|---|---|
| Generatore | [Astro](https://astro.build) 7, output statico |
| Stile | CSS puro con variabili |
| Contenuti | Markdown in `src/content/` (progetti, siti per clienti, prodotti) |
| Immagini | `astro:assets`, convertite in WebP con dimensioni dichiarate |
| SEO | title e description per pagina, canonical, Open Graph, JSON-LD, sitemap |
| Server | nginx su VPS Ubuntu, HTTPS con Let's Encrypt (certbot) |
| Modulo "avvisami" | [listmonk](https://listmonk.app) self-hosted, iscrizione a doppia conferma |
| Statistiche | [Umami](https://umami.is) self-hosted, senza cookie |

Lighthouse da mobile: 100 su prestazioni, accessibilità, best practice e SEO su tutte le pagine.

## Architettura sul server

```
                       ┌──────────────────────── VPS ────────────────────────┐
 visitatore ──HTTPS──▶ │ nginx (80/443, certificati Let's Encrypt)           │
                       │   ├─ giuseppecorso.it       → file statici          │
                       │   │                           /var/www/…/current    │
                       │   ├─ lista.giuseppecorso.it → listmonk  (Docker)    │
                       │   └─ stat.giuseppecorso.it  → Umami     (Docker)    │
                       └─────────────────────────────────────────────────────┘
```

I container ascoltano solo su `127.0.0.1`: dall'esterno si passa sempre da nginx.

## Sviluppo

```
npm install
npm run dev      # http://localhost:4321
npm run build    # genera dist/
```

Richiede Node 22 o superiore.

## Deploy

```
npm run deploy
```

Lo script [`deploy/deploy.ps1`](deploy/deploy.ps1) fa la build, carica un archivio sul server, lo scompatta in una nuova cartella `releases/<data>` e sposta il link simbolico `current` sulla nuova versione. Il cambio è atomico (il sito non è mai a metà aggiornamento) e per tornare indietro basta ripuntare il link a una release precedente. Vengono conservate le ultime 5.

## Aggiungere contenuti

- **Nuovo prodotto**: un file Markdown in `src/content/prodotti/`. Il nome del file diventa l'indirizzo della pagina.
- **Nuovo progetto**: un file in `src/content/progetti/`.
- **Nuovo sito cliente**: un file in `src/content/clienti/` e lo screenshot in `src/assets/clienti/`.

I campi richiesti sono definiti e validati in [`src/content.config.ts`](src/content.config.ts): un campo mancante blocca la build.

## Struttura

```
src/pages/        pagine
src/content/      contenuti in Markdown
src/components/   componenti
src/layouts/      layout con i tag SEO
deploy/           script di deploy, configurazioni nginx e Docker Compose
```

Le password dei servizi stanno in file `.env` solo sul server e non fanno parte del repository.
