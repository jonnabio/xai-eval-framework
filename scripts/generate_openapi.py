
import os
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.api.main import app

def generate_openapi():
    print("Generating OpenAPI schema...")
    openapi_schema = app.openapi()
    
    output_path = Path("docs/openapi.json")
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    print(f"✅ Schema exported to {output_path}")

if __name__ == "__main__":
    generate_openapi()
