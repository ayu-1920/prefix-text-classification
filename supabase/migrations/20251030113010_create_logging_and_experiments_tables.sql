/*
  # Create Logging and Experiments Tables

  ## Overview
  This migration creates tables for storing experiment results and system logs,
  enabling complete tracking of ML experiments and error monitoring.

  ## New Tables
  
  ### `experiments`
  Stores ML experiment results with full metrics and metadata
  - `id` (uuid, primary key) - Unique experiment identifier
  - `dataset_id` (text) - Dataset used (imdb, news)
  - `model_id` (text) - Model used (logistic, naive_bayes, svm)
  - `prefix_length` (integer) - Number of tokens used for prefix
  - `full_text_metrics` (jsonb) - Full text performance metrics
  - `prefix_metrics` (jsonb) - Prefix performance metrics
  - `performance_retention` (numeric) - Percentage of performance retained
  - `dataset_size` (integer) - Total dataset size
  - `train_size` (integer) - Training set size
  - `test_size` (integer) - Test set size
  - `label_names` (jsonb) - Array of label names
  - `plots` (jsonb) - Base64 encoded plot images
  - `created_at` (timestamptz) - Experiment timestamp

  ### `error_logs`
  Stores system errors and execution logs for debugging
  - `id` (uuid, primary key) - Unique log identifier
  - `source` (text) - Source of log (frontend, backend)
  - `level` (text) - Log level (info, warning, error, critical)
  - `message` (text) - Log message
  - `details` (jsonb) - Additional error details and context
  - `stack_trace` (text) - Stack trace for errors
  - `user_agent` (text) - Browser user agent (for frontend logs)
  - `created_at` (timestamptz) - Log timestamp

  ## Security
  - Enable RLS on both tables
  - Allow public read access for experiments (demo purposes)
  - Allow public insert access for experiments (demo purposes)
  - Allow public insert access for logs (demo purposes)
  - In production, these policies should be restricted to authenticated users
*/

-- Create experiments table
CREATE TABLE IF NOT EXISTS experiments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  dataset_id text NOT NULL,
  model_id text NOT NULL,
  prefix_length integer NOT NULL,
  full_text_metrics jsonb NOT NULL,
  prefix_metrics jsonb NOT NULL,
  performance_retention numeric NOT NULL,
  dataset_size integer NOT NULL,
  train_size integer NOT NULL,
  test_size integer NOT NULL,
  label_names jsonb NOT NULL,
  plots jsonb,
  created_at timestamptz DEFAULT now()
);

-- Create error_logs table
CREATE TABLE IF NOT EXISTS error_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source text NOT NULL CHECK (source IN ('frontend', 'backend')),
  level text NOT NULL CHECK (level IN ('info', 'warning', 'error', 'critical')),
  message text NOT NULL,
  details jsonb,
  stack_trace text,
  user_agent text,
  created_at timestamptz DEFAULT now()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_experiments_created_at ON experiments(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_experiments_dataset_model ON experiments(dataset_id, model_id);
CREATE INDEX IF NOT EXISTS idx_error_logs_created_at ON error_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_error_logs_source ON error_logs(source);
CREATE INDEX IF NOT EXISTS idx_error_logs_level ON error_logs(level);

-- Enable RLS
ALTER TABLE experiments ENABLE ROW LEVEL SECURITY;
ALTER TABLE error_logs ENABLE ROW LEVEL SECURITY;

-- Create policies for experiments (public for demo)
CREATE POLICY "Anyone can view experiments"
  ON experiments FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Anyone can insert experiments"
  ON experiments FOR INSERT
  TO anon
  WITH CHECK (true);

-- Create policies for error_logs (public for demo)
CREATE POLICY "Anyone can view logs"
  ON error_logs FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "Anyone can insert logs"
  ON error_logs FOR INSERT
  TO anon
  WITH CHECK (true);