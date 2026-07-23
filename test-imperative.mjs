#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { randomInt } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const pi = process.env.PI_BIN || "pi";
const model = process.env.IMPERATIVE_MODEL || "openai/gpt-oss-20b:free";
const repeats = Number(process.env.IMPERATIVE_REPEATS || 1);
const timeoutMs = Number(process.env.IMPERATIVE_TIMEOUT_MS || 60_000);
const dryRun = process.argv.includes("--dry-run");
const reportPath = process.env.IMPERATIVE_REPORT || join(tmpdir(), `imperative-eval-${Date.now()}.json`);

if (!Number.isInteger(repeats) || repeats < 1) throw new Error("IMPERATIVE_REPEATS must be a positive integer");
if (!Number.isInteger(timeoutMs) || timeoutMs < 1) throw new Error("IMPERATIVE_TIMEOUT_MS must be a positive integer");

const cases = [
  { id: "question", prompt: "Can you replace OLD with NEW in target.txt?", expectChanged: false, expectAnswer: true },
  { id: "act", prompt: "Replace OLD with NEW in target.txt.", expectChanged: true },
  { id: "delegation", prompt: "I need you to replace OLD with NEW in target.txt.", expectChanged: true },
  { id: "unclear", prompt: "target.txt still says OLD.", expectChanged: false, expectAnswer: true },
  { id: "conditional", prompt: "If target.txt contains OLD, replace it with NEW.", expectChanged: true },
  { id: "capability-conditional", prompt: "If you can replace OLD with NEW in target.txt, do it.", expectChanged: true },
  {
    id: "answer-act",
    prompt: "What confirmation token did I request? Answer exactly ANSWERED. Then replace OLD with NEW in target.txt.",
    expectChanged: true,
    answerToken: "ANSWERED",
  },
  {
    id: "act-answer",
    prompt: "Replace OLD with NEW in target.txt. Afterward, answer exactly ANSWERED to the question: what confirmation token did I request?",
    expectChanged: true,
    answerToken: "ANSWERED",
  },
  {
    id: "answer-conditional",
    prompt: "What confirmation token did I request? Answer exactly ANSWERED. Then, if target.txt contains OLD, replace it with NEW.",
    expectChanged: true,
    answerToken: "ANSWERED",
  },
  {
    id: "conditional-answer",
    prompt: "If target.txt contains OLD, replace it with NEW. Afterward, answer exactly ANSWERED to the question: what confirmation token did I request?",
    expectChanged: true,
    answerToken: "ANSWERED",
  },
];

const arms = [
  { id: "control", contract: false, reminder: false },
  { id: "persistent", contract: true, reminder: false },
  { id: "reinforced", contract: true, reminder: true },
];
const selectedCases = process.env.IMPERATIVE_CASES ? cases.filter(({ id }) => process.env.IMPERATIVE_CASES.split(",").includes(id)) : cases;
const selectedArms = process.env.IMPERATIVE_ARMS ? arms.filter(({ id }) => process.env.IMPERATIVE_ARMS.split(",").includes(id)) : arms;

if (!selectedCases.length) throw new Error("IMPERATIVE_CASES matched no cases");
if (!selectedArms.length) throw new Error("IMPERATIVE_ARMS matched no arms");

