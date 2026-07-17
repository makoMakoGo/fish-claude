import { execFileSync } from "node:child_process";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { expect, test } from "bun:test";

interface SearchResult {
	answer?: string;
}

type SearchPerplexity = (params: Record<string, unknown>) => Promise<SearchResult>;

function resolveOmpPackageRoot(): string {
	const override = process.env.OMP_PATCH_PACKAGE_ROOT?.trim();
	if (override) return path.resolve(override);
	const npmRoot = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
	return path.join(npmRoot, "@oh-my-pi", "pi-coding-agent");
}

const providerPath = path.join(resolveOmpPackageRoot(), "src", "web", "search", "providers", "perplexity.ts");
// The active FNM npm root is runtime-selected, so this module path cannot be a static import.
const providerModule = await import(pathToFileURL(providerPath).href);
const searchPerplexity = providerModule.searchPerplexity as SearchPerplexity;
const oauthToken = "perplexity-oauth-session-token";

function createOAuthOnlyStorage(): Record<string, unknown> {
	return {
		getOAuthAccess: async () => ({ accessToken: oauthToken }),
		getApiKey: async (provider: string) => (provider === "perplexity" ? oauthToken : undefined),
		getCredentialOrigin: (provider: string) => (provider === "perplexity" ? { kind: "oauth" } : undefined),
	};
}

test("retries transient OAuth transport failure without switching to the API endpoint", async () => {
	const requestedUrls: string[] = [];
	let oauthAttempts = 0;
	const fetch = async (input: string | URL | Request): Promise<Response> => {
		const url = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
		requestedUrls.push(url);
		if (!url.endsWith("/rest/sse/perplexity_ask")) {
			return new Response("Unauthorized", { status: 401 });
		}

		oauthAttempts++;
		if (oauthAttempts === 1) {
			throw new TypeError("socket connection closed");
		}
		const event = { status: "COMPLETED", final: true, text: "retry succeeded", blocks: [] };
		return new Response(`data: ${JSON.stringify(event)}\n\n`, {
			status: 200,
			headers: { "content-type": "text/event-stream" },
		});
	};

	const result = await searchPerplexity({
		query: "test query",
		authStorage: createOAuthOnlyStorage(),
		fetch,
	});

	expect(result.answer).toBe("retry succeeded");
	expect(requestedUrls).toEqual([
		"https://www.perplexity.ai/rest/sse/perplexity_ask",
		"https://www.perplexity.ai/rest/sse/perplexity_ask",
	]);
});
