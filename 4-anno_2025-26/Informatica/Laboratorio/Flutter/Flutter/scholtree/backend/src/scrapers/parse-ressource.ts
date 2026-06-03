export interface ParsedResource {
  code: string;
  type: string;
  name: string;
}

export interface ParsedGrille {
  code: string;
  gridCode: string;
}

export interface ParsedPeriode {
  resourceCode: string;
  grillCode: string;
}

const RESSOURCE_RE = /new\s+Ressource\s*\(([^)]+)\)/g;

function parseArgs(raw: string): string[] {
  return raw.split(',').map(s => s.trim().replace(/^['"]|['"]$/g, ''));
}

export function parseRessourceJs(raw: string): ParsedResource[] {
  const out: ParsedResource[] = [];
  for (const m of raw.matchAll(RESSOURCE_RE)) {
    const a = parseArgs(m[1]);
    if (a.length >= 3) out.push({ code: a[0], type: a[1], name: a[2] });
  }
  return out;
}

export function parseGrilleJs(raw: string): ParsedGrille[] {
  const out: ParsedGrille[] = [];
  for (const m of raw.matchAll(RESSOURCE_RE)) {
    const a = parseArgs(m[1]);
    if (a.length >= 2) out.push({ code: a[0], gridCode: a[1] });
  }
  return out;
}

export function parsePeriodeJs(raw: string): ParsedPeriode[] {
  const out: ParsedPeriode[] = [];
  for (const m of raw.matchAll(RESSOURCE_RE)) {
    const a = parseArgs(m[1]);
    if (a.length >= 2) out.push({ resourceCode: a[0], grillCode: a[1] });
  }
  return out;
}

export function parseSignature(raw: string): string {
  return raw.trim();
}
