from whylog import FrontInput, LineSource
from whylog_vim.output_formater.log_reader_formater import LogReaderOutput
from whylog_vim.output_formater.consts import LogReader


def tests_no_query_output():
    front_input = FrontInput(1, 'line content', LineSource('host', 'path'))
    query_output = []

    output = LogReaderOutput.format_query(front_input, query_output)
    content = output.get_content()

    assert content[0] == LogReader.LINE_HEADER % (LogReader.ITEM, front_input.line_source,
                                                  front_input.offset)
    assert content[1] == front_input.line_content
    assert content[2] == '# ' + LogReader.EMPTY_OUTPUT
    assert content[3] == '# ' + LogReader.EMPTY_OUTPUT2
