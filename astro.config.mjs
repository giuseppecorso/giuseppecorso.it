// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://giuseppecorso.it',
  trailingSlash: 'always',
  // the form's "thank you" and "error" pages are not for search engines
  integrations: [sitemap({ filter: (page) => !page.includes('/contatti/grazie/') && !page.includes('/contatti/errore/') })],
});
