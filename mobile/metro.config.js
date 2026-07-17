const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');
const { withNativeWind } = require('nativewind/metro');

const defaultConfig = getDefaultConfig(__dirname);

const config = mergeConfig(defaultConfig, {
  resolver: {
    nodeModulesPaths: [`${__dirname}/node_modules`],
  },
});

// NativeWind: pipe the global CSS through the bundler
module.exports = withNativeWind(config, { input: './src/global.css' });