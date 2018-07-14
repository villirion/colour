# -*- coding: utf-8 -*-
"""
References
----------
-   :cite:`AdobeSystems2013b` : Adobe Systems. (2013). Cube LUT Specification.
    Retrieved from https://drive.google.com/\
open?id=143Eh08ZYncCAMwJ1q4gWxVOqR_OSWYvs
"""

from __future__ import absolute_import

import os

from colour.utilities import CaseInsensitiveMapping, filter_kwargs
from .lut import LUT1D, LUT2D, LUT3D
from .iridas_cube import read_LUT_IridasCube, write_LUT_IridasCube
from .sony_spi1d import read_LUT_SonySPI1D, write_LUT_SonySPI1D
from .sony_spi3d import read_LUT_SonySPI3D, write_LUT_SonySPI3D

__all__ = ['LUT1D', 'LUT2D', 'LUT3D']
__all__ += ['read_LUT_IridasCube', 'write_LUT_IridasCube']
__all__ += ['read_LUT_SonySPI1D', 'write_LUT_SonySPI1D']
__all__ += ['read_LUT_SonySPI3D', 'write_LUT_SonySPI3D']

EXTENSION_TO_LUT_FORMAT_MAPPING = CaseInsensitiveMapping({
    '.cube': 'Iridas Cube',
    '.spi1d': 'Sony SPI1D',
    '.spi3d': 'Sony SPI3D'
})
"""
Extension to *LUT* format.

EXTENSION_TO_LUT_FORMAT_MAPPING : CaseInsensitiveMapping
    **{'.cube', '.spi1d'}**
"""

LUT_READ_METHODS = CaseInsensitiveMapping({
    'Iridas Cube': read_LUT_IridasCube,
    'Sony SPI1D': read_LUT_SonySPI1D,
    'Sony SPI3D': read_LUT_SonySPI3D,
})
LUT_READ_METHODS.__doc__ = """
Supported *LUT* reading methods.

References
----------
-   :cite:`AdobeSystems2013b`

LUT_READ_METHODS : CaseInsensitiveMapping
    **{'Iridas Cube', 'Sony SPI1D', 'Sony SPI3D'}**
"""


def read_LUT(path, method=None, **kwargs):
    """
    Reads given *LUT* file using given method.

    Parameters
    ----------
    path : unicode
        *LUT* path.
    method : unicode, optional
        **{None, 'Iridas Cube', 'Sony SPI1D', 'Sony SPI3D'}**,
        Reading method, if *None*, the method will be auto-detected according
        to extension.

    Returns
    -------
    LUT1D or LUT2D or LUT3d
        :class:`LUT1D`, :class:`LUT2D` or :class:`LUT3D` class instance.

    References
    ----------
    -   :cite:`AdobeSystems2013b`

    Examples
    --------
    Reading a 2D *Iridas* *.cube* *LUT*:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'iridas_cube',
    ...     'ACES_Proxy_10_to_ACES.cube')
    >>> print(read_LUT(path))
    LUT2D - ACES Proxy 10 to ACES
    -----------------------------
    <BLANKLINE>
    Dimensions : 2
    Domain     : [[0 0 0]
                  [1 1 1]]
    Size       : (32, 3)

    Reading a 1D *Sony* *.spi1d* *LUT*:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'sony_spi1d',
    ...     'oetf_reverse_sRGB_1D.spi1d')
    >>> print(read_LUT(path))
    LUT1D - oetf reverse sRGB 1D
    ----------------------------
    <BLANKLINE>
    Dimensions : 1
    Domain     : [-0.1  1.5]
    Size       : (16,)
    Comment 01 : Generated by "Colour 0.3.11".
    Comment 02 : "colour.models.oetf_reverse_sRGB".

    Reading a 3D *Sony* *.spi3d* *LUT*:

    >>> path = os.path.join(
    ...     os.path.dirname(__file__), 'tests', 'resources', 'sony_spi3d',
    ...     'ColourCorrect.spi3d')
    >>> print(read_LUT(path))
    LUT3D - ColourCorrect
    ---------------------
    <BLANKLINE>
    Dimensions : 3
    Domain     : [[0 0 0]
                  [1 1 1]]
    Size       : (4, 4, 4, 3)
    Comment 01 : Adapted from a LUT generated by Foundry::LUT.
    """

    if method is None:
        method = EXTENSION_TO_LUT_FORMAT_MAPPING[os.path.splitext(path)[-1]]

    function = LUT_READ_METHODS[method]

    return function(path, **filter_kwargs(function, **kwargs))


LUT_WRITE_METHODS = CaseInsensitiveMapping({
    'Iridas Cube': write_LUT_IridasCube,
    'Sony SPI1D': write_LUT_SonySPI1D,
    'Sony SPI3D': write_LUT_SonySPI3D,
})
LUT_WRITE_METHODS.__doc__ = """
Supported *LUT* reading methods.

References
----------
-   :cite:`AdobeSystems2013b`

LUT_WRITE_METHODS : CaseInsensitiveMapping
    **{'Iridas Cube', 'Sony SPI1D', 'Sony SPI3D'}**
"""


def write_LUT(LUT, path, decimals=7, method=None, **kwargs):
    """
    Writes given *LUT* to given file using given method.

    Parameters
    ----------
    LUT : LUT1D or LUT2D or LUT3d
        :class:`LUT1D`, :class:`LUT2D` or :class:`LUT3D` class instance to
        write at given path.
    path : unicode
        *LUT* path.
    decimals : int, optional
        Formatting decimals.
    method : unicode, optional
        **{None, 'Iridas Cube', 'Sony SPI1D', 'Sony SPI3D'}**,
        Writing method, if *None*, the method will be auto-detected according
        to extension.

    Returns
    -------
    bool
        Definition success.

    References
    ----------
    -   :cite:`AdobeSystems2013b`

    Examples
    --------
    Writing a 2D *Iridas* *.cube* *LUT*:

    >>> import numpy as np
    >>> LUT = LUT2D(
    ...     LUT2D.linear_table(16) ** (1 / 2.2),
    ...     'My LUT',
    ...     np.array([[-0.1, -0.2, -0.4], [1.5, 3.0, 6.0]]),
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT(LUT, 'My_LUT.cube')  # doctest: +SKIP

    Writing a 1D *Sony* *.spi1d* *LUT*:

    >>> LUT = LUT1D(
    ...     LUT1D.linear_table(16) ** (1 / 2.2),
    ...     'My LUT',
    ...     np.array([-0.1, 1.5]),
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT(LUT, 'My_LUT.spi1d')  # doctest: +SKIP

    Writing a 3D *Sony* *.spi3d* *LUT*:

    >>> LUT = LUT3D(
    ...     LUT3D.linear_table(16) ** (1 / 2.2),
    ...     'My LUT',
    ...     np.array([[0, 0, 0], [1, 1, 1]]),
    ...     comments=['A first comment.', 'A second comment.'])
    >>> write_LUT(LUT, 'My_LUT.cube')  # doctest: +SKIP
    """

    if method is None:
        method = EXTENSION_TO_LUT_FORMAT_MAPPING[os.path.splitext(path)[-1]]

    function = LUT_WRITE_METHODS[method]

    return function(LUT, path, decimals, **filter_kwargs(function, **kwargs))


__all__ += ['LUT_READ_METHODS', 'read_LUT', 'LUT_WRITE_METHODS', 'write_LUT']
