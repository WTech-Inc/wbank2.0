
$env:dataurl='postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
$env:HTTP_PORT='8080'
$env:HTTPS_PORT='8443'
Start-Process -WindowStyle Hidden -FilePath 'python' -ArgumentList 'main.py' -WorkingDirectory 'E:\wbank'
