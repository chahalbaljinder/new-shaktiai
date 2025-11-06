/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['images.unsplash.com', 'ui-avatars.com'],
  },
  
  // Simplified webpack config to avoid issues
  webpack: (config, { isServer, dev }) => {
    // Fix module resolution for Windows paths with spaces
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': require('path').resolve(__dirname),
    }
    
    // Increase chunk load timeout for slower systems
    if (!isServer) {
      config.output.chunkLoadTimeout = 120000 // 2 minutes
    }
    
    return config
  },
  
  // Minimal experimental features
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  
  // Disable source maps in development to reduce complexity
  productionBrowserSourceMaps: false,
  
  // Ensure proper serving
  trailingSlash: false,
}

module.exports = nextConfig
