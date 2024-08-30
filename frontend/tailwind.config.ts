import type { Config } from 'tailwindcss';

const config = {
  darkMode: ['class'],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: '',
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
      backgroundImage: {
        'home-dummy-background':
          'url("https://www.dhm.de/datenbank/linzdbv2/img.php?laufnr=LI000003")',
        'jdcrp-logo': 'url(/jdcrp_logo.png)',
        'jdcrp-logo-cut': 'url(/jdcrp_logo_cut.png)',
      },
      colors: {
        'highlight-blue': '#1E324C',
        'darker-blue': '#132030',
        'link-color': {
          DEFAULT: '#2C79DD',
          visited: '#B281DF',
        },
        'background-gray': '#E2E8F0',
        muted: {
          DEFAULT: '#646464',
        },
        primary: {
          DEFAULT: '#387B84',
        },
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
} satisfies Config;

export default config;
