const express = require('express');
const router = express.Router();
const pool = require('./db');
const attachments = require('./attachments');

router.get('/news', async (req, res) => {
  try {
    const result = await pool.query('SELECT id, title, created_at FROM news ORDER BY created_at DESC');
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.get('/news/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await pool.query('SELECT * FROM news WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'News not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

router.post('/news', async (req, res) => {
  const { title, description, image_url } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO news (title, description, image_url) VALUES ($1, $2, $3) RETURNING *',
      [title, description, image_url]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Endpoint pour lister les pièces jointes d'un article de news
router.get('/news/:id/attachments', (req, res) => {
  attachments.listAttachments(req, res, 'attachments', 'news_id');
});

// Endpoint pour obtenir une pièce jointe précise d'un article de news
router.get('/news/:id/attachments/:attachmentId', (req, res) => {
  attachments.getAttachment(req, res, 'attachments', 'news_id');
});

// Endpoint pour ajouter une pièce jointe à un article de news
router.post('/news/:id/attachments', (req, res) => {
  attachments.addAttachment(req, res, 'attachments', 'news_id');
});

// Endpoint pour mettre à jour une pièce jointe d'un article de news
router.put('/news/:id/attachments/:attachmentId', (req, res) => {
  attachments.updateAttachment(req, res, 'attachments', 'news_id');
});

// Endpoint pour supprimer une pièce jointe d'un article de news
router.delete('/news/:id/attachments/:attachmentId', (req, res) => {
  attachments.deleteAttachment(req, res, 'attachments', 'news_id');
});

module.exports = router;