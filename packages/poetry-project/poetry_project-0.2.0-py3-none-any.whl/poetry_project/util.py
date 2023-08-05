from importlib_resources import files
from pathlib import Path
import tomlkit


def load_pyproject_toml(base_path, file_name='pyproject.toml'):
    # Deprecated, as it uses a concrete base path and not a package
    d = Path(base_path)

    while d.parent != d:
        d = d.parent
        pyproject_path = Path(d, file_name)
        if pyproject_path.exists():
            with open(file=str(pyproject_path)) as handle:
                return tomlkit.parse(string=handle.read())
    return None


def load_toml_from_package(package, project_file_name='pyproject.toml'):
    package_path = files(package)

    while package_path.parent != package_path:
        package_path = package_path.parent
        possible_project_file_path = package_path.joinpath(project_file_name)
        if possible_project_file_path.exists():
            return tomlkit.parse(possible_project_file_path.read_text())

    return None


def get_poetry_attribute(attribute_name, package, pyproject_toml=None, project_file_name='pyproject.toml'):
    if pyproject_toml is None:
        pyproject_toml = load_toml_from_package(package, project_file_name)

    if pyproject_toml is None:
        return None

    if 'tool' not in pyproject_toml or 'poetry' not in pyproject_toml['tool']:
        return None

    attribute_path = attribute_name.split('.')
    unwrapped = pyproject_toml['tool']['poetry']
    for attribute in attribute_path:
        if attribute not in unwrapped:
            return None
        unwrapped = unwrapped[attribute]
    return unwrapped
