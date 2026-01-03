import argparse
from pathlib import Path
import re

def validate_results(tex_file):
    print(f"Validating Results Chapter: {tex_file}")
    
    if not Path(tex_file).exists():
        print("❌ Error: Main chapter file not found.")
        return
        
    content = Path(tex_file).read_text()
    
    # Check for table inclusions
    expected_tables = ["model_performance", "xai_metrics_comparison", "llm_evaluation"]
    for tbl in expected_tables:
        if f"\\input{{tables/{tbl}}}" not in content:
            print(f"❌ Error: Missing table input for {tbl}")
        else:
            print(f"✅ Found table reference: {tbl}")
            
            # Check table content if file exists
            tbl_path = Path(tex_file).parent / "tables" / f"{tbl}.tex"
            if tbl_path.exists():
                tbl_content = tbl_path.read_text()
                # Simple check: Does it have numbers?
                if re.search(r"\d+\.\d+", tbl_content):
                    print(f"  ✅ Table {tbl} contains numerical data.")
                else:
                    print(f"  ⚠️ Warning: Table {tbl} seems to contain no data (check for '-' everywhere).")
            else:
                 print(f"❌ Error: Table file {tbl}.tex not found.")

    print("Validation complete.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tex-file", required=True)
    args = parser.parse_args()
    validate_results(args.tex_file)

if __name__ == "__main__":
    main()
