// ====== LOAD ENV VARIABLES ======
require('dotenv').config();

const express = require('express');
const path = require('path');
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const bodyParser = require('body-parser');
const cors = require('cors');

// ====== FETCH (compatibility for Node < 18) ======
let fetchFn;
try {
  fetchFn = fetch; // If Node 18+, fetch is global
} catch {
  fetchFn = require('node-fetch'); // For Node 16 or lower
}

// ====== CONFIG ======
const app = express();
const PORT = process.env.PORT || 3000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/serene';
const JWT_SECRET = process.env.JWT_SECRET || 'supersecretkey';
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || null;

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
  password: { type: String, required: true }
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

  const hashedPassword = await bcrypt.hash(password, 10);

  try {
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

  if (!message) {
    return res.json({ success: false, response: 'No message provided' });
  }

  try {
    let botReply = "I'm here to listen. Tell me more.";

    if (GEMINI_API_KEY) {
      const aiResponse = await fetchFn('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      const aiData = await aiResponse.json();
      if (aiData && aiData.reply) botReply = aiData.reply;
    }

    res.json({
      success: true,
      response: botReply,
      sessionId: sessionId || Date.now().toString()
    });
  } catch (err) {
    console.error('Chat error:', err);
    res.json({ success: false, response: 'Error processing your message.' });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', mongo: mongoose.connection.readyState });
});

// ====== SPA FALLBACK ======
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'chat.html'));
});

// ====== START SERVER ======
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
