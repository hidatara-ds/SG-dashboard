import os
import hmac
from functools import wraps
from flask import request, jsonify

# Ambil API_KEY dari environment (Railway Variables)
API_KEY = os.environ.get("API_KEY")

def require_api_key(fn):
    """
    Decorator untuk proteksi route dengan API key.
    - Cek header X-API-KEY
    - Opsional: fallback query ?key= untuk testing di browser (boleh di-disable via ALLOW_QUERY_KEY_FALLBACK)
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        incoming = request.headers.get("X-API-KEY")

        # Fallback ke query param ?key= kalau env mengizinkan
        allow_fallback = (os.environ.get("ALLOW_QUERY_KEY_FALLBACK", "true").lower() == "true")
        if not incoming and allow_fallback:
            incoming = request.args.get("key")

        if API_KEY and incoming and hmac.compare_digest(incoming, API_KEY):
            return fn(*args, **kwargs)

        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        print(f"[auth] Unauthorized attempt from {client_ip}")
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    return wrapper
