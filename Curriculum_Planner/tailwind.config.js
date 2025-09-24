/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./templates/**/*.{html,js}",
      "./static/**/*.js",
    ],
    darkMode: 'class',
    theme: {
      extend: {
        colors: {
          primary: '#ff8066',
        },
      },
    },
    plugins: [],
  }