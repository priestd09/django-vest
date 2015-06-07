# coding: utf-8
from django.conf import settings
from django.utils._os import safe_join
from django.template.loaders.filesystem import Loader as BaseLoader

from django_vest import config

__ALL__ = ('Loader',)


class ThemeLoaderMixin(object):
    """ Adding ability for work with themes.
    Use settings:
        - DEFAULT_THEME - default (main) theme
        - CURRENT_THEME

    Theme - this is folder inside TEMPLATE_DIRS.

    Supports inheritance only from DEFAULT_THEME like this:

    .. code:: html

        {% extends 'DEFAULT_THEME/app/index.html' %}
        ...


    """
    def get_template_sources(self, template_name, template_dirs=None):
        if not template_dirs:
            template_dirs = settings.TEMPLATE_DIRS

        _template_dirs = template_dirs

        template_name = template_name.replace('DEFAULT_THEME',
                                              config.DEFAULT_THEME)

        # First we find templates in CURRENT_THEME folder
        template_dirs = [safe_join(t, config.CURRENT_THEME)
                         for t in template_dirs]

        if config.CURRENT_THEME != config.DEFAULT_THEME:
            # If this is not default theme - add extra folders for search
            template_dirs.extend([safe_join(t, config.DEFAULT_THEME)
                                  for t in _template_dirs])
            template_dirs.extend(_template_dirs)

        return super(ThemeLoaderMixin, self).get_template_sources(
            template_name, template_dirs)


class Loader(ThemeLoaderMixin, BaseLoader):
    """ Template loader class
    """