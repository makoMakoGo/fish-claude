import { execFileSync } from "node:child_process";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { tmpdir } from "node:os";
import { pathToFileURL } from "node:url";
import { afterAll, expect, test } from "bun:test";

interface SearchResult {
	answer?: string;
	model?: string;
}

interface CapturedRequest {
	url: string;
	authorization: string | null;
	model: string;
}

type SearchCodex = (params: Record<string, unknown>) => Promise<SearchResult>;
type HasCodexSearch = (authStorage: Record<string, unknown>) => Promise<boolean>;

function resolveOmpPackageRoot(): string {
	const override = process.env.OMP_PATCH_PACKAGE_ROOT?.trim();
	if (override) return path.resolve(override);
	const npmRoot = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
	return path.join(npmRoot, "@oh-my-pi", "pi-coding-agent");
}

const originalAgentDir = process.env.PI_CODING_AGENT_DIR;
const originalCodexModel = process.env.PI_CODEX_WEB_SEARCH_MODEL;
const testRoot = await mkdtemp(path.join(tmpdir(), "omp-codex-byok-test-"));
const agentDir = path.join(testRoot, "agent");
const projectDir = path.join(testRoot, "project");
process.env.PI_CODING_AGENT_DIR = agentDir;

await writeFile(path.join(testRoot, ".keep"), "");
await Bun.write(
	path.join(agentDir, "config.yml"),
	["modelRoles:", "  default: beta/beta-model:high", ""].join("\n"),
);
await Bun.write(
	path.join(agentDir, "models.yaml"),
	[
		"providers:",
		"  alpha:",
		"    api: openai-responses",
		"    baseUrl: https://alpha.example",
		"    apiKey: alpha-secret",
		"    models:",
		"      - id: alpha-model",
		"  beta:",
		"    api: openai-responses",
		"    baseUrl: https://beta.example",
		"    apiKey: beta-secret",
		"    models:",
		"      - id: beta-model",
		"",
	].join("\n"),
);

// The package root is runtime-selected so one harness can exercise pristine, desired, and installed OMP sources.
const packageRoot = resolveOmpPackageRoot();
const settingsPath = path.join(packageRoot, "src", "config", "settings.ts");
const { Settings, resetSettingsForTest, settings } = await import(pathToFileURL(settingsPath).href);
await Settings.init({ cwd: projectDir, agentDir });

const providerPath = path.join(packageRoot, "src", "web", "search", "providers", "codex.ts");
const providerModule = await import(pathToFileURL(providerPath).href);
const searchCodex = providerModule.searchCodex as SearchCodex;
const hasCodexSearch = providerModule.hasCodexSearch as HasCodexSearch;

afterAll(async () => {
	resetSettingsForTest();
	if (originalAgentDir === undefined) delete process.env.PI_CODING_AGENT_DIR;
	else process.env.PI_CODING_AGENT_DIR = originalAgentDir;
	if (originalCodexModel === undefined) delete process.env.PI_CODEX_WEB_SEARCH_MODEL;
	else process.env.PI_CODEX_WEB_SEARCH_MODEL = originalCodexModel;
	await rm(testRoot, { recursive: true, force: true });
});

async function runSearch(modelOverride: string | undefined): Promise<{ result: SearchResult; requests: CapturedRequest[] }> {
	if (modelOverride === undefined) delete process.env.PI_CODEX_WEB_SEARCH_MODEL;
	else process.env.PI_CODEX_WEB_SEARCH_MODEL = modelOverride;

	const requests: CapturedRequest[] = [];
	const fetch = async (input: string | URL | Request, init?: RequestInit): Promise<Response> => {
		const url = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
		const body = JSON.parse(String(init?.body)) as { model: string };
		requests.push({
			url,
			authorization: new Headers(init?.headers).get("authorization"),
			model: body.model,
		});
		const stream = [
			`data: ${JSON.stringify({ type: "response.output_text.delta", delta: `answer for ${body.model}` })}`,
			`data: ${JSON.stringify({ type: "response.completed", response: { id: `req-${body.model}`, model: body.model } })}`,
			"",
		].join("\n\n");
		return new Response(stream, { status: 200, headers: { "content-type": "text/event-stream" } });
	};

	const result = await searchCodex({
		query: "test query",
		systemPrompt: "Search the web.",
		authStorage: { getOAuthAccess: async () => undefined, hasOAuth: () => false },
		fetch,
	});
	return { result, requests };
}

test("uses the initialized default model role for the BYOK backend", async () => {
	const { result, requests } = await runSearch(undefined);

	expect(result.answer).toBe("answer for beta-model");
	expect(result.model).toBe("beta-model");
	expect(requests).toEqual([
		{
			url: "https://beta.example/v1/responses",
			authorization: "Bearer beta-secret",
			model: "beta-model",
		},
	]);
});

test("lets PI_CODEX_WEB_SEARCH_MODEL explicitly select the BYOK backend", async () => {
	const { result, requests } = await runSearch("alpha/alpha-model");

	expect(result.answer).toBe("answer for alpha-model");
	expect(result.model).toBe("alpha-model");
	expect(requests).toEqual([
		{
			url: "https://alpha.example/v1/responses",
			authorization: "Bearer alpha-secret",
			model: "alpha-model",
		},
	]);
});

test("does not select an arbitrary BYOK provider for a non-Responses default role", async () => {
	delete process.env.PI_CODEX_WEB_SEARCH_MODEL;
	settings.setModelRole("default", "xai-oauth/grok-4.5:xhigh");
	const authStorage = { getOAuthAccess: async () => undefined, hasOAuth: () => false };
	let fetchCalls = 0;

	try {
		expect(await hasCodexSearch(authStorage)).toBe(false);
		await expect(
			searchCodex({
				query: "test query",
				systemPrompt: "Search the web.",
				authStorage,
				fetch: async () => {
					fetchCalls++;
					return new Response("unexpected request", { status: 500 });
				},
			}),
		).rejects.toThrow("No Codex search backend available");
		expect(fetchCalls).toBe(0);
	} finally {
		settings.setModelRole("default", "beta/beta-model:high");
	}
});
