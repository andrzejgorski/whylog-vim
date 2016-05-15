from whylog_vim.output_formater.utils import convert_to_buttons


def tests_convert_to_buttons_empty_list():
    test_list = []
    assert '' == convert_to_buttons(test_list)


def tests_convert_to_buttons_1_elem_list():
    test_list = ['jajko']
    assert '[jajko]' == convert_to_buttons(test_list)


def tests_convert_to_buttons_many_elem_list():
    test_list = ['jajko', 'kanapka', 'ziemniak', 'mleko']
    assert '[jajko]\n[kanapka]\n[ziemniak]\n[mleko]' == convert_to_buttons(
        test_list)
