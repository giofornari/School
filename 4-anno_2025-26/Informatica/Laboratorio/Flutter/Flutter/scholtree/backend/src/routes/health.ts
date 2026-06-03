import { Router, Request, Response } from 'express';
import { getHealthStatus } from '../services/health';

const router = Router();

router.get('/health', async (req: Request, res: Response) => {
  const status = await getHealthStatus();
  res.json(status);
});

export default router;
