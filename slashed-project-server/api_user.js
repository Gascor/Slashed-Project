const express = require('express');
const router = express.Router();
const pool = require('./db');
const attachments = require('./attachments');

// Endpoint pour lister tous les utilisateurs
router.get('/user', async (req, res) => {
  try {
    const result = await pool.query('SELECT id, username, role, created_at FROM users ORDER BY created_at DESC');
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Endpoint pour obtenir les informations d'un utilisateur précis
router.get('/user/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query('SELECT id, username, role, created_at FROM users WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Endpoint pour lister les pièces jointes d'un utilisateur
router.get('/user/:id/attachments', (req, res) => {
  attachments.listAttachments(req, res, 'attachments', 'user_id');
});

// Endpoint pour obtenir une pièce jointe précise d'un utilisateur
router.get('/user/:id/attachments/:attachmentId', (req, res) => {
  attachments.getAttachment(req, res, 'attachments', 'user_id');
});

// Endpoint pour ajouter une pièce jointe à un utilisateur
router.post('/user/:id/attachments', (req, res) => {
  attachments.addAttachment(req, res, 'attachments', 'user_id');
});

// Endpoint pour mettre à jour une pièce jointe d'un utilisateur
router.put('/user/:id/attachments/:attachmentId', (req, res) => {
  attachments.updateAttachment(req, res, 'attachments', 'user_id');
});

// Endpoint pour supprimer une pièce jointe d'un utilisateur
router.delete('/user/:id/attachments/:attachmentId', (req, res) => {
  attachments.deleteAttachment(req, res, 'attachments', 'user_id');
});

module.exports = router;