import os

data_dir = "data/safety"
prefix = "safety"
save_path = "registry/dataset/safety.yaml"

items = []

for fname in sorted(os.listdir(data_dir)):
    if fname.endswith(".jsonl"):
        name = f"{prefix}_{fname[:-6]}"
        item = f"""{name}:
  class: audio_evals.dataset.dataset.JsonlFile
  args:
    default_task: {prefix}
    f_name: {data_dir}/{fname}
    ref_col: WavPath1
"""
        items.append(item)

with open(save_path, "w", encoding="utf-8") as f:
    f.write("\n\n".join(items))
