# flask_api/auth.py
import os, hmac
from functools import wraps
from flask import request, jsonify

API_KEY = os.environ.get("API_KEY")  # pastikan ini ter-set di Railway

def require_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # prioritas: header
        incoming = request.headers.get("X-API-KEY")
        # (opsional) izinkan query ?key= untuk testing cepat di browser
        if not incoming:
            incoming = request.args.get("key")

        if API_KEY and incoming and hmac.compare_digest(incoming, API_KEY):
            return fn(*args, **kwargs)

        # log tipis biar gampang tracing
        request_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        print(f"[auth] unauthorized from {request_ip}")
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    return wrapper
