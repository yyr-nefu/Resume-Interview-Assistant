import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [vue()],

    base: env.VITE_BASE_URL || '/',

    server: {
      port: Number(env.VITE_PORT) || 5173,
      host: true,
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    },

    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: mode === 'production' ? false : 'inline',
      minify: 'esbuild',
      chunkSizeWarningLimit: 1500,
      rollupOptions: {
        output: {
          manualChunks: {
            'element-plus': ['element-plus'],
            'vue-core': ['vue', 'vue-router', 'pinia'],
            'echarts': ['echarts', '@vueuse/core']
          },
          entryFileNames: 'assets/js/[name]-[hash].js',
          chunkFileNames: 'assets/js/[name]-[hash].js',
          assetFileNames: (assetInfo) => {
            const name = assetInfo.name || ''
            if (/\.(woff2?|eot|ttf|otf)$/i.test(name)) {
              return 'assets/fonts/[name]-[hash][extname]'
            }
            if (/\.(png|jpe?g|gif|svg|webp|ico)$/i.test(name)) {
              return 'assets/images/[name]-[hash][extname]'
            }
            if (/\.css$/i.test(name)) {
              return 'assets/css/[name]-[hash][extname]'
            }
            return 'assets/[name]-[hash][extname]'
          }
        }
      }
    },

    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
        '@views': resolve(__dirname, 'src/views'),
        '@components': resolve(__dirname, 'src/components'),
        '@stores': resolve(__dirname, 'src/stores'),
        '@utils': resolve(__dirname, 'src/utils'),
        '@types': resolve(__dirname, 'src/types')
      },
      extensions: ['.ts', '.tsx', '.vue', '.js', '.jsx', '.json']
    },

    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@use "@/styles/variables" as *;`
        }
      }
    }
  }
})
