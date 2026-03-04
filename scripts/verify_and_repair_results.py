import json
import os
import re
from pathlib import Path

def is_printable(char):
    """Check if a character is printable and not a control char (except \n, \r, \t)."""
    code = ord(char)
    return (code >= 32 and code <= 126) or char in '\n\r\t'

def clean_json_content(content_bytes):
    """Deep clean bytes by removing nulls and escaping control characters."""
    # 1. Strip null bytes completely
    clean_bytes = content_bytes.replace(b'\x00', b'')
    
    # 2. Convert to string and handle other control characters
    try:
        text = clean_bytes.decode('utf-8', errors='ignore')
    except UnicodeDecodeError:
        text = clean_bytes.decode('latin-1', errors='ignore')
        
    # Remove characters from U+0000 to U+001F (excluding \n, \r, \t)
    # These often break JSON parsers if not escaped
    def clean_char(m):
        c = m.group(0)
        if c in '\n\r\t':
            return c
        return '' # Strip other control chars
        
    text = re.sub(r'[\x00-\x1f]', clean_char, text)
    return text

def verify_and_fix():
    experiments_dir = Path("experiments")
    json_files = list(experiments_dir.rglob("results.json"))
    print(f"Checking {len(json_files)} files...")
    
    corrupt_count = 0
    fixed_count = 0
    total_instances = 0
    
    for p in json_files:
        try:
            with open(p, 'r') as f:
                data = json.load(f)
            total_instances += len(data.get("instance_evaluations", []))
        except (json.JSONDecodeError, UnicodeDecodeError, Exception) as e:
            print(f"CORRUPT: {p} - {str(e)[:100]}")
            corrupt_count += 1
            
            # Attempt FIX
            try:
                with open(p, 'rb') as rb:
                    raw = rb.read()
                
                cleaned_text = clean_json_content(raw)
                
                # Verify cleaned text
                data = json.loads(cleaned_text)
                
                # Save fixed version
                with open(p, 'w') as f:
                    json.dump(data, f)
                
                print(f"  -> FIXED {p}")
                fixed_count += 1
                total_instances += len(data.get("instance_evaluations", []))
            except Exception as fix_e:
                print(f"  !! FAILED TO FIX: {fix_e}")
                
    print("-" * 30)
    print("Scan complete.")
    print(f"Healthy files: {len(json_files) - corrupt_count + fixed_count}")
    print(f"Fixed: {fixed_count}")
    print(f"Still Corrupt: {corrupt_count - fixed_count}")
    print(f"Total Data Points: {total_instances}")

if __name__ == "__main__":
    verify_and_fix()
