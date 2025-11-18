from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    print("\n📊 REQUEST LOG (last 10):")
    result = conn.execute(text("""
        SELECT patent_number, user_tier, status_code, 
               response_time_ms, cache_hit, created_at 
        FROM request_log 
        ORDER BY created_at DESC 
        LIMIT 10
    """))
    for row in result:
        print(row)
    
    print("\n📦 PATENT CACHE:")
    result = conn.execute(text("""
        SELECT patent_number, source, fetch_count, created_at 
        FROM patent_cache 
        ORDER BY fetch_count DESC
    """))
    for row in result:
        print(row)