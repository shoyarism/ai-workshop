// ESLint flat config (ESLint 9+/10). Replaces the legacy .eslintrc.json.
// Mirrors the previous ruleset: eslint:recommended + @typescript-eslint
// recommended for TypeScript sources, plus the repo's rule tweaks, with the
// CommonJS install/build scripts treated as plain Node scripts.

const js = require('@eslint/js');
const tseslint = require('typescript-eslint');
const globals = require('globals');

module.exports = tseslint.config(
  {
    ignores: ['dist/', 'node_modules/', '**/*.d.ts'],
  },

  // Base recommended rules for every linted file.
  js.configs.recommended,

  // TypeScript sources.
  {
    files: ['**/*.ts'],
    extends: [...tseslint.configs.recommended],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
      globals: { ...globals.node },
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_', caughtErrorsIgnorePattern: '^_' },
      ],
      'no-console': ['warn', { allow: ['log', 'warn', 'error'] }],
      'prefer-const': 'error',
      'no-var': 'error',
    },
  },

  // CommonJS scripts (postinstall, skill staging, test fixtures) run under Node
  // with require(); they are plain JS, not TypeScript.
  {
    files: ['scripts/**/*.js', 'tests/**/*.js'],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'commonjs',
      globals: { ...globals.node },
    },
    rules: {
      'no-console': ['warn', { allow: ['log', 'warn', 'error'] }],
      'prefer-const': 'error',
      'no-var': 'error',
    },
  }
);
