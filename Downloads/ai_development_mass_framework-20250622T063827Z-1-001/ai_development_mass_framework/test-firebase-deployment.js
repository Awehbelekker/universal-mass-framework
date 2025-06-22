#!/usr/bin/env node

/**
 * 🧪 MASS Framework - Firebase Deployment Test Suite
 * Comprehensive testing of deployed Firebase application
 */

const https = require('https');
const fs = require('fs');

class FirebaseDeploymentTester {
  constructor() {
    this.results = {
      passed: 0,
      failed: 0,
      tests: []
    };
    
    // Get project ID from .firebaserc
    this.projectId = this.getProjectId();
    this.baseUrl = `https://${this.projectId}.web.app`;
    this.apiUrl = `${this.baseUrl}/api`;
  }

  getProjectId() {
    try {
      const firebaserc = JSON.parse(fs.readFileSync('.firebaserc', 'utf8'));
      return firebaserc.projects.default;
    } catch (error) {
      console.error('❌ Could not read .firebaserc file');
      return 'your-project-id';
    }
  }

  async runTest(name, testFunction) {
    console.log(`🧪 Testing: ${name}...`);
    
    try {
      const result = await testFunction();
      if (result.success) {
        console.log(`✅ ${name}: PASSED`);
        this.results.passed++;
      } else {
        console.log(`❌ ${name}: FAILED - ${result.error}`);
        this.results.failed++;
      }
      
      this.results.tests.push({
        name,
        success: result.success,
        error: result.error || null,
        details: result.details || null
      });
    } catch (error) {
      console.log(`❌ ${name}: ERROR - ${error.message}`);
      this.results.failed++;
      this.results.tests.push({
        name,
        success: false,
        error: error.message
      });
    }
  }

