from app.services.ai_service import _safe_parse


def test_safe_parse_valid_json():
    text = '[{"id": 1, "reason": "great pick"}, {"id": 2, "reason": "another one"}]'
    result = _safe_parse(text)
    assert result == [
        {"id": 1, "reason": "great pick"},
        {"id": 2, "reason": "another one"},
    ]


def test_safe_parse_wrapped_in_code_fence():
    text = '```json\n[{"id": 1, "reason": "great pick"}]\n```'
    result = _safe_parse(text)
    assert result == [{"id": 1, "reason": "great pick"}]


def test_safe_parse_wrapped_in_prose():
    text = 'Here are the top picks:\n\n[{"id": 1, "reason": "great pick"}]\n\nHope that helps!'
    result = _safe_parse(text)
    assert result == [{"id": 1, "reason": "great pick"}]


def test_safe_parse_malformed_json_returns_empty_list():
    text = '[{"id": 1, "reason": "cut off mid-strin'
    result = _safe_parse(text)
    assert result == []


def test_safe_parse_no_array_found_returns_empty_list():
    text = "Sorry, I can't help with that."
    result = _safe_parse(text)
    assert result == []


def test_safe_parse_empty_string_returns_empty_list():
    result = _safe_parse("")
    assert result == []