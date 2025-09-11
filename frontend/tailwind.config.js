/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          100: '#E6F2FF',
          200: '#B3D9FF',
          300: '#80BFFF',
          400: '#4DA6FF',
          500: '#1A8CFF',  // Primary blue
          600: '#0073E6',
          700: '#0059B3',
          800: '#004080',
          900: '#00264D',
        },
        accent: {
          100: '#F0E6FF',
          200: '#D9B3FF',
          300: '#C280FF',
          400: '#AB4DFF',
          500: '#941AFF',  // Primary purple
          600: '#7A00E6',
          700: '#5F00B3',
          800: '#440080',
          900: '#29004D',
        },
      },
      animation: {
        'gradient': 'gradient 8s linear infinite',
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'slide-up': 'slideUp 0.5s ease-out',
        'fade-in': 'fadeIn 0.5s ease-out',
      },
      keyframes: {
        gradient: {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          },
        },
        float: {
          '0%, 100%': {
            transform: 'translateY(0)',
          },
          '50%': {
            transform: 'translateY(-10px)',
          },
        },
        glow: {
          '0%': {
            boxShadow: '0 0 5px rgba(74, 222, 128, 0.2), 0 0 20px rgba(74, 222, 128, 0.1)',
          },
          '100%': {
            boxShadow: '0 0 10px rgba(74, 222, 128, 0.4), 0 0 40px rgba(74, 222, 128, 0.2)',
          },
        },
        slideUp: {
          '0%': {
            transform: 'translateY(20px)',
            opacity: '0',
          },
          '100%': {
            transform: 'translateY(0)',
            opacity: '1',
          },
        },
        fadeIn: {
          '0%': {
            opacity: '0',
          },
          '100%': {
            opacity: '1',
          },
        },
      },
      transitionTimingFunction: {
        'bounce-soft': 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
    },
  },
  plugins: [],
}
