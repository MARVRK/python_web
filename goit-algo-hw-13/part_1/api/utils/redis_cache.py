# import redis
# from api.core.config import Settings
#
# redis_client = redis.StrictRedis.from_url(Settings.REDIS_HOST)
#
# def cache_user(user_id: str, user_data: dict):
#     redis_client.set(user_id, user_data)
#
# def get_cached_user(user_id: str):
#     cached_user = redis_client.get(user_id)
#     if cached_user:
#         return cached_user
#     return None
