from config import configure_logger
#######################

def main() :
    """
        ЗАпуск CLI
    """
    configure_logger()
    from cli.cli import StartupCLI
    a = StartupCLI()
    a.run()


if __name__ == "__main__":
    from os import system
    print(system("sql-generate"))