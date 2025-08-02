def parse_swagger(swagger_json):
    endpoints = []
    paths = swagger_json.get("paths", {})

    for path, methods in paths.items():
        for method in methods:
            endpoints.append({
                "path": path,
                "method": method.upper()
            })

    return endpoints


def parse_openapi(openapi_yaml):
    endpoints = []
    paths = openapi_yaml.get("paths", {})

    for path, methods in paths.items():
        for method in methods:
            endpoints.append({
                "path": path,
                "method": method.upper()
            })

    return endpoints
