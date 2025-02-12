const { Pool } = require('pg');

const pool = new Pool({
  user: 'guest_user',
  host: 'db', // Utilisez le nom du service Docker pour l'hôte
  database: 'slashed_project',
  password: 'guest_password',
  port: 5432,
});

module.exports = pool;