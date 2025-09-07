# tests/test_app.py
import pytest

# If your app lives in a different file, change this import accordingly:
# from my_dash_file import app
from task2 import app


def test_header_present(dash_duo):
    dash_duo.start_server(app)
    # Wait until the <h1> renders and assert its text
    dash_duo.wait_for_text_to_equal("h1", "Sales for Pink Morsel")


def test_visualisation_present(dash_duo):
    dash_duo.start_server(app)
    # dcc.Graph mounts a Plotly div with class .js-plotly-plot
    dash_duo.wait_for_element("#region-sales-graph .js-plotly-plot")


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    # The RadioItems container
    dash_duo.wait_for_element("#selected-region")
    # Ensure at least one radio input is present
    radios = dash_duo.find_elements('#selected-region input[type="radio"]')
    assert len(radios) >= 1
