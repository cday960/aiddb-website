from flask import g


def apply_security_headers(response):
    # Hardening
    nonce = getattr(g, "csp_nonce", "")
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

    # Content security policy (change for more CDNs)
    response.headers["Content-Security-Policy"] = (
        # Baseline
        "default-src 'self'; "
        # Allow local js and cdn
        f"script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
        # Allow local css and cdn
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        # Allow local image files
        "img-src 'self' data:; "
        # Limit XHR/fetch/WebSocket targets to sites origin
        "connect-src 'self'; "
        # No embedding >:(
        "frame-ancestors 'none';"
    )

    return response
