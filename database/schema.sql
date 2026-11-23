-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Historical Incidents Table
CREATE TABLE IF NOT EXISTS incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_number VARCHAR(50) NOT NULL UNIQUE,
    service_name VARCHAR(100) NOT NULL,
    error_signature VARCHAR(255) NOT NULL,
    root_cause TEXT NOT NULL,
    remediation_steps TEXT NOT NULL,
    ssm_runbook VARCHAR(100),
    postmortem_summary TEXT NOT NULL,
    
    -- Lexical Search Vector (BM25 / GIN Index)
    tsv_content tsvector GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(error_signature, '') || ' ' || coalesce(root_cause, '') || ' ' || coalesce(postmortem_summary, ''))
    ) STORED,

    -- Semantic Search Vector (Titan Text Embeddings v2: 1024 dimensions)
    embedding vector(1024),

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Indices for Hybrid Search Performance
CREATE INDEX IF NOT EXISTS idx_incidents_tsv ON incidents USING GIN (tsv_content);
CREATE INDEX IF NOT EXISTS idx_incidents_hnsw ON incidents USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);
CREATE INDEX IF NOT EXISTS idx_incidents_service ON incidents (service_name);
