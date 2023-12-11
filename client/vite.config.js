import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs-extra'
import path from 'path'

// https://vitejs.dev/config/
const copy = () => {
    return {
        name: 'copy-sw-file',
        writeBundle() {
            const srcPath = path.resolve(__dirname, '../backend')
            const destPath = path.resolve(__dirname, 'dist', '')
            fs.copySync(srcPath, destPath)
            fs.removeSync(path.join(__dirname, 'dist', '.idea'));
            fs.removeSync(path.join(__dirname, 'dist', '__pycache__'));
            // fs.remove(path.resolve(__dirname, 'dist',  '__pycache__'));
            console.log('sw.js has been copied to dist folder.')
        }
    };
}
export default defineConfig({
    plugins: [
        vue(),
        copy()
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    server: {
        proxy: {
            // string shorthand: http://localhost:5173/foo -> http://localhost:4567/foo
            "/api": {
                target: "http://127.0.0.1:8000/",
                changeOrigin: true,
            },
        }
    },
})
