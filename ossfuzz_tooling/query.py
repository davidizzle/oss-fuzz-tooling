import json
import os
import yaml
# These dependencies are needed for the additional functions detailing crashes and fuzzers, but may not be necessary
import requests
import re
from bs4 import BeautifulSoup

OSS_FUZZ_PROJECTS_DIR = os.environ.get("OSS_FUZZ_PROJECTS_DIR", "../oss-fuzz/projects")

def list_projects():
    # We want to list all the projects, if what is contained in the projects directory is a directory
    return sorted([
        name for name in os.listdir(OSS_FUZZ_PROJECTS_DIR)
        if os.path.isdir(os.path.join(OSS_FUZZ_PROJECTS_DIR, name))
    ])

def get_project_info(project_name: str):
    try:
        yaml_path = os.path.join(OSS_FUZZ_PROJECTS_DIR, project_name, 'project.yaml')
        if not os.path.exists(yaml_path):
            return {}

        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception:
        print(f"Information on project {project_name} does not exist.")
        return {}
    
def list_crashes(project_name, limit=5):
    # TODO: [GSoC] This will fail due to GCS restricted access, so we throw exception and stub behavior with local .json
    url = f"https://oss-fuzz.com/testcase?project={project_name}"
    try:
        raise NotImplementedError(
            "Public crash listing not currently supported by oss-fuzz.com. "
            "This function is reserved for future GSoC enhancements."
            "❌ No fallback crash data found."
        )
        """List recent crash reports for a given OSS-Fuzz project."""
        res = requests.get(url)
        if res.status_code != 200:
            print("Error: " + str(res.status_code))
            raise Exception(f"Failed to fetch crash list for {project_name}")
        
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table")
        if not table:
            return []

        rows = table.find_all("tr")[1:limit+1]
        crashes = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            crash_id = cols[0].text.strip()
            title = cols[2].text.strip()
            last_updated = cols[3].text.strip()
            crash_url = f"https://oss-fuzz.com/testcase-detail/{crash_id}"
            crashes.append({
                "id": crash_id,
                "title": title,
                "url": crash_url,
                "last_updated": last_updated
            })

        return crashes
    except Exception:
        print(f"⚠️  Could not fetch crash data from {url} — using fallback data.")
        try: 
            path = os.path.join(os.path.dirname(__file__), '..', 'sample_data', 'sample_crashes.json')
            with open(path, 'r') as f:
                data = json.load(f)
            return data.get(project_name, [])
        except Exception as e:
            print(f"❌  No fallback crash data found.\n{e}")
            return []

def get_fuzzers(project_name: str):
    # TODO: [GSoC] Make a more clever function that better matches patterns extracting fuzzers
    url = f"https://raw.githubusercontent.com/google/oss-fuzz/master/projects/{project_name}/build.sh"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Could not fetch build.sh for {project_name}")

    lines = response.text.splitlines()
    fuzzers = []

    for line in lines:
        # Look for likely fuzzer binary builds
        # Pattern 1: -o $OUT/fuzzer_name
        match1 = re.search(r'\$OUT/([a-zA-Z0-9_\-\.]+)', line)
        if match1:
            fuzzers.append(match1.group(1))

        # Pattern 2: compile_*_fuzzer ... fuzzer_path
        match2 = re.search(r'compile_[a-z_]*fuzzer\s+[^\s]+\s+([^\s]+)', line)
        if match2:
            fuzzer_path = match2.group(1)
            fuzzer_name = fuzzer_path.split("/")[-1]  # Just get basename
            fuzzers.append(fuzzer_name)

    return fuzzers

def get_coverage(project_name: str):
    # TODO: [GSoC] This is supposed to work with commands like "gsutil ls gs://angular-corpus.clusterfuzz-external.appspot.com/" but access is restricted
    # We will stub behavior for now
    coverage_url = f"https://storage.googleapis.com/oss-fuzz-coverage/{project_name}/reports/latest/report.json"

    try:
        response = requests.get(coverage_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Non-200 response")
    except Exception as e:
        print(f"⚠️ Could not fetch coverage for {project_name}. Using fallback.\n{e}")
        try:
            path = os.path.join(os.path.dirname(__file__), '..', 'sample_data', 'sample_coverage.json')
            with open(path, 'r') as f:
                data = json.load(f)
            return data.get(project_name, {"status": "unavailable"})
        except Exception as e:
            print(f"❌ No fallback sample coverage data found.\n{e}")
            return {"status": "unavailable"}