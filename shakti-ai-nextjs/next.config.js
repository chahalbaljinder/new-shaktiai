/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['images.unsplash.com', 'ui-avatars.com'],
  },
  webpack: (config, { isServer, dev }) => {
    // Fix for chunk loading errors
    if (!isServer && !dev) {
      config.output.publicPath = '/_next/'
    }
    
    // Improve chunk loading reliability
    config.output.crossOriginLoading = 'anonymous'
    
    // Configure split chunks for better loading
    if (!isServer) {
      config.optimization.splitChunks.cacheGroups = {
        ...config.optimization.splitChunks.cacheGroups,
        commons: {
          name: 'commons',
          chunks: 'all',
          minChunks: 2,
          enforce: true,
        },
      }
    }
    
    return config
  },
  // Disable static optimization for layout to prevent chunk loading issues
  experimental: {
    optimizePackageImports: ['lucide-react', '@radix-ui/react-dialog'],
    runtime: undefined,
  },
  // Ensure proper asset serving
  assetPrefix: process.env.NODE_ENV === 'production' ? '' : undefined,
}

module.exports = nextConfig
