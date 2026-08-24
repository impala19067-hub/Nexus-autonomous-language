"""
Sapphire HTTP & Web Automation Standard Library
"""
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

try:
    import requests
except ImportError:
    requests = None

class HTTPModule:
    @staticmethod
    def get(url: str, headers: dict = None) -> dict:
        if requests is not None:
            try:
                resp = requests.get(url, headers=headers or {}, timeout=30)
                try:
                    body_json = resp.json()
                except Exception:
                    body_json = None
                return {
                    "status_code": resp.status_code,
                    "body": resp.text,
                    "json": body_json,
                    "headers": dict(resp.headers),
                    "ok": resp.ok
                }
            except Exception as e:
                return {
                    "status_code": 0,
                    "body": "",
                    "json": None,
                    "headers": {},
                    "ok": False,
                    "error": str(e)
                }
        else:
            # Fallback to standard library urllib.request
            try:
                req = urllib.request.Request(url, headers=headers or {})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    body_text = resp.read().decode('utf-8', errors='ignore')
                    try:
                        body_json = json.loads(body_text)
                    except Exception:
                        body_json = None
                    return {
                        "status_code": resp.status,
                        "body": body_text,
                        "json": body_json,
                        "headers": dict(resp.headers),
                        "ok": True
                    }
            except urllib.error.HTTPError as e:
                return {
                    "status_code": e.code,
                    "body": e.read().decode('utf-8', errors='ignore'),
                    "json": None,
                    "headers": dict(e.headers),
                    "ok": False
                }
            except Exception as e:
                return {
                    "status_code": 0,
                    "body": "",
                    "json": None,
                    "headers": {},
                    "ok": False,
                    "error": str(e)
                }

    @staticmethod
    def post(url: str, data: any = None, headers: dict = None) -> dict:
        headers = headers or {}
        if isinstance(data, dict):
            data_bytes = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        elif isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = b''

        if requests is not None:
            try:
                resp = requests.post(url, json=data if isinstance(data, dict) else None, data=None if isinstance(data, dict) else data, headers=headers, timeout=30)
                try:
                    body_json = resp.json()
                except Exception:
                    body_json = None
                return {
                    "status_code": resp.status_code,
                    "body": resp.text,
                    "json": body_json,
                    "headers": dict(resp.headers),
                    "ok": resp.ok
                }
            except Exception as e:
                return {"status_code": 0, "body": "", "json": None, "headers": {}, "ok": False, "error": str(e)}
        else:
            try:
                req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')
                with urllib.request.urlopen(req, timeout=30) as resp:
                    body_text = resp.read().decode('utf-8', errors='ignore')
                    try:
                        body_json = json.loads(body_text)
                    except Exception:
                        body_json = None
                    return {
                        "status_code": resp.status,
                        "body": body_text,
                        "json": body_json,
                        "headers": dict(resp.headers),
                        "ok": True
                    }
            except Exception as e:
                return {"status_code": 0, "body": "", "json": None, "headers": {}, "ok": False, "error": str(e)}
