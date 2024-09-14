import { config } from "dotenv";
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    clearMocks: true,
    globals: true,
    env: {
      ...config({ path: "./.env.development" }).parsed,
    }
  }
});
