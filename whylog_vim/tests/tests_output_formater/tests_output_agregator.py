from functools import partial
from whylog_vim.output_formater.output_aggregator import OutputAggregator


def tests_basic_output_aggregator():
    class TestFunctions(object):
        def test_function(self, param1, param2):
            self.called_test_function = param1 + param2

        def test_function2(self, param1, param2):
            self.called_test_function = param1 - param2

    some_object = TestFunctions()

    output = OutputAggregator()
    output.add('Some line.')
    output.add('Another line.')
    output.add('Clickable line.')

    output.create_button(
        partial(
            some_object.test_function,
            param1='foo ',
            param2='bar'
        ),
        (
            'functin name',
            'foo ',
            'bar'
        )
    )

    output.add('Next line.')
    output.add('Next Clickable line.')

    output.create_button(
        partial(
            some_object.test_function2,
            param1=100,
            param2=50
        ),
        (
            'funciton2 name',
            100,
            50
        )
    )

    content = [
        'Some line.', 'Another line.', 'Clickable line.', 'Next line.', 'Next Clickable line.'
    ]
    assert output.get_content() == content
    output.call_button(3)
    assert some_object.called_test_function == 'foo bar'
    output.call_button(5)
    assert some_object.called_test_function == 50
