import {
  parseRessourceJs,
  parseGrilleJs,
  parsePeriodeJs,
  parseSignature,
} from '../../scrapers/parse-ressource';

describe('parseRessourceJs', () => {
  it('returns 3 items from 3 valid Ressource calls', () => {
    const raw = `
      new Ressource("c0000001", "IND", "1A", "1", "", 1, 1, 1)
      new Ressource("c0000002", "PROF", "Rossi", "2", "", 1, 1, 1)
      new Ressource("c0000003", "AULA", "Lab", "3", "", 1, 1, 1)
    `;
    const result = parseRessourceJs(raw);
    expect(result).toHaveLength(3);
    expect(result[0]).toEqual({ code: 'c0000001', type: 'IND', name: '1A' });
    expect(result[1]).toEqual({ code: 'c0000002', type: 'PROF', name: 'Rossi' });
    expect(result[2]).toEqual({ code: 'c0000003', type: 'AULA', name: 'Lab' });
  });

  it('handles single-quoted args', () => {
    const raw = `new Ressource('c0000001', 'IND', '1A', '1', '', 1, 1, 1)`;
    const result = parseRessourceJs(raw);
    expect(result).toHaveLength(1);
    expect(result[0]).toEqual({ code: 'c0000001', type: 'IND', name: '1A' });
  });

  it('returns [] for empty string', () => {
    expect(parseRessourceJs('')).toEqual([]);
  });

  it('returns [] for malformed input with no Ressource calls', () => {
    expect(parseRessourceJs('var x = 42; console.log(x);')).toEqual([]);
  });

  it('returns [] for vm.Script injection — no execution', () => {
    expect(parseRessourceJs("new vm.Script('malicious')")).toEqual([]);
  });
});

describe('parseGrilleJs', () => {
  it('parses grid code from Ressource call', () => {
    const raw = `new Ressource('g001', 'GRID1', 'extra')`;
    const result = parseGrilleJs(raw);
    expect(result).toHaveLength(1);
    expect(result[0]).toEqual({ code: 'g001', gridCode: 'GRID1' });
  });

  it('returns [] for empty string', () => {
    expect(parseGrilleJs('')).toEqual([]);
  });
});

describe('parsePeriodeJs', () => {
  it('maps resourceCode and grillCode', () => {
    const raw = `new Ressource('c0000001', 'GRID_A', 'extra')`;
    const result = parsePeriodeJs(raw);
    expect(result).toHaveLength(1);
    expect(result[0]).toEqual({ resourceCode: 'c0000001', grillCode: 'GRID_A' });
  });
});

describe('parseSignature', () => {
  it('trims whitespace', () => {
    expect(parseSignature('  sig_12345  ')).toBe('sig_12345');
  });

  it('returns empty string for empty input', () => {
    expect(parseSignature('')).toBe('');
  });
});
