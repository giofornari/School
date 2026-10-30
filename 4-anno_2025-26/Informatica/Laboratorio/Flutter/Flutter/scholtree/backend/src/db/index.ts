import knex from 'knex';
import path from 'path';
import { DB_PATH } from '../config';

const db = knex({
  client: 'better-sqlite3',
  connection: {
    filename: path.resolve(DB_PATH),
  },
  useNullAsDefault: true,
});

export type DB = typeof db;
export default db;
