import re
import site
import sys
import sysconfig
import traceback

import pygments.lexers
from colored_traceback.colored_traceback import Colorizer

LIB_DIRS = [sysconfig.get_path('stdlib'), site.USER_SITE, 'File "<frozen']
if hasattr(sys, 'real_prefix'):
    LIB_DIRS.append(sys.prefix)
    LIB_DIRS.append(sysconfig.get_path('stdlib')
                    .replace(sys.prefix, sys.real_prefix))


def color_traceback(previous_hook=None):
    previous_hook = sys.excepthook

    def on_crash(type, value, tb):
        if getattr(sys.stderr, 'isatty'):
            colorizer = CustomColorizer('default')
            colorizer.colorize_traceback(type, value, tb)
            if previous_hook is not sys.__excepthook__:
                previous_hook(type, value, tb)

    sys.excepthook = on_crash


class CustomColorizer(Colorizer):
    def colorize_traceback(self, type, value, tb):

        rows = traceback.format_exception(type, value, tb)
        lines = [l for row in rows for l in row.split('\n')]
        lines = [l for l in lines if l.strip()]

        lexer = pygments.lexers.get_lexer_by_name("pytb", stripall=True)
        colored_tb = pygments.highlight("\n".join(lines), lexer, self.formatter)
        clines = colored_tb.split('\n')

        def filter_lines(lines, clines):

            lines = (l.strip('\n') for l in lines if l.strip())
            clines = (l.strip('\n') for l in clines if l.strip())
            gen = iter(zip(lines, clines))

            for line, colline in gen:

                if "Traceback (most recent call last):" in line:
                    yield "\n" + colline + "\n"
                    continue

                if (line.strip().startswith('File ')
                    and not any(d in line for d in LIB_DIRS)):  # noqa
                    yield colline
                    line, colline = next(gen)
                    yield colline + "\n"
                    continue

                if re.match('\w+Error:', line):
                    yield colline
                    for _, cline in gen:
                        yield cline
                    yield "\n"
                    break

                yield line
                line, colline = next(gen)
                yield line + "\n"

        self.stream.write("\n".join(filter_lines(lines, clines)))
