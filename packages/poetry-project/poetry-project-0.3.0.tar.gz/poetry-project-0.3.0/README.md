# poetry-project
Load pyproject.toml information into your project.
If you want to centralize your version information of your package at e.g. your *pyproject.toml*, then you simply might want to use
```python
from importlib_metadata import version
__version__ = version('pyklopp')
```
to load your package version.
This actually accesses the installed package in your current environment and retrieves the metadata version from there.
However, if you want to actually access content of your (probably not installed) *pyproject.toml*, you can use
``pip install poetry_project``

Usage:
```python
from poetry_project import get_version
__version__ = get_version('your_package_name')
```
or:
```python
import your_package  # must contain a pyproject.toml
from poetry_project import get_version
__version__ = get_version('your_package')
```

**Importantly** note, that you need to ship your *pyproject.toml* explicitly to your package.
This requires additional configuration, e.g. by adding the file to the include-statement within your *pyproject.toml*:
```toml
[tool.poetry]
include = [
    "pyproject.toml"
]
```
Only then this file gets actually packaged when delivered e.g. by PyPi.


# Development

## Deployment to PyPi
``poetry build``
``twine upload dist/*``