import { C as Check, D as DimensionId, R as Report, S as ScanIncompleteReason, a as ScanContext, b as DimensionScore, c as ResolvedScanConfig, d as ScanVerdict, e as CliConfigOverrides } from './registry-Dq4QBLCp.js';
export { f as CONFIG_FILENAME, g as CheckOutcome, h as CheckResult, i as DEFAULT_CONFIG, j as DIMENSIONS, k as DimensionInfo, E as ExtraRootEntry, G as GateMode, H as HarnessScoreConfig, L as LevelInfo, P as PRESET_REGISTRY, l as PROTECTED_CHECKS, m as PresetInfo, n as ResolvedSeverity, o as ScanDiagnostic, p as ScanIncompleteReasonCode, q as ScanVerdictStatus, r as ScopeFlag, s as ScoreSnapshot, t as Severity, T as TOOL_DISPLAY_NAMES, u as ToolId, v as discoverConfig, w as loadConfigFile, x as parseConfigObject, y as parseScopeFlagList, z as resolveScanConfig, A as resolveSeverities, B as toolDisplayName } from './registry-Dq4QBLCp.js';

declare const ALL_CHECKS: Check[];

interface DimensionDelta {
    id: DimensionId;
    title: string;
    before: number;
    after: number;
    delta: number;
}
interface CheckDelta {
    id: string;
    title: string;
    points: number;
    change: 'newly-passing' | 'newly-failing' | 'became-applicable' | 'became-not-applicable';
}
interface ReportDiff {
    level: {
        before: number;
        beforeName: string;
        after: number;
        afterName: string;
        delta: number;
    };
    score: {
        before: {
            earned: number;
            max: number;
            percent: number;
        };
        after: {
            earned: number;
            max: number;
            percent: number;
        };
        /** Raw point delta. Only meaningful when `before.max === after.max` — prefer deltaPercent otherwise. */
        deltaEarned: number;
        deltaPercent: number;
    };
    dimensions: DimensionDelta[];
    checksChanged: CheckDelta[];
    /**
     * True when baseline and current come from different tool versions or the
     * check catalog (ids or point values) differs. A scan `score.max` that moved
     * only because a check became applicable or not applicable is a repository
     * change, not a maturity-model change.
     */
    maturityModelChanged: boolean;
    /**
     * True when the team customization (`.harness-score.json`'s `extends`/`rules`) actually
     * applied differs between baseline and current — dimension/score deltas may then reflect
     * a config change rather than an actual change in the repository.
     */
    presetChanged: boolean;
}
/**
 * Compares two reports from the same maturity model version. Checks present in
 * `current` but absent from `baseline` (e.g. the model gained a check between
 * scans) are ignored for the pass/fail delta — that's a maturity model change, not a
 * regression or improvement in the scanned repository.
 */
declare function computeDiff(baseline: Report, current: Report): ReportDiff;

/**
 * shields.io pattern: 20px height, 11px Verdana, fixed width (level only).
 */
declare function renderBadge(report: Report): string;

declare function renderMarkdown(report: Report, diff?: ReportDiff | null): string;

declare function renderTerminal(report: Report, diff?: ReportDiff | null): string;

interface ScanOverlay {
    label: string;
    /** Repo-relative path → absolute path for reading (repo wins on conflict). */
    files: Map<string, string>;
    truncated?: boolean;
    incompleteReasons?: ScanIncompleteReason[];
}
interface CreateScanOptions {
    overlays?: ScanOverlay[];
}
declare function createScanContext(rootInput: string, options?: CreateScanOptions): ScanContext;

declare const DOCS_BASE_URL = "https://paladini.github.io/harness-score/guide/measure-and-improve";
declare const TOOL_VERSION = "1.8.1";
declare const LEVEL_NAMES: readonly ["Unharnessed", "Documented", "Guided", "Sensing", "Self-correcting"];
interface Requirement {
    label: string;
    /** Set only by dimAtLeast — lets computeLevel tell "structurally unreachable" apart from "not yet met". */
    blockedDimension?: DimensionId;
    met(dims: Map<DimensionId, DimensionScore>, totalPercent: number): boolean;
}
/**
 * The maturity ladder. A level is reached when ALL of its requirements
 * (and every previous level's) are met. Mirrored verbatim in the guide's
 * Maturity Model chapter — change both together.
 */
declare const LEVEL_REQUIREMENTS: Requirement[][];
declare function buildReportFromContext(maturityCtx: ScanContext, effectiveCtx: ScanContext, config: ResolvedScanConfig, resolvedRoots: Report['resolvedRoots']): Report;
/** Build a full report for a repository root with optional scope configuration. */
declare function buildReport(rootInput: string, config?: ResolvedScanConfig): Report;
/** @deprecated Prefer buildReport(root, config). Kept for internal use with a pre-built context. */
declare function buildReportFromScanContext(ctx: ScanContext): Report;

type VerdictScope = 'maturity' | 'effective';
/** Resolve additive verdicts while preserving fail-closed behavior for legacy reports. */
declare function reportVerdict(report: Report, scope: VerdictScope): ScanVerdict;
declare function reportScopeIsComplete(report: Report, scope: VerdictScope): boolean;
declare function formatIncompleteReason(reason: ScanIncompleteReason): string;

interface ScoreOptions extends CliConfigOverrides {
}
/** One-call API: scan a directory and get the full report. */
declare function score(root: string, options?: ScoreOptions): Report;

export { ALL_CHECKS, Check, type CheckDelta, CliConfigOverrides, type CreateScanOptions, DOCS_BASE_URL, type DimensionDelta, DimensionId, DimensionScore, LEVEL_NAMES, LEVEL_REQUIREMENTS, Report, type ReportDiff, ResolvedScanConfig, ScanContext, ScanIncompleteReason, type ScanOverlay, ScanVerdict, type ScoreOptions, TOOL_VERSION, type VerdictScope, buildReport, buildReportFromContext, buildReportFromScanContext, computeDiff, createScanContext, formatIncompleteReason, renderBadge, renderMarkdown, renderTerminal, reportScopeIsComplete, reportVerdict, score };
