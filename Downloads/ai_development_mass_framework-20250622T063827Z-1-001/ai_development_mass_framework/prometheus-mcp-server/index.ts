#!/usr/bin/env node

import { PrometheusServer } from './src/server.js';
import { defaultConfig } from './src/config/default.js';
import { logger } from './src/utils/logger.js';
import { cache } from './src/utils/cache.js';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

async function main() {
  try {
    logger.info('Starting Prometheus MCP Server...');
    
    // Initialize Redis cache
    await cache.connect();
    logger.info('Redis cache connected');
    
    // Create and start server
    const server = new PrometheusServer(defaultConfig);
    await server.start();
    
    logger.info('Prometheus MCP Server started successfully');
    
    // Handle graceful shutdown
    process.on('SIGTERM', async () => {
      logger.info('Received SIGTERM, shutting down gracefully');
      await server.stop();
      await cache.disconnect();
      process.exit(0);
    });
    
    process.on('SIGINT', async () => {
      logger.info('Received SIGINT, shutting down gracefully');
      await server.stop();
      await cache.disconnect();
      process.exit(0);
    });
    
  } catch (error) {
    logger.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception:', error);
  process.exit(1);
});

main().catch((error) => {
  logger.error('Error in main:', error);
  process.exit(1);
});
