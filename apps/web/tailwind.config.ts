import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: '#507d2a',
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ['lemonade'],
    darkTheme: 'lemonade',
  },
} satisfies Config
