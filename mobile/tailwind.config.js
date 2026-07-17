/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef6ff', 100: '#d9eaff', 200: '#bcdcff', 300: '#8ec5ff',
          400: '#59a6ff', 500: '#3385ff', 600: '#1e66f5', 700: '#1850e1',
          800: '#1a42b6', 900: '#1b3a8f',
        },
      },
    },
  },
  plugins: [],
};