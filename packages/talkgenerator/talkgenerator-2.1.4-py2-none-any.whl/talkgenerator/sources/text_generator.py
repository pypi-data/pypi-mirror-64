""" This module helps out with generating text using templates """
import json
import random
import re
from functools import lru_cache

import tracery
from tracery.modifiers import base_english

from talkgenerator.sources import conceptnet
from talkgenerator.sources import phrasefinder
from talkgenerator.sources import wikihow
from talkgenerator.util import language_util
from talkgenerator.util import os_util
from talkgenerator.util import random_util

known_functions = {
    "title": str.title,
    "lower": str.lower,
    "upper": str.upper,
    "dashes": lambda words: words.replace(" ", "-"),
    "first_letter": lambda words: words[0],
    "last_letter_is_vowel": lambda word: word
    if language_util.is_vowel(word[-1])
    else None,
    "last_letter_is_consonant": lambda word: word
    if language_util.is_consonant(word[-1])
    else None,
    "a": lambda word: language_util.add_article(word),
    "ing": language_util.to_present_participle,
    "plural": language_util.to_plural,
    "singular": language_util.to_singular,
    # "synonym": generator_util.FromListGenerator(language_util.get_synonyms),
    "2_to_1_pronouns": language_util.second_to_first_pronouns,
    "wikihow_action": lambda seed: random_util.choice_optional(
        wikihow.get_related_wikihow_actions(seed)
    ),
    "get_last_noun_and_article": language_util.get_last_noun_and_article,
    # Conceptnet
    "conceptnet_location": conceptnet.weighted_location_generator,
    "conceptnet_related": conceptnet.weighted_related_word_generator,
    "conceptnet_related_single_word": lambda word: phrasefinder.get_rarest_word(
        conceptnet.weighted_related_word_generator(word)
    ),
    # Checkers
    "is_noun": lambda word: word if language_util.is_noun(word) else None,
    "is_verb": lambda word: word if language_util.is_verb(word) else None,
    # Unique: To make a variable not be the same as something else with the same parameters
    "unique": lambda x: x,
}


class AbstractTextGenerator(object):
    def generate(self, variables_dictionary):
        raise NotImplementedError()

    def generate_with_seed(self, seed):
        return self.generate({"seed": seed})


class TemplatedTextGenerator(AbstractTextGenerator):
    def __init__(self, template_file=None, templates_list=None):
        templates = []
        if template_file:
            templates.extend(read_lines(template_file))
        if templates_list:
            templates.extend(templates_list)
        # Create a tuple so no templates can accidentally be deleted from the generator
        self._templates = tuple(templates)

    def generate(self, variables_dictionary=None):
        """ Generates a text from the templates using the given variables dictionary"""
        # Set empty dictionary if none is given
        if not bool(variables_dictionary):
            variables_dictionary = {}
        # Create a mutable copy of the templates list
        possible_templates = list(self._templates)
        for i in range(len(possible_templates)):
            template = random.choice(possible_templates)
            if can_format_with(template, variables_dictionary):
                result = apply_variables_to_template(template, variables_dictionary)
                if result:
                    return result
            # Remove the template from the possible templates list, such that it won
            possible_templates.remove(template)


class TraceryTextGenerator(AbstractTextGenerator):
    def __init__(self, tracery_json, variable="origin"):
        with open(os_util.to_actual_file(tracery_json)) as grammar_file:
            grammar = get_tracery_grammar(grammar_file)
            grammar.add_modifiers(base_english)
            self._grammar = grammar
            self._variable = variable

    def generate(self, variables_dictionary=None):
        """ Generates a text from internal tracery grammar using the given variables dictionary"""
        # Set empty dictionary if none is given
        if not bool(variables_dictionary):
            variables_dictionary = {}

        # Generate
        for i in range(100):  # TODO prune the grammar instead of retrying
            template = self._grammar.flatten("#" + self._variable + "#")
            if can_format_with(template, variables_dictionary):
                result = apply_variables_to_template(template, variables_dictionary)
                if result:
                    return result


@lru_cache(maxsize=20)
def get_tracery_grammar(grammar_file):
    return tracery.Grammar(json.load(grammar_file))


def can_format_with(template, variables_dictionary):
    """ Checks if the template can be fully formatted by the given variable dictionary without errors"""
    format_variables = get_format_variables(template)
    return (len(format_variables) == 0 and len(variables_dictionary) == 0) or set(
        format_variables
    ) <= set(variables_dictionary.keys())


def get_format_variables(template):
    """ Finds all the names of the variables used in the template """
    return {x[0] for x in get_format_variables_and_functions(template)}


def get_format_variables_and_functions(template):
    """ Finds all the names of the variables used in the template with their functions in a large tuple"""
    matches = re.findall(r"{(\w+)((?:[.]\w+)*)}", template)
    return set(matches)


def apply_variables_to_template(template, variables_dictionary):
    variables_and_functions = get_format_variables_and_functions(template)
    applied = apply_functions_to_variables(
        template, variables_dictionary, variables_and_functions
    )
    if applied:
        (template, variables_dictionary) = applied
        return template.format(**variables_dictionary)


def apply_functions(variable, functions):
    """ Applies a list of functions to a variable """
    result = variable
    for func in functions:
        # Check if it transformed the result into None
        if result is None:
            return None

        if func in known_functions:
            result = known_functions[func](result)
        # Check if it is a dictionary, as is allowed in real str.format
        elif isinstance(result, dict) and func in result:
            result = result[func]
        # Unique identifier to make similar functions on a variable have different effects
        elif func.isdigit():
            result = result
        else:
            raise ValueError("Unknown function:", func)

    return result


def apply_functions_to_variables(
    template, variables_dictionary, variables_and_functions
):
    """ Applies the functions of the variables_and_functions tuple and stores them in the variable dictionary and
    updates the template """
    variables_and_functions = list(variables_and_functions)
    variables_and_functions.sort(key=lambda a: len(a), reverse=True)

    for var_func in variables_and_functions:
        # Check if it has functions to apply
        if len(var_func) > 1 and len(var_func[1]) > 0:
            old_var_name = var_func[0] + var_func[1]
            functions = var_func[1][1:].split(".")
            variable_name = var_func[0]
            variable = variables_dictionary[variable_name]
            applied_functions = apply_functions(variable, functions)
            if applied_functions is not None:
                applied_var_name = old_var_name.replace(".", "_")
                # Replace all occurrences with the dot to the underscore notation
                template = template.replace(old_var_name, applied_var_name)
                # Store in dictionary
                variables_dictionary[applied_var_name] = applied_functions
            else:
                return None

    return template, variables_dictionary


def read_lines(filename):
    """ Reads all the string lines from a file """
    return os_util.read_lines(filename)
