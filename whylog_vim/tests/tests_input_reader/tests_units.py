from whylog_vim.input_reader import InputReader


def tests_unit_filter_comments():
    buffor = [
        '# commented line',
        '# commented line 2',
        'not commented line',
        '# commented line',
        'not commented line',
        '# commented line',
        '# commented line',
    ]
    result = InputReader.filter_comments(buffor)
    assert result == ['not commented line', 'not commented line']


def tests_unit_get_button_name():
    line = '[button1] [dummy_button] something else'
    assert InputReader.get_button_name(line, 1) == 'button1'
    assert InputReader.get_button_name(line, 5) == 'button1'
    assert InputReader.get_button_name(line, 9) == 'button1'
    assert InputReader.get_button_name(line, 10) == None
    assert InputReader.get_button_name(line, 11) == 'dummy_button'
    assert InputReader.get_button_name(line, 14) == 'dummy_button'
    assert InputReader.get_button_name(line, 24) == 'dummy_button'
    assert InputReader.get_button_name(line, 25) == None
    assert InputReader.get_button_name(line, 34) == None
