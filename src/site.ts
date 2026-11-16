// Single source for personal data shown on the site.
export const SITE = {
  name: 'Giuseppe Corso',
  email: 'info@giuseppecorso.it',
  github: 'https://github.com/giuseppecorso',
  linkedin: 'https://www.linkedin.com/in/giuseppe-corso',
  fiverr: 'https://it.fiverr.com/users/giuseppewppro',
  phone: '+39 320 803 1918',
  whatsapp: 'https://wa.me/393208031918',
};

/** WhatsApp link with a pre-written first message. */
export const whatsappLink = (text: string) => `${SITE.whatsapp}?text=${encodeURIComponent(text)}`;

/** How prices are invoiced (no VAT number for now). */
export const PRICE_NOTE = "Prezzi senza IVA: lavoro con prestazione occasionale e ritenuta d'acconto.";
