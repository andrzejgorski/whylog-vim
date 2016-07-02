from whylog_vim.output_formater.consts import LogReader
from whylog_vim.output_formater.output_aggregator import OutputAggregator


class LogReaderOutput(object):
    @classmethod
    def _format_input_line(cls, output, front_input):
        output.add(
            LogReader.LINE_HEADER % (LogReader.ITEM,
                                     front_input.line_source,
                                     front_input.offset,)
        )
        output.add(front_input.line_content)

    @classmethod
    def format_investigation_result(cls, output, investigation_result):
        for line in investigation_result.lines:
            cls._format_input_line(output, line)
        if investigation_result.constraints:
            output.add(LogReader.CONSTRAINT_LINKAGE % investigation_result.constraints_linkage)
            for constraint in investigation_result.constraints:
                output.add(str(constraint))

    @classmethod
    def format_query(cls, front_input, query_output):
        output = OutputAggregator()
        cls._format_input_line(output, front_input)
        if not query_output:
            output.add('')
            output.add_commented(LogReader.EMPTY_OUTPUT)
            output.add_commented(LogReader.EMPTY_OUTPUT_CONTINUE)
            return output

        if len(query_output) == 1:
            output.add('')
            cls.format_investigation_result(output, query_output[0])
            return output

        for result_number, result in enumerate(query_output, 1):
            output.add('')
            output.add(LogReader.RESULT_HEADER % result_number)
            cls.format_investigation_result(output, result)
        return output
