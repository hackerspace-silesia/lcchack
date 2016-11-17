from string import ascii_uppercase
import re


class LccData(object):
    re_split_start_classes = re.compile(r'([A-Z]{1,3}) *([A-Z0-9.]*)')
    re_split_end_classes = re.compile(r'([A-Z]{1,3})? *([A-Z0-9.]*)')
    re_split_the_rest = re.compile(r'(^[A-Z][0-9]*) *(?:R?([0-9]+))?')

    def __init__(self, main_class_range, sub_class_range, author=None, year=None):
        self.main_class_start = main_class_range[0]
        self.main_class_end = main_class_range[1]
        self.sub_class_start = sub_class_range[0]
        self.sub_class_end = sub_class_range[1]
        self.author = author
        self.year = year

    @classmethod
    def parse(cls, raw):
        raw = raw.upper()
        classes, the_rest = cls.get_classes_and_the_rest(raw)
        start, end = cls.split_classes(classes)
        author, year = cls.get_author_and_year(the_rest)
        main_class_start, sub_class_start = cls.parse_range_class(start)

        if end is not None:
            if end[0] is None:
                main_class_end = main_class_start
            else:
                main_class_end = cls.parse_main_class(end[0])
            sub_class_end = cls.parse_sub_class(end[1])
        else:
            main_class_end = main_class_start
            sub_class_end = sub_class_start

        return cls(
            main_class_range=(main_class_start, main_class_end),
            sub_class_range=(sub_class_start, sub_class_end),
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
        start, delimeter, end = classes.partition('-')
        start = start.strip()
        end = end.strip()
        start_match = cls.re_split_start_classes.match(start)
        if start_match is None:
            raise ValueError(start)
        if not delimeter:
            return start_match.groups(), None

        end_match = cls.re_split_end_classes.match(end)
        if end_match is None:
            raise ValueError(end)
        return start_match.groups(), end_match.groups()

    @classmethod
    def get_author_and_year(cls, the_rest):
        if the_rest is None:
            return None, None
        match = cls.re_split_the_rest.match(the_rest)
        if match is None:
            raise ValueError(the_rest)
        return match.groups()

    @classmethod
    def parse_range_class(cls, classes):
        main_class = cls.parse_main_class(classes[0])
        sub_class = cls.parse_sub_class(classes[1])
        return (main_class, sub_class)

    @staticmethod
    def parse_main_class(main_class):
        return int(main_class, 36)

    @staticmethod
    def parse_sub_class(subclass):
        subclass = subclass.strip()
        if not subclass:
            return None
        left_value, delimeter, right_value = subclass.partition('.')
        value = '{}{:<05}'.format(left_value, right_value)
        return int(value, 36)
