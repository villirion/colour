# -*- coding: utf-8 -*-
"""
UPRTek and Sekonic Spectral Data
================================

Defines the input and output objects for *UPRTek* and *Sekonic*
*Pseudo-XLS*/*CSV* spectral data files.

-   :class:`colour.SpectralDistribution_UPRTek`
-   :class:`colour.SpectralDistribution_Sekonic`
"""

import csv
import json
import os
import re
from collections import defaultdict

from colour.io import SpectralDistribution_IESTM2714
from colour.utilities import as_float_array, is_string

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2021 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = ['SpectralDistribution_UPRTek', 'SpectralDistribution_Sekonic']


class SpectralDistribution_UPRTek(SpectralDistribution_IESTM2714):
    """
    This class serves as a parser to read and write *IES TM-27-14*
    spectral data XML file from a *UPRTek* *Pseudo-XLS* file.

    Parameters
    ----------
    path : unicode
        Path for *UPRTek* *Pseudo-XLS* file.

    Methods
    -------
    -   :meth:`~colour.SpectralDistribution_UPRTek.__init__`
    -   :meth:`~colour.SpectralDistribution_UPRTek.read`
    -   :meth:`~colour.SpectralDistribution_UPRTek.write`

    Examples
    --------
    >>> from os.path import dirname, join
    >>> from colour import SpectralShape
    >>> directory = join(dirname(__file__), 'tests', 'resources')
    >>> sd = SpectralDistribution_UPRTek(
    ...     join(directory, 'ESPD2021_0104_231446.xls'))
    >>> print(sd.read().align(SpectralShape(380, 780, 10)))
    [[  3.80000000e+02   3.02670000e-02]
     [  3.90000000e+02   3.52230000e-02]
     [  4.00000000e+02   1.93250000e-02]
     [  4.10000000e+02   2.94260000e-02]
     [  4.20000000e+02   8.76780000e-02]
     [  4.30000000e+02   6.32578000e-01]
     [  4.40000000e+02   3.62565900e+00]
     [  4.50000000e+02   1.42069180e+01]
     [  4.60000000e+02   1.70112970e+01]
     [  4.70000000e+02   1.19673130e+01]
     [  4.80000000e+02   8.42736200e+00]
     [  4.90000000e+02   7.97729800e+00]
     [  5.00000000e+02   8.71903600e+00]
     [  5.10000000e+02   9.55321500e+00]
     [  5.20000000e+02   9.90610500e+00]
     [  5.30000000e+02   9.91394400e+00]
     [  5.40000000e+02   9.74738000e+00]
     [  5.50000000e+02   9.53404900e+00]
     [  5.60000000e+02   9.27392200e+00]
     [  5.70000000e+02   9.02323400e+00]
     [  5.80000000e+02   8.91788800e+00]
     [  5.90000000e+02   9.11454600e+00]
     [  6.00000000e+02   9.55787100e+00]
     [  6.10000000e+02   1.00600760e+01]
     [  6.20000000e+02   1.04846200e+01]
     [  6.30000000e+02   1.05679540e+01]
     [  6.40000000e+02   1.04359870e+01]
     [  6.50000000e+02   9.82122300e+00]
     [  6.60000000e+02   8.77578300e+00]
     [  6.70000000e+02   7.56471800e+00]
     [  6.80000000e+02   6.29808600e+00]
     [  6.90000000e+02   5.15623400e+00]
     [  7.00000000e+02   4.05390600e+00]
     [  7.10000000e+02   3.06638600e+00]
     [  7.20000000e+02   2.19250000e+00]
     [  7.30000000e+02   1.53922800e+00]
     [  7.40000000e+02   1.14938200e+00]
     [  7.50000000e+02   9.05095000e-01]
     [  7.60000000e+02   6.90947000e-01]
     [  7.70000000e+02   5.08426000e-01]
     [  7.80000000e+02   4.11766000e-01]]
    >>> sd.header.comments
    '{"Model Name": "CV600", "Serial Number": "19J00789", \
"Time": "2021/01/04_23:14:46", "Memo": [], "LUX": 695.154907, \
"fc": 64.605476, "CCT": 5198.0, "Duv": -0.00062, "I-Time": 12000.0, \
"X": 682.470886, "Y": 695.154907, "Z": 631.635071, "x": 0.339663, \
"y": 0.345975, "u\\'": 0.209915, "v\\'": 0.481087, "LambdaP": 456.0, \
"LambdaPValue": 18.404581, "CRI": 92.956993, "R1": 91.651062, \
"R2": 93.014732, "R3": 97.032013, "R4": 93.513229, "R5": 92.48259, \
"R6": 91.48687, "R7": 93.016129, "R8": 91.459312, "R9": 77.613075, \
"R10": 86.981613, "R11": 94.841324, "R12": 74.139542, "R13": 91.073837, \
"R14": 97.064323, "R15": 88.615669, "TLCI": 97.495056, "TLMF-A": 1.270032, \
"SSI-A": 44.881924, "Rf": 87.234917, "Rg": 98.510712, "IRR": 2.607891}'
    >>> sd.write(join(directory, 'ESPD2021_0104_231446.spdx'))
    ... # doctest: +SKIP
    """

    def __init__(self, path, delimiter='\t', spectra_section='380', **kwargs):
        super(SpectralDistribution_UPRTek, self).__init__(path, **kwargs)

        self._delimiter = '\t'
        self.delimiter = delimiter

        self._spectra_section = '380'
        self.spectra_section = spectra_section

        self._metadata = {}

    @property
    def delimiter(self):
        """
        Getter and setter property for the delimiter.

        Parameters
        ----------
        value : unicode
            Value to set the delimiter with.

        Returns
        -------
        unicode
            Delimiter.
        """

        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        """
        Setter for the **self.delimiter** property.
        """

        if value is not None:
            assert is_string(
                value
            ), '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                'delimiter', value)

        self._delimiter = value

    @property
    def spectra_section(self):
        """
        Getter and setter property for the spectral section.

        Parameters
        ----------
        value : unicode
            Value to set the spectral section with.

        Returns
        -------
        unicode
            Spectra section.
        """

        return self._spectra_section

    @spectra_section.setter
    def spectra_section(self, value):
        """
        Setter for the **self.spectra_section** property.
        """

        if value is not None:
            assert is_string(
                value
            ), '"{0}" attribute: "{1}" is not a "string" like object!'.format(
                'spectra_section', value)

        self._spectra_section = value

    @property
    def metadata(self):
        """
        Getter and setter property for the metadata.

        Parameters
        ----------
        value : dict
            Value to set the metadata with.

        Returns
        -------
        unicode
            Metadata.
        """

        return self._metadata

    def read(self):
        """
        Reads and parses the spectral data from a given *UPRTek* *CSV* file.

        Returns
        -------
        SpectralDistribution_UPRTek
            *UPRTek* spectral distribution.

        Examples
        --------
        >>> from os.path import dirname, join
        >>> from colour import SpectralShape
        >>> directory = join(dirname(__file__), 'tests', 'resources')
        >>> sd = SpectralDistribution_UPRTek(
        ...     join(directory, 'ESPD2021_0104_231446.xls'))
        >>> print(sd.read().align(SpectralShape(380, 780, 10)))
        [[  3.80000000e+02   3.02670000e-02]
         [  3.90000000e+02   3.52230000e-02]
         [  4.00000000e+02   1.93250000e-02]
         [  4.10000000e+02   2.94260000e-02]
         [  4.20000000e+02   8.76780000e-02]
         [  4.30000000e+02   6.32578000e-01]
         [  4.40000000e+02   3.62565900e+00]
         [  4.50000000e+02   1.42069180e+01]
         [  4.60000000e+02   1.70112970e+01]
         [  4.70000000e+02   1.19673130e+01]
         [  4.80000000e+02   8.42736200e+00]
         [  4.90000000e+02   7.97729800e+00]
         [  5.00000000e+02   8.71903600e+00]
         [  5.10000000e+02   9.55321500e+00]
         [  5.20000000e+02   9.90610500e+00]
         [  5.30000000e+02   9.91394400e+00]
         [  5.40000000e+02   9.74738000e+00]
         [  5.50000000e+02   9.53404900e+00]
         [  5.60000000e+02   9.27392200e+00]
         [  5.70000000e+02   9.02323400e+00]
         [  5.80000000e+02   8.91788800e+00]
         [  5.90000000e+02   9.11454600e+00]
         [  6.00000000e+02   9.55787100e+00]
         [  6.10000000e+02   1.00600760e+01]
         [  6.20000000e+02   1.04846200e+01]
         [  6.30000000e+02   1.05679540e+01]
         [  6.40000000e+02   1.04359870e+01]
         [  6.50000000e+02   9.82122300e+00]
         [  6.60000000e+02   8.77578300e+00]
         [  6.70000000e+02   7.56471800e+00]
         [  6.80000000e+02   6.29808600e+00]
         [  6.90000000e+02   5.15623400e+00]
         [  7.00000000e+02   4.05390600e+00]
         [  7.10000000e+02   3.06638600e+00]
         [  7.20000000e+02   2.19250000e+00]
         [  7.30000000e+02   1.53922800e+00]
         [  7.40000000e+02   1.14938200e+00]
         [  7.50000000e+02   9.05095000e-01]
         [  7.60000000e+02   6.90947000e-01]
         [  7.70000000e+02   5.08426000e-01]
         [  7.80000000e+02   4.11766000e-01]]
        """

        def as_array(a):
            """
            Inputs list of numbers and converts each element to
            float data type.
            """

            return [float(e) for e in a]

        spectral_sections = defaultdict(list)
        with open(self.path, encoding='utf-8') as csv_file:
            content = csv.reader(csv_file, delimiter=self._delimiter)

            spectral_section = 0
            for row in content:
                if not ''.join(row).strip():
                    continue

                key, value = row[0], row[1:]
                value = value[0] if len(value) == 1 else value

                search = re.search('(\\d{3})\\[?nm\\]?', key)
                if search:
                    wavelength = search.group(1)

                    if wavelength == self._spectra_section:
                        spectral_section += 1

                    spectral_sections[spectral_section].append(
                        [wavelength, value])
                else:
                    for method in (int, float, as_array):
                        try:
                            self._metadata[key] = method(value)
                            break
                        except Exception:
                            self._metadata[key] = value

        self.name = os.path.splitext(os.path.basename(self.path))[0]
        spectral_data = as_float_array(spectral_sections[sorted(
            spectral_sections.keys())[-1]])

        self.wavelengths = spectral_data[..., 0]
        self.values = spectral_data[..., 1]

        self.header.comments = json.dumps(self._metadata)

        self.header.report_date = self._metadata.get('Time')
        self.header.measurement_equipment = self._metadata.get('Model Name')
        self.header.manufacturer = 'UPRTek'
        self.spectral_quantity = 'Irradiance'

        return self


