import { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
  await knex.schema.raw(`
    CREATE TABLE IF NOT EXISTS resources (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      type        TEXT NOT NULL CHECK(type IN ('class', 'room', 'teacher')),
      code        TEXT NOT NULL,
      name        TEXT NOT NULL,
      cache_path  TEXT,
      school_year TEXT NOT NULL DEFAULT '2025-26',
      active      INTEGER NOT NULL DEFAULT 1,
      updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  await knex.schema.raw(`CREATE INDEX IF NOT EXISTS idx_resources_type_code ON resources(type, code)`);
  await knex.schema.raw(`CREATE UNIQUE INDEX IF NOT EXISTS idx_resources_type_code_year ON resources(type, code, school_year)`);

  await knex.schema.raw(`
    CREATE TABLE IF NOT EXISTS timetable_images (
      id             INTEGER PRIMARY KEY AUTOINCREMENT,
      resource_code  TEXT NOT NULL,
      cache_path     TEXT NOT NULL,
      last_modified  TEXT,
      cached_at      DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  await knex.schema.raw(`CREATE UNIQUE INDEX IF NOT EXISTS idx_timetable_images_code ON timetable_images(resource_code)`);

  await knex.schema.raw(`
    CREATE TABLE IF NOT EXISTS users (
      id                    INTEGER PRIMARY KEY AUTOINCREMENT,
      ldap_uid              TEXT UNIQUE,
      email                 TEXT,
      name                  TEXT NOT NULL,
      role                  TEXT NOT NULL CHECK(role IN ('student', 'teacher', 'staff', 'admin')),
      password_hash         TEXT,
      teacher_resource_code TEXT,
      department            TEXT,
      class_name            TEXT,
      school_year           TEXT NOT NULL DEFAULT '2025-26',
      active                INTEGER NOT NULL DEFAULT 1,
      last_sync             DATETIME,
      created_at            DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  await knex.schema.raw(`CREATE UNIQUE INDEX IF NOT EXISTS idx_users_ldap_uid ON users(ldap_uid)`);
  await knex.schema.raw(`CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)`);
  await knex.schema.raw(`CREATE INDEX IF NOT EXISTS idx_users_class ON users(class_name)`);

  await knex.schema.raw(`
    CREATE TABLE IF NOT EXISTS substitutions (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      date         TEXT NOT NULL,
      hour_start   INTEGER NOT NULL,
      hour_end     INTEGER NOT NULL,
      teacher_id   INTEGER REFERENCES users(id),
      class_id     INTEGER,
      subject      TEXT,
      room         TEXT,
      notes        TEXT,
      created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(date, hour_start, teacher_id, class_id)
    )
  `);
  await knex.schema.raw(`CREATE INDEX IF NOT EXISTS idx_substitutions_date ON substitutions(date)`);

  await knex.schema.raw(`
    CREATE TABLE IF NOT EXISTS teacher_map (
      timetable_code TEXT PRIMARY KEY,
      ldap_uid       TEXT,
      display_name   TEXT,
      confidence     TEXT CHECK(confidence IN ('auto', 'manual')) DEFAULT 'auto',
      confirmed_at   DATETIME
    )
  `);

  await knex.schema.raw(`
    CREATE TABLE IF NOT EXISTS scrape_log (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      source       TEXT NOT NULL CHECK(source IN ('public', 'private', 'ldap')),
      status       TEXT NOT NULL CHECK(status IN ('ok', 'partial', 'error')),
      started_at   DATETIME NOT NULL,
      completed_at DATETIME,
      items_count  INTEGER,
      errors       TEXT,
      signature    TEXT
    )
  `);

  await knex.schema.raw(`
    CREATE TABLE IF NOT EXISTS revoked_tokens (
      jti        TEXT PRIMARY KEY,
      revoked_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
}

export async function down(knex: Knex): Promise<void> {
  await knex.schema.dropTableIfExists('revoked_tokens');
  await knex.schema.dropTableIfExists('scrape_log');
  await knex.schema.dropTableIfExists('teacher_map');
  await knex.schema.dropTableIfExists('substitutions');
  await knex.schema.dropTableIfExists('users');
  await knex.schema.dropTableIfExists('timetable_images');
  await knex.schema.dropTableIfExists('resources');
}
