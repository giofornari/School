import type { Knex } from 'knex';
import path from 'path';
import dotenv from 'dotenv';

dotenv.config();

const config: Record<string, Knex.Config> = {
  development: {
    client: 'better-sqlite3',
    connection: {
      filename: process.env.DB_PATH ?? path.resolve('./data/scholtree.db'),
    },
    useNullAsDefault: true,
    migrations: {
      directory: path.resolve('./src/db/migrations'),
      extension: 'ts',
    },
    seeds: {
      directory: path.resolve('./src/db/seeds'),
    },
  },
  production: {
    client: 'better-sqlite3',
    connection: {
      filename: process.env.DB_PATH ?? path.resolve('./data/scholtree.db'),
    },
    useNullAsDefault: true,
    migrations: {
      directory: path.resolve('./src/db/migrations'),
      extension: 'ts',
    },
    seeds: {
      directory: path.resolve('./src/db/seeds'),
    },
  },
};

export default config;
