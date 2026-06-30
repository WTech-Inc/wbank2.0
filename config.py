"""
Local configuration - NOT committed to git.
"""
import os

DATABASE_URL = os.environ.get(
    "dataurl",
    "postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
)
