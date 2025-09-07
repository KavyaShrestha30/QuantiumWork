from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict

# Import the names of callback functions you want to test
from task2 import display, update_graph, update

def test_update_callback():
    output = update("east")
    assert output == 'Region is east.'

def test_display_callback():
    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "selected-region.value"}]}))
        return display("east")

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output == f'You last clicked button with ID selected-region'
