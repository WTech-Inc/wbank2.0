"""Fix session config for admin panel"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/main.py"
c = open(path, "r", encoding="utf-8").read()

# Increase session lifetime
old1 = "app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=10)"
new1 = "app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=24)"
if old1 in c:
    c = c.replace(old1, new1)
    print("Session lifetime increased to 24h")

# Add SameSite config
old2 = "app.config['SECRET_KEY'] = hashlib.sha256(\"WTech2225556\".encode()).hexdigest()"
new2 = "app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'\napp.config['SECRET_KEY'] = hashlib.sha256(\"WTech2225556\".encode()).hexdigest()"
if old2 in c:
    c = c.replace(old2, new2)
    print("SESSION_COOKIE_SAMESITE added")

open(path, "w", encoding="utf-8").write(c)
print("Done")
