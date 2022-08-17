"""python web scrapper: images, EXIF and metadata"""

from src.logger import Mainlogger
from src.config import Configlibrary
from src.scrapper import Spiderscrapper

def main():
    """main function of the program"""
    scrap_logger = Mainlogger()
    scrap_config = Configlibrary()
    class_config = {}

    scrap_logger.set_log_level(scrap_config.get_log_level())
    scrap_config.parser.add_argument('url', metavar='<URL>', type=str)
    scrap_config.parser.add_argument('-r', '--recursive', action='store_true',
                        help="recursive images download")
    scrap_config.parser.add_argument('-l', '--level', metavar='<N>',
                        type=int, help="sets the downloading recursive-level")
    scrap_config.parser.add_argument('-p', '--path', metavar='<PATH>', type=str,
                        help="sets the path where the info downloaded is going to be saved")
    scrap_config.parser.add_argument('-rl', '--recursive-level', metavar='<URL> <N>',
                        type=str, help=scrap_config.argparse.SUPPRESS)
    scrap_config.parser.add_argument('-rp', '--recursive-path', metavar='<URL> <PATH>', type=str,
                        help=scrap_config.argparse.SUPPRESS)

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
    if (args.path or args.recursive) and args.recursive_path:
        scrap_logger.logger.error("invalid arguments")
        return

    #setting recursive level
    if args.recursive and (args.level is None or args.level is False):
        class_config["level"] = scrap_config.get_recursive_level()
    elif args.level and args.recursive:
        class_config["level"] = args.level
    else:
        class_config["level"] = scrap_config.get_default_level()

    #setting path to store the downloaded files
    if args.path or args.recursive_path:
        if args.recursive_path:
            args.path = args.recursive_path
        class_config["path"] = args.path
    else:
        class_config["path"] = scrap_config.get_default_path()

    class_config["extensions"] = scrap_config.get_extensions()

    if not Spiderscrapper.validate_url(args.url):
        scrap_logger.logger.error("invalid url")
        return
    spider = Spiderscrapper(args.url, class_config, scrap_logger)
    spider.run()
    scrap_logger.logger.info("scrape finished")

if __name__ == "__main__":
    main()
