from mock import MagicMock, patch
from whylog_vim.gui import get_gui_object
from whylog.front import Whylog
from whylog.front.utils import FrontInput, LocallyAccessibleLogOpener
from whylog_vim.const import LOG_FILE, WHYLOG_OUTPUT
from whylog_vim.front_output import SimpleOutputFormater


class WhylogMain():
    def __init__(self, config={}):
        self.front = Front(config=config)
        self.output_formater = SimpleOutputFormater()
        self.gui = get_gui_object()

    def check_if_state_is_expired(self):
        if not self.gui._is_output_open():
            self.front.end_client()

    def client_skip_to_cause(self):
        current_line = self.gui.get_current_line()
        match = self.output_formater.match_output_line(current_line)
        if match is not False:
            file_name, offset = match
            self.gui.open_cause_window(file_name, offset)
        else:
            self.front.end_client()
            self.gui.close_output_window()

    def mock_query_output(self):
        if self.gui.get_cursor_offset() == 34:
            return [FrontInput(
                21, '2 root cause',
                LocallyAccessibleLogOpener(self.gui.input_window.filename))
            ]
        else:
            return []

    def get_front_input(self):
        filename = self.gui.get_current_filename()
        resource_location = LocallyAccessibleLogOpener(filename)
        cursor_position = self.gui.get_cursor_offset()
        line_content = self.gui.get_current_line()

        return FrontInput(cursor_position, line_content, resource_location)

    def client_query(self):
        self.gui.init_gui()
        front_input = self.get_front_input()

        # Mock
        with patch('whylog.client.Client.get_causes') as mock:
            mock.return_value = self.mock_query_output()
            query_output = self.front.get_causes(front_input)

        contents = self.output_formater.write_query(front_input, query_output)
        self.gui.set_output(contents, line=4)
        self.gui.go_to_output_window()
        return True

    def new_effect(self):
        self.gui.init_gui()
        front_input = self.get_front_input()

        contents = self.output_formater.teacher_init(front_input)
        teacher = self.front.add_effect(front_input)
        self.gui.set_output(contents, line=4)
        self.gui.go_to_output_window()

    def add_cause(self):
        front_input = self.get_front_input()

        self.front.add_cause(front_input)
        causes = self.front.causes
        effect = self.front.effect
        contents = self.output_formater.add_causes(effect, causes)

        self.gui.set_output(contents, line=4)
        self.gui.go_to_output_window()

    def warning_message(self, message):
        print message

    def add_dependences(self):
        teacher = self.front.new_teacher()


# whylog_main = WhylogMain()


def _whylog_1():
    whylog_main.check_if_state_is_expired()
    whylog_state = whylog_main.front.get_state()
    window_type = whylog_main.gui.get_window_type()

    if whylog_state == states.EDITOR_NORMAL:
        whylog_main.client_query()
    elif whylog_state == states.CLIENT_QUERY:
        if window_type == WHYLOG_OUTPUT:
            whylog_main.client_skip_to_cause()
        else:
            # closing whylog client
            whylog_main.front.end_client()
            whylog_main.gui.close_output_window()
    elif whylog_state == states.ADD_CAUSES:
        whylog_main.gui.go_to_input_window()


def _whylog_2():
    whylog_main.check_if_state_is_expired()
    whylog_state = whylog_main.front.get_state()
    window_type = whylog_main.gui.get_window_type()

    if whylog_state == states.EDITOR_NORMAL:
        whylog_main.new_effect()
    elif whylog_state == states.CLIENT_QUERY:
        pass
    elif whylog_state == states.ADD_CAUSES:
        if window_type != WHYLOG_OUTPUT:
            whylog_main.add_cause()
        else:
            if whylog_main.front.causes == []:
                whylog_main.warning_message('No line selected as cause')
            else:
                whylog_main.add_dependences()


whylog = Whylog(config={}, editor=get_gui_object())


def whylog_1():
    whylog.signal_1()


def whylog_2():
    whylog.signal_2()
