#!/usr/bin/env python3

import argparse
import json
import yaml
from modules.finder import find_api_docs
from modules.parser import parse_swagger, parse_openapi

def print_banner():
    print("""
                     _      _   
                    | |    | |  
 ___  ___ __ _ _ __ | | ___| |_ 
/ __|/ __/ _` | '_ \| |/ _ \ __|
\__ \ (_| (_| | | | | |  __/ |_ 
|___/\___\__,_|_| |_|_|\___|\__|                    
[ API Recon Toolkit by Lucas ]
    """)

def main():
    parser = argparse.ArgumentParser(description="Scanlet - API Recon Toolkit")
    parser.add_argument("-u", "--url", help="Base API URL (e.g. https://api.example.com)", required=True)
    parser.add_argument("-c", "--cors", help="Check for CORS misconfigurations", action="store_true")
    parser.add_argument("-a", "--auth", help="Check for unauthenticated endpoints", action="store_true")
    parser.add_argument("-e", "--export", help="Export results to a file (e.g. output.json)")
    args = parser.parse_args()

    print_banner()
    print(f"[SCANLET] Target: {args.url}")

    # Step 1: Vind API documentatie
    api_doc = find_api_docs(args.url)
    if not api_doc:
        print("[!] No API documentation found.")
        return

    print(f"[+] Found API doc: {api_doc['path']} ({api_doc['type']})")

    # Step 2: Parse API documentatie naar endpoints
    try:
        if api_doc["type"] == "swagger":
            parsed = json.loads(api_doc["content"])
            endpoints = parse_swagger(parsed)
        elif api_doc["type"] == "openapi":
            parsed = yaml.safe_load(api_doc["content"])
            endpoints = parse_openapi(parsed)
        else:
            print("[!] Unknown doc type.")
            return
    except Exception as e:
        print("[!] Failed to parse API documentation:", str(e))
        return

    print(f"[✓] Parsed {len(endpoints)} endpoints.")
    for ep in endpoints:
        print(f"    {ep['method']:6} {ep['path']}")

    # Resulten structuren
    results = {
        "url": args.url,
        "doc_path": api_doc["path"],
        "doc_type": api_doc["type"],
        "endpoints": endpoints
    }

    # CORS en AUTH modules komen later...

    # Stap 3: Exporteren
    if args.export:
        try:
            with open(args.export, "w") as f:
                json.dump(results, f, indent=2)
            print(f"[✓] Results saved to {args.export}")
        except Exception as e:
            print("[!] Export failed:", str(e))

if __name__ == "__main__":
    main()
