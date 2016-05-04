from whylog_vim.input_reader import filter_comments, get_button_name, prepare_regex


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
    result = filter_comments(buffor)
    assert result == ['not commented line', 'not commented line']


def tests_unit_get_button_name():
    line = '[button1] [dummy_button] something else'
    assert 'button1' == get_button_name(line, 1)
    assert 'button1' == get_button_name(line, 5)
    assert 'button1' == get_button_name(line, 9)
    assert None == get_button_name(line, 10)
    assert 'dummy_button' == get_button_name(line, 11)
    assert 'dummy_button' == get_button_name(line, 14)
    assert 'dummy_button' == get_button_name(line, 24)
    assert None == get_button_name(line, 25)
    assert None == get_button_name(line, 34)
