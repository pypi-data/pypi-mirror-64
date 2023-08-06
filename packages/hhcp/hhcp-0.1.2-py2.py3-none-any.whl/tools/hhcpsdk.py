import argparse
import os
import sys
from argparse import RawTextHelpFormatter

from hhcp.cp_dir_multi import cp_dir
from hhcp.cp_list_multi import cp_list


class InvalidInputException(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Provide (a file list)|(a dir) and a destination,
        cp (all the files in the list)|(the dir) to the destination
        with multi-thread.
        This will NOT overwrite existing files on default.\n
        """,
        formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "-p",
        help="The path of the directory to be copied.",
        default=None,
        type=str,
    )
    parser.add_argument(
        "-f",
        help="The location of the file list.",
        default=None,
        type=str,
    )
    parser.add_argument(
        "-d",
        required=True,
        help="The path of the destination",
        default=None,
        type=str,
    )
    parser.add_argument(
        "--force",
        help="add this to allow force overwrite",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--pre",
        help="The path prefix of the files in the list",
        default=None,
        type=str,
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    return parser.parse_args()


def load_config(args):
    """
    Given the arguemnts, load and initialize the configs.
    Args:
        args (argument): `p`, `f`, `d`, `n`, `force`, `pre`
    """
    if args.p is not None and args.f is not None:
        raise InvalidInputException(
            "Only one of -p and -f could be provided but get two.")
    elif args.p is None and args.f is None:
        raise InvalidInputException(
            "At least one of -p and -f should be provided.")
    else:
        # 判断 p 是否为合法路径
        if args.p is not None:
            if not os.path.exists(args.p):
                raise FileNotFoundError("The dir to be copied does not exist.")
            elif not os.path.isdir(args.p):
                raise InvalidInputException("-p should be a dir.")
        # 判断 f 是否为合法路径
        elif args.f is not None:
            if not os.path.exists(args.f):
                raise FileNotFoundError("Could not find the filelist.")
    # 判断 d 是否为合法路径
    if args.d is not None:
        if not os.path.isdir(args.d):
            raise InvalidInputException("-d should be a dir.")
        if not os.path.exists(args.d):
            raise FileNotFoundError("The destination dir does not exist.")
    if args.pre is None:
        args.pre = ''
    return args.p, args.f, args.d, args.pre, args.force


def main():
    directory, filelist, destination, prefix, force = load_config(parse_args())
    if filelist is not None:
        cp_list(filelist, destination, prefix, force)
    elif directory is not None:
        cp_dir(directory, destination, force)
    else:
        print("At least one of -p and -f should be provided.")


if __name__ == "__main__":
    main()
