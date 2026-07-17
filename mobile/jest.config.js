module.exports = {
  preset: 'react-native',
  setupFiles: ['./jest.setup.js'],
  moduleNameMapper: {
    '^@core/(.*)$': '<rootDir>/src/core/$1',
    '^@features/(.*)$': '<rootDir>/src/features/$1',
    '^@shared/(.*)$': '<rootDir>/src/shared/$1',
    '^@navigation$': '<rootDir>/src/navigation',
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  transformIgnorePatterns: ['node_modules/(?!(@react-native|react-native|@reduxjs|@tanstack)/)'],
};