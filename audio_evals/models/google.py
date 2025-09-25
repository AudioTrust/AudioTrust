import base64
import os
from copy import deepcopy
from typing import Dict, Any
import openai
import requests
from pydub import AudioSegment
import io
from audio_evals.base import PromptStruct
from audio_evals.models.model import APIModel
from audio_evals.utils import MIME_TYPE_MAP


class Gemini(APIModel):

    def __init__(
        self, model_name: str = "gemini-1.5-flash", sample_params: Dict[str, any] = None
    ):
        super().__init__(True, sample_params)
        self.model = model_name
        assert "GOOGLE_API_KEY" in os.environ, ValueError(
            "not found GOOGLE_API_KEY in your ENV"
        )
        self.key = os.environ["GOOGLE_API_KEY"]

    def _inference(self, prompt: PromptStruct, **kwargs) -> str:
        system_instruct = ""

        payload = {"contents": []}

        for content in deepcopy(prompt):
            if content["role"] == "user":
                for i, line in enumerate(content["contents"]):
                    if line["type"] == "text":
                        content["contents"][i] = {"text": line["value"]}
                    else:
                        file_path = line["value"]
                        file_extension = os.path.splitext(file_path)[1].lower()
                        if file_extension not in MIME_TYPE_MAP:
                            ValueError(
                                "only support [{}] type, but get {}".format(
                                    MIME_TYPE_MAP.keys(), file_extension
                                )
                            )

                        with open(file_path, "rb") as file:
                            file_content = file.read()
                            base64_encoded = base64.b64encode(file_content).decode(
                                "utf-8"
                            )

                        content["contents"][i] = {
                            "inline_data": {
                                "mime_type": MIME_TYPE_MAP[file_extension],
                                "data": base64_encoded,
                            }
                        }
            elif content["role"] == "system":
                system_instruct = content["content"]
                continue
            else:
                raise ValueError(
                    "only support role [user, system], but get {}".format(
                        content["role"]
                    )
                )

            content["parts"] = content["contents"]
            del content["contents"]
            payload["contents"].append(content)

        inf_args = {}
        if system_instruct:
            inf_args["systemInstruction"] = system_instruct
        if kwargs:
            payload["generationConfig"] = kwargs

        headers = {
            "Content-Type": "application/json",
        }
        url = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent?key={}".format(
            self.model, self.key
        )

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            msg_data = response.json()
        else:
            raise RuntimeError(
                f"请求失败，状态码: {response.status_code}, {response.text}"
            )

        return msg_data["candidates"][0]["content"]["parts"][0]["text"]

class GoogleAudio(APIModel):
    def __init__(self, model_name: str, sample_params: Dict[str, Any] = None):
        super().__init__(True, sample_params)
        self.model_name = model_name
        assert "GOOGLE_API_KEY" in os.environ, ValueError(
            "not found OPENAI_API_KEY in your ENV"
        )
        self.clint = openai.OpenAI(api_key=os.getenv("GOOGLE_API_KEY"), timeout=120)

    def read_audio_file(self, file_path: str) -> str:
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_data = wav_buffer.getvalue()
        encoded_string = base64.b64encode(wav_data).decode("utf-8")
        return encoded_string

    def _inference(self, prompt: PromptStruct, **kwargs) -> str:
        # system_instruct = ""

        # payload = {"contents": []}
        audio_data = None
        text_data = None

        for content in prompt:
            if content["role"] == "user":
                for i, line in enumerate(content["contents"]):
                    if line["type"] == "text":
                        # content["contents"][i] = {"text": line["value"]}
                        text_data = line["value"]
                    elif line["type"] == "audio":
                        file_path = line["value"]
                        audio_data = self.read_audio_file(file_path)

        assert audio_data is not None, ValueError(
            "not found audio data in your prompt, please check your prompt"
        )
        assert text_data is not None, ValueError(
            "not found text data in your prompt, please check your prompt"
        )
        completion = self.clint.chat.completions.create(
            model=self.model_name,
            # modalities=["text", "audio"],
            # audio={"voice": "alloy", "format": "wav"},  # 这个字段可以省略，除非生成音频
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text_data,
                        },
                        {
                            "type": "input_audio",
                            "input_audio": {"data": audio_data, "format": "wav"},
                        },
                    ],
                },
            ],
        )
        return completion.choices[0].message.content
