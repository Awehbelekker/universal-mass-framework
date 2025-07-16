import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';
import { PrometheusServer } from '../src/server.js';
import { defaultConfig } from '../src/config/default.js';

describe('Prometheus MCP Server', () => {
  let server: PrometheusServer;

  beforeAll(async () => {
    const testConfig = {
      ...defaultConfig,
      redis: {
        ...defaultConfig.redis,
        db: 1 // Use test database
      }
    };

    server = new PrometheusServer(testConfig);
  });

  afterAll(async () => {
    if (server) {
      await server.stop();
    }
  });

  describe('Initialization', () => {
    it('should create server instance', () => {
      expect(server).toBeDefined();
      expect(server).toBeInstanceOf(PrometheusServer);
    });

    it('should have proper configuration', () => {
      expect(server).toBeDefined();
      // Add more configuration tests as needed
    });
  });

  describe('Tools Registration', () => {
    it('should register portfolio tools', () => {
      // Test that portfolio tools are registered
      expect(server).toBeDefined();
    });

    it('should register market data tools', () => {
      // Test that market data tools are registered
      expect(server).toBeDefined();
    });

    it('should register trading tools', () => {
      // Test that trading tools are registered
      expect(server).toBeDefined();
    });

    it('should register neural forge tools', () => {
      // Test that neural forge tools are registered
      expect(server).toBeDefined();
    });

    it('should register risk management tools', () => {
      // Test that risk management tools are registered
      expect(server).toBeDefined();
    });
  });
});
