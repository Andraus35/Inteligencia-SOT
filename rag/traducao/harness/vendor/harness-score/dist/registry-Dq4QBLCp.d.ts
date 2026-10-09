type GateMode = 'maturity' | 'effective';
type ScopeFlag = 'user' | 'system';
/**
 * A check's scoring severity, borrowing ESLint's own vocabulary. Only 'off'
 * and 'error' are accepted in v1.5 — 'warn' is a recognized value that's
 * deliberately rejected for now (reserved for a future "advisory, non-blocking"
 * mode), not an unrecognized one.
 */
type Severity = 'off' | 'warn' | 'error';
interface ExtraRootEntry {
    id: string;
    path: string;
}
interface HarnessScoreConfig {
    scopes: {
        user: boolean;
        system: boolean;
    };
    extraRoots: ExtraRootEntry[];
    gate: GateMode;
    /** Named, maintainer-curated presets to apply, in order (see PRESET_REGISTRY). */
    extends: string[];
    /** Per-check-ID severity override, applied after every preset in `extends`. */
    rules: Record<string, Severity>;
}
interface ResolvedScanConfig {
    scopes: {
        user: boolean;
        system: boolean;
    };
    extraRoots: ExtraRootEntry[];
    gate: GateMode;
    /** Scopes included in the effective score (repo is always first). */
    effectiveScopes: Array<'repo' | 'user' | 'system' | string>;
    extends: string[];
    rules: Record<string, Severity>;
}
declare const DEFAULT_CONFIG: HarnessScoreConfig;
declare const CONFIG_FILENAME = ".harness-score.json";
/**
 * Built-in, maintainer-curated presets — the ESLint-flavored alternative to
 * free-form per-repo waivers. Each preset is a named, versioned, PR-reviewed
 * bundle of severity overrides (see CONTRIBUTING.md "Proposing a preset").
 * `no-hooks` is derived from ALL_CHECKS rather than hardcoded IDs so it never
 * drifts if the hooks dimension gains a check.
 */
declare const PRESET_REGISTRY: Record<string, Record<string, Severity>>;
/**
 * Checks that detect actively leaked/exposed credentials — never eligible for
 * "off", from either a local `rules` override or a preset, regardless of how
 * the exclusion is justified. This is the one thing "customizable, but still
 * serious" can't bend on: nothing in this config format may silence an actual
 * secret-leak detector, only disclosure-and-review protects everything else.
 */
declare const PROTECTED_CHECKS: Set<string>;
interface CliConfigOverrides {
    configPath?: string | null;
    /** When set, replaces config-file scope toggles. */
    scopeFlags?: ScopeFlag[] | null;
    gate?: GateMode | null;
}
/** Parse and validate a config object (strict — unknown keys are rejected). */
declare function parseConfigObject(raw: unknown, source: string): HarnessScoreConfig;
interface ResolvedSeverity {
    severity: Severity;
    source: 'default' | string;
}
/**
 * Resolves the final severity for every check: default 'error' → each preset
 * in `extends`, applied in array order → `rules` local overrides, applied
 * last (highest precedence). Map insertion order follows ALL_CHECKS order and
 * is never disturbed by later overwrites, keeping output deterministic.
 */
declare function resolveSeverities(cfg: {
    extends: string[];
    rules: Record<string, Severity>;
}): Map<string, ResolvedSeverity>;
declare function loadConfigFile(configPath: string): HarnessScoreConfig;
declare function discoverConfig(repoRoot: string): HarnessScoreConfig | null;
declare function parseScopeFlagList(value: string): ScopeFlag[];
/** Merge defaults → config file → CLI overrides. */
declare function resolveScanConfig(repoRoot: string, overrides?: CliConfigOverrides): ResolvedScanConfig;

