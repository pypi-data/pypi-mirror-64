from importlib_resources import files
import tomlkit


def load_toml_from_package(package, project_file_name='pyproject.toml'):
    if package is None:
        raise ValueError('Expected package to load a <{file}>-file from, but got <{package}>'.format(file=project_file_name, package=str(package)))

    package_path = files(package)

    while package_path.parent != package_path:
        possible_project_file_path = package_path.joinpath(project_file_name)
        if possible_project_file_path.exists():
            return tomlkit.parse(possible_project_file_path.read_text())
        package_path = package_path.parent

    raise ValueError('Could not find <{file}>-file in package <{package}>'.format(file=project_file_name, package=str(package)))


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
