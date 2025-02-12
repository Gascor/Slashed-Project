const express = require('express');
const router = express.Router();
const pool = require('./db');
const attachments = require('./attachments');

// Endpoint pour obtenir le profil d'un utilisateur
router.get('/profile/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query('SELECT * FROM profiles WHERE user_id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Profile not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Endpoint pour créer ou mettre à jour le profil d'un utilisateur
router.post('/profile/:id', async (req, res) => {
  const { id } = req.params;
  const { avatar_url, bio } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO profiles (user_id, avatar_url, bio) VALUES ($1, $2, $3) ON CONFLICT (user_id) DO UPDATE SET avatar_url = $2, bio = $3 RETURNING *',
      [id, avatar_url, bio]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Endpoint pour lister les pièces jointes d'un profil
router.get('/profile/:id/attachments', (req, res) => {
  attachments.listAttachments(req, res, 'attachments', 'user_id');
});

// Endpoint pour obtenir une pièce jointe précise d'un profil
router.get('/profile/:id/attachments/:attachmentId', (req, res) => {
  attachments.getAttachment(req, res, 'attachments', 'user_id');
});

// Endpoint pour ajouter une pièce jointe à un profil
router.post('/profile/:id/attachments', (req, res) => {
  attachments.addAttachment(req, res, 'attachments', 'user_id');
});

// Endpoint pour mettre à jour une pièce jointe d'un profil
router.put('/profile/:id/attachments/:attachmentId', (req, res) => {
  attachments.updateAttachment(req, res, 'attachments', 'user_id');
});

// Endpoint pour supprimer une pièce jointe d'un profil
router.delete('/profile/:id/attachments/:attachmentId', (req, res) => {
  attachments.deleteAttachment(req, res, 'attachments', 'user_id');
});

module.exports = router;