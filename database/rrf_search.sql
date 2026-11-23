-- Reciprocal Rank Fusion (RRF) Hybrid Search Function
-- Combines BM25 Full-Text Search (GIN) with Cosine Vector Search (HNSW)
-- Constant k = 60 prevents high rankings from overly dominating the fused score.

CREATE OR REPLACE FUNCTION search_incidents_hybrid(
    query_text TEXT,
    query_vector vector(1024),
    match_count INT DEFAULT 5,
    rrf_k INT DEFAULT 60
)
RETURNS TABLE (
    id UUID,
    incident_number VARCHAR(50),
    service_name VARCHAR(100),
    error_signature VARCHAR(255),
    root_cause TEXT,
    remediation_steps TEXT,
    ssm_runbook VARCHAR(100),
    lexical_rank BIGINT,
    semantic_rank BIGINT,
    rrf_score DOUBLE PRECISION
)
LANGUAGE sql
AS $$
WITH lexical_search AS (
    SELECT 
        i.id,
        ROW_NUMBER() OVER (ORDER BY ts_rank_cd(i.tsv_content, plainto_tsquery('english', query_text)) DESC) AS rank
    FROM incidents i
    WHERE i.tsv_content @@ plainto_tsquery('english', query_text)
    LIMIT match_count * 2
),
semantic_search AS (
    SELECT 
        i.id,
        ROW_NUMBER() OVER (ORDER BY i.embedding <=> query_vector ASC) AS rank
    FROM incidents i
    WHERE i.embedding IS NOT NULL
    LIMIT match_count * 2
),
fused_scores AS (
    SELECT 
        coalesce(l.id, s.id) AS id,
        l.rank AS lexical_rank,
        s.rank AS semantic_rank,
        (coalesce(1.0 / (rrf_k + l.rank), 0.0) + coalesce(1.0 / (rrf_k + s.rank), 0.0)) AS rrf_score
    FROM lexical_search l
    FULL OUTER JOIN semantic_search s ON l.id = s.id
)
SELECT 
    i.id,
    i.incident_number,
    i.service_name,
    i.error_signature,
    i.root_cause,
    i.remediation_steps,
    i.ssm_runbook,
    f.lexical_rank,
    f.semantic_rank,
    f.rrf_score
FROM fused_scores f
JOIN incidents i ON i.id = f.id
ORDER BY f.rrf_score DESC
LIMIT match_count;
$$;
