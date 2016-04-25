import re


_output_str = '--- {} [{} offset {}]:'


class LogReaderOutput():

    def __init__(self, output_str=_output_str):
        self.output_str = output_str

    def _format_single_line(self, message, line_fi_style):
        result_prefix = (
            self.output_str
            .format(
                message,
                line_fi_style.line_source.path,
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
