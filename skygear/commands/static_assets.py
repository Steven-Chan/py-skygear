import logging
import os

from ..options import options
from ..registry import get_registry
from ..assets import CollectorException, StaticAssetsCollector

_registry = get_registry()
log = logging.getLogger(__name__)


def collect_static_assets():
    dist = os.path.abspath(os.path.expanduser(options.collect_assets))
    collector = StaticAssetsCollector(dist)

    if os.path.exists(dist):
        if not options.force_assets:
            log.error('Directory %s already exists. Remove the directory '
                      'first, or specify --force-assets to discard files in '
                      'the directory.',
                      dist)
            exit(1)
        collector.clean()

    if not _registry.static_assets:
        log.warn('No static assets are declared.')
        return collector.dist

    for prefix, func in _registry.static_assets.items():
        log.info('Static assets %s', prefix)
        path = func()
        try:
            collector.collect(prefix, path)
        except CollectorException as e:
            log.error(str(e))
            exit(1)

    return collector.dist
