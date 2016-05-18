from whylog.constraints.const import ConstraintType
from whylog_vim.consts import Constraint
from whylog_vim.input_reader import ConstraintReader, InputReader
from whylog_vim.utils import get_parser_name


def tests_unit_filter_comments():
    buffor = [
        '# commented line',
        '# commented line 2',
        'not commented line',
        '# commented line',
        'not commented line',
        '# commented line',
        '# commented line',
    ]
    result = InputReader.filter_comments(buffor)
    assert result == ['not commented line', 'not commented line']


def tests_unit_get_button_name():
    line = '[button1] [dummy_button] something else'
    assert InputReader.get_button_name(line, 1) == 'button1'
    assert InputReader.get_button_name(line, 5) == 'button1'
    assert InputReader.get_button_name(line, 9) == 'button1'
    assert InputReader.get_button_name(line, 10) == None
    assert InputReader.get_button_name(line, 11) == 'dummy_button'
    assert InputReader.get_button_name(line, 14) == 'dummy_button'
    assert InputReader.get_button_name(line, 24) == 'dummy_button'
    assert InputReader.get_button_name(line, 25) == None
    assert InputReader.get_button_name(line, 34) == None


def create_constraint_text(constraint_type, groups):
    constraint = [Constraint.TYPE % constraint_type]
    for group in groups:
        group = (get_parser_name(group[0]), group[1])
        constraint.append(Constraint.GROUP % group)
    return constraint


def tests_unit_parse_Identical():
    groups = [(1, 1), (2, 1), (3, 1), (4, 1)]
    raw_constraint = create_constraint_text(ConstraintType.IDENTICAL, groups)
    created_constraint = ConstraintReader.create_constraint(raw_constraint)
    assert created_constraint.groups == groups
    assert created_constraint.TYPE == ConstraintType.IDENTICAL
