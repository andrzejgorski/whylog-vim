from whylog_vim.output_formater.utils import convert_to_buttons


def tests_convert_to_buttons_empty_list():
    test_list = []
    assert '' == convert_to_buttons(test_list)


def tests_convert_to_buttons_1_elem_list():
    test_list = ['foo']
    assert '[foo]' == convert_to_buttons(test_list)


def tests_convert_to_buttons_many_elem_list():
    test_list = ['foo', 'bar', 'baz']
    assert '[foo]\n[bar]\n[baz]' == convert_to_buttons(test_list)
