CREATE TABLE IF NOT EXISTS jobs (
  id BIGSERIAL PRIMARY KEY,
  job_id VARCHAR(128) NOT NULL UNIQUE,
  raw_job_title VARCHAR(255),
  job_title VARCHAR(255),
  normalized_job_title VARCHAR(255),
  company VARCHAR(255),
  location VARCHAR(255),
  city VARCHAR(128),
  country VARCHAR(128),
  employment_type VARCHAR(64),
  experience_level VARCHAR(64),
  salary_min NUMERIC,
  salary_max NUMERIC,
  salary_currency VARCHAR(16),
  job_description TEXT,
  skills_raw TEXT,
  category VARCHAR(128),
  industry VARCHAR(128),
  remote_type VARCHAR(64),
  posted_date DATE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS normalized_skills (
  id BIGSERIAL PRIMARY KEY,
  skill_name VARCHAR(128) UNIQUE NOT NULL,
  normalized_name VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS job_skills (
  id BIGSERIAL PRIMARY KEY,
  job_pk BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
  skill_name VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS resume_analyses (
  id BIGSERIAL PRIMARY KEY,
  original_filename VARCHAR(255) NOT NULL,
  extracted_text TEXT NOT NULL,
  extracted_skills_json JSONB NOT NULL,
  top_roles_json JSONB NOT NULL,
  skill_gap_json JSONB NOT NULL,
  match_score NUMERIC NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_jobs_normalized_job_title ON jobs(normalized_job_title);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_country ON jobs(country);
CREATE INDEX IF NOT EXISTS idx_jobs_city ON jobs(city);
CREATE INDEX IF NOT EXISTS idx_jobs_category ON jobs(category);
CREATE INDEX IF NOT EXISTS idx_jobs_industry ON jobs(industry);
CREATE INDEX IF NOT EXISTS idx_jobs_experience_level ON jobs(experience_level);
CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date);
CREATE INDEX IF NOT EXISTS idx_job_skills_job_pk ON job_skills(job_pk);
CREATE INDEX IF NOT EXISTS idx_job_skills_skill_name ON job_skills(skill_name);
