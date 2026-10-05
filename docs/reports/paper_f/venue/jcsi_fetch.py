"""Download the PDFs of recent JCSI issues and convert them to text."""
import re, subprocess, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).parent
BASE = "https://ph.pollub.pl/index.php/jcsi"
ISSUES = {40: 779, 39: 768, 38: 758, 37: 752, 36: 706}
UA = {"User-Agent": "Mozilla/5.0 (research reading of published open-access articles)"}


def get(url):
    # curl uses the system certificate store; Python's own store rejects this network's chain
    return subprocess.run(["curl", "-sSL", "--max-time", "90", "-A", UA["User-Agent"], url],
                          capture_output=True, check=True).stdout


rows = []
for vol, iid in ISSUES.items():
    html = get(f"{BASE}/issue/view/{iid}").decode("utf-8", "replace")
    pairs = sorted(set(re.findall(r"/article/view/(\d+)/(\d+)", html)))
    print(vol, len(pairs), "galleys", flush=True)
    for art, gal in pairs:
        pdf = HERE / f"v{vol}_{art}.pdf"
        if not pdf.exists():
            try:
                pdf.write_bytes(get(f"{BASE}/article/download/{art}/{gal}"))
            except Exception as e:  # noqa: BLE001
                print("FAIL", art, e)
                continue
            time.sleep(1)
        subprocess.run(["pdftotext", "-layout", str(pdf), str(pdf.with_suffix(".txt"))], check=False)
print("done")
