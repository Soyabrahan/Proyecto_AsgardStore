/** @type {import('next').NextConfig} */
const nextConfig = {
  // Ignorar errores durante el build
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  // Configuración de imágenes
  images: {
    unoptimized: true,
  },
  // Configuración de salida
  output: 'standalone',
}

export default nextConfig
