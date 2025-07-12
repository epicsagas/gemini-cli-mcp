const { writeFileSync, readFileSync } = require("fs");
const { join } = require("path");
const pkg = JSON.parse(readFileSync(join(__dirname, "package.json"), "utf-8"));
writeFileSync(join(__dirname, "src/version.ts"), `export const VERSION = "${pkg.version}";\n`); 