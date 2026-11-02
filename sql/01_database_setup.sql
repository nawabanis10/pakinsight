-- PakInsight Database Setup

CREATE DATABASE IF NOT EXISTS pakinsight;

USE pakinsight;

-- Verify database
SELECT DATABASE();

-- Display available tables
SHOW TABLES;

-- Check sample records
SELECT * FROM weather_data LIMIT 5;

SELECT * FROM cost_of_living LIMIT 5;

SELECT * FROM economic_summary LIMIT 5;

SELECT * FROM economic_categories LIMIT 6;