"""
This module represents the abstractions of a presentation schema (responsible for specifying how to generate a
presentation), and slide generators, that have functions for generating slides along with some other metadata.

"""
import time
import logging
from multiprocessing.pool import ThreadPool
import random
from typing import List, Collection, Callable, Dict, Union, Optional

from talkgenerator.datastructures.image_data import ImageData
from talkgenerator.schema.slide_topic_generators import SlideSeedGenerator
from talkgenerator.datastructures.slide_generator_data import (
    _filter_generated_elements,
    SlideGeneratorData,
)
from talkgenerator.slide import slide_generator_types
from talkgenerator.slide.slide_deck import SlideDeck
from talkgenerator.util import random_util

logger = logging.getLogger("talkgenerator")


class PresentationSchema:
    """ Class responsible for determining which slide generators to use in a presentation, and how the (topic) seed for
    each slide is generated """

    def __init__(
        self,
        powerpoint_creator,
        seed_generator: Callable[[List[str], int], SlideSeedGenerator],
        title_generator,
        slide_generators: List[SlideGeneratorData],
        max_allowed_tags=None,
        ignore_weights=False,
    ):
        self._powerpoint_creator = powerpoint_creator
        self._seed_generator = seed_generator
        self._slide_generators = slide_generators
        if max_allowed_tags is None:
            max_allowed_tags = {}
        self._max_allowed_tags = max_allowed_tags
        self._ignore_weights = ignore_weights
        self._title_generator = title_generator

    def generate_presentation(
        self,
        topics: List[str],
        num_slides: int,
        presenter=None,
        title: str = None,
        parallel: bool = False,
        int_seed: int = None,
    ):
        """Generate a presentation about a certain topic with a certain number of slides"""

        # Generate random talk title
        if not title or title is None:
            if self._title_generator is not None:
                title = self._title_generator({"seed": topics[0]})
            else:
                title = "About " + topics[0]

        # Create new presentation
        presentation = self._powerpoint_creator()
        slide_deck = SlideDeck(num_slides)

        # Create the topic-for-each-slide generator
        seed_generator = self._seed_generator(topics, num_slides)

        # Create main presentation_context
        main_presentation_context = {
            "topic": topics[0],
            "topics": topics,
            "presenter": presenter,
            "title": title,
        }

        used_tags = {}
        used_elements = set()

        # Generate
        if parallel:
            self._generate_slide_deck_parallel(
                slide_deck,
                num_slides,
                main_presentation_context,
                seed_generator,
                used_elements,
                used_tags,
                int_seed,
            )
        else:
            self._generate_slide_deck(
                slide_deck,
                num_slides,
                main_presentation_context,
                seed_generator,
                used_elements,
                used_tags,
                int_seed,
            )

        slide_deck.save_to_powerpoint(presentation)
        return presentation, slide_deck

    def _generate_slide_deck_parallel(
        self,
        slide_deck,
        num_slides: int,
        main_presentation_context,
        seed_generator: SlideSeedGenerator,
        used_elements,
        used_tags: Dict[str, int],
        int_seed: int,
    ):
        logger.info("Generating the slide deck in parallel")
        slide_nrs_to_generate = range(num_slides)

        generated_results = [None] * num_slides

        while len(slide_nrs_to_generate) > 0:
            if len(slide_nrs_to_generate) < num_slides:
                logger.info(
                    "Regenerating the following slides: " + str(slide_nrs_to_generate)
                )

            with ThreadPool(processes=num_slides) as pool:
                all_slide_results = pool.map(
                    SlideGeneratorContext(
                        presentation_schema=self,  # reference the enclosing presentation schema
                        presentation_context=main_presentation_context,
                        seed_generator=seed_generator,
                        num_slides=num_slides,
                        used_elements=used_elements,
                        prohibited_generators=self._calculate_prohibited_generators(
                            used_tags, num_slides
                        ),
                        int_seed=int_seed,
                    ),
                    slide_nrs_to_generate,
                )
                slide_nrs_to_generate = []
                for slide_result in all_slide_results:
                    if slide_result:
                        (
                            slide,
                            generated_elements,
                            slide_generator_data,
                            slide_nr,
                        ) = slide_result
                        generated_results[slide_nr] = slide_result

            # Check Constraints

            for i in range(num_slides):
                if not slide_deck.has_slide_nr(i):
                    if not generated_results[i]:
                        slide_nrs_to_generate.append(i)
                    else:
                        success = self._update_slide_deck_with_generated_result(
                            slide_deck,
                            generated_results[i],
                            used_elements,
                            used_tags,
                            num_slides,
                        )
                        if not success:
                            slide_nrs_to_generate.append(i)

        return slide_deck

    def _generate_slide_deck(
        self,
        slide_deck,
        num_slides,
        main_presentation_context,
        seed_generator,
        used_elements,
        used_tags,
        int_seed=None,
    ):
        for slide_nr in range(num_slides):
            # Generate the slide
            slide_results = self.generate_slide(
                presentation_context=create_slide_presentation_context(
                    main_presentation_context, seed_generator.get_seed(slide_nr)
                ),
                slide_nr=slide_nr,
                num_slides=num_slides,
                used_elements=used_elements,
                prohibited_generators=self._calculate_prohibited_generators(
                    used_tags, num_slides
                ),
                int_seed=int_seed,
            )

            if slide_results:
                success = self._update_slide_deck_with_generated_result(
                    slide_deck, slide_results, used_elements, used_tags, num_slides
                )
                assert success

        return slide_deck

    def _update_slide_deck_with_generated_result(
        self, slide_deck, generated_result, used_elements, used_tags, num_slides
    ):
        slide, generated_elements, slide_generator_data, slide_nr = generated_result
        # Check if allowed according to repeated elements & slide type tags
        if slide_generator_types.is_different_enough_for_allowed_repeated(
            generated_elements,
            used_elements,
            slide_generator_data.get_allowed_repeated_elements(),
        ) and slide_generator_data not in self._calculate_prohibited_generators(
            used_tags, num_slides
        ):
            slide_deck.add_slide(slide_nr, slide)
            self._update_used_elements(
                used_elements, used_tags, generated_elements, slide_generator_data
            )
            return True
        return False

    @classmethod
    def _update_used_elements(
        cls, used_elements, used_tags, generated_elements, slide_generator_data
    ):
        # Add generated items to used_elements list
        generated_elements = set(generated_elements)
        _filter_generated_elements(generated_elements)
        used_elements.update(generated_elements)

        # Add generator tags to used_tags list
        add_tags(used_tags, slide_generator_data.get_tags())

    def generate_slide(
        self,
        presentation_context,
        slide_nr,
        num_slides,
        used_elements=None,
        prohibited_generators=None,
        int_seed=None,
    ):
        if int_seed is not None:
            random.seed(int_seed + slide_nr)

        # Default arguments: avoid mutable defaults
        if prohibited_generators is None:
            prohibited_generators = set()

        # Select the slide generator to generate with
        generator = self._select_generator(slide_nr, num_slides, prohibited_generators)

        start_time = time.time()
        if generator:
            logger.info(
                "* Generating slide {} about {} using {} *".format(
                    slide_nr + 1, presentation_context["seed"], generator
                )
            )
            slide_result = generator.generate(presentation_context, used_elements)

            # Try again if slide is None, and prohibit generator for generating for this topic
            if not bool(slide_result):
                end_time = time.time()
                logger.info(
                    "Failed to generate after {} seconds using: {}".format(
                        round(end_time - start_time, 2), generator
                    )
                )
                prohibited_generators.add(generator)

                return self.generate_slide(
                    presentation_context=presentation_context,
                    slide_nr=slide_nr,
                    num_slides=num_slides,
                    used_elements=used_elements,
                    prohibited_generators=prohibited_generators,
                )

            slide, generated_elements = slide_result
            end_time = time.time()
            logger.info(
                "* Finished generating slide {} about {} using {} in {} seconds *".format(
                    slide_nr + 1,
                    presentation_context["seed"],
                    generator,
                    round(end_time - start_time, 2),
                )
            )
            return slide, generated_elements, generator, slide_nr
        else:
            logger.warning(
                "No generator found to generate about ",
                presentation_context["Presentation"],
            )

    def _select_generator(self, slide_nr, total_slides, prohibited_generators):
        """Select a generator for a certain slide number"""
        if self._ignore_weights:
            return random_util.choice_optional(self._slide_generators)
        return random_util.weighted_random(
            self._get_weighted_generators_for_slide_nr(
                slide_nr, total_slides, prohibited_generators
            )
        )

    def _get_weighted_generators_for_slide_nr(
        self, slide_nr, total_slides, prohibited_generators
    ):
        weighted_generators = []
        for i in range(len(self._slide_generators)):
            generator = self._slide_generators[i]
            if generator in prohibited_generators:
                continue
            weighted_generator = (
                generator.get_weight_for(slide_nr, total_slides),
                generator,
            )
            weighted_generators.append(weighted_generator)

        if len(weighted_generators) == 0:
            raise ValueError("No generators left to generate slides with!")

        return weighted_generators

    def _calculate_prohibited_generators(
        self, used_tags: Dict[str, int], num_slides: int
    ):
        prohibited_tags = set()
        for key, value in used_tags.items():
            if key in self._max_allowed_tags:
                max_tag = self._max_allowed_tags[key]

                # Assumes integer maximum
                max_number_of_slides = max_tag

                # If Procentua/Double ratio:
                if 0 < max_tag < 1:
                    max_number_of_slides = int(max_tag * num_slides)

                # Check if currently over the max allowed slides of this tag
                if value >= max_number_of_slides:
                    prohibited_tags.add(key)

        prohibited_generators = set()
        for generator in self._slide_generators:
            if set(generator.get_tags()) & prohibited_tags:
                prohibited_generators.add(generator)

        return prohibited_generators


