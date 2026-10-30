import dotenv from 'dotenv';
dotenv.config();

export const PORT = parseInt(process.env.PORT ?? '3000', 10);
export const NODE_ENV = process.env.NODE_ENV ?? 'development';

const jwtSecret = process.env.JWT_SECRET ?? '';
if (!jwtSecret || jwtSecret.length < 32) {
  throw new Error('JWT_SECRET missing or too short — minimum 32 characters');
}
export const JWT_SECRET: string = jwtSecret;

export const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN ?? '8h';
export const DB_PATH = process.env.DB_PATH ?? './data/scholtree.db';
export const CACHE_DIR = process.env.CACHE_DIR ?? './cache';
export const UPLOAD_DIR = process.env.UPLOAD_DIR ?? './uploads';
export const NTLM_USER = process.env.NTLM_USER ?? '';
export const NTLM_PASS = process.env.NTLM_PASS ?? '';
export const NTLM_DOMAIN = process.env.NTLM_DOMAIN ?? 'ITIS';
export const LDAP_URL = process.env.LDAP_URL ?? 'ldap://192.168.64.26:389';
export const LDAP_BASE_DN = process.env.LDAP_BASE_DN ?? 'DC=itis,DC=pr,DC=it';

const ACCOUNT_EXPIRY = new Date('2026-07-15');
if (new Date() > ACCOUNT_EXPIRY) {
  console.warn('⚠ Service account may be expired — check LDAP/NTLM connectivity');
}
