import argparse
import re
from pathlib import Path
import yaml

def validate_methodology(tex_file, bib_file, config_dir):
    """
    Validates the generated methodology chapter.
    1. Checks for required sections.
    2. Checks for consistent hyperparameters (sanity check against one known config).
    3. Checks bibliography entries.
    """
    print(f"Validating {tex_file}...")
    
    content = Path(tex_file).read_text()
    
    # 1. Required Sections
    required_sections = [
        "Experimental Design",
        "Model Architectures",
        "Explainability Techniques",
        "Evaluation Metrics Framework",
        "Reproducibility"
    ]
    
    for section in required_sections:
        if section not in content:
            print(f"❌ Missing required section: {section}")
        else:
            print(f"✅ Found section: {section}")
            
    # 2. Bibliography Check
    citations = re.findall(r"\\cite\{([^}]+)\}", content)
    bib_content = Path(bib_file).read_text()
    
    print(f"\nChecking {len(citations)} citations...")
    for cite in citations:
        # Simple check: is the key present in the bib file?
        if cite in bib_content:
            print(f"✅ Citation found: {cite}")
        else:
            print(f"❌ Warning: Citation not found in bib file: {cite}")
            
    # 3. Hyperparameter Spot Check (Example: Random Forest n_estimators)
    # We load the tex table file for hyperparameters
    hp_table_path = Path(tex_file).parent / "tables" / "hyperparameters.tex"
    if hp_table_path.exists():
        hp_content = hp_table_path.read_text()
        
        # Load actual config to compare
        try:
            rf_config = yaml.safe_load(open(Path(config_dir) / "exp1_adult_rf_lime.yaml"))
            if 'params' in rf_config['model'] and 'n_estimators' in rf_config['model']['params']:
                n_estimators = rf_config['model']['params']['n_estimators']
                
                # Simple string search in the latex table
                if f"& {n_estimators}" in hp_content or f"& {n_estimators} \\\\" in hp_content:
                     print(f"✅ Hyperparameter check passed: n_estimators={n_estimators} found in table.")
                else:
                     print(f"⚠️ Warning: Could not explicitly verify n_estimators={n_estimators} in table entry. Please check formatting.")
            else:
                print("ℹ️ Note: 'n_estimators' not found in config. Skipping strict validaton against config.")
                
                # Alternate check: Ensure table is not empty/dummy
                # LaTeX escapes underscores, so we search for n\_estimators
                if "n\\_estimators" in hp_content or "n_estimators" in hp_content:
                    print("✅ Table appears to contain 'n_estimators' (extracted from model file).")
                else:
                    print(f"⚠️ Warning: Table does not contain 'n_estimators'. Content snippet: {hp_content[:100]}...")

        except Exception as e:
            print(f"Could not perform hyperparameter spot check: {e}")
            
    print("\nValidation complete.")

def main():
    parser = argparse.ArgumentParser(description="Validate Methodology Chapter")
    parser.add_argument("--tex-file", required=True, help="Path to chapter_3_methodology.tex")
    parser.add_argument("--bib-file", default="docs/thesis/references.bib", help="Path to references.bib")
    parser.add_argument("--config-dir", default="configs/experiments", help="Path to config directory")
    args = parser.parse_args()
    
    validate_methodology(args.tex_file, args.bib_file, args.config_dir)

if __name__ == "__main__":
    main()
