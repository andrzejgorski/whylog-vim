def convert_to_buttons(elem_list):
    return '\n'.join('[%s]' % seq for seq in elem_list)


def convert_to_buttons_list(elem_list):
    return ['[%s]' % seq for seq in elem_list]
