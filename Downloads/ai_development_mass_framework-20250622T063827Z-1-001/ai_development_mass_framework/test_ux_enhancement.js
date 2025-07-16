#!/usr/bin/env node

/**
 * PROMETHEUS UX/UI Enhancement Deployment and Testing Script
 * Tests all new UX/UI components and ensures proper integration
 */

const fs = require('fs');
const path = require('path');

class PrometheusUXTester {
    constructor() {
        this.testResults = {
            passed: 0,
            failed: 0,
            warnings: 0,
            details: []
        };
        
        this.requiredFiles = [
            'prometheus_ux_master_enhancer.js',
            'prometheus_logo_system_v2.js',
            'prometheus_workflow_enhancer.js',
            'PROMETHEUS_UX_ENHANCEMENT_GUIDE.md'
        ];
        
        this.htmlFiles = [
            'prometheus_landing.html',
            'prometheus_dashboard.html',
            'prometheus_registration.html',
            'prometheus_admin.html',
            'prometheus_login.html'
        ];
    }

    /**
     * Run all tests
     */
    async runTests() {
        console.log('🚀 Starting PROMETHEUS UX/UI Enhancement Tests...\n');
        
        // Test file existence
        this.testFileExistence();
        
        // Test HTML integration
        this.testHTMLIntegration();
        
        // Test JavaScript syntax
        this.testJavaScriptSyntax();
        
        // Test CSS completeness
        this.testCSSCompleteness();
        
        // Test accessibility features
        this.testAccessibilityFeatures();
        
        // Test mobile responsiveness
        this.testMobileResponsiveness();
        
        // Generate report
        this.generateReport();
        
        return this.testResults;
    }

    /**
     * Test if all required files exist
     */
    testFileExistence() {
        console.log('📁 Testing file existence...');
        
        this.requiredFiles.forEach(file => {
            const filePath = path.join(__dirname, file);
            if (fs.existsSync(filePath)) {
                this.pass(`✅ ${file} exists`);
            } else {
                this.fail(`❌ ${file} missing`);
            }
        });
        
        console.log();
    }

    /**
     * Test HTML integration
     */
    testHTMLIntegration() {
        console.log('🔗 Testing HTML integration...');
        
        this.htmlFiles.forEach(file => {
            const filePath = path.join(__dirname, file);
            
            if (!fs.existsSync(filePath)) {
                this.warn(`⚠️  ${file} not found`);
                return;
            }
            
            const content = fs.readFileSync(filePath, 'utf8');
            
            // Check for required script includes
            const requiredScripts = [
                'prometheus_ux_master_enhancer.js',
                'prometheus_logo_system_v2.js',
                'prometheus_workflow_enhancer.js'
            ];
            
            requiredScripts.forEach(script => {
                if (content.includes(script)) {
                    this.pass(`✅ ${file} includes ${script}`);
                } else {
                    this.fail(`❌ ${file} missing ${script}`);
                }
            });
            
            // Check for viewport meta tag
            if (content.includes('viewport')) {
                this.pass(`✅ ${file} has viewport meta tag`);
            } else {
                this.warn(`⚠️  ${file} missing viewport meta tag`);
            }
            
            // Check for accessibility features
            if (content.includes('aria-label') || content.includes('role=')) {
                this.pass(`✅ ${file} has accessibility attributes`);
            } else {
                this.warn(`⚠️  ${file} could use more accessibility attributes`);
            }
        });
        
        console.log();
    }

    /**
     * Test JavaScript syntax
     */
    testJavaScriptSyntax() {
        console.log('🔍 Testing JavaScript syntax...');
        
        const jsFiles = this.requiredFiles.filter(f => f.endsWith('.js'));
        
        jsFiles.forEach(file => {
            const filePath = path.join(__dirname, file);
            
            if (!fs.existsSync(filePath)) {
                this.fail(`❌ ${file} not found for syntax test`);
                return;
            }
            
            try {
                const content = fs.readFileSync(filePath, 'utf8');
                
                // Basic syntax checks
                const openBraces = (content.match(/{/g) || []).length;
                const closeBraces = (content.match(/}/g) || []).length;
                
                if (openBraces === closeBraces) {
                    this.pass(`✅ ${file} has balanced braces`);
                } else {
                    this.fail(`❌ ${file} has unbalanced braces`);
                }
                
                // Check for proper class definitions
                if (content.includes('class ') && content.includes('constructor')) {
                    this.pass(`✅ ${file} has proper class structure`);
                } else {
                    this.warn(`⚠️  ${file} may be missing class structure`);
                }
                
                // Check for error handling
                if (content.includes('try') && content.includes('catch')) {
                    this.pass(`✅ ${file} includes error handling`);
                } else {
                    this.warn(`⚠️  ${file} could use more error handling`);
                }
                
            } catch (error) {
                this.fail(`❌ ${file} syntax error: ${error.message}`);
            }
        });
        
        console.log();
    }

