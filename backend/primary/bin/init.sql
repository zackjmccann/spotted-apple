CREATE TABLE IF NOT EXISTS users (
  user_id  BIGSERIAL PRIMARY KEY,
  email    TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  created  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS access_tokens (
  access_token_id VARCHAR PRIMARY KEY,
  account         VARCHAR,
  user_id         BIGINT references users(user_id),
  access_token    VARCHAR,
  token_type      VARCHAR,
  scope           VARCHAR,
  expiration_time TIMESTAMPTZ NOT NULL,
  refresh_token   VARCHAR,
  created         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
