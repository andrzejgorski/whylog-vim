import re


_regex_str = '^--- .+ \[(.+) offset (\d+)\]:$'
_output_str = '--- {} [{} offset {}]:'


# http://stackoverflow.com/questions/24804453/how-can-i-copy-a-python-string
def copy_str(input_):
    return (input_ + '.')[:-1]


class AbstractClientOutputFormater():

    def match_output_line(self, line_content):
        raise NotImplemented()

    def format_query(self, front_input, query_output):
        raise NotImplemented()


class SimpleClientOutputFormater(AbstractClientOutputFormater):

    def __init__(self, regex_str=_regex_str, output_str=_output_str):
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

    def format_query(self, front_input, query_output):
        result = [self._format_single_line('investigation item', front_input)]
        if query_output != []:
            for single_output in query_output:
                result.append(self._format_single_line('has been caused by', single_output))
        else:
            result.append('There is no cause of this line in config.\n'
                          'To add new rules press whylog2')

        result = '\n'.join(result)
        return result
