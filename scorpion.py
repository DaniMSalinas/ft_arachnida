"""python image metadata analyzer"""

import os
import argparse
from src.logger import Mainlogger
from src import metadata

def main():
    """main function of the program"""
    scorpion_logger = Mainlogger()
    scorpion_logger.set_log_level("INFO")
    parser = argparse.ArgumentParser(description="""SCORPION METADATA DUMPER\n
                                    Scorpion program extracts metadata from files""")
    parser.add_argument('files', metavar="<FILE>", type=str, nargs='+',
                        help='extract files metadata information')
    metadata_dict = {}
    extensions_list = []
    with open('configuration/extensions', 'rb') as extensions_file:
        extensions_str = extensions_file.read().decode("utf-8")
    extensions_list = extensions_str.split('\r\n')

    try:
        args, unknown = parser.parse_known_args()
    except SystemExit:
        return

    if unknown:
        scorpion_logger.logger.error("Unknown args")
        return

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
            elif extension in extensions_list:
                if metadata.status_exif_data(file):
                    metadata_dict[file]["EXIF"] = metadata.get_exif_metadata(file)
                metadata_dict[file]["METADATA"] = metadata.get_pillow_metadata(file)
            else:
                scorpion_logger.logger.error("invalid file extension")

    for file in args.files:
        print("\nmetadata from: " + str(file))
        print(metadata_dict[file])

if __name__ == "__main__":
    main()
 