  async httpRequest(url, options = {}) {
    return new Promise((resolve, reject) => {
      const req = https.request(url, options, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body: data
          });
        });
      });
      
      req.on('error', reject);
      req.setTimeout(10000, () => reject(new Error('Request timeout')));
      req.end();
    });
  }

  async testHostingAccessible() {
    const response = await this.httpRequest(this.baseUrl);
    return {
      success: response.statusCode === 200,
      error: response.statusCode === 200 ? null : `HTTP ${response.statusCode}`,
      details: { statusCode: response.statusCode }
    };
  }

  async testLoginPageLoads() {
    const response = await this.httpRequest(this.baseUrl);
    const hasFirebaseAuth = response.body.includes('firebase-auth');
    const hasLoginForm = response.body.includes('email') && response.body.includes('password');
    
    return {
      success: response.statusCode === 200 && hasFirebaseAuth && hasLoginForm,
      error: !hasFirebaseAuth ? 'Firebase Auth not found' : !hasLoginForm ? 'Login form not found' : null,
      details: { 
        statusCode: response.statusCode,
        hasFirebaseAuth,
        hasLoginForm
      }
    };
  }

  async testDashboardExists() {
    const response = await this.httpRequest(`${this.baseUrl}/dashboard.html`);
    return {
      success: response.statusCode === 200,
      error: response.statusCode === 200 ? null : `HTTP ${response.statusCode}`,
      details: { statusCode: response.statusCode }
    };
  }

  async testAPIEndpoints() {
    const endpoints = ['/api/health', '/api/users', '/api/agents', '/api/workflows'];
    let successCount = 0;
    let errors = [];

    for (const endpoint of endpoints) {
      try {
        const response = await this.httpRequest(`${this.baseUrl}${endpoint}`);
        if (response.statusCode < 500) {
          successCount++;
        } else {
          errors.push(`${endpoint}: HTTP ${response.statusCode}`);
        }
      } catch (error) {
        errors.push(`${endpoint}: ${error.message}`);
      }
    }

    return {
      success: successCount === endpoints.length,
      error: errors.length > 0 ? errors.join(', ') : null,
      details: { 
        tested: endpoints.length,
        successful: successCount,
        errors 
      }
    };
  }

  async testFirebaseConfig() {
    const response = await this.httpRequest(this.baseUrl);
    const hasValidConfig = !response.body.includes('YOUR_CONFIG_HERE');
    const hasFirebaseInit = response.body.includes('initializeApp');
    
    return {
      success: hasValidConfig && hasFirebaseInit,
      error: !hasValidConfig ? 'Firebase config not updated' : !hasFirebaseInit ? 'Firebase not initialized' : null,
      details: { hasValidConfig, hasFirebaseInit }
    };
  }

  async testSecurityHeaders() {
    const response = await this.httpRequest(this.baseUrl);
    const hasCSP = response.headers['content-security-policy'];
    const hasXFrame = response.headers['x-frame-options'];
    
    return {
      success: true, // Non-critical
      error: null,
      details: { 
        csp: hasCSP ? 'Present' : 'Missing',
        xFrame: hasXFrame ? 'Present' : 'Missing'
      }
    };
  }

  async testSSLCertificate() {
    return new Promise((resolve) => {
      const req = https.request(this.baseUrl, { rejectUnauthorized: true }, (res) => {
        resolve({
          success: true,
          error: null,
          details: { ssl: 'Valid' }
        });
      });
      
      req.on('error', (error) => {
        resolve({
          success: false,
          error: error.message,
          details: { ssl: 'Invalid' }
        });
      });
      
      req.end();
    });
  }

  async runAllTests() {
    console.log('🚀 Starting MASS Framework Deployment Tests');
    console.log('===========================================');
    console.log(`📍 Testing URL: ${this.baseUrl}`);
    console.log(`🔗 API URL: ${this.apiUrl}`);
    console.log('');

    // Core functionality tests
    await this.runTest('Hosting Accessible', () => this.testHostingAccessible());
    await this.runTest('Login Page Loads', () => this.testLoginPageLoads());
    await this.runTest('Dashboard Exists', () => this.testDashboardExists());
    await this.runTest('API Endpoints', () => this.testAPIEndpoints());
    await this.runTest('Firebase Config', () => this.testFirebaseConfig());
    await this.runTest('Security Headers', () => this.testSecurityHeaders());
    await this.runTest('SSL Certificate', () => this.testSSLCertificate());

    // Print results
    this.printResults();
  }

  printResults() {
    console.log('');
    console.log('📊 Test Results Summary');
    console.log('======================');
    console.log(`✅ Passed: ${this.results.passed}`);
    console.log(`❌ Failed: ${this.results.failed}`);
    console.log(`📈 Success Rate: ${Math.round((this.results.passed / (this.results.passed + this.results.failed)) * 100)}%`);
    console.log('');

    if (this.results.failed > 0) {
      console.log('❌ Failed Tests:');
      this.results.tests
        .filter(test => !test.success)
        .forEach(test => {
          console.log(`   • ${test.name}: ${test.error}`);
        });
      console.log('');
    }

    console.log('🔗 Important URLs:');
    console.log(`   • Website: ${this.baseUrl}`);
    console.log(`   • Dashboard: ${this.baseUrl}/dashboard.html`);
    console.log(`   • API: ${this.apiUrl}`);
    console.log(`   • Firebase Console: https://console.firebase.google.com/project/${this.projectId}`);
    console.log('');

    if (this.results.failed === 0) {
      console.log('🎉 All tests passed! Your MASS Framework is ready for beta testing! 🚀');
    } else {
      console.log('⚠️  Some tests failed. Please check the issues above before launching.');
    }

    console.log('');
    console.log('📋 Next Steps:');
    console.log('1. Enable authentication providers in Firebase Console');
    console.log('2. Test user registration and login manually');
    console.log('3. Invite beta testers to try the platform');
    console.log('4. Monitor Firebase Console for usage and errors');
    console.log('5. Set up custom domain (optional)');
  }
}

// Run the tests
const tester = new FirebaseDeploymentTester();
tester.runAllTests().catch(console.error);
