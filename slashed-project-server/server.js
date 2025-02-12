const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

// Importer les routeurs
const newsRouter = require('./api_news');
const authRouter = require('./api_auth');
const userRouter = require('./api_user');
const profileRouter = require('./api_profile');

app.use(newsRouter);
app.use(authRouter);
app.use(userRouter);
app.use(profileRouter);

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});