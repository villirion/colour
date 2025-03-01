# -*- coding: utf-8 -*-

import sys

from .data_structures import (Lookup, Structure, CaseInsensitiveMapping,
                              LazyCaseInsensitiveMapping)
from .common import (
    CacheRegistry, CACHE_REGISTRY, handle_numpy_errors, ignore_numpy_errors,
    raise_numpy_errors, print_numpy_errors, warn_numpy_errors,
    ignore_python_warnings, batch, disable_multiprocessing,
    multiprocessing_pool, is_matplotlib_installed, is_networkx_installed,
    is_openimageio_installed, is_pandas_installed, is_tqdm_installed, required,
    is_iterable, is_string, is_numeric, is_integer, is_sibling, filter_kwargs,
    filter_mapping, first_item, get_domain_range_scale, set_domain_range_scale,
    domain_range_scale, to_domain_1, to_domain_10, to_domain_100,
    to_domain_degrees, to_domain_int, from_range_1, from_range_10,
    from_range_100, from_range_degrees, from_range_int, copy_definition,
    validate_method)
from .verbose import (
    ColourWarning, ColourUsageWarning, ColourRuntimeWarning, message_box,
    show_warning, warning, runtime_warning, usage_warning, filter_warnings,
    suppress_warnings, numpy_print_options, ANCILLARY_COLOUR_SCIENCE_PACKAGES,
    ANCILLARY_RUNTIME_PACKAGES, ANCILLARY_DEVELOPMENT_PACKAGES,
    ANCILLARY_EXTRAS_PACKAGES, describe_environment)
from .array import (as_array, as_int_array, as_float_array, as_numeric, as_int,
                    as_float, set_float_precision, set_int_precision,
                    as_namedtuple, closest_indexes, closest, interval,
                    is_uniform, in_array, tstack, tsplit, row_as_diagonal,
                    orient, centroid, fill_nan, ndarray_write, zeros, ones,
                    full, index_along_last_axis)
from ..algebra.common import (normalise_maximum, vector_dot, matrix_dot,
                              linear_conversion, linstep_function)
from .metrics import metric_mse, metric_psnr

from colour.utilities.deprecation import ModuleAPI, build_API_changes
from colour.utilities.documentation import is_documentation_building

__all__ = [
    'Lookup', 'Structure', 'CaseInsensitiveMapping',
    'LazyCaseInsensitiveMapping'
]
__all__ += [
    'CacheRegistry', 'CACHE_REGISTRY', 'handle_numpy_errors',
    'ignore_numpy_errors', 'raise_numpy_errors', 'print_numpy_errors',
    'warn_numpy_errors', 'ignore_python_warnings', 'batch',
    'disable_multiprocessing', 'multiprocessing_pool',
    'is_matplotlib_installed', 'is_networkx_installed',
    'is_openimageio_installed', 'is_pandas_installed', 'is_tqdm_installed',
    'required', 'is_iterable', 'is_string', 'is_numeric', 'is_integer',
    'is_sibling', 'filter_kwargs', 'filter_mapping', 'first_item',
    'get_domain_range_scale', 'set_domain_range_scale', 'domain_range_scale',
    'to_domain_1', 'to_domain_10', 'to_domain_100', 'to_domain_degrees',
    'to_domain_int', 'from_range_1', 'from_range_10', 'from_range_100',
    'from_range_degrees', 'from_range_int', 'copy_definition',
    'validate_method'
]
__all__ += [
    'ColourWarning', 'ColourUsageWarning', 'ColourRuntimeWarning',
    'message_box', 'show_warning', 'warning', 'runtime_warning',
    'usage_warning', 'filter_warnings', 'suppress_warnings',
    'numpy_print_options', 'ANCILLARY_COLOUR_SCIENCE_PACKAGES',
    'ANCILLARY_RUNTIME_PACKAGES', 'ANCILLARY_DEVELOPMENT_PACKAGES',
    'ANCILLARY_EXTRAS_PACKAGES', 'describe_environment'
]
__all__ += [
    'as_array', 'as_int_array', 'as_float_array', 'as_numeric', 'as_int',
    'as_float', 'set_float_precision', 'set_int_precision', 'as_namedtuple',
    'closest_indexes', 'closest', 'normalise_maximum', 'interval',
    'is_uniform', 'in_array', 'tstack', 'tsplit', 'row_as_diagonal',
    'vector_dot', 'matrix_dot', 'orient', 'centroid', 'linear_conversion',
    'fill_nan', 'linstep_function', 'ndarray_write', 'zeros', 'ones', 'full',
    'index_along_last_axis'
]
__all__ += ['metric_mse', 'metric_psnr']


# ----------------------------------------------------------------------------#
# ---                API Changes and Deprecation Management                ---#
# ----------------------------------------------------------------------------#
class utilities(ModuleAPI):
    def __getattr__(self, attribute):
        return super(utilities, self).__getattr__(attribute)


# v0.4.0
API_CHANGES = {
    'ObjectFutureAccessChange': [
        [
            'colour.utilities.linstep_function',
            'colour.algebra.linstep_function',
        ],
        [
            'colour.utilities.linear_conversion',
            'colour.algebra.linear_conversion',
        ],
        [
            'colour.utilities.matrix_dot',
            'colour.algebra.matrix_dot',
        ],
        [
            'colour.utilities.normalise_maximum',
            'colour.algebra.normalise_maximum',
        ],
        [
            'colour.utilities.vector_dot',
            'colour.algebra.vector_dot',
        ],
    ]
}
"""
Defines the *colour.utilities* sub-package API changes.

API_CHANGES : dict
"""

if not is_documentation_building():
    sys.modules['colour.utilities'] = utilities(
        sys.modules['colour.utilities'], build_API_changes(API_CHANGES))

    del ModuleAPI, is_documentation_building, build_API_changes, sys
