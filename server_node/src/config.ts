export interface GeminiCLIConfig {
    model: string;
    allFiles: boolean;
    sandbox: boolean;
    apiKey?: string;
    queryTimeout: number;
    useShell: boolean;
    projectRoot?: string;
    debug: boolean;
}

export interface AppConfig {
    geminiCLI: GeminiCLIConfig;
}

export function loadConfig(): AppConfig {
    const geminiCLI: GeminiCLIConfig = {
        model: process.env.GEMINI_MODEL || "gemini-2.5-flash",
        allFiles: process.env.GEMINI_ALL_FILES !== "false",
        sandbox: process.env.GEMINI_SANDBOX !== "false",
        apiKey: process.env.GEMINI_API_KEY,
        queryTimeout: parseInt(process.env.QUERY_TIMEOUT || "300", 10),
        useShell: process.env.USE_SHELL === "true",
        projectRoot: process.env.PROJECT_ROOT,
        debug: process.env.DEBUG === "true"
    };

    return { geminiCLI };
} 