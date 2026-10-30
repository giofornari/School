import { Router, Request, Response, NextFunction } from 'express';
import db from '../db';

const router = Router();

router.get('/teachers', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const limit = Math.min(parseInt(req.query.limit as string) || 50, 200);
    const offset = parseInt(req.query.offset as string) || 0;

    const [data, countResult] = await Promise.all([
      db('users')
        .where({ role: 'teacher', active: 1, school_year: '2025-26' })
        .select('id', 'ldap_uid', 'name', 'role', 'department', 'teacher_resource_code', 'email')
        .limit(limit)
        .offset(offset),
      db('users')
        .where({ role: 'teacher', active: 1, school_year: '2025-26' })
        .count('id as total')
        .first(),
    ]);

    const total = Number((countResult as { total: number } | undefined)?.total ?? 0);
    res.json({ data, total, limit, offset });
  } catch (err) {
    next(err);
  }
});

router.get('/search', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const q = (req.query.q as string) || '';
    const role = req.query.role as string | undefined;
    const limit = Math.min(parseInt(req.query.limit as string) || 20, 100);
    const offset = parseInt(req.query.offset as string) || 0;

    if (!q || q.length < 2) {
      res.status(400).json({ error: 'query must be at least 2 characters' });
      return;
    }

    let query = db('users')
      .whereNot({ role: 'admin' })
      .where(function () {
        this.where('name', 'like', `%${q}%`).orWhere('ldap_uid', 'like', `%${q}%`);
      });

    if (role) {
      query = query.andWhere({ role });
    }

    const [data, countResult] = await Promise.all([
      query.clone()
        .select('id', 'ldap_uid', 'name', 'role', 'department', 'class_name', 'email', 'teacher_resource_code')
        .limit(limit)
        .offset(offset),
      query.clone().count('id as total').first(),
    ]);

    const total = Number((countResult as { total: number } | undefined)?.total ?? 0);
    res.json({ data, total, limit, offset, query: q });
  } catch (err) {
    next(err);
  }
});

router.get('/users/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.status(400).json({ error: 'invalid id' });
      return;
    }

    const user = await db('users')
      .where({ id, active: 1 })
      .select('id', 'ldap_uid', 'name', 'role', 'department', 'class_name', 'email', 'teacher_resource_code')
      .first();

    if (!user) {
      res.status(404).json({ error: 'user not found' });
      return;
    }

    res.json(user);
  } catch (err) {
    next(err);
  }
});

export default router;
