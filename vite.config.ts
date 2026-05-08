import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: '/3-meses-carolina/',
  plugins: [react()],
  build: {
    sourcemap: false,
    cssMinify: true
  }
});
