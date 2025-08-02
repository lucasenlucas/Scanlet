#!/usr/bin/env python3

import argparse
from modules.finder import find_api_docs
from modules.parser import parse_swagger, parse_openapi
from modules.cors_checker import check_cors
from modules.auth_probe import probe_auth
from utils.exporter import export_results
import json
import yaml

def main():
    parser = argparse.ArgumentParser(description="Scanlet - API Recon Toolkit")
    parser.add_argument("-u", "--url", help="Base API URL (e.g. https://api.example.com)", required=True)
    parser.add_argument("-c", "--cors", help="Check CORS misconfigurations", action="store_true")
    parser.add_argument("-a", "--auth", help="Check which endpoints require authentication", action="store_true")
    parser.add_argument("-e", "--export", help="Export results to a file (e.g. output.json)")
    args = parser.parse_args()

    print("[SCANLET] Starting scan on:", args.url)

    # Step 1: Find API docs
    api_doc = find_api_docs(args.url)
    if not api_doc:
        print("[!] No API documentation found.")
        return

    print(f"[+] Found API doc: {api_doc['path']} ({api_doc['type']})")

    # Step 2: Parse endpoints
    endpoints = []
    try:
        if api_doc["type"] == "swagger":
            endpoints = parse_swagger(json.loads(api_doc["content"]))
        elif api_doc["type"] == "openapi":
            endpoints = parse_openapi(yaml.safe_load(api_doc["content"]))
    except Exception as e:
        print("[!] Failed to parse API documentation:", e)
        return

    print(f"[+] Parsed {len(endpoints)} endpoints.")

    results = {
        "url": args.url,
        "api_doc": api_doc["path"],
        "endpoints": endpoints
    }

    # Step 3: CORS check
    if args.cors:
        cors_issues = check_cors(args.url, endpoints)
        results["cors_issues"] = cors_issues
        print(f"[CORS] Found {len(cors_issues)} potential CORS misconfigs.")

    # Step 4: Auth check
    if args.auth:
        unprotected = probe_auth(args.url, endpoints)
        results["unprotected_endpoints"] = unprotected
        print(f"[AUTH] Found {len(unprotected)} endpoints that don't require auth.")

    # Step 5: Export
    if args.export:
        export_results(args.export, results)
        print(f"[EXPORT] Results saved to {args.export}")

if __name__ == "__main__":
    main()
