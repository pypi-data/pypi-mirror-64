from py_command.base import BaseCommand


class Command(BaseCommand):

    help = "Just for test"
    version = "1.0.0"

    def add_arguments(self, parser):
        parser.add_argument("--test", "-t", dest="test", type=str, default="Hello test", help="Test argument.")
        return parser

    def execute(self, *args, **options):
        print("Execute command entry....")
        print("Get test argument: {}".format(options.pop("test")))
        print("Test end")
