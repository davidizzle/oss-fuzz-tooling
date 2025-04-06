# 🛠️ ossfuzz-tooling

> A self-contained Python module for exploring OSS-Fuzz metadata and project state — built for researchers, contributors, and the GSoC community.

---

## 📌 Project Overview

`ossfuzz-tooling` is a CLI-friendly module designed to query and analyze OSS-Fuzz projects. It provides fast access to:

- ✅ Project listings & metadata
- ✅ Fuzzer configurations
- ✅ (Stubbed) Crash reports
- ✅ (Stubbed) Code coverage stats

This tool aims to reduce the friction of OSS-Fuzz research and experimentation, especially for:

- **GSoC contributors** working on [Project 8](https://gist.github.com/dynamicwebpaige/92f7739ad69d2863ac7e2032fe52fbad#8-self-contained-oss-fuzz-module-for-researchers-) or [Project 10](https://gist.github.com/dynamicwebpaige/92f7739ad69d2863ac7e2032fe52fbad#10-integrating-research-innovations-into-oss-fuzz-gen)
- **Security researchers** analyzing fuzzing coverage or crashes
- **Educators** building tooling demos or examples
- **ML researchers** linking fuzzing metadata with LLM-based agents

---

## 🚀 Installation

```bash
git clone https://github.com/davidizzle/oss-fuzz-tooling.git
cd oss-fuzz-tooling
pip install .
```

## 🧪 Features & Commands

### CLI Examples

```bash
# List all active OSS-Fuzz projects
oss-fuzz-tooling list-projects

# Get metadata about a specific project
oss-fuzz-tooling get-project --project ansible

# List fuzzers for a project
oss-fuzz-tooling get-fuzzers --project ansible

# Stub: View coverage info (fallback to sample)
oss-fuzz-tooling get-coverage --project ansible
```

## 📁 Project Structure

```bash
ossfuzz_tooling/
│
├── query.py        # Core data fetchers
├── cli.py          # CLI interface using argparse
├── __init__.py
├── sample_data/    # JSON fallback stubs
├── tests/          # pytest-compatible unit tests
```

## 🎯 Future Goals

- 🔄 Real-time crash & coverage querying via authenticated GCS access
- 📊 Integration with OSS-Fuzz-Gen dashboards
- 📦 Publish on PyPI for wider adoption
- 📘 Add example notebooks and docs

##

This tool is developed as part of a GSoC proposal for DeepMind’s OSS-Fuzz ecosystem:

- Project 8: Self-contained OSS-Fuzz Module for Researchers
- Project 10: Integrating Research Innovations into OSS-Fuzz-Gen

PRs, feedback, and extensions are welcome!