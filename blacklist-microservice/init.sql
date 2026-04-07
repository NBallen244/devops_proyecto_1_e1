-- Initialization script for blacklist database
-- This script runs automatically when the PostgreSQL container starts

-- Create database if it doesn't exist (handled by POSTGRES_DB environment variable)
-- CREATE DATABASE blacklist_db;

-- Connect to the blacklist database
\c blacklist_db;

-- Create extension for UUID generation if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions to the application user
GRANT ALL PRIVILEGES ON DATABASE blacklist_db TO blacklist_user;
GRANT ALL ON SCHEMA public TO blacklist_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO blacklist_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO blacklist_user;

-- The application will create its tables automatically via SQLAlchemy
-- This script just ensures proper permissions and extensions