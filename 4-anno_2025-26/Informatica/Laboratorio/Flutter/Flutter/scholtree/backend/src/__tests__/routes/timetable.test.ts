jest.mock('../../db', () => {
  const qb: any = {
    where: jest.fn().mockReturnThis(),
    limit: jest.fn().mockReturnThis(),
    offset: jest.fn().mockResolvedValue([]),
    count: jest.fn().mockReturnThis(),
    first: jest.fn().mockResolvedValue({ count: 0 }),
  };
  return { __esModule: true, default: jest.fn(() => qb) };
});

jest.mock('../../config', () => ({
  CACHE_DIR: '/tmp/scholtree-test-cache',
}));

import express from 'express';
import request from 'supertest';
import timetableRouter from '../../routes/timetable';

const app = express();
app.use(express.json());
app.use('/timetable', timetableRouter);

describe('GET /timetable/image/:type/:code', () => {
  it('returns 400 invalid code when code sanitizes to empty (special chars)', async () => {
    const res = await request(app).get('/timetable/image/class/%21%21%21');
    expect(res.status).toBe(400);
    expect(res.body).toEqual({ error: 'invalid code' });
  });

  it('returns 400 invalid type for unknown type', async () => {
    const res = await request(app).get('/timetable/image/invalid/c0000001');
    expect(res.status).toBe(400);
    expect(res.body).toEqual({ error: 'invalid type' });
  });

  it('returns 404 timetable not available when file missing', async () => {
    const res = await request(app).get('/timetable/image/class/c0000001');
    expect(res.status).toBe(404);
    expect(res.body).toEqual({ error: 'timetable not available' });
  });
});

describe('GET /timetable/classes', () => {
  it('returns 200 with empty data and total 0', async () => {
    const res = await request(app).get('/timetable/classes');
    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({
      data: [],
      total: 0,
      limit: 50,
      offset: 0,
    });
  });
});
