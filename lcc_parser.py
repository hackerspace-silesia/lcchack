from string import ascii_uppercase
import re


class LccData(object):

    re_split_classes = re.compile(r'([A-Z]{1,2}) *([A-Z0-9.]*)')
    re_split_the_rest = re.compile(r'(^[A-Z][0-9]+) *(?:R?([0-9]+))?')

    def __init__(self, main_class, sub_class, author=None, year=None):
        self.main_class_start = main_class
        self.main_class_end = main_class
        self.sub_class_start = sub_class
        self.sub_class_end = sub_class
        self.author = author
        self.year = year

    @classmethod
    def parse(cls, raw):
        raw = raw.upper()
        classes, the_rest = cls.get_classes_and_the_rest(raw)
        main_class, sub_class = cls.split_classes(classes)
        author, year = cls.get_author_and_year(the_rest)

        return cls(
            main_class=cls.parse_main_class(main_class),
            sub_class=cls.parse_sub_class(sub_class),
            author=author,
            year=year,
        )

    @classmethod
    def get_classes_and_the_rest(cls, raw):
        classes, delimeter, the_rest = raw.rpartition('.')
        if not delimeter:
            return raw.strip(), None

        if len(the_rest) and the_rest[0] in ascii_uppercase:
            return classes.strip(), the_rest.strip()
        else:
            return raw.strip(), None

    @classmethod
    def split_classes(cls, classes):
        match = cls.re_split_classes.match(classes)
        if match is None:
            raise ValueError(classes)
        return match.groups()

    @classmethod
    def get_author_and_year(cls, the_rest):
        if the_rest is None:
            return None, None
        match = cls.re_split_the_rest.match(the_rest)
        if match is None:
            raise ValueError(the_rest)
        return match.groups()

    @staticmethod
    def parse_main_class(main_class):
        return int(main_class, 36)

    @staticmethod
    def parse_sub_class(subclass):
        left_value, delimeter, right_value = subclass.partition('.')
        value = '{}{:<05}'.format(left_value, right_value)
        return int(value)
