import fs from 'fs';
import path from 'path';
import https from 'https';
import { CACHE_DIR } from '../config';
import { parseRessourceJs, parseSignature } from './parse-ressource';
import db from '../db';

const BASE_URL = 'https://dati.itis.pr.it/orariodiurno';
const SCHOOL_YEAR = '2025-26';

function fetchText(url: string): Promise<string> {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode} for ${url}`));
        res.resume();
        return;
      }
      const chunks: Buffer[] = [];
      res.on('data', (c: Buffer) => chunks.push(c));
      res.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
      res.on('error', reject);
    }).on('error', reject);
  });
}

function fetchBinary(url: string): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode} for ${url}`));
        res.resume();
        return;
      }
      const chunks: Buffer[] = [];
      res.on('data', (c: Buffer) => chunks.push(c));
      res.on('end', () => resolve(Buffer.concat(chunks)));
      res.on('error', reject);
    }).on('error', reject);
  });
}

function savePng(buffer: Buffer, type: 'classi' | 'aule', code: string): string {
  const safeCode = code.replace(/[^a-zA-Z0-9_-]/g, '');
  if (!safeCode) throw new Error(`invalid code: ${code}`);
  const dir = path.join(CACHE_DIR, 'img', type);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, `${safeCode}.png`), buffer);
  return `img/${type}/${safeCode}.png`;
}

export async function runPublicScraper(): Promise<void> {
  const sigRaw = await fetchText(`${BASE_URL}/js_to_replace/_signature.js`);
  const newSig = parseSignature(sigRaw);

  const last = await db('scrape_log').where({ source: 'public' }).orderBy('id', 'desc').first();
  if (last && last.signature === newSig) {
    console.log('public scraper: signature unchanged, skip');
    return;
  }

  const startedAt = new Date();
  let itemsCount = 0;
  let failedImages = 0;

  try {
    const ressourceRaw = await fetchText(`${BASE_URL}/js_to_replace/_ressource.js`);
    const resources = parseRessourceJs(ressourceRaw).filter(r => r.type === 'IND');

    for (const r of resources) {
      const resType = r.code.startsWith('c') ? 'class' : 'room';
      await db('resources')
        .insert({ type: resType, code: r.code, name: r.name, school_year: SCHOOL_YEAR })
        .onConflict(['type', 'code', 'school_year'])
        .merge();
      itemsCount++;
    }

    for (const r of resources) {
      const resType = r.code.startsWith('c') ? 'class' : 'room';
      const imgType = resType === 'class' ? 'classi' : 'aule';
      try {
        const buf = await fetchBinary(`${BASE_URL}/img/${imgType}/${r.code}.png`);
        const cachePath = savePng(buf, imgType, r.code);
        await db('timetable_images')
          .insert({ resource_code: r.code, cache_path: cachePath })
          .onConflict(['resource_code'])
          .merge();
      } catch (err) {
        console.error(`public scraper: image failed for ${r.code}:`, err);
        failedImages++;
      }
    }

    await db('scrape_log').insert({
      source: 'public',
      status: failedImages > 0 ? 'partial' : 'ok',
      started_at: startedAt,
      completed_at: new Date(),
      items_count: itemsCount,
      signature: newSig,
    });
  } catch (err) {
    await db('scrape_log').insert({
      source: 'public',
      status: 'error',
      started_at: startedAt,
      completed_at: new Date(),
      items_count: itemsCount,
      errors: err instanceof Error ? err.message : String(err),
      signature: newSig,
    });
    throw err;
  }
}

export async function checkAndScrape(): Promise<void> {
  await runPublicScraper();
}
