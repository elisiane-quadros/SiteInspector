/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      keyframes: {
        'magnify-sweep': {
          '0%, 100%': { transform: 'translateX(0) rotate(-6deg)' },
          '50%': { transform: 'translateX(170px) rotate(6deg)' },
        },
      },
      animation: {
        'magnify-sweep': 'magnify-sweep 2.4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};
