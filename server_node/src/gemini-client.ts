import { spawn } from "child_process";
import { GeminiCLIConfig } from "./config";

export class GeminiClientError extends Error {
    constructor(message: string) {
        super(message);
        this.name = "GeminiClientError";
    }
}

export interface GeminiResult {
    stdout: string;
    stderr: string;
    returncode: number;
}

export class GeminiClient {
    private config: GeminiCLIConfig;

    constructor(config: GeminiCLIConfig) {
        this.config = config;
    }

    private verifyGeminiExecutable(): Promise<void> {
        return new Promise((resolve, reject) => {
            const child = spawn("which", ["gemini"]);
            child.on("close", (code) => {
                if (code === 0) {
                    resolve();
                } else {
                    reject(new GeminiClientError("gemini executable not found in PATH. Please ensure gemini-cli is installed and in your system's PATH."));
                }
            });
            child.on("error", () => {
                reject(new GeminiClientError("Failed to check gemini executable"));
            });
        });
    }

    private buildGeminiArgs(commandType: string, prompt: string, extraArgs: string[] = []): string[] {
        const args = [commandType];

        if (this.config.model) {
            args.push("--model", this.config.model);
        }
        if (this.config.allFiles) {
            args.push("--all-files");
        }
        if (this.config.sandbox) {
            args.push("--sandbox");
        }

        args.push(...extraArgs);
        args.push("--prompt", prompt);

        return args;
    }

    private processGeminiOutput(output: string): string {
        return output
            .split("\n")
            .filter(line =>
                line.trim() !== "Loaded cached credentials." &&
                !line.trim().startsWith("[DEBUG]") &&
                !line.includes("Flushing log events to Clearcut.")
            )
            .join("\n")
            .trim();
    }

    async runCommand(commandType: string, prompt: string, extraArgs: string[] = []): Promise<GeminiResult> {
        await this.verifyGeminiExecutable();

        const args = this.buildGeminiArgs(commandType, prompt, extraArgs);
        const env = { ...process.env };

        if (this.config.apiKey) {
            env.GEMINI_API_KEY = this.config.apiKey;
        }

        const options = {
            cwd: this.config.projectRoot || process.cwd(),
            env,
            shell: this.config.useShell,
        };

        return new Promise<GeminiResult>((resolve, reject) => {
            const child = spawn("gemini", args, options);
            let stdout = "";
            let stderr = "";
            let finished = false;

            const timeout = setTimeout(() => {
                if (!finished) {
                    finished = true;
                    child.kill();
                    reject(new GeminiClientError(`Command timed out after ${this.config.queryTimeout}s`));
                }
            }, this.config.queryTimeout * 1000);

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

                const processedStdout = this.processGeminiOutput(stdout);
                const processedStderr = stderr.trim();

                resolve({
                    stdout: processedStdout,
                    stderr: processedStderr,
                    returncode: code || 0
                });
            });

            child.on("error", (err) => {
                clearTimeout(timeout);
                if (finished) return;
                finished = true;
                reject(new GeminiClientError(`Failed to start gemini-cli: ${err.message}`));
            });
        });
    }
} 