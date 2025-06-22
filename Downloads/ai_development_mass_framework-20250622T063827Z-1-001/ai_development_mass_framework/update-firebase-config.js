#!/usr/bin/env node

/**
 * 🔥 Firebase Config Updater for MASS Framework
 * Automatically updates Firebase configuration in frontend files
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log('🔥 Firebase Config Updater for MASS Framework');
console.log('==============================================');
console.log('');
console.log('📋 Please provide your Firebase configuration:');
console.log('   (Get this from Firebase Console → Project Settings → General → Your apps → Config)');
console.log('');

// Collect Firebase config
const config = {};

function askQuestion(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer.trim());
    });
  });
}

async function collectConfig() {
  try {
    config.apiKey = await askQuestion('🔑 API Key: ');
    config.authDomain = await askQuestion('🌐 Auth Domain: ');
    config.projectId = await askQuestion('📊 Project ID: ');
    config.storageBucket = await askQuestion('🗂️ Storage Bucket: ');
    config.messagingSenderId = await askQuestion('📧 Messaging Sender ID: ');
    config.appId = await askQuestion('📱 App ID: ');
    
    // Optional analytics
    const hasAnalytics = await askQuestion('📈 Measurement ID (optional, press Enter to skip): ');
    if (hasAnalytics) {
      config.measurementId = hasAnalytics;
    }

    console.log('');
    console.log('✅ Configuration collected!');
    console.log('📝 Updating frontend files...');

    await updateFiles();
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    rl.close();
  }
}

async function updateFiles() {
  const firebaseConfigJS = `
    const firebaseConfig = {
      apiKey: "${config.apiKey}",
      authDomain: "${config.authDomain}",
      projectId: "${config.projectId}",
      storageBucket: "${config.storageBucket}",
      messagingSenderId: "${config.messagingSenderId}",
      appId: "${config.appId}"${config.measurementId ? `,\n      measurementId: "${config.measurementId}"` : ''}
    };`.trim();

  const files = [
    'public/index.html',
    'public/dashboard.html'
  ];

  for (const file of files) {
    if (fs.existsSync(file)) {
      try {
        let content = fs.readFileSync(file, 'utf8');
        
        // Replace the placeholder config
        const configRegex = /const firebaseConfig = {[\s\S]*?};/;
        const placeholderRegex = /YOUR_CONFIG_HERE/g;
        
        if (content.match(configRegex)) {
          content = content.replace(configRegex, firebaseConfigJS);
        } else if (content.match(placeholderRegex)) {
          content = content.replace(placeholderRegex, firebaseConfigJS);
        } else {
          console.log(`⚠️  Could not find config placeholder in ${file}`);
          continue;
        }
        
        fs.writeFileSync(file, content);
        console.log(`✅ Updated ${file}`);
        
      } catch (error) {
        console.error(`❌ Error updating ${file}:`, error.message);
      }
    } else {
      console.log(`⚠️  File not found: ${file}`);
    }
  }

  console.log('');
  console.log('🎉 Firebase configuration updated successfully!');
  console.log('');
  console.log('🚀 Next steps:');
  console.log('1. Run: firebase deploy');
  console.log('2. Visit your site and test authentication');
  console.log('3. Enable auth providers in Firebase Console');
  console.log('');
  console.log('🔗 Useful links:');
  console.log(`   • Firebase Console: https://console.firebase.google.com/project/${config.projectId}`);
  console.log(`   • Your site: https://${config.projectId}.web.app`);
}

// Start the process
collectConfig();
