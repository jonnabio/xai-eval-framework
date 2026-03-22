import os
import json

base_dir = r"c:\Users\jonna\OneDrive\Documentos\Code__Projects_Local\xai-eval-framework\experiments\exp2_scaled\results"
total = 0
valid = 0
invalid = 0

for root, _, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".json"):
            total += 1
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    # just checking if it can be parsed
                    valid += 1
            except Exception as e:
                invalid += 1
                print(f"Invalid: {path} - {e}")

print(f"Total .json files found: {total}")
print(f"Valid .json files: {valid}")
print(f"Invalid (malformed/empty) .json files: {invalid}")