type DimensionId = 'context' | 'skills' | 'hooks' | 'sensors' | 'ci' | 'hygiene';
interface DimensionInfo {
    id: DimensionId;
    title: string;
}
declare const DIMENSIONS: DimensionInfo[];
/** Everything a check may look at. Built once per scan; checks never touch the filesystem directly. */
interface ScanContext {
    /** Absolute path of the scanned repository root. */
    root: string;
    /** All file paths relative to root, POSIX separators, sorted. */
    files: string[];
    /** Compatibility alias: true whenever the scan is incomplete for any reason. */
    truncated: boolean;
    /** Deterministic reasons the filesystem walk or a requested file read could not complete. */
    incompleteReasons?: ScanIncompleteReason[];
    /** True when the relative path exists as a file. */
    has(relPath: string): boolean;
    /** File content as UTF-8, or null when missing/unreadable/over the read limit. Cached. */
    read(relPath: string): string | null;
    /** All files whose relative path matches the regex. */
    matching(re: RegExp): string[];
}
/** Non-fatal diagnostic attached to a check result. */
interface ScanDiagnostic {
    code: string;
    message: string;
    source?: string;
}
type ScanIncompleteReasonCode = 'file-count-limit' | 'depth-limit' | 'unreadable-directory' | 'unreadable-path' | 'outside-root-symlink';
interface ScanIncompleteReason {
    code: ScanIncompleteReasonCode;
    path?: string;
    limit?: number;
}
type ScanVerdictStatus = 'complete' | 'incomplete';
interface ScanVerdict {
    status: ScanVerdictStatus;
    reasons: ScanIncompleteReason[];
}
interface CheckOutcome {
    passed: boolean;
    /** Human-readable proof: what was found (or not found) and where. */
    evidence: string;
    /**
     * When false, the check does not apply to this repository and is excluded
     * from both the numerator and the denominator. Defaults to true.
     */
    applicable?: boolean;
    /** Forward-compatible or secondary findings that do not change points. */
    warnings?: ScanDiagnostic[];
}
interface Check {
    /** Stable id like "CTX-01"; doubles as the docs anchor (lowercased). */
    id: string;
    dimension: DimensionId;
    title: string;
    points: number;
    /** One actionable sentence shown when the check fails. */
    remediation: string;
    run(ctx: ScanContext): CheckOutcome;
}
interface CheckResult {
    id: string;
    dimension: DimensionId;
    title: string;
    points: number;
    earned: number;
    passed: boolean;
    evidence: string;
    remediation: string;
    docsUrl: string;
    /** Resolved severity ('off' checks are excluded from scoring but still listed here). */
    severity: Severity;
    /**
     * False when the check does not apply to this repository. Excluded from
     * scoring, distinct from severity 'off' (which is config). Older reports
     * omit this field; treat a missing value as true.
     */
    applicable: boolean;
    /** Non-fatal diagnostics emitted while evaluating this check. */
    warnings?: ScanDiagnostic[];
}
interface DimensionScore {
    id: DimensionId;
    title: string;
    earned: number;
    max: number;
    /** 0–100, rounded. */
    percent: number;
    /** False when no check in this dimension is scored ('off' and/or not applicable). */
    applicable: boolean;
}
interface LevelInfo {
    /** 0–4 */
    index: number;
    name: string;
    /** What is missing to reach the next level; empty at L4. */
    nextLevelGaps: string[];
    /** True when at least one blocking requirement for the next level can never be met under the current config (e.g. its dimension was excluded by a preset). */
    capped: boolean;
    /** Human-readable explanation of why the level is capped; set only when `capped` is true. */
    capReason?: string;
}
/** One scored snapshot (maturity or effective). */
interface ScoreSnapshot {
    level: LevelInfo;
    score: {
        earned: number;
        max: number;
        percent: number;
    };
    dimensions: DimensionScore[];
    checks: CheckResult[];
    detectedHarnesses: string[];
}

/** Local team customization actually applied to this scan, always present and never hidden behind a flag. */
interface PresetInfo {
    /** Preset names from `.harness-score.json`'s `extends`, in application order. */
    extends: string[];
    /** Raw per-check severity overrides from `.harness-score.json`'s `rules`. */
    rules: Record<string, Severity>;
    /** Every check whose resolved severity differs from the 'default' error baseline, with why. */
    resolved: Array<{
        id: string;
        severity: Severity;
        source: string;
    }>;
}
interface Report {
    tool: {
        name: string;
        version: string;
    };
    root: string;
    /** Compatibility alias: true whenever the maturity or effective snapshot is incomplete. */
    truncated: boolean;
    /** Authoritative completeness for repository-only and effective snapshots. */
    verdicts?: {
        maturity: ScanVerdict;
        effective: ScanVerdict;
    };
    /** Scopes included in each score. */
    scopes: {
        maturity: ['repo'];
        effective: Array<'repo' | 'user' | 'system' | string>;
    };
    /** Which score `--min-level` and CI gates use. */
    gate: GateMode;
    /** Absolute paths resolved for non-repo scopes (informational). */
    resolvedRoots?: Array<{
        scope: string;
        absPath: string;
    }>;
    /** Tool IDs with at least one harness artifact detected in the repo (informational). */
    detectedHarnesses: string[];
    /** Repository-only score — canonical for CI when gate is maturity. */
    level: LevelInfo;
    score: {
        earned: number;
        max: number;
        percent: number;
    };
    dimensions: DimensionScore[];
    checks: CheckResult[];
    /** Repo ∪ configured global/extra scopes — what the agent likely sees on this machine. */
    effective: ScoreSnapshot;
    /** Team customization (extends/rules) actually applied to this scan. */
    preset: PresetInfo;
}

