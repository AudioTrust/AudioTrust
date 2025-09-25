python utils/inference2evaluation.py res/salmonn/rubstness-adversarial_Robustness/rubstness-inference-adversarial-Robustness-exp1-v1.jsonl data/rubstness/adversarial_Robustness.jsonl
python main.py --dataset rubstness-adversarial_Robustness --prompt rubstness-evaluation-adversarial-Robustness-exp1-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-adversarial_Robustness/rubstness-inference-adversarial-Robustness-exp3-v1.jsonl data/rubstness/adversarial_Robustness.jsonl
python main.py --dataset rubstness-adversarial_Robustness --prompt rubstness-evaluation-exp3-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-Audio_Quality_Variation/rubstness-inference-Audio-Quality-Variation-exp1-v1.jsonl data/rubstness/Audio_Quality_Variation.jsonl
python main.py --dataset rubstness-Audio_Quality_Variation --prompt rubstness-evaluation-Audio-Quality-Variation-exp1-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-Audio_Quality_Variation/rubstness-inference-Audio-Quality-Variation-exp3-v1.jsonl data/rubstness/Audio_Quality_Variation.jsonl
python main.py --dataset rubstness-Audio_Quality_Variation --prompt rubstness-evaluation-exp3-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-Background_Conversation/rubstness-inference-Background-Conversation-exp1-v1.jsonl data/rubstness/Background_Conversation.jsonl
python main.py --dataset rubstness-Background_Conversation --prompt rubstness-evaluation-Background-Conversation-exp1-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-Background_Conversation/rubstness-inference-Background-Conversation-exp3-v1.jsonl data/rubstness/Background_Conversation.jsonl
python main.py --dataset rubstness-Background_Conversation --prompt rubstness-evaluation-exp3-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-Environmental_Sound/rubstness-inference-Environmental-Sound-exp1-v1.jsonl data/rubstness/Environmental_Sound.jsonl
python main.py --dataset rubstness-Environmental_Sound --prompt rubstness-evaluation-Environmental-Sound-exp1-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-Environmental_Sound/rubstness-inference-Environmental-Sound-exp3-v1.jsonl data/rubstness/Environmental_Sound.jsonl
python main.py --dataset rubstness-Environmental_Sound --prompt rubstness-evaluation-exp3-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-Multiple_speakers/rubstness-inference-Multiple-speakers-exp1-v1.jsonl data/rubstness/Multiple_speakers.jsonl
python main.py --dataset rubstness-Multiple_speakers --prompt rubstness-evaluation-Multiple-speakers-exp1-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-Multiple_speakers/rubstness-inference-Multiple-speakers-exp3-v1.jsonl data/rubstness/Multiple_speakers.jsonl
python main.py --dataset rubstness-Multiple_speakers --prompt rubstness-evaluation-exp3-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-Noise_Interference/rubstness-inference-Noise-Interference-exp1-v1.jsonl data/rubstness/Noise_Interference.jsonl
python main.py --dataset rubstness-Noise_Interference --prompt rubstness-evaluation-Noise-Interference-exp1-v1 --model gpt-4o-salmonn

python utils/inference2evaluation.py res/salmonn/rubstness-Noise_Interference/rubstness-inference-Noise-Interference-exp3-v1.jsonl data/rubstness/Noise_Interference.jsonl
python main.py --dataset rubstness-Noise_Interference --prompt rubstness-evaluation-exp3-v1 --model gpt-4o-salmonn
