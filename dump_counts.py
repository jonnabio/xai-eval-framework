import glob, json
for out in sorted(glob.glob("experiments/recovery/phase1/results/*/*/*/results.json")):
    with open(out) as f:
        print(f"{out}: {len(json.load(f).get('instance_evaluations',[]))}")
