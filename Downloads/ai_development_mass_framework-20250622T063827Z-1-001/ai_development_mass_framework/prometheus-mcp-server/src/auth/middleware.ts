import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { AuthenticatedRequest, User, AuthConfig } from '../types/index.js';
import { logger } from '../utils/logger.js';
import { cache } from '../utils/cache.js';

export class AuthMiddleware {
  private config: AuthConfig;

  constructor(config: AuthConfig) {
    this.config = config;
  }

  /**
   * Middleware to authenticate JWT tokens
   */
  authenticate = async (req: AuthenticatedRequest, res: Response, next: NextFunction): Promise<void> => {
    try {
      const token = this.extractToken(req);
      
      if (!token) {
        res.status(401).json({ error: 'No token provided' });
        return;
      }

      // Check if token is blacklisted
      const isBlacklisted = await cache.get(`blacklist:${token}`);
      if (isBlacklisted) {
        res.status(401).json({ error: 'Token has been revoked' });
        return;
      }

      // Verify and decode token
      const decoded = jwt.verify(token, this.config.jwtSecret) as any;
      
      // Check if user exists in cache or database
      const user = await this.getUserById(decoded.userId);
      if (!user) {
        res.status(401).json({ error: 'User not found' });
        return;
      }

      // Check if user is approved
      if (!user.approved) {
        res.status(403).json({ error: 'User account not approved' });
        return;
      }

      // Attach user to request
      req.user = user;
      req.token = token;
      
      next();
    } catch (error) {
      logger.error('Authentication error:', error as Record<string, any>);
      res.status(401).json({ error: 'Invalid token' });
    }
  };

  /**
   * Middleware to check if user has required permissions
   */
  authorize = (requiredRoles: string[] = []) => {
    return (req: AuthenticatedRequest, res: Response, next: NextFunction): void => {
      try {
        if (!req.user) {
          res.status(401).json({ error: 'User not authenticated' });
          return;
        }

        if (requiredRoles.length > 0 && !requiredRoles.includes(req.user.role)) {
          res.status(403).json({ error: 'Insufficient permissions' });
          return;
        }

        next();
      } catch (error) {
        logger.error('Authorization error:', error as Record<string, any>);
        res.status(403).json({ error: 'Access denied' });
      }
    };
  };

  /**
   * Middleware to check if user is admin
   */
  requireAdmin = (req: AuthenticatedRequest, res: Response, next: NextFunction): void => {
    if (!req.user || req.user.role !== 'admin') {
      res.status(403).json({ error: 'Admin access required' });
      return;
    }
    next();
  };

  /**
   * Middleware to validate API keys for external services
   */
  validateApiKey = (req: Request, res: Response, next: NextFunction): void => {
    try {
      const apiKey = req.headers['x-api-key'] as string;
      
      if (!apiKey) {
        res.status(401).json({ error: 'API key required' });
        return;
      }

      if (apiKey !== this.config.apiKey) {
        res.status(401).json({ error: 'Invalid API key' });
        return;
      }

      next();
    } catch (error) {
      logger.error('API key validation error:', error as Record<string, any>);
      res.status(401).json({ error: 'Invalid API key' });
    }
  };

  /**
   * Extract token from request headers
   */
  private extractToken(req: Request): string | null {
    const authHeader = req.headers.authorization;
    if (authHeader && authHeader.startsWith('Bearer ')) {
      return authHeader.substring(7);
    }
    return null;
  }

  /**
   * Get user by ID (with caching)
   */
  private async getUserById(userId: string): Promise<User | null> {
    try {
      // Try to get from cache first
      const cachedUser = await cache.get(`user:${userId}`);
      if (cachedUser) {
        return JSON.parse(cachedUser as string);
      }

      // In a real implementation, this would fetch from database
      // For now, return a mock user structure
      const mockUser: User = {
        id: userId,
        email: 'user@example.com',
        role: 'user',
        approved: true,
        createdAt: new Date(),
        updatedAt: new Date()
      };

      // Cache the user for 5 minutes
      await cache.set(`user:${userId}`, JSON.stringify(mockUser), 300);
      
      return mockUser;
    } catch (error) {
      logger.error('Error fetching user:', error as Record<string, any>);
      return null;
    }
  }

  /**
   * Generate JWT token for user
   */
  generateToken(user: User): string {
    const payload = { 
      userId: user.id, 
      email: user.email, 
      role: user.role 
    };
    
    const options: any = { 
      expiresIn: this.config.tokenExpiration || '24h',
      issuer: 'prometheus-mcp-server'
    };
    
    return jwt.sign(payload, this.config.jwtSecret, options);
  }

  /**
   * Revoke token by adding it to blacklist
   */
  async revokeToken(token: string): Promise<void> {
    try {
      // Add token to blacklist cache
      await cache.set(`blacklist:${token}`, 'true', 86400); // 24 hours
      logger.info('Token revoked successfully');
    } catch (error) {
      logger.error('Error revoking token:', error as Record<string, any>);
      throw error;
    }
  }

  /**
   * Validate and refresh token
   */
  async refreshToken(token: string): Promise<string | null> {
    try {
      const decoded = jwt.verify(token, this.config.jwtSecret) as any;
      const user = await this.getUserById(decoded.userId);
      
      if (!user || !user.approved) {
        return null;
      }

      // Generate new token
      return this.generateToken(user);
    } catch (error) {
      logger.error('Error refreshing token:', error as Record<string, any>);
      return null;
    }
  }
}
