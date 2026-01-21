try:
    import redis  # optional dependency
except Exception:
    redis = None


class RedisClient:
    _client = None

    @classmethod
    def init_app(cls, app):
        if redis is None:
            raise RuntimeError("redis package is not installed")

        cls._client = redis.Redis(
            host=app.config.get("REDIS_HOST", "localhost"),
            port=app.config.get("REDIS_PORT", 6379),
            db=app.config.get("REDIS_DB", 0),
            decode_responses=True,
        )

    @classmethod
    def client(cls):
        if cls._client is None:
            raise RuntimeError("Redis not initialized")
        return cls._client
