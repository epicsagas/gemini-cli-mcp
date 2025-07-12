#!/usr/bin/env node

import 'dotenv/config';
import { FastMCP } from "fastmcp";
import { z } from "zod";
import { spawn } from "child_process";
import { readFileSync } from "fs";
import { join } from "path";
import { VERSION } from "./version";

// 환경변수 상수 선언 복구
const GEMINI_MODEL = process.env.GEMINI_MODEL || "gemini-2.5-flash";
const GEMINI_ALL_FILES = process.env.GEMINI_ALL_FILES !== "false";
const GEMINI_SANDBOX = process.env.GEMINI_SANDBOX !== "false";
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "";
const PROJECT_ROOT = process.env.PROJECT_ROOT || "";
const QUERY_TIMEOUT = parseInt(process.env.QUERY_TIMEOUT || "300", 10);
const USE_SHELL = process.env.USE_SHELL === "true";

function printHelp() {
    console.log(`Usage: gemini-cli-mcp [options]\n\nOptions:\n  --version, -V    Show version information\n  --verbose, -v    Enable debug mode (set DEBUG=true)\n  --help, -h       Show this help message\n`);
}

function printVersionAndExit() {
    console.log(`gemini-cli-mcp-node version: ${VERSION}`);
    const child = spawn("gemini", ["--version"]);
    let geminiVersion = "";
    child.stdout.on("data", (data) => {
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

const server = new FastMCP({
    name: "gemini-cli-mcp",
    version: VERSION,
});

function buildGeminiArgs(prompt: string, extra: string[] = []): string[] {
    const args = ["ask"];
    if (extra.includes("agent")) {
        args[0] = "agent";
        if (!args.includes("--yolo")) args.push("--yolo");
    }
    if (GEMINI_MODEL) args.push("--model", GEMINI_MODEL);
    if (GEMINI_ALL_FILES) args.push("--all-files");
    if (GEMINI_SANDBOX) args.push("--sandbox");
    args.push("--prompt", prompt);
    return args;
}

function runGeminiCLI(args: string[]): Promise<string> {
    return new Promise<string>((resolve, reject) => {
        const env = { ...process.env };
        if (GEMINI_API_KEY) env.GEMINI_API_KEY = GEMINI_API_KEY;
        const options = {
            cwd: PROJECT_ROOT || process.cwd(),
            env,
            shell: USE_SHELL,
        };
        const child = spawn("gemini", args, options);
        let stdout = "";
        let stderr = "";
        let finished = false;
        const timeout = setTimeout(() => {
            if (!finished) {
                finished = true;
                child.kill();
                reject("Error: Command timed out after " + QUERY_TIMEOUT + "s");
            }
        }, QUERY_TIMEOUT * 1000);
        child.stdout.on("data", (data) => {
            stdout += data.toString();
        });
        child.stderr.on("data", (data) => {
            stderr += data.toString();
        });
        child.on("close", (code) => {
            clearTimeout(timeout);
            if (finished) return;
            finished = true;
            // Filter out 'Loaded cached credentials.' from stdout
            const filteredStdout = stdout
                .split("\n")
                .filter(line => line.trim() !== "Loaded cached credentials.")
                .join("\n")
                .trim();
            if (code === 0) {
                resolve(filteredStdout);
            } else {
                reject(stderr.trim() || `gemini exited with code ${code}`);
            }
        });
        child.on("error", (err) => {
            clearTimeout(timeout);
            if (finished) return;
            finished = true;
            reject("Failed to start gemini-cli: " + err.message);
        });
    });
}

// gemini_ask tool
server.addTool({
    name: "gemini_ask",
    description: "Ask a question to the Gemini model.",
    parameters: z.object({
        question: z.string(),
    }),
    execute: async (args) => {
        const geminiArgs = buildGeminiArgs(args.question);
        return runGeminiCLI(geminiArgs);
    },
});

// gemini_agent tool
server.addTool({
    name: "gemini_agent",
    description: "Run a complex prompt with Gemini Agent in auto-execution (--yolo) mode.",
    parameters: z.object({
        prompt: z.string(),
    }),
    execute: async (args) => {
        const geminiArgs = buildGeminiArgs(args.prompt, ["agent"]);
        return runGeminiCLI(geminiArgs);
    },
});

const transportType = process.env.MCP_TRANSPORT === "http" ? "httpStream" : "stdio";
server.start({ transportType }); 