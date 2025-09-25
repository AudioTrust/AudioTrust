import os
import json
import argparse
import torchaudio
import torchaudio.functional as F
import torch
from tqdm import tqdm

def concat_audio(filename1, filename2, save_path):
    waveform1, sample_rate1 = torchaudio.load(filename1)
    waveform2, sample_rate2 = torchaudio.load(filename2)

    if sample_rate1 != sample_rate2:
        waveform2 = F.resample(waveform2, sample_rate2, sample_rate1)

    channels1 = waveform1.shape[0]
    channels2 = waveform2.shape[0]

    if channels1 != channels2:
        if channels2 < channels1:
            waveform2 = waveform2.repeat(channels1 // channels2, 1)
        else:
            waveform2 = waveform2[:channels1, :]

    combined = torch.cat((waveform1, waveform2), dim=1)

    torchaudio.save(save_path, combined, sample_rate1)

def process_jsonl(jsonl_path, key1, key2):
    output_lines = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in tqdm(f):
            item = json.loads(line)
            path1 = item[key1]
            path2 = item[key2]

            dir1 = os.path.dirname(path1)
            base1 = os.path.basename(path1).split(".")[0]
            base2 = os.path.basename(path2).split(".")[0]
            save_name = f"{base1}_{base2}.wav"
            save_path = os.path.join(dir1, save_name)

            concat_audio(path1, path2, save_path)

            key_num = key2.replace("WavPath","")
            new_key = f"{key1}{key_num}"
            item[new_key] = save_path

            output_lines.append(json.dumps(item, ensure_ascii=False))

    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for line in output_lines:
            f.write(line + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Concatenate audio paths in a jsonl file")
    parser.add_argument('jsonl_path', type=str, help='Path to the jsonl file')
    parser.add_argument('key1', type=str, help='Key for the first audio path')
    parser.add_argument('key2', type=str, help='Key for the second audio path')
    args = parser.parse_args()

    process_jsonl(args.jsonl_path, args.key1, args.key2)
