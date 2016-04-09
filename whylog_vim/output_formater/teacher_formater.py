import re


EFFECT_LINE = 0


empty_line = ''
_output_str = '=== {} [file: {}, offset: {}, line_id: {}]:'
message_content = '=== %s: %s'
meta = 'file: %s, offset: %s'
line_buttons = '[edit_content] [copy_line] [delete_line]'
regex_head = '--- Regex: %s'
regex_buttons = '[edit_regex] [guess_regex]'
converters_head = '--- Convereters:'
others_head = '--- Other:'
log_type = 'log type name: %s'
log_type_buttons = '[edit_log_type] [add_new_log_type]'
primary_key = 'primary key groups: %s'
primary_key_button = '[edit_primary_key_groups]'


class TeacherOutput():

    def __init__(self, output_str=_output_str):
        self.output_str = output_str

    def _format_single_line(self, message, parser, line_id):
        result = []
        result.append(message_content % (message, parser.line_content))
        result.append(meta % (parser.line_resource_location, parser.line_offset))
        result.append(line_buttons)
        result.append(empty_line)
        result.append(regex_head % parser.pattern_name)
        result.append(parser.pattern)
        result.append(regex_buttons)
        result.append(empty_line)
        result.append(self._format_groups(parser.groups))
        result.append(empty_line)
        result.append(converters_head)
        result.append(self._format_converters(parser.groups))
        result.append(empty_line)
        result.append(others_head)
        result.append(log_type % parser.log_type_name)
        result.append(log_type_buttons)
        result.append(primary_key % parser.primary_key_groups)
        result.append(primary_key_button)
        result.append('\n')
        return '\n'.join(result)

    def _format_groups(self, groups):
        result = []
        for group in groups.keys():
            result.append('group %s: %s' % (group, groups[group].content))
        return '\n'.join(result)

    def _format_converters(self, groups):
        result = []
        for group in groups.keys():
            result.append('[edit_converter] group %s: %s' % (group, groups[group].converter))
        return '\n'.join(result)

    def _format_effect_line(self, raw_output, effect_id):
        return self._format_single_line(
                'effect line',
                raw_output.parsers[effect_id],
                effect_id,
            )

    def _format_causes(self, rule, effect_id):
        result = []
        causes_lines = rule.parsers.keys()
        causes_lines.remove(effect_id)
        for line_id in causes_lines:
            result.append(self._format_single_line(
                    'cause line',
                    rule.parsers[line_id],
                    line_id,
                ))
        return result

    def format(self, raw_output):
        result = ['# You are using whylog rule.\n']
        effect_id = raw_output.effect_id
        result.append(self._format_effect_line(raw_output, effect_id))
        result += self._format_causes(raw_output, effect_id)
        # result += self._format_constraing(raw_output.)
        return '\n'.join(result)
