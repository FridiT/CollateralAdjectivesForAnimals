import os
from main import run


def test_run_creates_html():
    run()
    assert os.path.exists("Collateral Adjectives For Animals.html"), "HTML file was not generated"
