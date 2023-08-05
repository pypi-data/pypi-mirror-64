import sys
import logging as log
from ..common import parsers, helpers, retrievers, data_handlers


def run_taiga(infile: str,
              outdir: str,
              email: str,
              gb_mode: int = 0,
              tid: bool = False,
              correction: bool = False,
              retries: int = 5,
              silent: bool = False) -> None:
    """ Wrapper for all of TaIGa's main functionalities

    Required Parameters:
    infile (str): Full path to input file
    outdir (str): Full path to output directory, wich doesn't need to be pre-existant
    email (str): Valid user e-mail

    Optional Parameters:
    gb_mode (int): An integer representing the reading mode for the input file. Options are:
                   0: a plain text file, which is not handled by this function (Default)
                   1: Genbank file with multiple records from different organisms
                   2: Genbank file with a single record from a single organism
                   3: Genbank file with multiple records from the same organism
    tid (bool: Default = False): Tells if TaIGa should expect a input file with Taxon IDs
    correction (bool: Default = False): Activates the name correction function.
    retries (int: Default = 5): How many time TaIGa should retry after a bad response.
    silent (bool: Default = False): Tells if TaIGa should stop printing and create a log file

    Returns:
    None

    """

    # Ouput and input paths
    input_path = infile
    if outdir[-1] == "/":
        output_path = outdir
    else:  # Adding a trailing forward slash to the output path if needed
        output_path = outdir + "/"

    # Providing the email when doing requests through E-Utils is recommended
    user_email = email

    # Minor config variables for some of TaIGa's functionalities
    retries = retries
    create_log = silent
    name_correction = correction

    # The switches for TaIGa's execution modes, either for Taxon IDs or Genbank files
    taxid = tid
    mode = gb_mode

    # A list to hold Taxon objects
    taxon_list = []

    # Inital configuration for the logging module
    # At this point, the output may be set to verbose or not
    helpers.config_log(create_log)

    log.info("""
    *********************************************
    *                                           *
    *   TaIGa - Taxonomy Information Gatherer   *
    *                                           *
    *********************************************""")

    # Checking if TaIGa is being run on Taxon ID mode with the '-c' argument
    # This is needed because, when run with '--tid', TaIGa never actually tries to correct spelling
    # as the retrieved name is assumed to be correct
    if taxid and name_correction:
        log.error("\nERROR: Please, when running TaIGa with the '--tid' option, don't use the '-c' "
                  "option as TaIGa already skips the name correction\n")
        sys.exit()

    # Check if input mode is for a Genbank format file or a text file and then parse the input
    if not (mode == 0):
        taxon_list = parsers.parse_gb(input_path, mode)
    else:
        taxon_list = parsers.parse_txt(input_path, taxid)

    log.info("\n> Searching for taxonomic information...")

    # Checking the type of input (Taxon ID or names) and fetching the rest of the information
    if tid:
        retrievers.retrieve_from_taxid(taxon_list, user_email, retries)
    else:
        retrievers.retrieve_from_names(
            taxon_list, user_email, name_correction, retries)

    # Calling the wrapper function to fetch for the taxonomic information for all organisms
    retrievers.retrieve_taxonomy(taxon_list, user_email, retries)

    # Calling a function to handle the fetched data and convert it to a Pandas DataFrame
    frame = data_handlers.create_df(taxon_list)
    # Calling the last function which takes the DataFrame and creates the output files
    data_handlers.create_output(output_path, frame, taxon_list)

    log.info(
        "\n> TaIGa was run successfully! You can check the results inside the output folder\n")