class SpectralDistribution_Sekonic(SpectralDistribution_UPRTek):
    """
    This class serves as a parser to read and write *IES TM-27-14*
    spectral data XML file from a *Sekonic* *CSV* file.

    Parameters
    ----------
    path : unicode
        Path for *Sekonic* *CSV* file.

    Methods
    -------
    -   :meth:`~colour.SpectralDistribution_Sekonic.__init__`
    -   :meth:`~colour.SpectralDistribution_Sekonic.read`
    -   :meth:`~colour.SpectralDistribution_Sekonic.write`

    Examples
    --------
    >>> from os.path import dirname, join
    >>> from colour import SpectralShape
    >>> directory = join(dirname(__file__), 'tests', 'resources')
    >>> sd = SpectralDistribution_Sekonic(
    ...     join(directory, 'RANDOM_001_02._3262K.csv'))
    >>> print(sd.read().align(SpectralShape(380, 780, 10)))
    [[  3.80000000e+02   1.69406589e-21]
     [  3.90000000e+02   2.11758237e-22]
     [  4.00000000e+02   1.19813650e-05]
     [  4.10000000e+02   1.97110530e-05]
     [  4.20000000e+02   2.99661440e-05]
     [  4.30000000e+02   6.38192720e-05]
     [  4.40000000e+02   1.68909683e-04]
     [  4.50000000e+02   3.31902935e-04]
     [  4.60000000e+02   3.33143020e-04]
     [  4.70000000e+02   2.30227481e-04]
     [  4.80000000e+02   1.66981976e-04]
     [  4.90000000e+02   1.64439844e-04]
     [  5.00000000e+02   2.01534538e-04]
     [  5.10000000e+02   2.57840526e-04]
     [  5.20000000e+02   3.04612651e-04]
     [  5.30000000e+02   3.41368344e-04]
     [  5.40000000e+02   3.63639323e-04]
     [  5.50000000e+02   3.87050648e-04]
     [  5.60000000e+02   4.21619130e-04]
     [  5.70000000e+02   4.58150520e-04]
     [  5.80000000e+02   5.01176575e-04]
     [  5.90000000e+02   5.40883630e-04]
     [  6.00000000e+02   5.71256795e-04]
     [  6.10000000e+02   5.83703280e-04]
     [  6.20000000e+02   5.57688472e-04]
     [  6.30000000e+02   5.17328095e-04]
     [  6.40000000e+02   4.39994939e-04]
     [  6.50000000e+02   3.62766819e-04]
     [  6.60000000e+02   2.96465587e-04]
     [  6.70000000e+02   2.43966802e-04]
     [  6.80000000e+02   2.04134776e-04]
     [  6.90000000e+02   1.75304012e-04]
     [  7.00000000e+02   1.52887544e-04]
     [  7.10000000e+02   1.29795619e-04]
     [  7.20000000e+02   1.03122693e-04]
     [  7.30000000e+02   8.77607820e-05]
     [  7.40000000e+02   7.61524130e-05]
     [  7.50000000e+02   7.06516880e-05]
     [  7.60000000e+02   3.72199210e-05]
     [  7.70000000e+02   3.63058860e-05]
     [  7.80000000e+02   3.55755470e-05]]
    >>> sd.header.comments # doctest: +SKIP
    >>> sd.write(join(directory, 'RANDOM_001_02._3262K.spdx')
    ... # doctest: +SKIP
    """

    def __init__(self, path, delimiter=',', spectra_section='380', **kwargs):
        super(SpectralDistribution_Sekonic, self).__init__(
            path, delimiter, spectra_section, **kwargs)

    def read(self):
        """
        Reads and parses the spectral data from a given *Sekonic* *Pseudo-XLS*
        file.

        Returns
        -------
        SpectralDistribution_Sekonic
            *Sekonic* spectral distribution.

        Examples
        --------
        >>> from os.path import dirname, join
        >>> from colour import SpectralShape
        >>> directory = join(dirname(__file__), 'tests', 'resources')
        >>> sd = SpectralDistribution_Sekonic(
        ...     join(directory, 'RANDOM_001_02._3262K.csv'))
        >>> print(sd.read().align(SpectralShape(380, 780, 10)))
        [[  3.80000000e+02   1.69406589e-21]
         [  3.90000000e+02   2.11758237e-22]
         [  4.00000000e+02   1.19813650e-05]
         [  4.10000000e+02   1.97110530e-05]
         [  4.20000000e+02   2.99661440e-05]
         [  4.30000000e+02   6.38192720e-05]
         [  4.40000000e+02   1.68909683e-04]
         [  4.50000000e+02   3.31902935e-04]
         [  4.60000000e+02   3.33143020e-04]
         [  4.70000000e+02   2.30227481e-04]
         [  4.80000000e+02   1.66981976e-04]
         [  4.90000000e+02   1.64439844e-04]
         [  5.00000000e+02   2.01534538e-04]
         [  5.10000000e+02   2.57840526e-04]
         [  5.20000000e+02   3.04612651e-04]
         [  5.30000000e+02   3.41368344e-04]
         [  5.40000000e+02   3.63639323e-04]
         [  5.50000000e+02   3.87050648e-04]
         [  5.60000000e+02   4.21619130e-04]
         [  5.70000000e+02   4.58150520e-04]
         [  5.80000000e+02   5.01176575e-04]
         [  5.90000000e+02   5.40883630e-04]
         [  6.00000000e+02   5.71256795e-04]
         [  6.10000000e+02   5.83703280e-04]
         [  6.20000000e+02   5.57688472e-04]
         [  6.30000000e+02   5.17328095e-04]
         [  6.40000000e+02   4.39994939e-04]
         [  6.50000000e+02   3.62766819e-04]
         [  6.60000000e+02   2.96465587e-04]
         [  6.70000000e+02   2.43966802e-04]
         [  6.80000000e+02   2.04134776e-04]
         [  6.90000000e+02   1.75304012e-04]
         [  7.00000000e+02   1.52887544e-04]
         [  7.10000000e+02   1.29795619e-04]
         [  7.20000000e+02   1.03122693e-04]
         [  7.30000000e+02   8.77607820e-05]
         [  7.40000000e+02   7.61524130e-05]
         [  7.50000000e+02   7.06516880e-05]
         [  7.60000000e+02   3.72199210e-05]
         [  7.70000000e+02   3.63058860e-05]
         [  7.80000000e+02   3.55755470e-05]]
        """

        super(SpectralDistribution_Sekonic, self).read()

        self.header.report_date = self._metadata.get('Date Saved')
        self.header.manufacturer = 'Sekonic'

        return self
