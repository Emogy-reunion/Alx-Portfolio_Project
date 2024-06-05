from flask_bcrypt import generate_password_hash                               
password = "Evhjnnbbhbvr702m"
hashed_password = generate_password_hash(password)
print("Hashed Password:", hashed_password)
print("Hashed Password Length:", len(hashed_password))
