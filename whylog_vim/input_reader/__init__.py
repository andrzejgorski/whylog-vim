from whylog.constraints import IdenticalConstraint
from whylog.constraints.const import ConstraintType

from whylog_vim.input_reader.consts import RegexPatterns, ConstraintInput, Groups
from whylog_vim.utils import get_id_from_name


class InputReader(object):
    @classmethod
    def filter_comments(cls, content):
        return [line for line in content if not RegexPatterns.COMMENTS.match(line)]

    @classmethod
    def get_button_name(cls, line, offset):
        offset -= 1
        for match in RegexPatterns.BUTTON.finditer(line):
            if offset >= match.start(0) and offset < match.end(0):
                return match.group(0)[1:-1]

    @classmethod
    def parse_primary_key_groups(cls, content):
        return [int(group) for group in content[0].split(', ')]


class ConstraintReader(object):

    CONSTRAINTS = {ConstraintType.IDENTICAL: IdenticalConstraint,}

    @classmethod
    def _parse_constraint(cls, lines):
        constr_type = ConstraintInput.TYPE.match(lines[0]).group(1)
        groups = []
        for line in lines[1:]:
            match = ConstraintInput.GROUP.match(line)
            if match:
                groups.append(
                    (get_id_from_name(match.group(Groups.GROUP1)), int(match.group(Groups.GROUP2)))
                )
            else:
                break
        else:
            return constr_type, groups, {}
        return constr_type, groups, {}

    @classmethod
    def create_constraint(cls, lines):
        constraint_type, groups, params = cls._parse_constraint(lines)
        return cls.CONSTRAINTS[constraint_type](groups=groups, param_dict=params)
