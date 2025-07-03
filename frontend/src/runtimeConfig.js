const runtime = window.__RUNTIME_CONFIG__ || {};

const config = {
  api: {
    protocol: runtime.API_PROTOCOL || 'http',
    host: runtime.API_HOST || 'localhost',
    port: runtime.API_PORT || '8000',
    basePath: runtime.API_BASE_PATH || '',
  },
  app: {
    baseUrl: runtime.BASE_URL || '/',
    authTokenStorageKey: 'readTrackerAuthToken',
  }
};

config.api.baseUrl = `${config.api.protocol}://${config.api.host}:${config.api.port}${config.api.basePath}`;

export default config;