from whylog_vim.output_formater.consts import LogReader
from whylog_vim.output_formater.output_aggregator import OutputAggregator


class LogReaderOutput():
    @classmethod
    def _format_input_line(cls, output, front_input):
        output.add(
            LogReader.LINE_HEADER % (
                LogReader.ITEM,
                front_input.line_source,
                front_input.offset,
            )
        )
        output.add(front_input.line_content)

    @classmethod
    def format_query(cls, front_input, query_output):
        output = OutputAggregator()
        cls._format_input_line(output, front_input)
        if query_output == []:
            output.add_commented(LogReader.EMPTY_OUTPUT)
            output.add_commented(LogReader.EMPTY_OUTPUT2)

        return output