    /**
     * Test CSS completeness
     */
    testCSSCompleteness() {
        console.log('🎨 Testing CSS completeness...');
        
        const jsFiles = this.requiredFiles.filter(f => f.endsWith('.js'));
        
        jsFiles.forEach(file => {
            const filePath = path.join(__dirname, file);
            
            if (!fs.existsSync(filePath)) {
                return;
            }
            
            const content = fs.readFileSync(filePath, 'utf8');
            
            // Check for CSS injection
            if (content.includes('createElement(\'style\')')) {
                this.pass(`✅ ${file} injects CSS styles`);
            } else {
                this.warn(`⚠️  ${file} may not inject CSS styles`);
            }
            
            // Check for responsive CSS
            if (content.includes('@media')) {
                this.pass(`✅ ${file} includes responsive CSS`);
            } else {
                this.warn(`⚠️  ${file} may lack responsive CSS`);
            }
            
            // Check for CSS variables
            if (content.includes('var(--') || content.includes('--prometheus')) {
                this.pass(`✅ ${file} uses CSS variables`);
            } else {
                this.warn(`⚠️  ${file} could use CSS variables`);
            }
        });
        
        console.log();
    }

    /**
     * Test accessibility features
     */
    testAccessibilityFeatures() {
        console.log('♿ Testing accessibility features...');
        
        const jsFiles = this.requiredFiles.filter(f => f.endsWith('.js'));
        
        jsFiles.forEach(file => {
            const filePath = path.join(__dirname, file);
            
            if (!fs.existsSync(filePath)) {
                return;
            }
            
            const content = fs.readFileSync(filePath, 'utf8');
            
            // Check for ARIA support
            if (content.includes('aria-label') || content.includes('setAttribute')) {
                this.pass(`✅ ${file} includes ARIA support`);
            } else {
                this.warn(`⚠️  ${file} may lack ARIA support`);
            }
            
            // Check for keyboard navigation
            if (content.includes('keydown') || content.includes('keyup')) {
                this.pass(`✅ ${file} supports keyboard navigation`);
            } else {
                this.warn(`⚠️  ${file} may lack keyboard navigation`);
            }
            
            // Check for focus management
            if (content.includes('focus') || content.includes('tabindex')) {
                this.pass(`✅ ${file} includes focus management`);
            } else {
                this.warn(`⚠️  ${file} may lack focus management`);
            }
            
            // Check for reduced motion support
            if (content.includes('prefers-reduced-motion')) {
                this.pass(`✅ ${file} supports reduced motion`);
            } else {
                this.warn(`⚠️  ${file} may lack reduced motion support`);
            }
        });
        
        console.log();
    }

    /**
     * Test mobile responsiveness
     */
    testMobileResponsiveness() {
        console.log('📱 Testing mobile responsiveness...');
        
        const jsFiles = this.requiredFiles.filter(f => f.endsWith('.js'));
        
        jsFiles.forEach(file => {
            const filePath = path.join(__dirname, file);
            
            if (!fs.existsSync(filePath)) {
                return;
            }
            
            const content = fs.readFileSync(filePath, 'utf8');
            
            // Check for touch support
            if (content.includes('touch') || content.includes('Touch')) {
                this.pass(`✅ ${file} includes touch support`);
            } else {
                this.warn(`⚠️  ${file} may lack touch support`);
            }
            
            // Check for responsive breakpoints
            if (content.includes('breakpoint') || content.includes('768px')) {
                this.pass(`✅ ${file} includes responsive breakpoints`);
            } else {
                this.warn(`⚠️  ${file} may lack responsive breakpoints`);
            }
            
            // Check for mobile-specific features
            if (content.includes('mobile') || content.includes('Mobile')) {
                this.pass(`✅ ${file} includes mobile-specific features`);
            } else {
                this.warn(`⚠️  ${file} may lack mobile-specific features`);
            }
        });
        
        console.log();
    }

    /**
     * Helper methods
     */
    pass(message) {
        this.testResults.passed++;
        this.testResults.details.push({ type: 'pass', message });
        console.log(`  ${message}`);
    }

    fail(message) {
        this.testResults.failed++;
        this.testResults.details.push({ type: 'fail', message });
        console.log(`  ${message}`);
    }

    warn(message) {
        this.testResults.warnings++;
        this.testResults.details.push({ type: 'warn', message });
        console.log(`  ${message}`);
    }

    /**
     * Generate test report
     */
    generateReport() {
        console.log('📊 Test Results Summary:');
        console.log('========================');
        console.log(`✅ Passed: ${this.testResults.passed}`);
        console.log(`❌ Failed: ${this.testResults.failed}`);
        console.log(`⚠️  Warnings: ${this.testResults.warnings}`);
        
        const total = this.testResults.passed + this.testResults.failed + this.testResults.warnings;
        const passRate = ((this.testResults.passed / total) * 100).toFixed(1);
        
        console.log(`📈 Pass Rate: ${passRate}%`);
        
        if (this.testResults.failed === 0) {
            console.log('\n🎉 All critical tests passed! UX/UI enhancement is ready for deployment.');
        } else {
            console.log('\n⚠️  Some tests failed. Please review and fix before deployment.');
        }
        
        // Save detailed report
        const reportPath = path.join(__dirname, 'ux_test_report.json');
        fs.writeFileSync(reportPath, JSON.stringify(this.testResults, null, 2));
        console.log(`\n📄 Detailed report saved to: ${reportPath}`);
    }
}

// Run tests if this file is executed directly
if (require.main === module) {
    const tester = new PrometheusUXTester();
    tester.runTests().then(results => {
        process.exit(results.failed > 0 ? 1 : 0);
    });
}

module.exports = PrometheusUXTester;
