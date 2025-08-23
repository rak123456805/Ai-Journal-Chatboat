require('dotenv').config();

const express = require('express');
const path = require('path');
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const bodyParser = require('body-parser');
const cors = require('cors');
const fetch = require('node-fetch'); // Works in all Node versions

// ====== CONFIG ======
const app = express();
const PORT = process.env.PORT || 3000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/serene';
const JWT_SECRET = process.env.JWT_SECRET || 'supersecretkey';
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://127.0.0.1:8000/chat';

// ====== MIDDLEWARE ======
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// ====== CONNECT TO MONGODB ======
mongoose
  .connect(MONGODB_URI)
  .then(() => console.log('✅ MongoDB Connected'))
  .catch(err => console.error('❌ MongoDB Error:', err));

// ====== USER MODEL ======
const UserSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  password: { type: String, required: true },
});
const User = mongoose.model('User', UserSchema);

// ====== AUTH MIDDLEWARE ======
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.status(401).json({ success: false, message: 'No token provided' });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ success: false, message: 'Invalid token' });
    req.user = user;
    next();
  });
}

// ====== ROUTES ======

// Register
app.post('/api/register', async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) return res.json({ success: false, message: 'Missing fields' });

  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    const newUser = new User({ username, password: hashedPassword });
    await newUser.save();
    res.json({ success: true, message: 'User registered' });
  } catch (err) {
    res.json({ success: false, message: 'User already exists' });
  }
});

// Login
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ username });
  if (!user) return res.json({ success: false, message: 'Invalid credentials' });

  const valid = await bcrypt.compare(password, user.password);
  if (!valid) return res.json({ success: false, message: 'Invalid credentials' });

  const token = jwt.sign({ username: user.username }, JWT_SECRET, { expiresIn: '1h' });
  res.json({ success: true, token });
});

// Profile
app.get('/api/profile', authenticateToken, (req, res) => {
  res.json({ success: true, user: req.user });
});

// Chat endpoint
app.post('/api/chat', authenticateToken, async (req, res) => {
  const { message, sessionId } = req.body;

  if (!message) return res.json({ success: false, response: 'No message provided' });

  let botReply = "I'm here to listen. Tell me more.";

  try {
    const aiResponse = await fetch(PYTHON_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: message }),
    });

    if (aiResponse.ok) {
      const aiData = await aiResponse.json();
      if (aiData && aiData.response) botReply = aiData.response;
    } else {
      console.error('Python API Error:', aiResponse.status, aiResponse.statusText);
    }
  } catch (err) {
    console.error('Failed to connect to Python API:', err.message);
  }

  res.json({
    success: true,
    response: botReply,
    sessionId: sessionId || Date.now().toString(),
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', mongo: mongoose.connection.readyState });
});

// SPA fallback
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'chat.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
