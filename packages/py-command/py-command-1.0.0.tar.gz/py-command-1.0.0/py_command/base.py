import sys
import os
from argparse import ArgumentParser


class BaseCommand:
    help = "Sub command Help message."
    version = "Version string."

    def __init__(self):
        self.argv = None
        self.kwargv = {}

    def setup(self, argv, **kwargs):
        self.argv = argv
        self.kwargv = kwargs.copy()

    def add_arguments(self, parser):
        """
        Add externd argument with parser
        :param parser: [ArgumentParser] Argument parser
        :return:
        """
        return parser

    def work(self):
        print(self.argv)
        prog_name = self.argv[0]
        subcommand = self.argv[1]
        parser = self.create_parser(prog_name=prog_name, subcommand=subcommand, **self.kwargv)
        options = parser.parse_args(self.argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        try:
            self.execute(*args, **cmd_options)
        except Exception as e:
            sys.stderr.write("{}: {}".format(e.__class__.__name__, e))
            exit(1)

    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = ArgumentParser(
            prog="{} {}".format(os.path.basename(prog_name), subcommand),
            description=self.help or None,
            **kwargs
        )
        parser.add_argument("-v", "--version", action="version", version=self.version)
        parser = self.add_arguments(parser)
        return parser

    def print_help(self, prog_name, subcommand):
        parser = self.create_parser(prog_name=prog_name, subcommand=subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        try:
            self.execute(*args, **cmd_options)
        except Exception as e:
            sys.stderr.write("{}: {}".format(e.__class__.__name__, e))
            exit(1)

    def execute(self, *args, **options):
        raise NotImplementedError("Method execute must implement")