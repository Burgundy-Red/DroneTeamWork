import os
import argparse
import logging
import time
import sys
from pathlib import Path

def get_arguments():
    """
    argument parse
    """
    parser = argparse.ArgumentParser("")
    parser.add_argument('--connect-string', type=str, default='', 
            help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    parser.add_argument('--altitude', type=int, default=10,
            help="fly to altitude")
    parser.add_argument('--logdir', type=str, default='./log',
            help="logging save directory")
    parser.add_argument('--logfile', type=str, default='',
            help="logging save file")
    parser.add_argument('--loglevel', type=str, default='debug',
            help="logging level")
    parser.add_argument('--coordfile', type=str, default='./coordfile.txt',
            help="coordinate file")
    args = parser.parse_args()
    return args


def get_absolute_path(path):
    """
    relative path to absolute path
    Args:
        path(str): relative path
    Returns:
        absoute path
    """    
    return os.path.abspath(path)


def get_logger(args, mode='w', stdout=True):
    """logging
    Args:
        log_dir(str): 日志文件路径
        mode(str): 'a' append 'w' 覆盖
        stdout(bool): 同时输出到终端
    Returns:
        logger
    """
    import datetime
    def get_date_str():
        now = datetime.datetime.now()
        # return now.strftime('%Y-%m-%d_%H-%M-%S')
        return now.strftime('%Y-%m-%d')

    args.logdir = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) \
                            if not len(args.logdir) else os.path.abspath(args.logdir)
    args.logfile = 'main_' + get_date_str() + '.txt' \
                            if not len(args.logfile) else args.logfile
    if not os.path.exists(args.logdir):
        os.makedirs(args.logdir)
    args.logfile = os.path.join(args.logdir, args.logfile)

    args.loglevel = logging.DEBUG if args.loglevel.lower == "debug" else logging.INFO
    logging.basicConfig(level=args.loglevel,
                        filename=args.logfile,
                        filemode=mode,
                        datefmt='%Y/%m/%d %H:%M:%S',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

    if stdout:
        console = logging.StreamHandler(stream=sys.stdout)
        console.setLevel(args.loglevel)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(lineno)d -%(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    return logging


def read_coordfile(coordfilepath):
    """
    read coordination file
    Args:
        coordfilepath(str):
    Returns:
        coord(list): [(lat, lon), ]
    """
    with open(coordfile, "r") as f:
        logger.info("open coordfile success.")
        lines = [tuple(line.strip().split(',')) for line in f.readlines() 
                # if not line and not line.startswith('#')]
                if len(line.strip()) > 0 and not line.startswith('#')]
        coord = list(map(lambda x: [x[0].strip(), x[1].strip()], lines))
    return coord


