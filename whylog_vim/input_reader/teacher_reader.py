_regex_str = '^=== .+ \[file: (.+) offset: (\d+) line_id: (\d+)\]:$'


class TeacherInputReader():

    def __init__(self, regex_str=_regex_str):
        self.regex = regex_str

    def match_output_line(self, line_content):
        if line_content.startswith('--- '):
            matcher = re.match(self.regex, line_content)
            assert matcher is not None, 'malformed line: %s' % (line_content)

            return matcher.group(1), int(matcher.group(2))
        else:
            return False
