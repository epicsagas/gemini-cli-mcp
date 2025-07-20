import { FastMCP } from "fastmcp";
import { z } from "zod";
import { GeminiClient, GeminiClientError } from "./gemini-client";

export class ToolManager {
    private mcp: FastMCP;
    private geminiClient: GeminiClient;

    constructor(mcp: FastMCP, geminiClient: GeminiClient) {
        this.mcp = mcp;
        this.geminiClient = geminiClient;
        this.registerTools();
    }

    private registerTools(): void {
        // gemini_ask tool
        this.mcp.addTool({
            name: "gemini_ask",
            description: "Ask a simple question to the Gemini model.",
            parameters: z.object({
                question: z.string(),
            }),
            execute: async (args) => {
                try {
                    const result = await this.geminiClient.runCommand("ask", args.question);
                    return result.stdout;
                } catch (error) {
                    if (error instanceof GeminiClientError) {
                        throw new Error(error.message);
                    }
                    throw new Error(`Unexpected error: ${error}`);
                }
            },
        });

        // gemini_yolo tool
        this.mcp.addTool({
            name: "gemini_yolo",
            description: "Run a complex prompt with Gemini Agent in auto-execution (--yolo) mode.",
            parameters: z.object({
                prompt: z.string(),
            }),
            execute: async (args) => {
                try {
                    const result = await this.geminiClient.runCommand("agent", args.prompt, ["--yolo"]);
                    return result.stdout;
                } catch (error) {
                    if (error instanceof GeminiClientError) {
                        throw new Error(error.message);
                    }
                    throw new Error(`Unexpected error: ${error}`);
                }
            },
        });

        // gemini_git_diff tool
        this.mcp.addTool({
            name: "gemini_git_diff",
            description: "Summarize code changes using Gemini AI.",
            parameters: z.object({
                diff_args: z.string().optional(),
            }),
            execute: async (args) => {
                try {
                    let prompt = "Summarize the code changes.";
                    if (args.diff_args) {
                        prompt += ` Use git diff arguments: '${args.diff_args}'.`;
                    }
                    const result = await this.geminiClient.runCommand("ask", prompt);
                    return result.stdout;
                } catch (error) {
                    if (error instanceof GeminiClientError) {
                        throw new Error(error.message);
                    }
                    throw new Error(`Unexpected error: ${error}`);
                }
            },
        });

        // gemini_git_commit tool
        this.mcp.addTool({
            name: "gemini_git_commit",
            description: "Generate a conventional commit message from staged changes and perform a git commit.",
            parameters: z.object({
                branch_name: z.string().optional(),
            }),
            execute: async (args) => {
                try {
                    let prompt = "Generate a conventional commit message for the current staged changes and commit them.";
                    if (args.branch_name) {
                        prompt += ` Use the branch '${args.branch_name}'.`;
                    }
                    const result = await this.geminiClient.runCommand("ask", prompt);
                    return result.stdout;
                } catch (error) {
                    if (error instanceof GeminiClientError) {
                        throw new Error(error.message);
                    }
                    throw new Error(`Unexpected error: ${error}`);
                }
            },
        });

        // gemini_git_pr tool
        this.mcp.addTool({
            name: "gemini_git_pr",
            description: "Automatically commit, push, and create a PR with a conventional commit message.",
            parameters: z.object({
                commit_message: z.string().optional(),
                branch_name: z.string().optional(),
                pr_title: z.string().optional(),
            }),
            execute: async (args) => {
                try {
                    let prompt = "Create a pull request with a conventional commit message.";
                    if (args.commit_message) {
                        prompt += ` Use this commit message: '${args.commit_message}'.`;
                    }
                    if (args.branch_name) {
                        prompt += ` Use the branch '${args.branch_name}'.`;
                    }
                    if (args.pr_title) {
                        prompt += ` PR title: '${args.pr_title}'.`;
                    }
                    const result = await this.geminiClient.runCommand("ask", prompt);
                    return result.stdout;
                } catch (error) {
                    if (error instanceof GeminiClientError) {
                        throw new Error(error.message);
                    }
                    throw new Error(`Unexpected error: ${error}`);
                }
            },
        });
    }
} 