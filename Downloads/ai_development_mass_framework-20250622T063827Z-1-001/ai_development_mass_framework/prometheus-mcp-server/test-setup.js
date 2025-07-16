import { PrometheusServer } from './dist/server.js';
import { defaultConfig } from './dist/config/default.js';

// Simple test to verify basic functionality
async function testBasicSetup() {
  console.log('Testing basic MCP server setup...');
  
  try {
    const server = new PrometheusServer(defaultConfig);
    console.log('✅ Server created successfully');
    
    const status = server.getStatus();
    console.log('📊 Server status:', status);
    
    console.log('✅ Basic setup test passed');
    return true;
  } catch (error) {
    console.error('❌ Basic setup test failed:', error);
    return false;
  }
}

testBasicSetup().then(success => {
  process.exit(success ? 0 : 1);
}).catch(error => {
  console.error('❌ Test failed:', error);
  process.exit(1);
});
