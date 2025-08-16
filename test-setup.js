const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.static('public'));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Serene server is running!' });
});

app.listen(PORT, () => {
  console.log(`✅ Serene server running on http://localhost:${PORT}`);
  console.log(`📁 Serving files from: ${__dirname}/public`);
  console.log(`🔗 Health check: http://localhost:${PORT}/health`);
});
