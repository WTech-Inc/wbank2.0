@echo off
cd /d E:\wbank
set dataurl=postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
set HTTP_PORT=8080
set HTTPS_PORT=8443
python main.py > run.log 2>&1
