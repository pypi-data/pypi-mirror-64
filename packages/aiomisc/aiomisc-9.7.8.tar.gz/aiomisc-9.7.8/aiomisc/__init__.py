import logging
import pkg_resources

from . import io
from . import log

from .backoff import asyncbackoff
from .context import Context, get_context
from .entrypoint import entrypoint
from .periodic import PeriodicCallback
from .service import Service
from .signal import Signal, receiver
from .iterator_wrapper import IteratorWrapper
from .thread_pool import (
    context_partial, IteratorWrapperSeparate, sync_wait_coroutine,
    threaded, threaded_iterable, threaded_iterable_separate,
    threaded_separate, ThreadPoolExecutor
)
from .process_pool import ProcessPoolExecutor
from .timeout import timeout
from .pool import PoolBase

from .utils import (
    awaitable,
    bind_socket,
    cancel_tasks,
    chunk_list,
    new_event_loop,
    select,
    SelectResult,
    shield,
)


plugins = {
    entry_point.name: entry_point.load()
    for entry_point
    in pkg_resources.iter_entry_points('aiomisc.plugins')
}


def setup_plugins():
    logger = logging.getLogger(__name__)
    for name, plugin in plugins.items():
        try:
            logger.debug("Trying to load %r %r", name, plugin)
            plugin.setup()
        except:  # noqa
            logger.exception('Error on %s aiomisc plugin setup', name)
            raise


setup_plugins()


__all__ = (
    'asyncbackoff',
    'awaitable',
    'bind_socket',
    'cancel_tasks',
    'chunk_list',
    'Context',
    'context_partial',
    'entrypoint',
    'get_context',
    'io',
    'IteratorWrapper',
    'IteratorWrapperSeparate',
    'log',
    'new_event_loop',
    'PeriodicCallback',
    'plugins',
    'PoolBase',
    'ProcessPoolExecutor',
    'receiver',
    'select',
    'SelectResult',
    'Service',
    'shield',
    'Signal',
    'sync_wait_coroutine',
    'threaded',
    'threaded_iterable',
    'threaded_iterable_separate',
    'threaded_separate',
    'ThreadPoolExecutor',
    'timeout',
)
