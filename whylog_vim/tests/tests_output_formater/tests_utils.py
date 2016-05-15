from whylog_vim.output_formater.utils import convert_to_buttons


def tests_to_buttons():
    test_list = ['jajko', 'kanapka', 'ziemniak', 'mleko']
    assert '[jajko]\n[kanapka]\n[ziemniak]\n[mleko]' == convert_to_buttons(test_list)
