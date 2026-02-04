"""
Cache Service for S2O Platform
Infrastructure layer service for caching operations
No business logic - pure caching abstraction
"""
import os
from typing import Optional, Any, Callable
import logging

logger = logging.getLogger(__name__)


class CacheService:
    """
    Infrastructure service for caching operations.
    Provides abstraction over caching backend (Redis/SimpleCache).
    
    Usage:
        from infrastructure.services import get_cache_service
        cache = get_cache_service()
        cache.set('key', 'value', timeout=300)
        value = cache.get('key')
    """
    
    def __init__(self, app=None):
        self._cache = None
        self._available = False
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize cache with Flask app"""
        try:
            from flask_caching import Cache
            
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
            
            # Try Redis first
            cache_config = {
                'CACHE_TYPE': 'RedisCache',
                'CACHE_REDIS_URL': redis_url,
                'CACHE_DEFAULT_TIMEOUT': 300,
                'CACHE_KEY_PREFIX': 's2o_'
            }
            
            try:
                app.config.from_mapping(cache_config)
                self._cache = Cache(app)
                # Test connection
                self._cache.set('_test_', 'test')
                self._cache.delete('_test_')
                self._available = True
                logger.info(f"CacheService: Redis connected at {redis_url}")
            except Exception as e:
                # Fallback to simple cache
                logger.warning(f"CacheService: Redis failed ({e}), using SimpleCache")
                app.config['CACHE_TYPE'] = 'SimpleCache'
                self._cache = Cache(app)
                self._available = True
                logger.info("CacheService: SimpleCache initialized")
                
        except ImportError:
            logger.warning("CacheService: Flask-Caching not installed")
            self._available = False
    
    @property
    def is_available(self) -> bool:
        """Check if cache is available"""
        return self._available
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if self._cache:
            return self._cache.get(key)
        return None
    
    def set(self, key: str, value: Any, timeout: int = 300) -> bool:
        """Set value in cache with TTL (default 5 minutes)"""
        if self._cache:
            self._cache.set(key, value, timeout=timeout)
            return True
        return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if self._cache:
            self._cache.delete(key)
            return True
        return False
    
    def clear(self) -> bool:
        """Clear all cache entries"""
        if self._cache:
            self._cache.clear()
            return True
        return False
    
    def get_or_set(self, key: str, getter: Callable, timeout: int = 300) -> Any:
        """Get from cache or compute and set"""
        value = self.get(key)
        if value is None:
            value = getter()
            if value is not None:
                self.set(key, value, timeout)
        return value
    
    @staticmethod
    def make_key(*parts) -> str:
        """Generate cache key from parts (e.g., 'menu', tenant_id)"""
        return ':'.join(str(p) for p in parts if p)


# Global instance
cache_service = CacheService()


def init_cache_service(app):
    """Initialize global cache service"""
    cache_service.init_app(app)
    return cache_service


def get_cache_service() -> CacheService:
    """Get global cache service instance"""
    return cache_service
