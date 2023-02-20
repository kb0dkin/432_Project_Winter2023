\c pg

-- Requirement 1
SELECT 'CREATE DATABASE req_1'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'req_1')\gexec


-- Requirement 2
SELECT 'CREATE DATABASE req_2'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'req_2')\gexec


-- Requirement 3
SELECT 'CREATE DATABASE req_3'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'req_3')\gexec


-- Requirement 4
SELECT 'CREATE DATABASE req_4'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'req_4')\gexec


-- Requirement 5
SELECT 'CREATE DATABASE req_5'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'req_5')\gexec


-- Requirement 6
SELECT 'CREATE DATABASE req_6'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'req_6')\gexec


