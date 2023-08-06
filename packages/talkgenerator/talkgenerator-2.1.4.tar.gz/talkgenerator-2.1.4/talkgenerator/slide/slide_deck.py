import logging

logger = logging.getLogger("talkgenerator")


class SlideDeck:
    """ Represents a deck of Slide objects    """

    def __init__(self, size):
        self._size = size
        self._slides = [None] * size

    def add_slide(self, slide_index: int, slide):
        self._slides[slide_index] = slide

    def is_complete(self):
        return len(self._slides) >= self._size and (None not in self._slides)

    def save_to_powerpoint(self, prs_template):
        """ Should generate a slide in the powerpoint """
        if not self.is_complete():
            logger.error(
                "ERROR: SOME SLIDES WERE NOT GENERATED: {}".format(self._slides)
            )
            self._slides = [slide for slide in self._slides if slide is not None]
        return [x.create_powerpoint_slide(prs_template) for x in self._slides]

    def get_structured_data(self):
        """ Return slide deck as structured data for alternative presentation """
        if not self.is_complete():
            logger.error(
                "ERROR: SOME SLIDES WERE NOT GENERATED: {}".format(self._slides)
            )
            self._slides = [slide for slide in self._slides if slide is not None]
        return [x for x in self._slides]

    def has_slide_nr(self, index):
        return 0 <= index < self._size and self._slides[index] is not None
