from pkgutil import iter_modules
from importlib import import_module
import sys
import os
from py_command import base


def find_sub_commands(sub_command_path):
    """
    Find sub commands

    :param sub_command_path: [str] Sub command dir path
    """
    command_modules = [name for _, name, _ in iter_modules([sub_command_path])]
    return command_modules


def get_command_class(sub_command_module_path, sub_command):
    """
    Get class of command
    :param sub_command_module_path: [str] Sub command module path
    :param sub_command: [str] Sub command module name
    :return:
    """
    module_str = "{0}.{1}".format(sub_command_module_path, sub_command)
    module = import_module(module_str)
    return module.Command


def print_main_help(prog_name, sub_command_path):
    """
    Main helper

    :param prog_name: [str] Name of program
    :param sub_command_path: [str] Sub command dir path
    """
    command_modules = find_sub_commands(sub_command_path)
    sys.stdout.write("Usage: {} [sub command] [option]\n".format(prog_name))
    sys.stdout.write("Available sub commands:\n")
    for command_module in command_modules:
        sys.stdout.write("\t{}\n".format(command_module))


class CommandManager:

    def __init__(self, sub_command_module_path, sub_command_path):
        """
        Initial method
        :param sub_command_module_path: [str] Sub command module path
        """
        self.sub_command_module_path = sub_command_module_path
        self.sub_command_path = sub_command_path

    def execute_from_argv(self):
        """
        Execute command from command line with argv
        :return:
        """
        argv = sys.argv
        prog_name = os.path.basename(argv[0])
        sub_command = ""
        try:
            sub_command = argv[1]
            if sub_command.lower() == "help":
                print_main_help(prog_name=prog_name, sub_command_path=self.sub_command_path)
                exit(0)
        except IndexError:
            print_main_help(prog_name=prog_name, sub_command_path=self.sub_command_path)
            exit(0)

        try:
            cls = get_command_class(self.sub_command_module_path, sub_command)
            instance = cls()
            if isinstance(instance, base.BaseCommand):
                instance.setup(argv=argv)
                instance.work()
        except ModuleNotFoundError:
            import traceback
            traceback.print_exc()
            sys.stderr.write("{} is not a command\n\r".format(sub_command))
            print_main_help(prog_name=prog_name, sub_command_path=self.sub_command_path)
            exit(-1)
        except AttributeError:
            sys.stderr.write("{} command is invalid, not instance if BaseCommand".format(sub_command))
            exit(-1)
