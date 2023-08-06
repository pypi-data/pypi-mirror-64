import re

from semantic_version import Version
from setuptools import setup

# find first version number in CHANGELOG.md and use that.
with open('CHANGELOG.md') as file_:
    for line in file_.readlines():
        if line.startswith("## ["):
            version = re.search("^(## ?\[)(.*)(\].*)$", line).group(2)
            break


try:
    Version(version)
    setup(version=version)
except:
    raise TypeError(f"Version '{version}' in CHANGELOG file is not a semantic version number.")
