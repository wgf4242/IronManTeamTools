import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    server: {
        proxy: {
            // string shorthand: http://localhost:5173/foo -> http://localhost:4567/foo
            // '/test': 'http://localhost:8000/test',
            '/test': {
                target: "http://127.0.0.1:8000",
                changeOrigin: true
            }
        }
    }
})
