from abc import ABCMeta, abstractmethod

from talkgenerator.slide import slides
from talkgenerator.util import generator_util


class SlideGenerator(metaclass=ABCMeta):
    """ Generating Slide objects using a list of generators """

    def __init__(self, slide_content_generator):
        """ The given content_providers is a function that when called,
        generates all of the arguments for the slide creator"""
        self._slide_content_generator = slide_content_generator

    @property
    @abstractmethod
    def slide_type(self):
        """ The function converting it to a Slide object """
        pass

    @classmethod
    def of(cls, *generators):
        return cls(CombinedSlideGenerator(*generators))

    def generate_slide(self, presentation_context, used) -> (slides.Slide, list):
        """ Generates the slide using the given generators """
        generated = self._slide_content_generator(presentation_context)
        if is_different_enough(generated, used):
            return self.slide_type(*generated), generated


class TitleSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, subtitle_generator):
        return cls(CombinedSlideGenerator(title_generator, subtitle_generator))

    @property
    def slide_type(self):
        return slides.TitleSlide


class LarqeQuoteSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, text_generator, background_image_generator):
        return cls(
            CombinedSlideGenerator(
                title_generator, text_generator, background_image_generator
            )
        )

    @property
    def slide_type(self):
        return slides.LarqeQuoteSlide


class ImageSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, image_generator=None, original_image_size=True):
        return cls(
            CombinedSlideGenerator(
                title_generator,
                image_generator,
                generator_util.StaticGenerator(original_image_size),
            )
        )

    @classmethod
    def of_tupled_captioned_image(cls, tuple_1_generator, original_image_size=True):
        return cls(
            TupledCaptionedImageGenerator(tuple_1_generator, original_image_size)
        )

    @property
    def slide_type(self):
        return slides.ImageSlide


class TupledCaptionedImageGenerator(object):
    def __init__(self, tuple_1_generator, original_image_size=True):
        self._tuple_1_generator = tuple_1_generator
        self._original_image_size = original_image_size

    def __call__(self, presentation_context):
        generated_tuple_1 = self._tuple_1_generator(presentation_context)
        return generated_tuple_1[0], generated_tuple_1[1], self._original_image_size


class FullImageSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, image_generator=None, original_image_size=True):
        return cls(
            CombinedSlideGenerator(
                title_generator,
                image_generator,
                generator_util.StaticGenerator(original_image_size),
            )
        )

    @property
    def slide_type(self):
        return slides.FullImageSlide


class TwoColumnImageSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(
        cls,
        title_generator,
        caption_1_generator,
        image_or_text_1_generator,
        caption_2_generator,
        image_or_text_2_generator,
        original_image_size=True,
    ):
        return cls(
            CombinedSlideGenerator(
                title_generator,
                caption_1_generator,
                image_or_text_1_generator,
                caption_2_generator,
                image_or_text_2_generator,
                generator_util.StaticGenerator(original_image_size),
            )
        )

    @classmethod
    def of_tupled_captioned_images(
        cls,
        title_generator,
        tuple_1_generator,
        tuple_2_generator,
        original_image_size=True,
    ):
        return cls(
            TwoTupledCaptionedImagesGenerator(
                title_generator,
                tuple_1_generator,
                tuple_2_generator,
                original_image_size,
            )
        )

    @classmethod
    def of_images_and_tupled_captions(
        cls,
        title_generator,
        captions_generator,
        image_1_generator,
        image_2_generator,
        original_image_size=True,
    ):
        return cls(
            TwoImagesAndTupledCaptions(
                title_generator,
                captions_generator,
                image_1_generator,
                image_2_generator,
                original_image_size,
            )
        )

    @property
    def slide_type(self):
        return slides.TwoColumnImageSlide


class TwoTupledCaptionedImagesGenerator(SlideGenerator):
    def __init__(
        self,
        title_generator,
        tuple_1_generator,
        tuple_2_generator,
        original_image_size=True,
    ):
        super().__init__(self)
        self._title_generator = title_generator
        self._tuple_1_generator = tuple_1_generator
        self._tuple_2_generator = tuple_2_generator
        self._original_image_size = original_image_size

    def __call__(self, presentation_context):
        generated_tuple_1 = self._tuple_1_generator(presentation_context)
        generated_tuple_2 = self._tuple_2_generator(presentation_context)
        return (
            self._title_generator(presentation_context),
            generated_tuple_1[0],
            generated_tuple_1[1],
            (generated_tuple_2[0]),
            generated_tuple_2[1],
            self._original_image_size,
        )

    @property
    def slide_type(self):
        return slides.TwoColumnImageSlide


class TwoImagesAndTupledCaptions(SlideGenerator):
    def __init__(
        self,
        title_generator,
        captions_generator,
        image_1_generator,
        image_2_generator,
        original_image_size=True,
    ):
        super().__init__(self)
        self._title_generator = title_generator
        self._captions_generator = captions_generator
        self._image_1_generator = image_1_generator
        self._image_2_generator = image_2_generator
        self._original_image_size = original_image_size

    def __call__(self, presentation_context):
        generated_tuple = self._captions_generator(presentation_context)
        return (
            self._title_generator(presentation_context),
            generated_tuple[0],
            self._image_1_generator(presentation_context),
            generated_tuple[1],
            self._image_2_generator(presentation_context),
            self._original_image_size,
        )

    @property
    def slide_type(self):
        return slides.TwoColumnImageSlide


class ThreeColumnImageSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(
        cls,
        title_generator,
        caption_1_generator,
        image_or_text_1_generator,
        caption_2_generator,
        image_or_text_2_generator,
        caption_3_generator,
        image_or_text_3_generator,
        original_image_size=True,
    ):
        return cls(
            CombinedSlideGenerator(
                title_generator,
                caption_1_generator,
                image_or_text_1_generator,
                caption_2_generator,
                image_or_text_2_generator,
                caption_3_generator,
                image_or_text_3_generator,
                generator_util.StaticGenerator(original_image_size),
            )
        )

    @classmethod
    def of_tupled_captioned_images(
        cls,
        title_generator,
        tuple_1_generator,
        tuple_2_generator,
        tuple_3_generator,
        original_image_size=True,
    ):
        return cls(
            ThreeTupledCaptionedImagesGenerator(
                title_generator,
                tuple_1_generator,
                tuple_2_generator,
                tuple_3_generator,
                original_image_size,
            )
        )

    @classmethod
    def of_images_and_tupled_captions(
        cls,
        title_generator,
        captions_generator,
        image_1_generator,
        image_2_generator,
        image_3_generator,
        original_image_size=True,
    ):
        return cls(
            ThreeImagesAndTupledCaptions(
                title_generator,
                captions_generator,
                image_1_generator,
                image_2_generator,
                image_3_generator,
                original_image_size,
            )
        )

    @property
    def slide_type(self):
        return slides.ThreeColumnImageSlide


class ThreeTupledCaptionedImagesGenerator(SlideGenerator):
    def __init__(
        self,
        title_generator,
        tuple_1_generator,
        tuple_2_generator,
        tuple_3_generator,
        original_image_size=True,
    ):
        super().__init__(self)
        self._title_generator = title_generator
        self._tuple_1_generator = tuple_1_generator
        self._tuple_2_generator = tuple_2_generator
        self._tuple_3_generator = tuple_3_generator
        self._original_image_size = original_image_size

    def __call__(self, presentation_context):
        generated_tuple_1 = self._tuple_1_generator(presentation_context)
        generated_tuple_2 = self._tuple_2_generator(presentation_context)
        generated_tuple_3 = self._tuple_3_generator(presentation_context)
        return (
            self._title_generator(presentation_context),
            generated_tuple_1[0],
            generated_tuple_1[1],
            (generated_tuple_2[0]),
            generated_tuple_2[1],
            generated_tuple_3[0],
            generated_tuple_3[1],
            self._original_image_size,
        )

    @property
    def slide_type(self):
        return slides.ThreeColumnImageSlide


class ThreeImagesAndTupledCaptions(SlideGenerator):
    def __init__(
        self,
        title_generator,
        captions_generator,
        image_1_generator,
        image_2_generator,
        image_3_generator,
        original_image_size=True,
    ):
        super().__init__(self)
        self._title_generator = title_generator
        self._captions_generator = captions_generator
        self._image_1_generator = image_1_generator
        self._image_2_generator = image_2_generator
        self._image_3_generator = image_3_generator
        self._original_image_size = original_image_size

    def __call__(self, presentation_context):
        generated_tuple = self._captions_generator(presentation_context)
        return (
            self._title_generator(presentation_context),
            generated_tuple[0],
            self._image_1_generator(presentation_context),
            generated_tuple[1],
            self._image_2_generator(presentation_context),
            generated_tuple[2],
            self._image_3_generator(presentation_context),
            self._original_image_size,
        )

    @property
    def slide_type(self):
        return slides.ThreeColumnImageSlide


class ChartSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(
        cls,
        title_generator,
        chart_type_generator,
        chart_data_generator,
        chart_modifier=None,
    ):
        return cls(
            CombinedSlideGenerator(
                title_generator,
                chart_type_generator,
                chart_data_generator,
                generator_util.StaticGenerator(chart_modifier),
            )
        )

    @property
    def slide_type(self):
        return slides.ChartSlide


# HELPERS


class CombinedSlideGenerator(object):
    def __init__(self, *generators):
        # print("CombinedGenerator:", self, generators)
        self._generators = generators

    def __call__(self, presentation_context):
        # print("CombinedGenerator:", self)
        return [
            content_generator(presentation_context) if content_generator else None
            for content_generator in self._generators
        ]


def is_different_enough(generated, used):
    (used_elements, allowed_repeated_elements) = used
    return is_different_enough_for_allowed_repeated(
        generated, used_elements, allowed_repeated_elements
    )


def is_different_enough_for_allowed_repeated(
    generated, used_elements, allowed_repeated_elements
):
    if generated:
        if not used_elements:
            return True
        intersection = set(generated) & used_elements
        return allowed_repeated_elements >= len(intersection)
    return False
