import { config } from '@vue/test-utils'

// Mock global components
config.global.mocks = {
  $route: {
    path: '/',
    query: {}
  },
  $router: {
    push: jest.fn(),
    replace: jest.fn()
  }
}

// Mock Font Awesome icons
jest.mock('@fortawesome/vue-fontawesome', () => ({
  FontAwesomeIcon: 'font-awesome-icon'
}))