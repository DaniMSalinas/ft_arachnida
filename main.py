"""python web scrapper: images, EXIF and metadata"""

from src.logger import Mainlogger
from src.config import Configlibrary
from src.spider import Spiderscrapper

def main():
    """main function of the program"""
    scrap_logger = Mainlogger()
    scrap_config = Configlibrary()
    class_config = {}
    scrap_logger.set_log_level(scrap_config.get_log_level())

    try:
        args, unknown = scrap_config.parser.parse_known_args()
    except SystemExit:
        return

    #handling possible wrong arguments
    if unknown:
        scrap_logger.logger.error("Unknown args")
        return
    if args.level and (args.recursive is None or args.recursive is False):
        scrap_logger.logger.error("argument --level requires argument --recursive")
        return

    #setting recursive level
    if args.recursive and (args.level is None or args.level is False):
        class_config["level"] = scrap_config.get_recursive_level()
    elif args.level and args.recursive:
        class_config["level"] = args.level
    else:
        class_config["level"] = scrap_config.get_default_level()

    #setting path to store the downloaded files
    if args.path:
        class_config["path"] = args.path
    else:
        class_config["path"] = scrap_config.get_default_path()

    class_config["extensions"] = scrap_config.get_extensions()

    if not Spiderscrapper.validate_url(args.url):
        scrap_logger.logger.error("invalid url")
        return
    spider = Spiderscrapper(args.url, class_config, scrap_logger)
    spider.run()

if __name__ == "__main__":
    main()
