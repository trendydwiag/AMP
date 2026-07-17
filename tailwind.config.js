/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./templates/**/*.html",
    "./apps/**/templates/**/*.html",
    "./static/**/*.js",
    "./utils/**/*.py"
  ],
  theme: {
    extend: {
      colors: {
        coffee: {
          50: '#FAF7F3',
          100: '#F5F0EA',
          200: '#E7DDD3',
          300: '#C89B6D',
          400: '#8C5A3C',
          500: '#6B4226',
          600: '#4E2F1F',
          700: '#3A2318',
          800: '#2B1A13',
          900: '#1A0F0B',
        },
        live: '#E53935',
        success: '#2F9E44',
      },
      fontFamily: {
        heading: ['Poppins', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
      maxWidth: {
        'site': '1440px',
        'content': '1280px',
      },
      spacing: {
        'section': '96px',
        'section-md': '64px',
        'section-sm': '48px',
      },
      borderRadius: {
        'card': '20px',
        'card-lg': '24px',
      },
      boxShadow: {
        'card': '0 10px 30px rgba(0,0,0,.08)',
        'card-hover': '0 20px 40px rgba(0,0,0,.12)',
        'hero-card': '0 30px 60px rgba(0,0,0,.20)',
        'header': '0 1px 3px rgba(0,0,0,.06)',
        'player': '0 -4px 20px rgba(0,0,0,.08)',
      },
      transitionDuration: {
        '250': '250ms',
      }
    },
  },
  plugins: [],
}
