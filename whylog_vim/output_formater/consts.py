class LogReader(object):
    ITEM = 'investigation item'
    LINE_HEADER = '--- %s [%s offset %s]:'
    EMPTY_OUTPUT = 'There is no cause of this line in config.'
    EMPTY_OUTPUT_CONTINUE = 'To add new rules press WhylogTeach (<F4> by default).'
    CONSTRAINT_LINKAGE = '--- constraints due to %s'
    RESULT_HEADER = '=== Investigation Result %s'


class TeacherMenu(object):
    BUTTONS_HEADER = '--- Buttons:'
    END_BRACKET = '<<<'
    ABANDON_BUTTON = '[abandon_rule]'
    VERIFY_BUTTON = '[verify_rule]'
    RETURN_BUTTON = '[return_to_file]'
    SAVE_BUTTON = '[save]'
