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
                                    Scorpion program extracts metadata from images""")
    parser.add_argument('images', metavar="<IMG>", type=str, nargs='+',
                        help='extract images metadata information')
    metadata_dict = {}

    try:
        args, unknown = parser.parse_known_args()
    except SystemExit:
        return

    if unknown:
        scorpion_logger.logger.error("Unknown args")
        return

    for image in args.images:
        if not os.path.isfile(image):
            scorpion_logger.logger.error("%s doesn't exists", str(image))
        elif image in metadata_dict:
            scorpion_logger.logger.warning("%s have been already analyzed. Skipping", str(image))
        else:
            metadata_dict[image] = {}
            if metadata.status_exif_data(image):
                metadata_dict[image]["EXIF"] = metadata.get_exif_metadata(image)
            metadata_dict[image]["METADATA"] = metadata.get_pillow_metadata(image)

    print(metadata_dict)

if __name__ == "__main__":
    main()
 