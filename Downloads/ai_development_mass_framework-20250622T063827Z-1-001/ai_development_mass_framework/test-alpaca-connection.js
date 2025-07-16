// 🧪 Alpaca API Connection Test Script
// Run this to verify your API keys are working correctly

const https = require('https');

// Configuration - Replace with your actual API keys
const config = {
  paper: {
    keyId: 'YOUR_PAPER_API_KEY_HERE',
    secretKey: 'YOUR_PAPER_SECRET_KEY_HERE',
    baseUrl: 'https://paper-api.alpaca.markets/v2'
  },
  live: {
    keyId: 'YOUR_LIVE_API_KEY_HERE',  // Optional for initial testing
    secretKey: 'YOUR_LIVE_SECRET_KEY_HERE',  // Optional for initial testing
    baseUrl: 'https://api.alpaca.markets/v2'
  }
};

// Test function for API connection
function testAlpacaConnection(environment = 'paper') {
  console.log(`🧪 Testing ${environment.toUpperCase()} trading API connection...`);
  
  const apiConfig = config[environment];
  
  if (!apiConfig.keyId || apiConfig.keyId.includes('YOUR_')) {
    console.log(`❌ Please update your ${environment} API keys in this script first`);
    return;
  }

  const options = {
    hostname: apiConfig.baseUrl.replace('https://', '').split('/')[0],
    port: 443,
    path: '/v2/account',
    method: 'GET',
    headers: {
      'APCA-API-KEY-ID': apiConfig.keyId,
      'APCA-API-SECRET-KEY': apiConfig.secretKey
    }
  };

  const req = https.request(options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
      data += chunk;
    });

    res.on('end', () => {
      if (res.statusCode === 200) {
        const account = JSON.parse(data);
        console.log(`✅ ${environment.toUpperCase()} API connection successful!`);
        console.log(`📊 Account Status: ${account.status}`);
        console.log(`💰 Buying Power: $${parseFloat(account.buying_power).toLocaleString()}`);
        console.log(`📈 Portfolio Value: $${parseFloat(account.portfolio_value).toLocaleString()}`);
        console.log(`💵 Cash: $${parseFloat(account.cash).toLocaleString()}`);
        console.log(`🎯 Day Trade Count: ${account.daytrade_count}`);
        
        if (environment === 'paper') {
          console.log('🔄 Paper trading is ready for testing!');
        } else {
          console.log('🚀 Live trading is ready!');
        }
      } else {
        console.log(`❌ API Error (${res.statusCode}): ${data}`);
        
        // Common error messages
        if (res.statusCode === 401) {
          console.log('🔑 Check your API keys - they may be incorrect');
        } else if (res.statusCode === 403) {
          console.log('🚫 Account may not be approved for trading');
        }
      }
    });
  });

  req.on('error', (error) => {
    console.log(`❌ Connection Error: ${error.message}`);
    console.log('🌐 Check your internet connection and API endpoints');
  });

  req.end();
}

// Test market data access
function testMarketData(environment = 'paper') {
  console.log(`📈 Testing ${environment.toUpperCase()} market data access...`);
  
  const apiConfig = config[environment];
  
  const options = {
    hostname: apiConfig.baseUrl.replace('https://', '').split('/')[0],
    port: 443,
    path: '/v2/stocks/AAPL/quotes/latest',
    method: 'GET',
    headers: {
      'APCA-API-KEY-ID': apiConfig.keyId,
      'APCA-API-SECRET-KEY': apiConfig.secretKey
    }
  };

  const req = https.request(options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
      data += chunk;
    });

    res.on('end', () => {
      if (res.statusCode === 200) {
        const quote = JSON.parse(data);
        console.log(`✅ Market data access successful!`);
        console.log(`📊 AAPL Latest Quote:`);
        console.log(`   Ask: $${quote.quote.ask_price}`);
        console.log(`   Bid: $${quote.quote.bid_price}`);
        console.log(`   Time: ${quote.quote.timestamp}`);
      } else {
        console.log(`❌ Market Data Error (${res.statusCode}): ${data}`);
      }
    });
  });

  req.on('error', (error) => {
    console.log(`❌ Market Data Connection Error: ${error.message}`);
  });

  req.end();
}

// Test order placement (paper trading only for safety)
function testOrderPlacement() {
  console.log(`🔄 Testing PAPER order placement (safe test)...`);
  
  const apiConfig = config.paper;
  
  if (!apiConfig.keyId || apiConfig.keyId.includes('YOUR_')) {
    console.log(`❌ Please update your paper API keys first`);
    return;
  }

  const orderData = JSON.stringify({
    symbol: 'AAPL',
    qty: 1,
    side: 'buy',
    type: 'market',
    time_in_force: 'day'
  });

  const options = {
    hostname: apiConfig.baseUrl.replace('https://', '').split('/')[0],
    port: 443,
    path: '/v2/orders',
    method: 'POST',
    headers: {
      'APCA-API-KEY-ID': apiConfig.keyId,
      'APCA-API-SECRET-KEY': apiConfig.secretKey,
      'Content-Type': 'application/json',
      'Content-Length': orderData.length
    }
  };

  const req = https.request(options, (res) => {
    let data = '';

    res.on('data', (chunk) => {
      data += chunk;
    });

    res.on('end', () => {
      if (res.statusCode === 201) {
        const order = JSON.parse(data);
        console.log(`✅ Test order placed successfully!`);
        console.log(`📝 Order ID: ${order.id}`);
        console.log(`📊 Symbol: ${order.symbol}`);
        console.log(`📈 Side: ${order.side}`);
        console.log(`🔢 Quantity: ${order.qty}`);
        console.log(`⏰ Status: ${order.status}`);
        console.log(`🎯 Paper trading orders are working!`);
      } else {
        console.log(`❌ Order Error (${res.statusCode}): ${data}`);
      }
    });
  });

  req.on('error', (error) => {
    console.log(`❌ Order Placement Error: ${error.message}`);
  });

  req.write(orderData);
  req.end();
}

// Main execution
console.log('🚀 MASS AI Trading - Alpaca API Test Suite');
console.log('==========================================');
console.log('');
console.log('📝 Instructions:');
console.log('1. Update the API keys in this script');
console.log('2. Run: node test-alpaca-connection.js');
console.log('3. Check the results below');
console.log('');

// Run tests
setTimeout(() => {
  testAlpacaConnection('paper');
}, 1000);

setTimeout(() => {
  testMarketData('paper');
}, 3000);

setTimeout(() => {
  testOrderPlacement();
}, 5000);

// If you have live API keys, uncomment this:
// setTimeout(() => {
//   testAlpacaConnection('live');
// }, 7000);
