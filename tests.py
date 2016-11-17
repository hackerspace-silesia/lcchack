from lcc_parser import LccData


def test_parse_main_class_raw_compare():
    value = LccData.parse_main_class('A1')
    assert value == 10 * (36 ** 1) + 1 * (36 ** 0)


def test_parse_sub_class_raw_compare():
    value = LccData.parse_sub_class('10')
    assert value == 1000000


def test_parse_sub_class():
    value = LccData.parse_sub_class('5')
    assert value == int('500000', 10)


def test_parse_subclass_with_subclass():
    value = LccData.parse_sub_class('767')
    assert value == int('76700000', 10)


def test_parse_subclass_with_fractional_part():
    value = LccData.parse_sub_class('767.9')
    assert value == int('76790000', 10)


def test_parse_without_range():
    data = LccData.parse('HQ767.9 .C675 2014')
    classification = LccData.parse_main_class('HQ')
    subclass = LccData.parse_sub_class('767.9')
    assert data.main_class_start == classification
    assert data.main_class_end == classification
    assert data.sub_class_start == subclass
    assert data.sub_class_end == subclass
    assert data.author == 'C675'
    assert data.year == '2014'


def test_parse_without_range_and_year():
    data = LccData.parse('HQ767.9 .C675')
    assert data.author == 'C675'
    assert data.year is None


def test_parse_without_range_and_year_and_author():
    data = LccData.parse('HQ767.9')
    assert data.author is None
    assert data.year is None

