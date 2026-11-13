---
title: Curio Lane — e-commerce full stack
order: 1
summary: Negozio online completo, dal catalogo all'ordine, con backend REST in Spring Boot e frontend Angular. Online in produzione sul mio VPS.
problem: Un e-commerce deve gestire prodotti, listini, clienti e ordini senza vendere merce che non c'è, e separare con sicurezza quello che può fare un cliente da quello che può fare un amministratore.
tech: [Java 21, Spring Boot, JPA/Hibernate, PostgreSQL, Angular, JWT, JUnit, Mockito, Docker, Nginx, GitHub Actions]
links:
  - { label: Demo online, url: 'https://curiolane.giuseppecorso.it' }
  - { label: Codice backend, url: 'https://github.com/giuseppecorso/ecommerce-backend' }
  - { label: Codice frontend, url: 'https://github.com/giuseppecorso/ecommerce-frontend' }
---

- API REST su tre livelli (controller, service, repository) con DTO e mapper scritti a mano, documentata con Swagger.
- Autenticazione JWT, password cifrate con BCrypt, ruoli cliente e amministratore.
- Modello dati con prodotti, categorie, listini, ordini e righe d'ordine; storico dei prezzi d'acquisto e controllo delle giacenze.
- Test con JUnit, Mockito e MockMvc, compresi i casi di accesso negato (401/403).
- In produzione con Docker Compose (Angular, Spring Boot, PostgreSQL) dietro Nginx, HTTPS con Let's Encrypt e integrazione continua con GitHub Actions.
