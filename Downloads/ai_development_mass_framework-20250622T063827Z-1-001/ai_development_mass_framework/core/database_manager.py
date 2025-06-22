"""
Database Manager for MASS Framework
Handles database operations and connection management
"""

import sqlite3
import threading
import logging
import os
from typing import List, Dict, Any, Optional, Tuple, Generator
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Thread-safe database manager for SQLite operations"""
    
    def __init__(self, db_path: Optional[str] = None, uri: bool = False, connection: Optional[sqlite3.Connection] = None):
        self.db_path = db_path or os.getenv("DATABASE_PATH", "ai_development_mass_framework/mass_framework.db")
        self.uri = uri
        self._local = threading.local()
        self._lock = threading.Lock()
        self._external_connection = connection
        # Ensure database directory exists (skip for in-memory)
        if not (self.db_path.startswith(":memory:") or self.db_path.startswith("file:")):
            db_dir = os.path.dirname(os.path.abspath(self.db_path))
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)        # Initialize database
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get thread-local database connection or use provided connection"""
        if self._external_connection is not None:
            # Always set row_factory for external connections
            self._external_connection.row_factory = sqlite3.Row
            return self._external_connection
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=30.0,
                uri=self.uri
            )
            self._local.connection.row_factory = sqlite3.Row
            # Enable foreign keys
            self._local.connection.execute("PRAGMA foreign_keys = ON")
        else:
            # Defensive: ensure row_factory is always set
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection
    
    def _init_database(self):
        """Initialize the database with basic schema"""
        try:
            with self.get_connection() as conn:
                # Create basic metadata table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS database_metadata (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Set database version
                conn.execute("""
                    INSERT OR REPLACE INTO database_metadata (key, value)
                    VALUES ('version', '2.0.0')
                """)
                
                conn.commit()
                logger.info(f"Database initialized at {self.db_path}")
                
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise

    def initialize_database(self):
        """Public method to initialize database - calls internal _init_database"""
        self._init_database()
        
    def run_migrations(self):
        """Run database migrations"""
        try:
            with self.get_connection() as conn:
                # Create additional tables for enterprise features
                self._create_enterprise_tables(conn)
                
                # Update database version
                conn.execute("""
                    INSERT OR REPLACE INTO database_metadata (key, value)
                    VALUES ('version', '2.1.0')
                """)
                
                conn.commit()
                logger.info("Database migrations completed successfully")
                
        except Exception as e:
            logger.error(f"Failed to run migrations: {str(e)}")
            raise
            
    def _create_enterprise_tables(self, conn: sqlite3.Connection):
        """Create enterprise-specific tables"""
        # User management table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Agent activities table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                details TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP
            )
        """)
        
        # System metrics table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Application configurations table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS app_configurations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT NOT NULL,
                config_key TEXT NOT NULL,
                config_value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(app_name, config_key)
            )
        """)
        
        logger.info("Enterprise tables created successfully")

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager for database connections"""
        conn = self._get_connection()
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error(f"Database operation failed: {str(e)}")
            raise
        finally:
            # Don't close the connection as it's thread-local
            pass
    
    def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> sqlite3.Cursor:
        """Execute a query and return cursor"""        # Debug: print params type and value before executing
        print(f"DEBUG: execute_query params: {params} (type: {type(params)})")
        if params:
            for i, p in enumerate(params):
                if isinstance(p, dict):
                    print(f"ERROR: Param at index {i} is a dict: {p}")
                    import traceback; traceback.print_stack()
                    raise TypeError(f"Param at index {i} is a dict: {p}")
            print(f"DEBUG: All param types: {[type(p) for p in params]}")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
    
    def fetch_one(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
        """Fetch one row from query"""
        cursor = self.execute_query(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def fetch_all(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        """Fetch all rows from query"""
        cursor = self.execute_query(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """Insert data into table and return row ID"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.execute_query(query, tuple(data.values()))
        return cursor.lastrowid
    
    def update(self, table: str, data: Dict[str, Any], where_clause: str, where_params: Optional[Tuple[Any, ...]] = None) -> int:
        """Update data in table and return number of affected rows"""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        params = tuple(data.values())
        if where_params:
            params += where_params
        
        cursor = self.execute_query(query, params)
        return cursor.rowcount
    
    def delete(self, table: str, where_clause: str, where_params: Optional[Tuple[Any, ...]] = None) -> int:
        """Delete data from table and return number of affected rows"""
        query = f"DELETE FROM {table} WHERE {where_clause}"
        cursor = self.execute_query(query, where_params)
        return cursor.rowcount
    
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists"""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.fetch_one(query, (table_name,))
        return result is not None
    
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get column names for a table"""
        query = f"PRAGMA table_info({table_name})"
        rows = self.fetch_all(query)
        return [row['name'] for row in rows]
    
    def backup_database(self, backup_path: str):
        """Create a backup of the database"""
        try:
            with self.get_connection() as source:
                backup_db = sqlite3.connect(backup_path)
                source.backup(backup_db)
                backup_db.close()
                logger.info(f"Database backed up to {backup_path}")
        except Exception as e:
            logger.error(f"Failed to backup database: {str(e)}")
            raise
    
    def close_all_connections(self):
        """Close all thread-local connections"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            delattr(self._local, 'connection')
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics
        
        Returns:
            Dict[str, Any]: A dictionary containing database statistics including:
                - size_bytes: Total database size in bytes
                - size_mb: Total database size in megabytes
                - table_count: Number of tables in the database
                - tables: Dictionary with table names as keys and row counts as values
                - version: Database schema version
                - database_type: Type of database (in-memory or file-based)
                - index_count: Number of indices in the database
                - performance_score: Calculated performance score based on structure
        """
        try:
            stats: Dict[str, Any] = {}
            
            # Get database size (skip for in-memory databases)
            if self.db_path != ':memory:':
                try:
                    stats['size_bytes'] = os.path.getsize(self.db_path)
                    stats['size_mb'] = round(stats['size_bytes'] / 1024 / 1024, 2)
                except (OSError, IOError):
                    stats['size_bytes'] = 0
                    stats['size_mb'] = 0
            else:
                stats['size_bytes'] = 0
                stats['size_mb'] = 0
                stats['database_type'] = 'in-memory'
            
            # Get table count and row counts
            tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
            tables = self.fetch_all(tables_query)
            stats['table_count'] = len(tables)
            stats['tables'] = {}
            
            # Performance optimization: Batch query for better performance
            all_tables_data = {}
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for table in tables:
                    table_name = table['name']
                    cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                    all_tables_data[table_name] = cursor.fetchone()[0]
            
            stats['tables'] = all_tables_data
            
            # Get indices for performance assessment
            indices_query = "SELECT name FROM sqlite_master WHERE type='index'"
            indices = self.fetch_all(indices_query)
            stats['index_count'] = len(indices)
            
            # Calculate a simple performance score based on indexing and structure
            # Higher score indicates better performance optimization
            perf_score = min(100, 50 + (stats['index_count'] * 5) - (stats['table_count'] * 2))
            stats['performance_score'] = max(0, perf_score)
            
            # Get database version
            try:
                version_result = self.fetch_one(
                    "SELECT value FROM database_metadata WHERE key = 'version'"
                )
                stats['version'] = version_result['value'] if version_result else 'unknown'
            except Exception:
                stats['version'] = 'unknown'
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {str(e)}")
            return {'error': str(e)}

# Singleton instance
_db_manager_instance = None
_db_manager_lock = threading.Lock()

def get_database_manager() -> DatabaseManager:
    """Get singleton database manager instance"""
    global _db_manager_instance
    if _db_manager_instance is None:
        with _db_manager_lock:
            if _db_manager_instance is None:
                _db_manager_instance = DatabaseManager()
    return _db_manager_instance
