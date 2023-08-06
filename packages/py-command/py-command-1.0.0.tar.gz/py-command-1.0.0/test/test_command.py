from py_command.entry import CommandManager
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
sys.path.append(current_dir)
print(sys.path)


if __name__ == '__main__':
    sub_command_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subcommand")
    command_manager = CommandManager(sub_command_module_path="test.subcommand", sub_command_path=sub_command_path)
    command_manager.execute_from_argv()
