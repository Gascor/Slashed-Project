const pool = require('./db');

async function listAttachments(req, res, tableName, foreignKey) {
  const { id } = req.params;
  const userId = req.user.id; // Assurez-vous que l'ID de l'utilisateur est disponible dans req.user
  try {
    const result = await pool.query(
      `SELECT * FROM ${tableName} WHERE ${foreignKey} = $1 AND (visibility = 'public' OR owner_id = $2) ORDER BY created_at DESC`,
      [id, userId]
    );
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}

async function getAttachment(req, res, tableName, foreignKey) {
  const { id, attachmentId } = req.params;
  const userId = req.user.id; // Assurez-vous que l'ID de l'utilisateur est disponible dans req.user
  try {
    const result = await pool.query(
      `SELECT * FROM ${tableName} WHERE ${foreignKey} = $1 AND id = $2 AND (visibility = 'public' OR owner_id = $3)`,
      [id, attachmentId, userId]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Attachment not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}

async function addAttachment(req, res, tableName, foreignKey) {
  const { id } = req.params;
  const { data, type, visibility } = req.body;
  const userId = req.user.id; // Assurez-vous que l'ID de l'utilisateur est disponible dans req.user
  try {
    const result = await pool.query(
      `INSERT INTO ${tableName} (${foreignKey}, data, type, owner_id, visibility) VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [id, data, type, userId, visibility]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}

async function updateAttachment(req, res, tableName, foreignKey) {
  const { id, attachmentId } = req.params;
  const { data, type, visibility } = req.body;
  const userId = req.user.id; // Assurez-vous que l'ID de l'utilisateur est disponible dans req.user
  try {
    const result = await pool.query(
      `UPDATE ${tableName} SET data = $1, type = $2, visibility = $3 WHERE ${foreignKey} = $4 AND id = $5 AND owner_id = $6 RETURNING *`,
      [data, type, visibility, id, attachmentId, userId]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Attachment not found or you do not have permission to update it' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}

async function deleteAttachment(req, res, tableName, foreignKey) {
  const { id, attachmentId } = req.params;
  const userId = req.user.id; // Assurez-vous que l'ID de l'utilisateur est disponible dans req.user
  try {
    const result = await pool.query(
      `DELETE FROM ${tableName} WHERE ${foreignKey} = $1 AND id = $2 AND owner_id = $3 RETURNING *`,
      [id, attachmentId, userId]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Attachment not found or you do not have permission to delete it' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    console.error('Error executing query', err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}

module.exports = {
  listAttachments,
  getAttachment,
  addAttachment,
  updateAttachment,
  deleteAttachment
};