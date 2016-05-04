def to_buttons(elem_list):
    result = '[%s]' % elem_list[0]
    for elem in elem_list[1:]:
        result += '\n[%s]' % elem
    return result
