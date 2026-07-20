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
  // immer v11 ships an ESM build (immer.legacy-esm.js) selected by the
  // `react-native` exports condition; it must be transpiled to CJS or Jest
  // fails with "Unexpected token 'export'".
  transformIgnorePatterns: ['node_modules/(?!(@react-native|react-native|@reduxjs|@tanstack|immer)/)'],
};