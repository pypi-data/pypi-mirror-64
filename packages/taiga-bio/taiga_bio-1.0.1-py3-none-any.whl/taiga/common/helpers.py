import logging as log


def config_log(create_log: bool) -> None:
    """Sets the global configuration for the output mode of the 'logging' module

    Parameters:
    create_log (boolean): Sets TaIGa's verbosity mode. If True, TaIGa will not be verbose

    Returns:
    None

    """

    if create_log:
        log.basicConfig(filename="TaIGa_run.log",
                        format="%(message)s", level=log.DEBUG)
    else:
        log.basicConfig(format="%(message)s", level=log.DEBUG)
