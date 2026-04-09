-- Drop existing table if it exists to ensure clean schema
DROP TABLE IF EXISTS messages;

-- Create messages table with correct schema
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on created_at for better query performance
CREATE INDEX idx_messages_created_at ON messages(created_at DESC);

DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully for CICD application';
    RAISE NOTICE 'Messages table created with created_at column';
END $$;