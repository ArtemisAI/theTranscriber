import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000", // Or whatever port the backend runs on locally
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, "/api"), // Ensure /api prefix is maintained if needed by backend
      },
    },
  },
});
