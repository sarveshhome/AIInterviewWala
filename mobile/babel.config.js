module.exports = {
  presets: [['module:@react-native/babel-preset', { enableImportExportTransform: true }]],
  plugins: [
    ['nativewind/babel'],
    [
      'module-resolver',
      {
        root: ['./src'],
        alias: {
          '@core': './src/core',
          '@features': './src/features',
          '@shared': './src/shared',
          '@': './src',
        },
      },
    ],
  ],
};