/** Stable tool identifiers surfaced in scan reports. */
type ToolId = 'cursor' | 'windsurf' | 'cline' | 'continue' | 'copilot' | 'claude-code' | 'devin' | 'codex' | 'opencode' | 'antigravity' | 'zed';
type HarnessKind = 'rules' | 'skills' | 'commands' | 'subagents' | 'hooks' | 'mcp';
/** Human-readable tool names for report renderers. */
declare const TOOL_DISPLAY_NAMES: Record<ToolId, string>;
/** Display name for a detected tool id; unknown ids pass through as-is. */
declare function toolDisplayName(id: string): string;
interface PathSpec {
    toolId: ToolId;
    kind: HarnessKind;
    /** Regex tested against ScanContext file paths (POSIX). */
    pathRegex: RegExp;
    /** Tool-native directory that may itself be used as the scan root. */
    nativeRoot?: string;
}
interface PathSpecMatch {
    /** Physical path relative to ScanContext.root. */
    path: string;
    /** Canonical repository-relative shape used by PATH_SPECS. */
    canonicalPath: string;
    /** Number of path segments before the native tool directory. */
    nativeDepth: number;
}
/** Match a path spec without changing the public root-relative ScanContext contract. */
declare function matchPathSpec(ctx: ScanContext, spec: PathSpec): PathSpecMatch[];
/** Project guide paths checked by CTX-01/02. Order is preference for evidence only. */
declare const CONTEXT_ROOT_FILES: readonly ["AGENTS.md", "CLAUDE.md", "GEMINI.md", ".claude/CLAUDE.md", ".claude/AGENTS.md"];
/** Claude Code session-start instructions — never CTX-03..06 rule artifacts. */
declare const CLAUDE_PROJECT_GUIDE_PATHS: Set<string>;
declare const PATH_SPECS: PathSpec[];
/** Plugin-facing path hints — kept in sync with PATH_SPECS via plugins:sync-check. */
declare const PLUGIN_TOOL_PATHS: Record<string, {
    skillsDir: string;
    commandsDir: string;
    mcpConfigPath: string;
}>;
declare function specsForKind(kind: HarnessKind): PathSpec[];

export { resolveSeverities as A, toolDisplayName as B, type Check as C, type DimensionId as D, type ExtraRootEntry as E, CLAUDE_PROJECT_GUIDE_PATHS as F, type GateMode as G, type HarnessScoreConfig as H, CONTEXT_ROOT_FILES as I, type HarnessKind as J, PATH_SPECS as K, type LevelInfo as L, PLUGIN_TOOL_PATHS as M, type PathSpec as N, type PathSpecMatch as O, PRESET_REGISTRY as P, matchPathSpec as Q, type Report as R, type ScanIncompleteReason as S, TOOL_DISPLAY_NAMES as T, specsForKind as U, type ScanContext as a, type DimensionScore as b, type ResolvedScanConfig as c, type ScanVerdict as d, type CliConfigOverrides as e, CONFIG_FILENAME as f, type CheckOutcome as g, type CheckResult as h, DEFAULT_CONFIG as i, DIMENSIONS as j, type DimensionInfo as k, PROTECTED_CHECKS as l, type PresetInfo as m, type ResolvedSeverity as n, type ScanDiagnostic as o, type ScanIncompleteReasonCode as p, type ScanVerdictStatus as q, type ScopeFlag as r, type ScoreSnapshot as s, type Severity as t, type ToolId as u, discoverConfig as v, loadConfigFile as w, parseConfigObject as x, parseScopeFlagList as y, resolveScanConfig as z };
