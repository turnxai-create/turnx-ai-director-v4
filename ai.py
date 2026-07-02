from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)


SYSTEM_PROMPT = """
You are TURNX AI Director.

You are a world-class AI Creative Director.

Never act like a normal chatbot.

Only support these workflows:

IMAGES
- Nano Banana Pro 2
- Nano Banana Pro
- ChatGPT Image 2.0

VIDEO
- Veo 3.1
- Omni
- Seedance
- Grok

IMAGE TO VIDEO
- Veo 3.1
- Omni
- Seedance
- Grok

Rules:

• Think before writing.
• Build production-ready prompts.
• Keep prompts cinematic.
• Keep prompts realistic.
• Use professional camera language.
• Optimize specifically for the selected AI model.
• Return only the final prompt.
"""


def ask_ai(prompt: str) -> str:
    """Send a prompt to Groq and return the response."""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8,
        max_tokens=2048
    )

    return response.choices[0].message.content.strip()


def generate_image_prompt(model: str, prompt: str) -> str:

    request = f"""
IMAGE MODEL:
{model}

USER REQUEST:
{prompt}

Generate one premium image prompt optimized specifically for {model}.

Return only the final prompt.
"""

    return ask_ai(request)


def generate_video_prompt(model: str, prompt: str) -> str:

    request = f"""
VIDEO MODEL:
{model}

USER REQUEST:
{prompt}

Generate one premium cinematic video prompt optimized for {model}.

Include:

• Camera
• Lens
• Lighting
• Movement
• Composition
• Scene
• Mood

Return only the final prompt.
"""

    return ask_ai(request)


def generate_i2v_prompt(model: str, prompt: str) -> str:

    request = f"""
IMAGE TO VIDEO MODEL:
{model}

USER REQUEST:
{prompt}

Generate one premium Image-to-Video prompt.

Include:

• Character consistency
• Camera movement
• Motion
• Timing
• Scene transition
• Lighting

Return only the final prompt.
"""

    return ask_ai(request)
