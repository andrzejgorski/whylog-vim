import re


_regex_str = '^--- .+ \[(.+) offset (\d+)\]:$'


class QueryInputReader():

    def __init__(self, regex_str=_regex_str):
        self.regex = regex_str

    def match_output_line(self, line_content):
        if line_content.startswith('--- '):
            matcher = re.match(self.regex, line_content)
            assert matcher is not None, 'malformed line: %s' % (line_content,)

            # TODO consider if try except block is necessary here
            # return file name and line
            return matcher.group(1), int(matcher.group(2))
        else:
            return False
