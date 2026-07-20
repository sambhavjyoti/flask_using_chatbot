import os
from base64 import b64encode
from io import BytesIO

from groq import Groq
from deep_translator import GoogleTranslator
from gtts import gTTS


api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Add it to your environment or a local .env file."
    )

client = Groq(api_key=api_key)


def ask_ai(question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Keep answers concise."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.7,
        max_tokens=500,
    )

    answer = response.choices[0].message.content

    # Translate to Hindi
    hindi = GoogleTranslator(source="en", target="hi").translate(answer)

    # Keep audio in memory: Vercel Function filesystems are read-only.
    tts = gTTS(text=hindi, lang="hi")
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_base64 = b64encode(audio_file.getvalue()).decode("ascii")

    return answer, hindi, audio_base64
