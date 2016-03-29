import re


_regex_str = '^--- .+ \[(.+) offset (\d+)\]:$'
_output_str = '--- {} [{} offset {}]:'


class AbstractTeacherMenu():

    def format_effect(self, front_input):
        raise NotImplemented()

    def format_effect_and_causes():
        raise NotImplemented()


# http://stackoverflow.com/questions/24804453/how-can-i-copy-a-python-string
def copy_str(input_):
    return (input_ + '.')[:-1]


class TeacherMenu(AbstractTeacherMenu):

    def __init__(self, regex_str=_regex_str, output_str=_output_str):
        self.regex = regex_str
        self.output_str = output_str

    def match_output_line(self, line_content):
        if line_content.startswith('--- '):
            matcher = re.match(self.regex, line_content)
            assert matcher is not None, 'malformed line: %s' % (line_content)

            return matcher.group(1), int(matcher.group(2))
        else:
            return False

    def _format_single_line(self, message, line_fi_style):
        result_prefix = (
            copy_str(self.output_str)
            .format(
                message,
                line_fi_style.resource_location,
                line_fi_style.offset
            )
        )
        return result_prefix + '\n' + line_fi_style.line_content + '\n'

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
