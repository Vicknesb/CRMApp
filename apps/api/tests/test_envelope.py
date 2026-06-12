from app.core.envelope import ok, err


def test_ok_shapes_data() -> None:
    result = ok({"status": "ok"})
    assert result["data"] == {"status": "ok"}
    assert result["error"] is None
    assert isinstance(result["meta"], dict)


def test_ok_with_meta() -> None:
    result = ok([1, 2], meta={"total": 2})
    assert result["data"] == [1, 2]
    assert result["meta"]["total"] == 2


def test_err_shapes_error() -> None:
    result = err("Something went wrong", details={"field": "name"})
    assert result["data"] is None
    assert result["error"]["message"] == "Something went wrong"
    assert result["error"]["details"]["field"] == "name"
