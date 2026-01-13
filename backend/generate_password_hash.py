"""
Script to generate a secure password hash for admin user
Usage: python generate_password_hash.py
"""
import bcrypt
import getpass

def generate_hash():
    print("=" * 50)
    print("Admin Password Hash Generator")
    print("=" * 50)
    print()
    
    password = getpass.getpass("Enter admin password: ")
    confirm = getpass.getpass("Confirm password: ")
    
    if password != confirm:
        print("\nERROR: Passwords do not match!")
        return
    
    if len(password) < 8:
        print("\nWARNING: Password should be at least 8 characters long")
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Generate hash
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hash_str = hashed.decode('utf-8')
    
    print("\n" + "=" * 50)
    print("Generated Password Hash:")
    print("=" * 50)
    print(hash_str)
    print()
    print("Add this to your .env file:")
    print(f"ADMIN_PASSWORD_HASH={hash_str}")
    print("=" * 50)

if __name__ == '__main__':
    try:
        generate_hash()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\nError: {e}")
