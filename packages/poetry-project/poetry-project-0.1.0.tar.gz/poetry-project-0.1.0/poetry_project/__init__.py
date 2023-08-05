from poetry_project.util import get_poetry_attribute


def get_version(base_path=__file__, pyproject_toml=None):
    return get_poetry_attribute('version', base_path, pyproject_toml)


def get_name(base_path=__file__, pyproject_toml=None):
    return get_poetry_attribute('name', base_path, pyproject_toml)
