from lcc_parser import LccData


# Helpers
MainClass = LccData.parse_main_class
SubClass = LccData.parse_sub_class

def test_parse_main_class_raw_compare():
    value = LccData.parse_main_class('A1')
    assert value == 10 * (36 ** 1) + 1 * (36 ** 0)


def test_parse_sub_class_raw_compare():
    value = LccData.parse_sub_class('10')
    assert value == 1 * 36 ** 6


def test_parse_sub_class():
    value = LccData.parse_sub_class('767')
    assert value == int('76700000', 36)


def test_parse_subclass_with_fractional_part():
    value = LccData.parse_sub_class('767.9')
    assert value == int('76790000', 36)


def test_parse_without_range():
    data = LccData.parse('HQ767.9')
    classification = MainClass('HQ')
    subclass = SubClass('767.9')
    assert data.main_class_start == classification
    assert data.main_class_end == classification
    assert data.sub_class_start == subclass
    assert data.sub_class_end == subclass
    #assert data.year == '2014'


def test_parse_without_range_and_year_and_author():
    data = LccData.parse('HQ767.9')
    assert data.year is None


def test_parse_with_range():
    data = LccData.parse('N5300 - 5308')
    assert data.main_class_start == MainClass('N')
    assert data.main_class_end == MainClass('N')
    assert data.sub_class_start == SubClass('5300')
    assert data.sub_class_end == SubClass('5308')


def test_parse_with_range_with_fractional_part_on_right_side():
    data = LccData.parse('N7101 - 7113.3')
    assert data.main_class_start == MainClass('N')
    assert data.main_class_end == MainClass('N')
    assert data.sub_class_start == SubClass('7101')
    assert data.sub_class_end == SubClass('7113.3')


def test_parse_with_range_with_fractional_part_on_left_side():
    data = LccData.parse('ML75.5 - 76')
    assert data.main_class_start == MainClass('ML')
    assert data.main_class_end == MainClass('ML')
    assert data.sub_class_start == SubClass('75.5')
    assert data.sub_class_end == SubClass('76')


def test_parse_with_range_main_class():
    data = LccData.parse('A5 - B10')
    assert data.main_class_start == MainClass('A')
    assert data.main_class_end == MainClass('B')
    assert data.sub_class_start == SubClass('5')
    assert data.sub_class_end == SubClass('10')


def test_parse_with_range_with_letters():
    data = LccData.parse('ML385 - 410.P')
    assert data.main_class_start == MainClass('ML')
    assert data.main_class_end == MainClass('ML')
    assert data.sub_class_start == SubClass('385')
    assert data.sub_class_end == SubClass('410.P')

