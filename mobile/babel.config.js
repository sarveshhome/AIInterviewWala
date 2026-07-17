module.exports = {
  presets: [
    ['module:@react-native/babel-preset', { enableImportExportTransform: true }],
    // nativewind/babel returns a preset ({ plugins: [...] }) and must be
    // registered under `presets`, not `plugins`. It also bundles
    // react-native-reanimated/plugin as its last entry, so reanimated does
    // not need a separate plugin entry here.
    ['nativewind/babel'],
  ],
  plugins: [
    [
      'module-resolver',
      {
        root: ['./src'],
        alias: {
          '@core': './src/core',
          '@features': './src/features',
          '@shared': './src/shared',
          '@navigation': './src/navigation',
          '@': './src',
        },
      },
    ],
  ],
};