import test from "node:test";
import assert from "node:assert/strict";

test("frontend env example exposes api base url", async () => {
  const env = await import("node:fs/promises").then((fs) => fs.readFile(new URL("../.env.example", import.meta.url), "utf8"));
  assert.match(env, /NEXT_PUBLIC_API_BASE_URL=/);
});
