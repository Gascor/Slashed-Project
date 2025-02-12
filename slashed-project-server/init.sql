-- Créer les rôles avec des privilèges spécifiques
CREATE ROLE guest;
CREATE ROLE user;
CREATE ROLE moderator;
CREATE ROLE administrator;
CREATE ROLE owner;

-- Créer l'utilisateur guest_user avec le rôle guest
CREATE USER guest_user WITH PASSWORD 'guest_password';
GRANT guest TO guest_user;

-- Créer la base de données
CREATE DATABASE slashed_project;

-- Attribuer les privilèges de connexion à tous les rôles sur la base de données
GRANT CONNECT ON DATABASE slashed_project TO guest;
GRANT CONNECT ON DATABASE slashed_project TO user;
GRANT CONNECT ON DATABASE slashed_project TO moderator;
GRANT CONNECT ON DATABASE slashed_project TO administrator;
GRANT CONNECT ON DATABASE slashed_project TO owner;

-- Connexion à la base de données
\c slashed_project;

-- Créer la table news
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Créer la table users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Créer la table profiles
CREATE TABLE profiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    avatar_url VARCHAR(255),
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Créer la table login_logs
CREATE TABLE login_logs (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Créer la table attachments
CREATE TABLE attachments (
    id SERIAL PRIMARY KEY,
    entity_id INTEGER NOT NULL,
    entity_type VARCHAR(50) NOT NULL, -- 'user', 'profile', 'news', etc.
    data TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    owner_id INTEGER NOT NULL REFERENCES users(id),
    visibility VARCHAR(50) NOT NULL DEFAULT 'public', -- 'public', 'private', 'restricted'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attribuer des privilèges spécifiques aux rôles sur les tables
GRANT SELECT ON news TO guest;
GRANT SELECT, INSERT ON news TO user;
GRANT SELECT, INSERT, UPDATE ON news TO moderator;
GRANT SELECT, INSERT, UPDATE, DELETE ON news TO administrator;
GRANT ALL PRIVILEGES ON news TO owner;

GRANT SELECT, INSERT ON users TO guest;
GRANT SELECT, INSERT ON users TO user;
GRANT SELECT, INSERT, UPDATE ON users TO moderator;
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO administrator;
GRANT ALL PRIVILEGES ON users TO owner;

GRANT SELECT, INSERT ON profiles TO guest;
GRANT SELECT, INSERT, UPDATE ON profiles TO user;
GRANT SELECT, INSERT, UPDATE, DELETE ON profiles TO moderator;
GRANT ALL PRIVILEGES ON profiles TO administrator;
GRANT ALL PRIVILEGES ON profiles TO owner;

GRANT SELECT, INSERT ON login_logs TO guest;
GRANT SELECT, INSERT ON login_logs TO user;
GRANT SELECT, INSERT, UPDATE ON login_logs TO moderator;
GRANT SELECT, INSERT, UPDATE, DELETE ON login_logs TO administrator;
GRANT ALL PRIVILEGES ON login_logs TO owner;

GRANT SELECT, INSERT ON attachments TO guest;
GRANT SELECT, INSERT, UPDATE ON attachments TO user;
GRANT SELECT, INSERT, UPDATE, DELETE ON attachments TO moderator;
GRANT ALL PRIVILEGES ON attachments TO administrator;
GRANT ALL PRIVILEGES ON attachments TO owner;