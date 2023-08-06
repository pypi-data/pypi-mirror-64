import os
from .engine import makedir
from pathlib import Path


def get_scratch():
    # where intermediate files get written
    if "CML_SCRATCH" in os.environ:
        scratch_location = os.environ["CML_SCRATCH"]
    else:
        # default to current running path of the script + /cml_scratch/
        current = os.environ["PWD"]
        scratch_location = os.path.join(current, "cml_scratch")

    scratch_location = Path(os.path.normpath(scratch_location))
    scratch_location.mkdir(parents=True, exist_ok=True)

    return scratch_location


# $CML_DATASET_PATH: Search path for Datasets.
# Formatted like any other path,
# i.e. separated:by:colons
if "CML_DATASET_PATH" in os.environ:
    dataset_path = [Path(p) for p in str(os.environ["CML_DATASET_PATH"]).split(":")]
else:
    dataset_path = []

dataset_path.append(Path.cwd())


# $CML_PLUGINS: List of plugins.
# Plugins to be loaded,
# separated by comma!
def get_plugins():
    if "CML_PLUGINS" in os.environ:
        return os.environ["CML_PLUGINS"].split(",")
    else:
        return []


# $CML_CACHE: Cache directory.
# currently NOT USED
if "CML_CACHE" in os.environ:
    cache_location = str(os.environ["CML_CACHE"])
    makedir(cache_location)
else:
    # default to current running path of the script + /cml_cache/
    current = os.environ["PWD"]
    cache_location = os.path.join(current, "cml_cache")

cache_location = os.path.normpath(cache_location)

# For this, see representation.sf
# path of ruNNer binary (needed for symmetry functions)
if "CML_RUNNER_PATH" in os.environ:
    runner_path = Path(os.environ["CML_RUNNER_PATH"])
else:
    runner_path = None

# For this, see representation.soap
# environment variables for quippy integreation
if "CML_QUIPPY_PYTHONPATH" in os.environ:
    quippy_pythonpath = os.path.normpath(os.environ["CML_QUIPPY_PYTHONPATH"])
else:
    quippy_pythonpath = None

if "CML_QUIPPY_PYTHON_EXE" in os.environ:
    quippy_python_exe = os.path.normpath(os.environ["CML_QUIPPY_PYTHON_EXE"])
else:
    quippy_python_exe = None
