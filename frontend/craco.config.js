// Minimal CRACO config: just the "@/" path alias. Tailwind/autoprefixer are
// applied automatically via postcss.config.js.
const path = require("path");

module.exports = {
  webpack: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
};
