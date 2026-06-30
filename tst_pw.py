from werkzeug.security import generate_password_hash, check_password_hash

# Test the exact users dict
users = {
    "wtech": generate_password_hash("wtechStaff1234#"),
}

for u, pw_hash in users.items():
    result = check_password_hash(pw_hash, "wtechStaff1234#")
    print(f'{u}: check={result} hash={pw_hash[:50]}...')
