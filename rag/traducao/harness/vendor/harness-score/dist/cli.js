#!/usr/bin/env node
import{i as d,j as m,k as g,l,m as h,n as b,o as y,r as v,v as w,x as S,y as k}from"./chunk-3K6E42PW.js";import"./chunk-XBA7NARO.js";import*as a from"fs";import*as R from"path";var $=`harness-score \u2014 deterministic harness-maturity scanner for AI-assisted repositories

Usage:
  harness-score [path] [options]

Options:
  --json               Print the full report as JSON instead of the terminal view
  --md <file|->        Write a markdown report to <file> (or stdout with "-")
  --badge <file>       Write an SVG maturity badge to <file>
  --min-level <0-4>    Exit with code 1 when the gated score is below <n> (CI gate)
  --diff <file>        Compare against a baseline report (a previous --json output)
  --config <file>      Load scan configuration from a JSON file
  --scope <scopes>     Include global harness scopes: user, system (comma-separated)
  --gate <mode>        Score used for --min-level: maturity (repo-only, default) or effective
  --quiet              Suppress the terminal report
  --version            Print version
  --help               Show this help

Exit codes: 0 complete/pass, 1 complete scan below --min-level, 2 invalid usage or incomplete gated scan.

Configuration file (optional): .harness-score.json in the scan root.
See the guide: https://paladini.github.io/harness-score/guide/measure-and-improve

The scan is 100% deterministic: filesystem reads and parsing only.
No LLM calls, no network, no telemetry.

Guide: https://paladini.github.io/harness-score/
`;function A(e){let t={root:".",json:!1,md:null,badge:null,minLevel:null,diff:null,quiet:!1,configPath:null,scopeFlags:null,gate:null};for(let o=0;o<e.length;o+=1){let u=e[o];switch(u){case"--help":case"-h":process.stdout.write($),process.exit(0);break;case"--version":case"-v":process.stdout.write(`${v}
`),process.exit(0);break;case"--json":t.json=!0;break;case"--quiet":case"-q":t.quiet=!0;break;case"--md":t.md=e[++o]??"-";break;case"--badge":{let s=e[++o];if(!s)return n("--badge requires a file path");t.badge=s;break}case"--diff":{let s=e[++o];if(!s)return n("--diff requires a path to a baseline JSON report");t.diff=s;break}case"--config":{let s=e[++o];if(!s)return n("--config requires a file path");t.configPath=s;break}case"--scope":{let s=e[++o];if(!s)return n("--scope requires a comma-separated list (user, system)");try{t.scopeFlags=d(s)}catch(x){return n(String(x).replace(/^Error: /,""))}break}case"--gate":{let s=e[++o];if(s!=="maturity"&&s!=="effective")return n('--gate must be "maturity" or "effective"');t.gate=s;break}case"--min-level":{let s=Number(e[++o]);if(!Number.isInteger(s)||s<0||s>4)return n("--min-level must be an integer between 0 and 4");t.minLevel=s;break}default:if(u.startsWith("-"))return n(`Unknown option: ${u}

${$}`);t.root=u}}return t}function n(e){process.stderr.write(`harness-score: ${e}
`),process.exit(2)}function F(e){if(!e||typeof e!="object")return!1;let t=e,o=t.level;return typeof o=="object"&&o!==null&&typeof o.index=="number"&&Array.isArray(t.checks)&&Array.isArray(t.dimensions)&&typeof t.score=="object"&&t.score!==null}function q(e){return e.gate==="effective"?e.effective.level:e.level}function C(e){let t=["maturity"];return(e.gate==="effective"||e.scopes.effective.some(o=>o!=="repo"))&&t.push("effective"),t}function N(e){return C(e).filter(t=>!l(e,t))}function O(e,t){return l(e,e.gate)?t!==null&&q(e).index<t?1:0:2}var r=A(process.argv.slice(2)),c=R.resolve(r.root);(!a.existsSync(c)||!a.statSync(c).isDirectory())&&n(`not a directory: ${c}`);var L;try{L=m(c,{configPath:r.configPath,scopeFlags:r.scopeFlags,gate:r.gate})}catch(e){n(String(e).replace(/^Error: /,""))}var i=w(c,L),p=null,f=null;if(r.diff!==null){let e;try{e=JSON.parse(a.readFileSync(r.diff,"utf8"))}catch(t){n(`--diff: could not read/parse baseline report at ${r.diff}: ${String(t)}`)}F(e)||n(`--diff: ${r.diff} does not look like a harness-score report (expected the JSON output of a previous --json run).`),p=e,l(p,"maturity")||n("--diff: baseline maturity report is incomplete and cannot be compared."),l(i,"maturity")||n("--diff: current maturity report is incomplete and cannot be compared."),f=b(p,i)}if(r.json){let e=f?{current:i,baseline:p,diff:f}:i;process.stdout.write(`${JSON.stringify(e,null,2)}
`)}else r.quiet||process.stdout.write(`${k(i,f)}
`);if(r.md!==null){let e=S(i,f);r.md==="-"?process.stdout.write(e):(a.writeFileSync(r.md,e,"utf8"),r.quiet||process.stderr.write(`markdown report written to ${r.md}
`))}r.badge!==null&&(a.writeFileSync(r.badge,y(i),"utf8"),r.quiet||process.stderr.write(`badge written to ${r.badge}
`));var P=N(i);for(let e of P){let t=g(i,e).reasons.map(h).join("; ");process.stderr.write(`harness-score: ${e} scan is incomplete; no authoritative ${e} verdict is available${t?`: ${t}`:"."}
`)}var j=O(i,r.minLevel);j===2&&process.exit(2);if(j===1&&r.minLevel!==null){let e=q(i);process.stderr.write(`harness-score: ${i.gate} L${e.index} is below required L${r.minLevel} \u2014 missing: ${e.nextLevelGaps.join("; ")||"see failed checks"}
`),process.exit(1)}
