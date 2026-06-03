import net from 'net';
import { LDAP_URL } from '../config';
import db from '../db';

export interface HealthStatus {
  status: 'ok' | 'degraded';
  uptime: number;
  ldap: {
    connected: boolean;
    last_sync: string | null;
  };
  scrape: {
    public: { status: string | null; last_run: string | null; items: number | null };
    private: { status: string | null; last_run: string | null; error: string | null };
  };
  db: {
    resources: number;
    users: number;
  };
}

export async function isLdapReachable(): Promise<boolean> {
  return new Promise((resolve) => {
    const url = new URL(LDAP_URL);
    const socket = net.createConnection(
      { host: url.hostname, port: parseInt(url.port || '389'), timeout: 2000 },
      () => { socket.destroy(); resolve(true); }
    );
    socket.on('timeout', () => { socket.destroy(); resolve(false); });
    socket.on('error', () => resolve(false));
  });
}

export async function getHealthStatus(): Promise<HealthStatus> {
  const [pubLog, privLog, ldapLog, resourcesRow, usersRow, ldapReachable] = await Promise.all([
    db('scrape_log').where('source', 'public').orderBy('id', 'desc').first(),
    db('scrape_log').where('source', 'private').orderBy('id', 'desc').first(),
    db('scrape_log').where('source', 'ldap').orderBy('id', 'desc').first(),
    db('resources').count('* as n').first(),
    db('users').count('* as n').first(),
    isLdapReachable(),
  ]);

  const pubOk = pubLog?.status === 'ok';

  return {
    status: ldapReachable && pubOk ? 'ok' : 'degraded',
    uptime: process.uptime(),
    ldap: {
      connected: ldapReachable,
      last_sync: ldapLog?.completed_at ?? null,
    },
    scrape: {
      public: {
        status: pubLog?.status ?? null,
        last_run: pubLog?.completed_at ?? null,
        items: pubLog?.items_count ?? null,
      },
      private: {
        status: privLog?.status ?? null,
        last_run: privLog?.completed_at ?? null,
        error: privLog?.errors ?? null,
      },
    },
    db: {
      resources: Number(resourcesRow?.n ?? 0),
      users: Number(usersRow?.n ?? 0),
    },
  };
}
