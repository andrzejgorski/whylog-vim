from whylog_vim.output_formater.output_agregator import OutputAgregator, Button


def tests_basic_output_agregator():

    class TestFunctions():
        def click_function(self, param1, param2):
            self.test_attr = param1 + param2

        def click_function2(self, param1, param2):
            self.test_attr2 = param1 - param2

    some_object = TestFunctions()

    output = OutputAgregator()
    output.add('Some line.')
    output.add('Another line.')
    output.add('Clickable line.')

    button = Button(some_object.click_function, param1='foo ', param2='bar')
    output.set_button(button)

    output.add('Next line.')
    output.add('Next Clickable line.')

    output.create_button(some_object.click_function2, param1=100, param2=50)

    content = ['Some line.', 'Another line.', 'Clickable line.', 'Next line.', 'Next Clickable line.']
    assert output.get_content() == content
    import ipdb; ipdb.set_trace()
    output.call_button(3)
    assert some_object.test_attr == 'foo bar'
    output.call_button(5)
    assert some_object.test_attr2 == 50
    output.call_button(4)
