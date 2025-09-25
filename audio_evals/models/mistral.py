import os
from openai import OpenAI
from typing import Dict
import base64
import json
from audio_evals.base import PromptStruct
from audio_evals.models.model import APIModel
import requests
from mistralai import Mistral


class MistralAi(APIModel):
    def __init__(self, model="voxtral-small-2507", sample_params: Dict[str, any] = None):
        super().__init__(True, sample_params)
        self.model = model
        self.api_key = os.environ["MISTRAL_API_KEY"]
        assert self.api_key is not None and self.api_key != "", "MISTRAL_API_KEY 环境变量未设置或为空"
        self.client = Mistral(api_key=self.api_key)

    def encode_audio(self, audio_file):
        with open(audio_file, "rb") as f:
            content = f.read()
        audio_base64 = base64.b64encode(content).decode('utf-8')

        return audio_base64

    def _inference(self, prompt: PromptStruct, **kwargs) -> str:
        audio_file = ""
        for content in prompt:
            if content["role"] == "user":
                for line in content["contents"]:
                    if line["type"] == "audio":
                        audio_file = line["value"]
                        break

        prompt = ""
        for content in prompt:
            if content["role"] == "user":
                for line in content["contents"]:
                    if line["type"] == "text":
                        prompt = line["value"]
                        break
        
        assert os.path.exists(audio_file), f"{audio_file} is not exists."

        audio_base64 = self.encode_audio(audio_file)

        chat_response = self.client.chat.complete(
            model=self.model,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": audio_base64,
                    },
                    {
                        "type": "text",
                        "text": prompt
                    },
                ]
            }],
        )


        answer = chat_response.choices[0].message.content

        return json.dumps({"text": answer}, ensure_ascii=False)

