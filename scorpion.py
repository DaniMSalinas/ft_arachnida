"""python image metadata analyzer"""

import os
from src.logger import Mainlogger
from src.config import Configlibrary
from src import metadata

def main():
    """main function of the program"""
    scorpion_config = Configlibrary()
    scorpion_logger = Mainlogger()
    metadata_dict = {}
    extensions = scorpion_config.get_extensions()

    scorpion_logger.set_log_level(scorpion_config.get_log_level())
    scorpion_config.set_parser_description("""SCORPION METADATA DUMPER\n
                                Scorpion program extracts metadata from files""")
    scorpion_config.parser.add_argument('files', metavar="<FILE>", type=str, nargs='+',
                            help='extract files metadata information')

    try:
        args, unknown = scorpion_config.parser.parse_known_args()
    except SystemExit:
        return

    #handle unknown args
    if unknown:
        scorpion_logger.logger.error("Unknown args")
        return

    #extractind metadata from files
    for file in args.files:
        if not os.path.isfile(file):
            scorpion_logger.logger.error("%s doesn't exists", str(file))
        elif file in metadata_dict:
            scorpion_logger.logger.warning("%s have been already analyzed. Skipping", str(file))
        else:
            metadata_dict[file] = {}
            extension = file.split('.')[-1]
            scorpion_logger.logger.info("extracting metadata from %s", file)
            if extension == "pdf":
                metadata_dict[file]["METADATA"] = metadata.get_pdf_metadata(file)
            elif extension == "docx":
                metadata_dict[file]["METADATA"] = metadata.get_docx_metadata(file)
            elif extension in extensions:
                if metadata.status_exif_data(file):
                    metadata_dict[file]["EXIF"] = metadata.get_exif_metadata(file)
                metadata_dict[file]["METADATA"] = metadata.get_pillow_metadata(file)
            else:
                scorpion_logger.logger.error("invalid file extension")

    #printing metadata extracted from files
    for file in args.files:
        print("\nmetadata from: " + str(file))
        print(metadata_dict[file])

if __name__ == "__main__":
    main()
 