import pytest
from cifi.intelligence.detectors import EnvironmentDetector
from cifi.models import Language, Framework


def test_python_uv_detection():
    sample_log = (
        "Running uv sync...\n"
        "Traceback (most recent call last):\n"
        "  File \"app.py\", line 10, in <module>\n"
        "ModuleNotFoundError: No module named 'jwt'\n"
    )
    lang, fw = EnvironmentDetector.detect(sample_log)
    assert lang == Language.PYTHON
    assert fw == Framework.UV


def test_node_jest_detection():
    sample_log = (
        "FAIL src/components/Button.test.js\n"
        "  ● Button Component › renders correctly\n"
        "npm ERR! Test failed. See above for details.\n"
    )
    lang, fw = EnvironmentDetector.detect(sample_log)
    assert lang == Language.NODE
    assert fw == Framework.JEST
