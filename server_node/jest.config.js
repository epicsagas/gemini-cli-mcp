module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    testMatch: ['**/tests/**/*.test.ts'],
    moduleFileExtensions: ['ts', 'js', 'json', 'node'],
    roots: ['<rootDir>/tests'],
    verbose: true,
    modulePathIgnorePatterns: [
        '<rootDir>/../.vscode',
        '<rootDir>/../.cursor',
        '<rootDir>/../.windsurf',
        '/Users/hackme/Library/',
        '/Users/hackme/.vscode/',
        '/Users/hackme/.cursor/',
        '/Users/hackme/.windsurf/'
    ],
    transform: {
        '^.+\\.tsx?$': 'ts-jest',
    },
    transformIgnorePatterns: [
        '/node_modules/(?!fastmcp|@modelcontextprotocol).+\\.js$'
    ],
}; 