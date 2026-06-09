import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // 允许通过 cloudflared/ngrok 隧道域名访问
    allowedHosts: true,
    proxy: {
      // 前端把 /api 代理到本地后端，演示时只需暴露前端一个隧道
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
