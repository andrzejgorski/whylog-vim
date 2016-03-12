import re


class AbstractOutputFormater():

    def match_output_line(self, line_content):
        raise NotImplemented()

    def write_query(self, front_input, whylog_output):
        raise NotImplemented()

    def teacher_init(self, front_input):
        raise NotImplemented()


class regex_consts():
    # maybe be usefull in the future
    # LINE = '(?P<line>\d+)'
    # FILENAME = '(?P<filename>.+)'
    # MESSAGE = '(?P<message>.+)'
    _regex_str = '^--- .+ \[(.+) offset (\d+)\]:$'
    _output_str = '--- {} [{} offset {}]:'


# http://stackoverflow.com/questions/24804453/how-can-i-copy-a-python-string
def copy_str(input_):
    return (input_ + '.')[:-1]


class SimpleOutputFormater(AbstractOutputFormater):

    def __init__(self, regex_str=regex_consts._regex_str, output_str=regex_consts._output_str):
        self.regex = regex_str
        self.output_str = output_str

    def match_output_line(self, line_content):
        if line_content.startswith('--- '):
            matcher = re.match(self.regex, line_content)
            assert matcher is not None, 'malformed line: %s' % (line_content,)

            # TODO consider if try except block is necessary here
            # return file name and line
            return matcher.group(1), int(matcher.group(2))
        else:
            return False

    def _write_single_line(self, line_fi_style):
        result_prefix = (
            copy_str(self.output_str)
            .format(
                'investigated item',
                line_fi_style.resource_location,
                line_fi_style.offset
            )
        )
        return result_prefix + '\n' + line_fi_style.line_content + '\n'

    def write_query(self, front_input, query_output):
        result = [self._write_single_line(front_input)]
        if query_output != []:
            for single_output in query_output:
                result.append(self._write_single_line(single_output))
        else:
            result.append('There is no cause of this line in config.\n'
                          'To add new rules press whylog2')

        result = '\n'.join(result)
        return result

    def teacher_init(self, front_input):
        result = []
        result.append(
            'You begin teaching whylog a new rule. '
            'You selected as an effect line:'
        )
        result.append(self._write_single_line(front_input))
        result.append('Press whylog1 to back to the input file and add causes.')
        result = '\n'.join(result)
        return result

    def add_causes(self, front_input, causes):
        result = []
        result.append(
            'You begin teaching whylog a new rule. '
            'You selected as an effect line:'
        )
        result.append(self._write_single_line(front_input))
        result.append('Here are lines that you selected as causes:')
        for cause in causes:
            result.append(self._write_single_line(cause))
        result.append('Press whylog1 to back to the input file and add more causes.')
        result.append('If you want to add constraints press whylog2')
        result = '\n'.join(result)
        return result
