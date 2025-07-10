import importlib.util
import json
import sys
from pathlib import Path

import pytest


def load_module(monkeypatch):
    monkeypatch.setenv("SINCERA_API_KEY", "dummy")
    monkeypatch.setitem(sys.modules, "requests", type("_R", (), {}))
    monkeypatch.setitem(sys.modules, "numpy", type("_N", (), {"percentile": lambda v, q: q}))
    if "sample_a2cr" in sys.modules:
        del sys.modules["sample_a2cr"]
    spec = importlib.util.spec_from_file_location(
        "sample_a2cr", Path("scripts/sample_a2cr.py")
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["sample_a2cr"] = module
    spec.loader.exec_module(module)
    return module


def test_list_sellers_files(monkeypatch):
    sa = load_module(monkeypatch)
    files = sa.list_sellers_files()
    assert any(f.endswith("sellers_aditude.json") for f in files)


def test_load_domains(monkeypatch):
    sa = load_module(monkeypatch)
    path = Path("reference_sellers_lists/sellers_aditude.json")
    domains = sa.load_domains(str(path))
    assert "moneywise.com" in domains
    assert len(domains) == len(set(domains))


def test_sample_domains(monkeypatch):
    sa = load_module(monkeypatch)
    domains = ["a", "b", "c", "d"]
    result = sa.sample_domains(domains, n=2)
    assert len(result) == 2
    result2 = sa.sample_domains(["x", "y"], n=5)
    assert len(result2) == 2


def test_fetch_a2cr_success(monkeypatch):
    sa = load_module(monkeypatch)

    class Resp:
        status_code = 200
        headers = {}

        @staticmethod
        def json():
            return {"avg_ads_to_content_ratio": 0.12}

    monkeypatch.setattr(sa, "respect_rate_limits", lambda: None)
    monkeypatch.setattr(sa.requests, "get", lambda *a, **kw: Resp(), raising=False)

    a2cr, data = sa.fetch_a2cr("foo.com")
    assert a2cr == 0.12
    assert data["avg_ads_to_content_ratio"] == 0.12


def test_fetch_a2cr_retry(monkeypatch):
    sa = load_module(monkeypatch)

    class Resp429:
        status_code = 429
        headers = {"Retry-After": "0.1"}
        text = "rate limit"

    class Resp200:
        status_code = 200
        headers = {}

        @staticmethod
        def json():
            return {"avg_ads_to_content_ratio": 0.2}

    responses = [Resp429(), Resp200()]

    def fake_get(*a, **kw):
        return responses.pop(0)

    sleeps = []
    monkeypatch.setattr(sa.requests, "get", fake_get, raising=False)
    monkeypatch.setattr(sa, "respect_rate_limits", lambda: None)
    monkeypatch.setattr(sa.time, "sleep", lambda s: sleeps.append(s))

    a2cr, data = sa.fetch_a2cr("foo.com")
    assert a2cr == 0.2
    assert sleeps
    assert sleeps[0] >= 0.1


def test_process_group(tmp_path, monkeypatch):
    sa = load_module(monkeypatch)

    sellers_file = tmp_path / "sellers.json"
    with open(sellers_file, "w") as f:
        json.dump({"sellers": [{"domain": "a.com"}, {"domain": "b.com"}]}, f)

    monkeypatch.setattr(sa, "RAW_OUTPUT_DIR", str(tmp_path / "raw"))
    monkeypatch.setattr(sa, "sample_domains", lambda domains, n=sa.SAMPLE_SIZE: domains)
    monkeypatch.setattr(sa, "fetch_a2cr", lambda domain: (0.1, {"total_supply_paths": 5, "avg_page_weight": 1.0}))
    monkeypatch.setattr(sa.time, "sleep", lambda s: None)

    summary = sa.process_group(str(sellers_file), "test")

    assert summary["a2cr"]["n"] == 2
    result_path = Path(sa.RAW_OUTPUT_DIR) / "test_results.json"
    assert result_path.exists()
    with open(result_path) as f:
        data = json.load(f)
    assert "a.com" in data


def test_main(tmp_path, monkeypatch):
    sa = load_module(monkeypatch)

    monkeypatch.setattr(sa, "ANALYSIS_DIR", str(tmp_path / "analysis"))
    monkeypatch.setattr(sa, "list_sellers_files", lambda: ["/tmp/sellers_a.json", "/tmp/sellers_b.json"])
    monkeypatch.setattr(sa, "process_group", lambda path, name: {"a2cr": {"n": 1}})
    monkeypatch.setattr(sys.modules['builtins'], "print", lambda *a, **kw: None)

    sa.main()

    summary_file = Path(sa.ANALYSIS_DIR) / "summary.json"
    assert summary_file.exists()
    data = json.load(open(summary_file))
    assert data == {"sellers_a_percentiles": {"a2cr": {"n": 1}}, "sellers_b_percentiles": {"a2cr": {"n": 1}}}
