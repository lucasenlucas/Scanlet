import requests

COMMON_API_DOC_PATHS = [
    "/swagger.json",
    "/swagger.yaml",
    "/openapi.json",
    "/openapi.yaml",
    "/api-docs",
    "/docs/swagger.json",
    "/postman.json"
]

def find_api_docs(base_url):
    if base_url.endswith("/"):
        base_url = base_url[:-1]

    headers = {
        "User-Agent": "Scanlet/1.0"
    }

    for path in COMMON_API_DOC_PATHS:
        full_url = base_url + path
        try:
            response = requests.get(full_url, headers=headers, timeout=5)
            if response.status_code == 200 and len(response.text) > 10:
                doc_type = detect_doc_type(path, response.text)
                return {
                    "path": path,
                    "type": doc_type,
                    "content": response.text
                }
        except requests.exceptions.RequestException:
            pass  # negeer fouten en ga door met volgende

    return None

def detect_doc_type(path, content):
    if path.endswith(".yaml") or path.endswith(".yml"):
        return "openapi"
    elif path.endswith(".json"):
        # probeer te zien of het swagger of openapi is
        try:
            import json
            data = json.loads(content)
            if "swagger" in data:
                return "swagger"
            elif "openapi" in data:
                return "openapi"
        except:
            pass
        return "swagger"  # fallback
    elif "openapi" in content:
        return "openapi"
    else:
        return "swagger"
