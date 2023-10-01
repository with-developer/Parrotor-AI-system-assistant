import hashlib

def hash_password(password, salt):
    # 패스워드와 솔트를 합친 후, 이를 해시합니다.
    password_salt_comb = password + salt
    hashed_password = hashlib.sha256(password_salt_comb.encode('utf-8')).hexdigest()
    return hashed_password



