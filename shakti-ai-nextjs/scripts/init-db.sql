-- Initialize database tables for SHAKTI-AI authentication

-- Create users table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Insert a test user (password is 'test123')
INSERT INTO users (name, email, password) 
VALUES ('Test User', 'test@example.com', '$2a$12$6gHIqPjUyMWH4ZEEqV.AYu8ZnAhN6V.aAqGVlI.1QmJe2v/8w.lKC')
ON CONFLICT (email) DO NOTHING;
