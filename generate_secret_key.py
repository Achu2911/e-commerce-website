#!/usr/bin/env python
"""
Generate a secure Django secret key for production use.
Run: python generate_secret_key.py
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("=" * 60)
    print("Generated Django Secret Key:")
    print("=" * 60)
    print(secret_key)
    print("=" * 60)
    print("\nAdd this to your .env file:")
    print(f"DJANGO_SECRET_KEY={secret_key}")
    print("=" * 60)


