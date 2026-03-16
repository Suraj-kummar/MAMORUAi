import { config } from "dotenv";
import { defineConfig } from "prisma/config";

// Load environment variables
config({ path: ".env" });

export default defineConfig({
    schema: "prisma/schema.prisma",
    migrations: {
        path: "prisma/migrations",
    },
    datasource: {
        url: process.env.DATABASE_URL || "postgresql://postgres:postgres@localhost:5432/mamoruai",
    },
});
