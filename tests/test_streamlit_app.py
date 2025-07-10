import importlib.util
import json
import sys
import types
from pathlib import Path


def load_module(monkeypatch, data_file: Path):
    # stub minimal dependencies for import
    streamlit = types.ModuleType("streamlit")
    streamlit.cache_data = lambda func: func
    monkeypatch.setitem(sys.modules, "streamlit", streamlit)
    monkeypatch.setitem(sys.modules, "pandas", types.ModuleType("pandas"))
    monkeypatch.setitem(sys.modules, "altair", types.ModuleType("altair"))

    if "streamlit_app" in sys.modules:
        del sys.modules["streamlit_app"]
    spec = importlib.util.spec_from_file_location(
        "streamlit_app", Path("streamlit_app/streamlit_app.py")
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["streamlit_app"] = module
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "DATA_FILE", data_file)
    return module


def test_load_data(monkeypatch, tmp_path):
    data_path = tmp_path / "summary.json"
    with open(data_path, "w") as f:
        json.dump({"foo": 1}, f)
    module = load_module(monkeypatch, data_path)
    assert module.load_data() == {"foo": 1}
