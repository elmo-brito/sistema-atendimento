/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        'royal': '#0057D9',
        'noturno': '#001A33',
        'ciano': '#00E0FF',
        'titanium': '#2A2A2A',
        'pure-white': '#FFFFFF',
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(to right, #0057D9, #00E0FF)',
      }
    },
  },
  plugins: [],
}
