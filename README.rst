DEVPY
-----

Devpy is a set of tools to ease Python development.


Autolog
========

Setuping proper loging is tedious, so you may want to do it later, but you wish you could get basic logging right now:

    import devpy

    # Get a logger that automatically log to console and a rotating file
    # The rotating file is setup in the temp directory of your system, in
    # a subdir named after your __name__.
    # The file path is printed at the begining of the program.

    log = devpy.autolog() # log is a regular stdlib logger object

    # start logging:

    log.info('Yes')

Once you have time to setup logging seriously, you can just replace the autolog with a regular custom Python logger, and all your logs will still work.


Stacktrace helper
=================

Format the stack trace so that:

- it separates the various logicial blocs
- it emphasis the lines of your programs and not the stdlb
- lines of your program are syntax highlited

::
    import devpy
    log = devpy.color_traceback()


All helpers at once
===================

::
    import devpy
    log = devpy.dev_mode()  # can set color_traceback=True, autolog=True

    # or just
    # import devpy.develop as log
    # for a one liner to activate it all
