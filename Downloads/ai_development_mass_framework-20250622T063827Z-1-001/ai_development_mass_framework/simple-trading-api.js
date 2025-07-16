// MASS AI Trading - Simple Live API
// Save this as: functions/index.js

const functions = require('firebase-functions');
const express = require('express');
const axios = require('axios');
const app = express();

// Your working Alpaca API config
const ALPACA_CONFIG = {
    apiKey: 'PKD86B3W4830DOMGZWED',
    secretKey: 'nqF3VPLLNuFqaTtKFbXQg6F3bhXUwVAxdfkIebQa',
    baseURL: 'https://paper-api.alpaca.markets/v2'
};

const headers = {
    'APCA-API-KEY-ID': ALPACA_CONFIG.apiKey,
    'APCA-API-SECRET-KEY': ALPACA_CONFIG.secretKey
};

// Get account info
app.get('/account', async (req, res) => {
    try {
        const response = await axios.get(`${ALPACA_CONFIG.baseURL}/account`, { headers });
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get positions  
app.get('/positions', async (req, res) => {
    try {
        const response = await axios.get(`${ALPACA_CONFIG.baseURL}/positions`, { headers });
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Place order
app.post('/orders', async (req, res) => {
    try {
        const response = await axios.post(`${ALPACA_CONFIG.baseURL}/orders`, req.body, { headers });
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

exports.api = functions.https.onRequest(app);
