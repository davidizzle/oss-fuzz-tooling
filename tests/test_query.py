from ossfuzz_tooling import query

def test_list_projects():
    projects = query.list_projects()
    assert isinstance(projects, list)
    assert "zlib" in projects or len(projects) > 100

def test_get_project_info():
    sample = query.list_projects()[0]
    info = query.get_project_info(sample)
    assert isinstance(info, dict)
    assert "language" in info

def test_list_crashes_runs():
    # This just checks the function returns a list
    crashes = query.list_crashes("libxml2", limit=2)
    assert isinstance(crashes, list)
    assert all("id" in c and "url" in c for c in crashes)

def test_list_projects_has_common_names():
    projects = query.list_projects()
    common = {"zlib", "libxml2", "curl"}
    assert any(p in projects for p in common)

def test_get_project_info_handles_unknown():
    info = query.get_project_info("not-a-real-project")
    assert isinstance(info, dict)
    assert info == {}

def test_list_crashes_invalid_project():
    crashes = query.list_crashes("not-a-real-project", limit=1)
    assert crashes == []

def test_get_coverage_unavailable_project():
    result = query.get_coverage("not-a-real-project")
    assert isinstance(result, dict)
    assert result.get("status") == "unavailable"