"""
TURNX AI Director Prompt Engine
V4
"""

IMAGE_PROMPT_TEMPLATE = """
You are an elite AI Creative Director.

Create one production-ready image prompt.

AI MODEL:
{model}

USER IDEA:
{idea}

Requirements:

- Ultra photorealistic
- 8K quality
- Real skin pores
- Natural facial asymmetry
- FACS expressions
- Cinematic lighting
- High dynamic range
- Professional color grading
- Correct anatomy
- Premium composition
- Sharp focus
- Rich environmental details
- Physically accurate shadows
- Optimized specifically for {model}

Return ONLY the final prompt.
"""


VIDEO_PROMPT_TEMPLATE = """
You are an elite AI Film Director.

Create one production-ready cinematic video prompt.

VIDEO MODEL:
{model}

USER IDEA:
{idea}

Requirements:

- Strong hook
- Scene description
- Camera movement
- Lens
- Lighting
- Character movement
- Dialogue (if needed)
- Environment
- Mood
- Ending
- Cinematic realism
- Optimized specifically for {model}

Return ONLY the final prompt.
"""


IMAGE_TO_VIDEO_TEMPLATE = """
You are an elite AI Motion Director.

Create one professional Image-to-Video prompt.

VIDEO MODEL:
{model}

SOURCE IMAGE:
Character must remain identical.

USER IDEA:
{idea}

Requirements:

- Preserve identity
- Camera movement
- Character movement
- Eye movement
- Breathing
- Lip sync (when needed)
- Scene transitions
- Cinematic lighting
- Motion consistency
- Optimized specifically for {model}

Return ONLY the final prompt.
"""


UGC_PROMPT_TEMPLATE = """
Create a premium UGC advertisement.

Product:
{idea}

Requirements:

- Hook
- Problem
- Solution
- Product demonstration
- Result
- Soft CTA

Generate natural dialogue.

Keep it realistic.

Return ONLY the final prompt.
"""


CHARACTER_LOCK_TEMPLATE = """
LOCK THIS CHARACTER.

Never change:

- Face
- Skin tone
- Hair
- Body shape
- Age
- Facial proportions

Character Description:

{character}

This identity must remain consistent in every generated image and video.
"""


NEGATIVE_PROMPT = """
Avoid:

Low quality,
blurry,
extra fingers,
extra hands,
extra limbs,
deformed face,
bad anatomy,
cartoon look,
CGI look,
plastic skin,
oversaturated colors,
duplicate people,
text,
watermark,
logo,
artifacts.
"""
