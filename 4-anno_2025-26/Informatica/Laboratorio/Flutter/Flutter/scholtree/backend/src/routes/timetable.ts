import { Router, Request, Response, NextFunction } from 'express';
import path from 'path';
import fs from 'fs';
import { CACHE_DIR } from '../config';
import db from '../db';

const router = Router();

const VALID_TYPES = ['class', 'room', 'teacher'];

function validateTypeCode(
  type: string,
  code: string,
  res: Response
): { sanitizedCode: string } | null {
  if (!VALID_TYPES.includes(type)) {
    res.status(400).json({ error: 'invalid type' });
    return null;
  }
  const sanitizedCode = code.replace(/[^a-zA-Z0-9_-]/g, '');
  if (!sanitizedCode) {
    res.status(400).json({ error: 'invalid code' });
    return null;
  }
  return { sanitizedCode };
}

router.get('/image/:type/:code', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const type = req.params.type as string;
    const code = req.params.code as string;
    const validated = validateTypeCode(type, code, res);
    if (!validated) return;
    const { sanitizedCode } = validated;

    const filePath = path.join(CACHE_DIR, 'img', type, `${sanitizedCode}.png`);
    const absPath = path.resolve(filePath);

    if (!fs.existsSync(absPath)) {
      res.status(404).json({ error: 'timetable not available' });
      return;
    }

    res.setHeader('Cache-Control', 'public, max-age=3600');
    res.sendFile(absPath);
  } catch (err) {
    next(err);
  }
});

router.get('/meta/:type/:code', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const type = req.params.type as string;
    const code = req.params.code as string;
    const validated = validateTypeCode(type, code, res);
    if (!validated) return;
    const { sanitizedCode } = validated;

    const row = await db('timetable_images').where({ resource_code: sanitizedCode }).first();
    if (!row) {
      res.status(404).json({ error: 'timetable not available' });
      return;
    }

    const resource = await db('resources').where({ code: sanitizedCode }).first();

    res.json({
      image_url: `/api/timetable/image/${type}/${sanitizedCode}`,
      last_updated: row.cached_at,
      school_year: resource?.school_year ?? '2025-26',
    });
  } catch (err) {
    next(err);
  }
});

router.get('/classes', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const limit = Math.min(Number(req.query.limit) || 50, 200);
    const offset = Math.max(Number(req.query.offset) || 0, 0);

    const [data, countResult] = await Promise.all([
      db('resources').where({ type: 'class', active: 1, school_year: '2025-26' }).limit(limit).offset(offset),
      db('resources').where({ type: 'class', active: 1, school_year: '2025-26' }).count('id as count').first(),
    ]);

    const total = Number((countResult as { count: number })?.count ?? 0);
    res.json({ data, total, limit, offset });
  } catch (err) {
    next(err);
  }
});

router.get('/rooms', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const limit = Math.min(Number(req.query.limit) || 50, 200);
    const offset = Math.max(Number(req.query.offset) || 0, 0);

    const [data, countResult] = await Promise.all([
      db('resources').where({ type: 'room', active: 1, school_year: '2025-26' }).limit(limit).offset(offset),
      db('resources').where({ type: 'room', active: 1, school_year: '2025-26' }).count('id as count').first(),
    ]);

    const total = Number((countResult as { count: number })?.count ?? 0);
    res.json({ data, total, limit, offset });
  } catch (err) {
    next(err);
  }
});

export default router;
