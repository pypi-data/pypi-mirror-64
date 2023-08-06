from argparse import ArgumentParser

arguments = ArgumentParser()

arguments.add_argument("--host", type=str, default='127.0.0.1:8081',
    help="robot host name")