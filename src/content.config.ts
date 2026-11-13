import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const link = z.object({ label: z.string(), url: z.string() });

// Software projects: one Markdown file each. Body = "what I built".
const progetti = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/progetti' }),
  schema: z.object({
    title: z.string(),
    order: z.number(),
    summary: z.string(),
    problem: z.string(),
    tech: z.array(z.string()),
    links: z.array(link).default([]),
    note: z.string().optional(),
  }),
});

// Client websites: shown after software projects.
const clienti = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/clienti' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      order: z.number(),
      business: z.string(),
      work: z.string(),
      tech: z.array(z.string()),
      screenshot: image(),
      screenshotAlt: z.string(),
      url: z.string().optional(),
    }),
});

export const collections = { progetti, clienti };
