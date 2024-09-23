CREATE TABLE IF NOT EXISTS users (
  user_id    BIGSERIAL PRIMARY KEY,
  email      TEXT UNIQUE NOT NULL,
  first_name VARCHAR,
  last_name  VARCHAR,
  created    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_authentication (
  auth_id  BIGSERIAL PRIMARY KEY,
  user_id  BIGINT references users(user_id),
  password VARCHAR,
  created  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Seed DB with test user
INSERT INTO users (email, first_name, last_name)
VALUES ('test_user@test.com', 'test', 'user');

INSERT INTO user_authentication (user_id, password)
VALUES (1, 'test');
