import json

input_path = "data/fairness/age/fairness_age_decision_pairs_hiring.jsonl"

with open(input_path, "r", encoding="utf-8") as f:
    raw = f.read()

raw_objects = raw.split('}\n{')

if raw_objects:
    raw_objects[0] = raw_objects[0] + "}"
    for i in range(1, len(raw_objects) - 1):
        raw_objects[i] = "{" + raw_objects[i] + "}"
    raw_objects[-1] = "{" + raw_objects[-1]

cleaned_lines = []
for obj in raw_objects:
    try:
        parsed = json.loads(obj)
        cleaned_lines.append(json.dumps(parsed, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print("Parse error:", e)
        print("Problematic content:", obj)

# Write to JSONL file
with open(input_path, "w", encoding="utf-8") as f:
    for line in cleaned_lines:
        f.write(line + "\n")

print(f"Conversion completed. Processed {len(cleaned_lines)} records and saved to {input_path}")
