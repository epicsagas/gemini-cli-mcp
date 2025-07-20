#!/usr/bin/env node

import 'dotenv/config';
import { FastMCP } from "fastmcp";
import { VERSION } from "./version";
import { loadConfig } from "./config";
import { GeminiClient } from "./gemini-client";
import { ToolManager } from "./tools";

function printHelp(): void {
    console.log(`Usage: gemini-cli-mcp [options]\n\nOptions:\n  --version, -V    Show version information\n  --verbose, -v    Enable debug mode (set DEBUG=true)\n  --help, -h       Show this help message\n`);
}

function printVersionAndExit(): void {
    console.log(`gemini-cli-mcp-node version: ${VERSION}`);
    const { spawn } = require("child_process");
    const child = spawn("gemini", ["--version"]);
    let geminiVersion = "";
    child.stdout.on("data", (data: Buffer) => {
        geminiVersion += data.toString();
    });
    child.on("close", () => {
        if (geminiVersion.trim()) {
            console.log(`gemini version: ${geminiVersion.trim()}`);
        }
        process.exit(0);
    });
}

// Parse CLI options
const args = process.argv.slice(2);

if (args.includes("--help") || args.includes("-h")) {
    printHelp();
    process.exit(0);
}

if (args.includes("--version") || args.includes("-V")) {
    printVersionAndExit();
}

if (args.includes("--verbose") || args.includes("-v")) {
    process.env.DEBUG = "true";
}

// Load configuration
const appConfig = loadConfig();

// Initialize FastMCP server
const server = new FastMCP({
    name: "gemini-cli-mcp",
    version: VERSION,
});

// Initialize GeminiClient
const geminiClient = new GeminiClient(appConfig.geminiCLI);

// Register tools
new ToolManager(server, geminiClient);

// Start the server
const transportType = process.env.MCP_TRANSPORT === "http" ? "httpStream" : "stdio";
server.start({ transportType }); 