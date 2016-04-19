from whylog_vim.consts import ButtonsMetaConsts as BMC


def naturals_generator():
    i = 0
    while True:
        yield i
        i += 1


parsers_ids = naturals_generator()
constraints_its = naturals_generator()


class ReadInputInfo():

    def __init__(self, teacher_proxy, return_function, meta_info=None, loader=None):
        self.return_function = return_function
        self.meta_info = meta_info or {}
        self.loader = loader or teacher_proxy.editor.get_input_content

    def set_content(self, content):
        self.content = content

    def load_input(self):
        self.content = self.loader()
