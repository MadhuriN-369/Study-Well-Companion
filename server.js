// Simple Express server that proxies requests to Gemini using an env API key
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');

const app = express();
app.use(cors());
app.use(express.json());

const apiKey = process.env.GEMINI_API_KEY || process.env.GOOGLE_GENERATIVE_AI_API_KEY;
let genAI = null;
if (apiKey) {
  genAI = new GoogleGenerativeAI(apiKey);
}

app.get('/api/health', (req, res) => {
  res.json({ ok: true, hasApiKey: Boolean(apiKey) });
});

app.post('/api/ask', async (req, res) => {
  const prompt = (req.body && req.body.prompt) || '';
  if (!prompt || typeof prompt !== 'string') {
    return res.status(400).json({ error: 'prompt is required' });
  }
  if (!genAI) {
    return res.status(503).json({ error: 'Missing GEMINI_API_KEY on server' });
  }

  try {
    const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
    const result = await model.generateContent(prompt);
    const text = result.response.text();
    return res.json({ reply: text });
  } catch (err) {
    console.error('Gemini API error:', err && (err.response?.data || err.message || err));
    return res.status(500).json({ error: 'Gemini request failed' });
  }
});

// Serve the static client (this project keeps index.html at repo root)
app.use(express.static(path.join(__dirname)));
// Fallback to index.html for any non-API route (SPA)
app.get(/^\/(?!api).*/, (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on http://localhost:${port}`);
});
