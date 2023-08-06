import itertools
import re
from typing import List, Optional, Sequence

import numpy as np
from matplotlib.figure import Figure


class XVGFile:
    """Represents an XVG file produced by various GROMACS tools.

    Most important attributes are:
        - filename: the name of the file on the disk (str). The file will not be written, only read.
        - data: the data in the file in the form of a structured numpy array. This is a read-only property. In-place
            modifications are allowed, however.
        - title: title of the graph (str)
        - xaxis: x axis label (str)
        - yaxis: y axis label (str)
        - columntitles: list of column titles (str)

    XVG files support dict-like indexing with the column names.

    Lazy loading is implemented: as the numeric data in the XVG file can sometimes be very long, reading it can be
    postponed to first access.
    """

    filename: str
    _data: Optional[np.ndarray]
    title: str
    xaxis: str
    yaxis: str
    columntitles: List[str]

    def __init__(self, filename: str, lazyload: bool = True):
        """Initialize an instance

        :param filename: name of an XVG file on the disk
        :type filename: str
        :param lazyload: True if the file must be loaded only when the data is requested.
        :type lazyload: bool
        """
        self.filename = filename
        self._data = None
        self.load(load_data=not lazyload)

    def load(self, load_data: bool = True):
        """Load the XVG file from the disk. File name is taken from the `.filename` attribute.

        :param load_data: True if the data should be loaded (the header is always read)
        :type load_data: bool
        """
        # first read header
        ncol = None
        with open(self.filename, 'rt') as f:
            self.columntitles = []
            for line in f:
                if line.strip().startswith('#'):
                    continue
                l = line.strip()
                if not l:
                    continue
                elif not l.startswith('@'):
                    # this is the first line of data. See how much columns it really has, because some XVG files do not
                    # have enough labels for all columns :-(
                    ncol = len(l.split())
                    break
                m = re.match(r'@\s*(?P<left>.+)\s+"(?P<right>.+)"', l)
                if not m:
                    continue
                if m['left'] == 'title':
                    self.title = m['right']
                elif re.match(r'xaxis\s+label', m['left']):
                    self.xaxis = m['right']
                elif re.match(r'yaxis\s+label', m['left']):
                    self.yaxis = m['right']
                elif re.match(r's[0-9]+\s+legend', m['left']):
                    self.columntitles.append(m['right'])
                else:
                    raise ValueError(m['left'])
        m = re.match(r'(?P<xcolname>[^()]+)\s+\(.+\)', self.xaxis)
        self.columntitles.insert(0, m['xcolname'])
        assert ncol is not None
        # add dummy column labels for missing ones
        self.columntitles = self.columntitles + [f'_Untitled{i}' for i in range(ncol - len(self.columntitles))]
        if load_data:
            self._data = np.loadtxt(self.filename, comments=['@', '#', ';'],
                                    dtype=np.dtype(list(zip(self.columntitles, itertools.cycle(['float'])))))
        else:
            self._data = None

    def keys(self) -> List[str]:
        """Return a list of the available column names"""
        return self.columntitles[:]

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, item) -> np.ndarray:
        return self.data[item]

    def plot(self, columns: Optional[List[str]] = None, figure: Optional[Figure] = None) -> Figure:
        """Create a simple plot

        :param columns: list of column names. Set it to None if all columns are to be plotted
        :type columns: str or None
        :param figure: matplotlib Figure instance to plot into or None to auto-create a new one.
        :type figure: matplotlib.figure.Figure or None
        :return: the Figure instance into which the plotting has been made
        :rtype: Figure
        """
        if columns is None:
            columns = self.columntitles[1:]
        if figure is None:
            figure = Figure()
        figure.set_constrained_layout(True)
        figure.clear()
        gs = figure.add_gridspec(1, 1)
        axes = figure.add_subplot(gs[0, 0])
        x = self.data[self.columntitles[0]]
        for col in columns:
            axes.plot(x, self.data[col], label=col)
        axes.set_xlabel(self.xaxis)
        axes.set_ylabel(self.yaxis)
        axes.set_title(self.title)
        axes.grid(True, which='both')
        axes.legend(loc='best')
        return figure

    @property
    def data(self) -> np.ndarray:
        if self._data is None:
            self.load(load_data=True)
        return self._data

    def renamecolumns(self, colnames: Sequence[str]):
        """Rename columns

        :param colnames: list of column names (the same length as the present one)
        :type colnames: sequence of str
        """
        if len(colnames) != len(self.columntitles):
            raise ValueError('You must give exactly the same number of column labels as the current ones.')
        self.columntitles = list(colnames)
        self._data = self.data.astype(dtype=np.dtype(list(zip(self.columntitles, itertools.cycle(['float'])))))
