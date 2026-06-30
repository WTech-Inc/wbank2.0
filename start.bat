@echo off
cd /d E:\wbank
set dataurl=postgresql://neondb_owner:YOUR_NEON_PASSWORD@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
set HTTP_PORT=8080
set HTTPS_PORT=8443
python main.py > run.log 2>&1
