from ai import (
    generate_image_prompt,
    generate_video_prompt,
    generate_i2v_prompt,
)

from prompts import (
    IMAGE_PROMPT_TEMPLATE,
    VIDEO_PROMPT_TEMPLATE,
    IMAGE_TO_VIDEO_TEMPLATE,
    UGC_PROMPT_TEMPLATE,
)


class TurnxDirector:

    def __init__(self):
        pass

    # ==========================
    # IMAGE
    # ==========================

    def image(self, model, idea):

        prompt = IMAGE_PROMPT_TEMPLATE.format(
            model=model,
            idea=idea
        )

        return generate_image_prompt(
            model=model,
            prompt=prompt
        )

    # ==========================
    # VIDEO
    # ==========================

    def video(self, model, idea):

        prompt = VIDEO_PROMPT_TEMPLATE.format(
            model=model,
            idea=idea
        )

        return generate_video_prompt(
            model=model,
            prompt=prompt
        )

    # ==========================
    # IMAGE → VIDEO
    # ==========================

    def image_to_video(self, model, idea):

        prompt = IMAGE_TO_VIDEO_TEMPLATE.format(
            model=model,
            idea=idea
        )

        return generate_i2v_prompt(
            model=model,
            prompt=prompt
        )

    # ==========================
    # UGC
    # ==========================

    def ugc(self, idea):

        return UGC_PROMPT_TEMPLATE.format(
            idea=idea
        )

    # ==========================
    # ROUTER
    # ==========================

    def generate(
        self,
        mode,
        model,
        idea
    ):

        mode = mode.lower()

        if mode == "image":
            return self.image(model, idea)

        if mode == "video":
            return self.video(model, idea)

        if mode == "i2v":
            return self.image_to_video(model, idea)

        if mode == "ugc":
            return self.ugc(idea)

        return "Invalid generation mode."


director = TurnxDirector()
