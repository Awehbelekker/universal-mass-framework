#!/usr/bin/env node

/**
 * 🔍 MASS Framework - File Validation & Error Check
 * Comprehensive validation of all Firebase project files
 */

const fs = require('fs');
const path = require('path');

class ProjectValidator {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.validations = 0;
  }

  log(message, type = 'info') {
    const timestamp = new Date().toISOString();
    const prefix = {
      'info': '📋 [INFO]',
      'success': '✅ [SUCCESS]',
      'warning': '⚠️  [WARNING]',
      'error': '❌ [ERROR]'
    }[type];
    
    console.log(`${prefix} ${message}`);
    
    if (type === 'error') this.errors.push(message);
    if (type === 'warning') this.warnings.push(message);
  }

  validateFile(filePath, required = true) {
    this.validations++;
    
    if (!fs.existsSync(filePath)) {
      if (required) {
        this.log(`Missing required file: ${filePath}`, 'error');
        return false;
      } else {
        this.log(`Optional file missing: ${filePath}`, 'warning');
        return null;
      }
    }
    
    try {
      const stats = fs.statSync(filePath);
      if (stats.size === 0) {
        this.log(`Empty file: ${filePath}`, 'warning');
        return null;
      }
      
      this.log(`Valid file: ${filePath} (${stats.size} bytes)`, 'success');
      return true;
    } catch (error) {
      this.log(`Error reading file ${filePath}: ${error.message}`, 'error');
      return false;
    }
  }

  validateJSON(filePath, required = true) {
    const fileExists = this.validateFile(filePath, required);
    if (!fileExists) return fileExists;
    
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      JSON.parse(content);
      this.log(`Valid JSON: ${filePath}`, 'success');
      return true;
    } catch (error) {
      this.log(`Invalid JSON in ${filePath}: ${error.message}`, 'error');
      return false;
    }
  }

  validateHTML(filePath, required = true) {
    const fileExists = this.validateFile(filePath, required);
    if (!fileExists) return fileExists;
    
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      
      // Check for basic HTML structure
      if (!content.includes('<!DOCTYPE html>') && !content.includes('<html>')) {
        this.log(`Missing HTML structure in ${filePath}`, 'warning');
      }
      
      // Check for Firebase config
      if (content.includes('YOUR_CONFIG_HERE')) {
        this.log(`Firebase config not updated in ${filePath}`, 'error');
        return false;
      }
      
      // Check for Firebase imports
      if (!content.includes('firebase/app') && !content.includes('firebase-app')) {
        this.log(`Firebase imports missing in ${filePath}`, 'warning');
      }
      
      this.log(`Valid HTML: ${filePath}`, 'success');
      return true;
    } catch (error) {
      this.log(`Error reading HTML ${filePath}: ${error.message}`, 'error');
      return false;
    }
  }

  validateJS(filePath, required = true) {
    const fileExists = this.validateFile(filePath, required);
    if (!fileExists) return fileExists;
    
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      
      // Basic syntax check (simple)
      if (content.includes('function') || content.includes('=>') || content.includes('const') || content.includes('var')) {
        this.log(`Valid JavaScript: ${filePath}`, 'success');
        return true;
      } else {
        this.log(`Suspicious JavaScript content in ${filePath}`, 'warning');
        return null;
      }
    } catch (error) {
      this.log(`Error reading JavaScript ${filePath}: ${error.message}`, 'error');
      return false;
    }
  }

  validateFirebaseConfig() {
    this.log('Validating Firebase configuration...', 'info');
    
    // Check firebase.json
    const firebaseJson = this.validateJSON('firebase.json');
    if (firebaseJson) {
      try {
        const config = JSON.parse(fs.readFileSync('firebase.json', 'utf8'));
        
        // Check required sections
        if (!config.hosting) {
          this.log('Missing hosting configuration in firebase.json', 'error');
        }
        if (!config.functions) {
          this.log('Missing functions configuration in firebase.json', 'warning');
        }
        if (!config.firestore) {
          this.log('Missing firestore configuration in firebase.json', 'warning');
        }
        
        this.log('Firebase configuration structure valid', 'success');
      } catch (error) {
        this.log(`Error parsing firebase.json: ${error.message}`, 'error');
      }
    }
    
    // Check .firebaserc
    this.validateJSON('.firebaserc', false);
    
    // Check firestore.rules
    this.validateFile('firestore.rules');
  }

  validateFunctions() {
    this.log('Validating Firebase Functions...', 'info');
    
    // Check functions directory
    if (!fs.existsSync('functions')) {
      this.log('Functions directory missing', 'error');
      return false;
    }
    
    // Check package.json
    const packageJson = this.validateJSON('functions/package.json');
    if (packageJson) {
      try {
        const pkg = JSON.parse(fs.readFileSync('functions/package.json', 'utf8'));
        
        // Check required dependencies
        const requiredDeps = ['firebase-functions', 'firebase-admin', 'express'];
        for (const dep of requiredDeps) {
          if (!pkg.dependencies || !pkg.dependencies[dep]) {
            this.log(`Missing dependency: ${dep}`, 'error');
          }
        }
        
        // Check Node.js version
        if (pkg.engines && pkg.engines.node) {
          this.log(`Node.js version specified: ${pkg.engines.node}`, 'success');
        } else {
          this.log('No Node.js version specified in package.json', 'warning');
        }
        
      } catch (error) {
        this.log(`Error parsing functions/package.json: ${error.message}`, 'error');
      }
    }
    
    // Check index.js
    this.validateJS('functions/index.js');
    
    // Check node_modules
    if (fs.existsSync('functions/node_modules')) {
      this.log('Node modules installed', 'success');
    } else {
      this.log('Node modules not installed. Run: cd functions && npm install', 'warning');
    }
  }

  validateFrontend() {
    this.log('Validating Frontend files...', 'info');
    
    // Check public directory
    if (!fs.existsSync('public')) {
      this.log('Public directory missing', 'error');
      return false;
    }
    
    // Check HTML files
    this.validateHTML('public/index.html');
    this.validateHTML('public/dashboard.html');
    
    // Check for assets
    const assetDirs = ['public/css', 'public/js', 'public/images'];
    for (const dir of assetDirs) {
      if (fs.existsSync(dir)) {
        this.log(`Asset directory exists: ${dir}`, 'success');
      } else {
        this.log(`Asset directory missing: ${dir}`, 'warning');
      }
    }
  }

  validateCore() {
    this.log('Validating Core application...', 'info');
    
    // Check main application file
    this.validateFile('main.py');
    
    // Check requirements
    this.validateFile('requirements.txt');
    
    // Check configuration
    this.validateFile('.env', false);
    this.validateFile('.env.template', false);
    
    // Check core directories
    const coreDirs = ['config', 'core', 'agents', 'utils', 'workflows', 'tests'];
    for (const dir of coreDirs) {
      if (fs.existsSync(dir)) {
        this.log(`Core directory exists: ${dir}`, 'success');
      } else {
        this.log(`Core directory missing: ${dir}`, 'warning');
      }
    }
    
    // Check database
    this.validateFile('mass_framework.db', false);
  }

  validateDeploymentFiles() {
    this.log('Validating Deployment files...', 'info');
    
    // Check deployment scripts
    const deploymentFiles = [
      'launch-firebase-production.ps1',
      'launch-firebase-production.sh',
      'test-firebase-deployment.js',
      'update-firebase-config.js'
    ];
    
    for (const file of deploymentFiles) {
      this.validateFile(file, false);
    }
    
    // Check documentation
    const docs = [
      'README_FIREBASE_LAUNCH.md',
      'FIREBASE_DEPLOYMENT_GUIDE.md',
      'FIREBASE_LAUNCH_PRODUCTION.md'
    ];
    
    for (const doc of docs) {
      this.validateFile(doc, false);
    }
  }

  checkForDuplicates() {
    this.log('Checking for duplicate files...', 'info');
    
    try {
      const files = this.getAllFiles('.');
      const duplicates = {};
      
      for (const file of files) {
        const basename = path.basename(file);
        if (!duplicates[basename]) {
          duplicates[basename] = [];
        }
        duplicates[basename].push(file);
      }
      
      let duplicateCount = 0;
      for (const [basename, paths] of Object.entries(duplicates)) {
        if (paths.length > 1) {
          // Filter out acceptable duplicates
          const filtered = paths.filter(p => 
            !p.includes('node_modules') && 
            !p.includes('__pycache__') &&
            !p.includes('.git')
          );
          
          if (filtered.length > 1) {
            this.log(`Duplicate files found: ${basename}`, 'warning');
            filtered.forEach(p => this.log(`  - ${p}`, 'warning'));
            duplicateCount++;
          }
        }
      }
      
      if (duplicateCount === 0) {
        this.log('No problematic duplicate files found', 'success');
      }
      
    } catch (error) {
      this.log(`Error checking duplicates: ${error.message}`, 'error');
    }
  }

  getAllFiles(dir, files = []) {
    try {
      const items = fs.readdirSync(dir);
      for (const item of items) {
        const fullPath = path.join(dir, item);
        if (fs.statSync(fullPath).isDirectory()) {
          if (!item.startsWith('.') && item !== 'node_modules' && item !== '__pycache__') {
            this.getAllFiles(fullPath, files);
          }
        } else {
          files.push(fullPath);
        }
      }
    } catch (error) {
      // Ignore permission errors
    }
    return files;
  }

  async runAllValidations() {
    console.log('🔍 MASS Framework - File Validation & Error Check');
    console.log('================================================');
    console.log('');

    // Run all validations
    this.validateFirebaseConfig();
    this.validateFunctions();
    this.validateFrontend();
    this.validateCore();
    this.validateDeploymentFiles();
    this.checkForDuplicates();

    // Generate report
    console.log('');
    console.log('📊 Validation Report');
    console.log('==================');
    console.log(`✅ Total checks performed: ${this.validations}`);
    console.log(`❌ Errors found: ${this.errors.length}`);
    console.log(`⚠️  Warnings: ${this.warnings.length}`);
    console.log('');

    if (this.errors.length > 0) {
      console.log('❌ Critical Errors (must fix before deployment):');
      this.errors.forEach(error => console.log(`   • ${error}`));
      console.log('');
    }

    if (this.warnings.length > 0) {
      console.log('⚠️  Warnings (recommended to fix):');
      this.warnings.forEach(warning => console.log(`   • ${warning}`));
      console.log('');
    }

    // Overall status
    if (this.errors.length === 0) {
      console.log('🎉 Project validation passed! Ready for Firebase deployment! 🚀');
      console.log('');
      console.log('🚀 Next steps:');
      console.log('1. Run: npm install -g firebase-tools');
      console.log('2. Run: firebase login');
      console.log('3. Run: .\\launch-firebase-production.ps1');
      console.log('4. Test: node test-firebase-deployment.js');
    } else {
      console.log('🚨 Project has critical errors. Please fix before deployment.');
      console.log('');
      console.log('🔧 Quick fixes:');
      console.log('1. Update Firebase config in HTML files');
      console.log('2. Install missing dependencies');
      console.log('3. Re-run validation');
    }

    console.log('');
    console.log('📋 Project Health: ' + (this.errors.length === 0 ? '🟢 HEALTHY' : '🔴 NEEDS ATTENTION'));
  }
}

// Run the validator
const validator = new ProjectValidator();
validator.runAllValidations().catch(console.error);