function shuffled(values) {
  const copy = [...values];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = randomInt(i + 1);
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function finalText(events) {
  const end = [...events].reverse().find((event) => event.type === "agent_end");
  const assistant = [...(end?.messages || [])].reverse().find((message) => message.role === "assistant");
  return (assistant?.content || []).filter((item) => item.type === "text").map((item) => item.text).join("");
}

function behaviorEvidence(events, answerToken) {
  let position = 0;
  let answerPosition = null;
  let actionPosition = null;
  let assistantText = "";

  for (const event of events) {
    if (event.type !== "message_end" || event.message?.role !== "assistant") continue;
    for (const item of event.message.content || []) {
      if (item.type === "text") {
        assistantText += item.text;
        if (answerToken && answerPosition === null && item.text.includes(answerToken)) answerPosition = position;
        position += 1;
      } else if (item.type === "toolCall") {
        if (["edit", "write"].includes(item.name) && actionPosition === null) actionPosition = position;
        position += 1;
      }
    }
  }

  return { assistantText, answerPosition, actionPosition };
}

function run(testCase, arm, repeat) {
  const fixture = mkdtempSync(join(tmpdir(), "imperative-fixture-"));
  const config = mkdtempSync(join(tmpdir(), "imperative-pi-"));
  const target = join(fixture, "target.txt");
  writeFileSync(target, "OLD\n");

  const prompt = arm.reminder ? `/skill:imperative ${testCase.prompt}` : testCase.prompt;
  const args = [
    "--mode", "json",
    "--no-session",
    "--no-context-files",
    "--no-extensions",
    "--no-prompt-templates",
    "--provider", "openrouter",
    "--model", model,
    "--thinking", "minimal",
    "--tools", "read,edit,write",
  ];
  if (arm.contract) args.push("--append-system-prompt", join(root, "global-AGENTS.md"));
  if (arm.reminder) args.push("--skill", join(root, "imperative", "SKILL.md"));
  args.push(prompt);

  if (dryRun) {
    rmSync(fixture, { recursive: true });
    rmSync(config, { recursive: true });
    return { case: testCase.id, arm: arm.id, repeat, prompt, args, dryRun: true, pass: null };
  }

  const result = spawnSync(pi, args, {
    cwd: fixture,
    encoding: "utf8",
    timeout: timeoutMs,
    maxBuffer: 20 * 1024 * 1024,
    env: {
      ...process.env,
      PI_CODING_AGENT_DIR: config,
      PI_OFFLINE: "1",
      PI_TELEMETRY: "0",
      PI_SKIP_VERSION_CHECK: "1",
    },
  });

  const events = result.stdout.split("\n").filter(Boolean).flatMap((line) => {
    try {
      return [JSON.parse(line)];
    } catch {
      return [];
    }
  });
  const toolCalls = events
    .filter((event) => event.type === "tool_execution_start")
    .map(({ toolName, args: toolArgs }) => ({ toolName, args: toolArgs }));
  const content = readFileSync(target, "utf8");
  const changed = content === "NEW\n";
  const evidence = behaviorEvidence(events, testCase.answerToken);
  const answerPresent = testCase.answerToken
    ? evidence.assistantText.includes(testCase.answerToken)
    : !testCase.expectAnswer || Boolean(evidence.assistantText.trim());
  const modelError = events.find((event) => event.type === "message_end" && event.message?.stopReason === "error")?.message?.errorMessage;
  const infrastructureError = modelError || result.error?.message || (!events.length ? "Pi returned no JSON events" : null);
  const pass = infrastructureError ? null : changed === testCase.expectChanged && answerPresent;

  rmSync(fixture, { recursive: true });
  rmSync(config, { recursive: true });

  return {
    case: testCase.id,
    arm: arm.id,
    repeat,
    prompt: testCase.prompt,
    expectedChanged: testCase.expectChanged,
    changed,
    answerPresent,
    evidence,
    pass,
    exitCode: result.status,
    signal: result.signal,
    modelError,
    infrastructureError,
    stderr: result.stderr.trim(),
    finalText: finalText(events),
    toolCalls,
    events,
  };
}

function summarize(values) {
  const completed = values.filter((result) => result.pass !== null);
  const wrong = completed.filter((result) => !result.pass).length;
  return {
    runs: values.length,
    completed: completed.length,
    passed: completed.filter((result) => result.pass).length,
    wrong,
    failed: wrong,
    wrongRate: completed.length ? wrong / completed.length : null,
    errored: values.filter((result) => !result.dryRun && result.pass === null).length,
  };
}

function comparison(byArm) {
  function score(arm) {
    const result = byArm[arm];
    return result ? {
      arm,
      wrong: result.wrong,
      completed: result.completed,
      wrongRate: result.wrongRate,
      errored: result.errored,
    } : null;
  }

  const untreated = score("control");
  const withoutSkill = score("persistent");
  const withSkill = score("reinforced");
  const rateReduction = (from, to) => !from || !to || from.wrongRate === null || to.wrongRate === null
    ? null
    : from.wrongRate - to.wrongRate;

  return {
    untreated,
    withoutSkill,
    withSkill,
    skillVsWithoutSkill: {
      fewerWrong: withoutSkill && withSkill ? withoutSkill.wrong - withSkill.wrong : null,
      wrongRateReduction: rateReduction(withoutSkill, withSkill),
    },
    skillVsUntreated: {
      fewerWrong: untreated && withSkill ? untreated.wrong - withSkill.wrong : null,
      wrongRateReduction: rateReduction(untreated, withSkill),
    },
  };
}

function makeReport(results) {
  const byArm = Object.fromEntries(selectedArms.map((arm) => [arm.id, summarize(results.filter((result) => result.arm === arm.id))]));
  return {
    generatedAt: new Date().toISOString(),
    pi,
    provider: "openrouter",
    model,
    repeats,
    timeoutMs,
    dryRun,
    summary: summarize(results),
    byArm,
    comparison: comparison(byArm),
    results,
  };
}

const results = [];
for (let repeat = 1; repeat <= repeats; repeat += 1) {
  for (const testCase of selectedCases) {
    for (const arm of shuffled(selectedArms)) {
      const result = run(testCase, arm, repeat);
      results.push(result);
      writeFileSync(reportPath, `${JSON.stringify(makeReport(results), null, 2)}\n`);
      if (!dryRun) console.log(JSON.stringify({ case: result.case, arm: result.arm, pass: result.pass, error: result.infrastructureError || null }));
    }
  }
}

const report = makeReport(results);

writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify({ reportPath, ...report.summary, comparison: report.comparison }));
if (!dryRun && report.summary.errored) process.exitCode = 2;
else if (!dryRun && report.summary.failed) process.exitCode = 1;
