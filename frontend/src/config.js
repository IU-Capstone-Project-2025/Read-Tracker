const config = {
  // API configuration
  api: {
    protocol: process.env.VUE_APP_API_PROTOCOL || 'http',
    host: process.env.VUE_APP_API_HOST || 'localhost',
    port: process.env.VUE_APP_API_PORT || '8000',
    basePath: process.env.VUE_APP_API_BASE_PATH || '',
  },
  
  // Application configuration
  app: {
    baseUrl: process.env.VUE_APP_BASE_URL || '/',
    authTokenStorageKey: 'readTrackerAuthToken',
  }
}

// Build full API base URL
config.api.baseUrl = `${config.api.protocol}://${config.api.host}:${config.api.port}${config.api.basePath}`

export default config