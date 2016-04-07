import re


EFFECT_LINE = 0


_output_str = '=== {} [file: {}, offset: {}, line_id: {}]:'


class TeacherOutput():

    def __init__(self, output_str=_output_str):
        self.output_str = output_str

    def _format_single_line(self, message, line_fi_style, line_id):
        result_prefix = (
            self.output_str
            .format(
                message,
                line_fi_style.resource_location,
                line_fi_style.offset,
                line_id,
            )
        )
        return result_prefix + '\n' + line_fi_style.line_content + '\n'

    def _print_effect_line(self, teacher, effect_id):
        return self._format_single_line(
                'effect line',
                teacher._lines[effect_id],
                effect_id,
            )

    def _print_causes(self, teacher, effect_id):
        result = []
        causes_lines = teacher._lines.keys()
        causes_lines.remove(effect_id)
        for line_id in causes_lines:
            result.append(self._format_single_line(
                    'cause line',
                    teacher._lines[line_id],
                    line_id,
                ))
        return result

    def print_teacher(self, teacher):
        result = ['# You are using whylog teacher.']
        effect_id = teacher.rule_intent.effect_id
        result.append(self._print_effect_line(teacher, effect_id))
        result += self._print_causes(teacher, effect_id)
        result = '\n'.join(result)
        return result

    def format_effect(self, front_input):
        result = []
        result.append('You begin teaching whylog a new rule.')
        result.append(self._format_single_line('effect line', front_input))
        result.append('Press whylog1 to back to the input file and add causes.')
        result = '\n'.join(result)
        return result

    def add_causes(self, front_input, causes):
        result = []
        result.append(
            'You begin teaching whylog a new rule. '
            'You selected as an effect line:'
        )
        result.append(self._format_single_line('effect line', front_input))
        result.append('Here are lines that you selected as causes:')
        for cause in causes:
            result.append(self._format_single_line('cause line', cause))
        result.append('Press whylog1 to back to the input file and add more causes.')
        result.append('If you want to add constraints press whylog2')
        result = '\n'.join(result)
        return result