class SlideGeneratorContext(object):
    def __init__(
        self,
        presentation_schema,
        presentation_context,
        seed_generator: SlideSeedGenerator,
        num_slides: int,
        used_elements: Optional[Collection[Union[str, ImageData]]] = None,
        prohibited_generators: Optional[Collection[SlideGeneratorData]] = None,
        int_seed: Optional[int] = None,
    ):
        self.presentation_schema = presentation_schema
        self.presentation_context = presentation_context
        self.seed_generator: SlideSeedGenerator = seed_generator
        self.num_slides = num_slides
        self.used_elements = used_elements
        self.prohibited_generators = prohibited_generators
        self.int_seed = int_seed

    def __call__(self, slide_nr):
        if self and self.int_seed and self.int_seed is not None:
            random.seed(self.int_seed + slide_nr)

        return self.presentation_schema.generate_slide(
            # presentation_context=dict(),
            create_slide_presentation_context(
                self.presentation_context,
                self.seed_generator.get_seed(slide_nr)
                # 'cat'
            ),
            slide_nr=slide_nr,
            num_slides=self.num_slides,
            used_elements=self.used_elements,
            prohibited_generators=self.prohibited_generators,
        )


# Helper functions
def create_slide_presentation_context(main_presentation_context, seed):
    presentation_context = dict(main_presentation_context)
    presentation_context["seed"] = seed
    return presentation_context


def add_tags(used_tags, tags):
    for tag in tags:
        if tag not in used_tags:
            used_tags[tag] = 1
        else:
            used_tags[tag] += 1
