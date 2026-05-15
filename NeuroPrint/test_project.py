from project import generate_progress_bar
from project import detect_communication_style
from project import generate_writing_fingerprint


def test_generate_progress_bar():
    result = generate_progress_bar(50)

    assert "50%" in result


def test_detect_communication_style():

    text = "I analyze situations carefully because logic matters."

    result = detect_communication_style(text)

    assert result == "Analytical and Structured"


def test_generate_writing_fingerprint():

    text = "This is a sentence. This is another sentence."

    result = generate_writing_fingerprint(text)

    assert result["average_sentence_length"] > 0
