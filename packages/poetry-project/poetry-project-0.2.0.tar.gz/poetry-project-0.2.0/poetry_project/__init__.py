from poetry_project.util import get_poetry_attribute


def get_version(package=__package__):
    return get_poetry_attribute('version', package)


def get_name(package=__package__):
    return get_poetry_attribute('name', package)
