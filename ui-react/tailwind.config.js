/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'saas-bg': '#F7F7F8',
        'saas-sidebar': '#F1F1F3',
        'saas-primary': '#1F1F1F',    /* Dark gray for typography */
        'saas-secondary': '#6B7280',  /* Muted gray for body/small text */
        'saas-accent': '#E5EDFF',     /* Soft blue for circles/highlights */
        'saas-border': '#E5E7EB',     /* Light gray for subtle borders */
      },
      borderRadius: {
        'saas': '16px',
      },
      boxShadow: {
        'saas-soft': '0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03)',
      }
    },
  },
  plugins: [],
}
