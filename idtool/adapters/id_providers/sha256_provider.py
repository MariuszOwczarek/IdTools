import os, hashlib

class SHA256IdProvider:
    name = "sha256"
    def generate_id(self) -> str:
        return hashlib.sha256(os.urandom(32)).hexdigest()