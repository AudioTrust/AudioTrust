import json
import os
import sys
from pathlib import Path

def process_files(inference_file, dataset_file):
    with open(inference_file, 'r', encoding='utf-8') as f:
        inference_lines = f.readlines()
    
    with open(dataset_file, 'r', encoding='utf-8') as f:
        dataset_lines = f.readlines()
    
    output_file = Path(dataset_file).stem + '_with_responses.jsonl'
    
    inference_results = {}
    for line in inference_lines:
        try:
            data = json.loads(line)
            if data.get('type') == 'inference':
                inference_results[data['id']] = data['data']['content']
        except json.JSONDecodeError:
            continue
    
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for line in dataset_lines:
            try:
                data = json.loads(line)
                line_id = dataset_lines.index(line)
                if line_id in inference_results:
                    data['ModelResponse'] = inference_results[line_id]
                out_f.write(json.dumps(data, ensure_ascii=False) + '\n')
            except json.JSONDecodeError:
                continue
    os.rename(output_file, dataset_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python inference2evaluation.py <inference_result_file> <dataset_file>")
        sys.exit(1)
    
    inference_file = sys.argv[1]
    dataset_file = sys.argv[2]
    
    process_files(inference_file, dataset_file)