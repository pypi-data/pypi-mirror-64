import warnings
from typing import Tuple, List, Optional, Sequence, Dict


class ParseError(Exception):
    """Error raised when a parsing error occurs."""
    pass


class TopologyFilter:
    """Simple preprocessor for GROMACS topology files
    """
    filename: str
    defines: Dict[str, List[str]]
    ifdefs: List[Tuple[str, bool]]
    section: Optional[str] = None
    handleincludes: bool = True
    handleifdefs: bool = True
    handleempty: bool = True

    def __init__(self, filename: str, defines: Optional[Sequence[str]] = None, handleincludes: bool = True,
                 handleifdefs: bool = True, handleempty: bool = True):
        """Initialize the preprocessor

        :param filename: main file name
        :type filename: str
        :param defines: set of defined macros
        :type defines: set of str
        :param handleincludes: if True, follow #include directives. If False, pass them through
        :type handleincludes: bool
        :param handleifdefs: if True, handle preprocessor conditionals. If False, pass them throgh
        :type handleifdefs: bool
        :param handleempty: if True, hide empty (or pure comment) lines. If False, pass them through
        :type handleempty: bool
        """
        self.handleempty = handleempty
        self.handleincludes = handleincludes
        self.handleifdefs = handleifdefs
        self.defines = dict(zip(defines, [[]] * len(defines))) if defines else {}
        self.filename = filename
        self.ifdefs = []

    def parse(self, filename: Optional[str] = None):
        """Start parsing the file.

        This is a generator. Yields the following:
            - stripped line (str),
            - comment (str or None),
            - current section name (str or None),
            - file name (str),
            - line number (int),
            - full line (str)

        Empty lines, are not yielded.

        #ifdef/#ifndef/#else/#endif lines are only yielded if `self.handleifdefs` is set to False.

        #include lines are only yielded if `self.handleincludes` is set to False.

        :param filename: the file name to parse. Do not set this by yourself, leave it None
        :type filename: str or None
        """
        if filename is None:
            # we are starting at the main file.
            filename = self.filename
            # also reset ifdefs and section
            self.ifdefs = []
            self.section = None
        with open(filename, 'rt') as f:
            for i, line in enumerate(f, start=1):
                try:
                    l, *comment = line.split(';', 1)
                    comment = None if not comment else comment[0]
                    l = l.strip()
                    # first of all, check #ifdef, #ifndef, #else and #endif directives.
                    if l.startswith('#ifdef') and self.handleifdefs:
                        _, macro = l.split()
                        self.ifdefs.append((macro, True))
                    elif l.startswith('#ifndef') and self.handleifdefs:
                        _, macro = l.split()
                        self.ifdefs.append((macro, False))
                    elif l.startswith('#else') and self.handleifdefs:
                        self.ifdefs[-1] = (self.ifdefs[-1][0], not self.ifdefs[-1][1])
                    elif l.startswith('#endif') and self.handleifdefs:
                        del self.ifdefs[-1]
                    elif l.startswith('#include') and self.handleincludes:  # include directives are also always treated
                        _, incfilename = l.split()
                        if not (incfilename.startswith('"') and incfilename.endswith('"')) and not (
                                incfilename.startswith('<') and incfilename.endswith('>')):
                            raise ParseError(f'Invalid #include directive in file {f.name} at line #{i}.')
                        self.parse(incfilename)
                    elif self.ifdefs_allow_reading() or (not self.handleifdefs):
                        # #define, #undef, #error and #warning directives are only treated if the #ifdef clauses allow it.
                        if l.startswith('#define'):
                            _, macro, *values = l.split()
                            self.defines[macro] = values
                        elif l.startswith('#undef'):
                            _, macro = l.split()
                            del self.defines[macro]
                        elif l.startswith('#error'):
                            _, message = l.split(None, 1)
                            raise ParseError(f'#error directive encountered with message: {message}')
                        elif l.startswith('#warn'):
                            directive, message = l.split(None, 1)
                            warnings.warn(f'{directive} directive encountered with message: {message}')
                        elif l.startswith('[') and l.endswith(']'):
                            # we are in a new section
                            self.section = l[1:-1].strip()
                            yield l, comment, self.section, f.name, i, line
                        elif (not l) and self.handleempty:
                            # empty line
                            pass
                        else:
                            # yield information on this line
                            yield l, comment, self.section, f.name, i, line
                except (ValueError, IndexError):
                    raise ParseError(f'Error in file {filename} on line #{i}: {line}')

    def defined(self, macro: str) -> bool:
        """Check if a preprocessor macro is #defined or not"""
        return macro in self.defines

    def ifdefs_allow_reading(self) -> bool:
        """Check if the current state of #ifdef and #ifndef clauses allow reading/interpreting or not."""
        return all([(self.defined(macro) and state)  # ifdef and macro defined
                    or (not self.defined(macro) and not state)  # ifndef and macro undefined
                    for macro, state in self.ifdefs])
