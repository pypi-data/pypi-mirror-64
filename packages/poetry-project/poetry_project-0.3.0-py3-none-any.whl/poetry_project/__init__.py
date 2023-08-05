from poetry_project.util import get_poetry_attribute, load_toml_from_package


def get_version(package=__package__):
    try:
        return get_poetry_attribute('version', package)
    except ValueError:
        import importlib_metadata
        return importlib_metadata.version(package)


def get_name(package=__package__):
    return get_poetry_attribute('name', package)


def get_authors(package=__package__):
    return get_poetry_attribute('authors', package)


def get_dependencies(package=__package__):
    return get_poetry_attribute('dependencies', package)


def get_toml(package=__package__, toml_file_name='pyproject.toml'):
    return load_toml_from_package(package, toml_file_name)
