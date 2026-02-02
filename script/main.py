import sys
from script.commands.create_table import CreateTableCommand
from script.commands.add_employee import AddEmployeeCommand
from script.commands.unique import UniqueCommand
from script.commands.generate_data import GenerateDataCommand
from script.commands.prefiltered import PrefilteredCommand
from script.commands.optimize_query import OptimizeQueryCommand
from script.commands.drop_table import DropTableCommand
from script.commands.statistic import StatisticCommand
from script.commands.quit import QuitCommand

MENU = """
--- DB Script ---
1. Create table
2. Add employee
3. Unique
4. Generate data
5. Prefiltered
6. Optimize query
7. Statistic
0. Drop table
q. Quit
"""


def run_command(mode: str, args: list[str] | None = None) -> bool:
    """Run command by mode. Returns False to exit loop."""
    match mode:
        case "1":
            CreateTableCommand().run()
        case "2":
            if args and len(args) >= 3:
                AddEmployeeCommand().run(args)
            else:
                full_name = input("Full name: ").strip()
                dob = input("Date of birth (YYYY-MM-DD): ").strip()
                gender = input("Gender (male/female): ").strip()
                AddEmployeeCommand().run([full_name, dob, gender])
        case "3":
            UniqueCommand().run()
        case "4":
            GenerateDataCommand().run()
        case "5":
            PrefilteredCommand().run()
        case "6":
            OptimizeQueryCommand().run()
        case "7":
            StatisticCommand().run()
        case "0":
            DropTableCommand().run()
        case "q":
            QuitCommand().run()
        case _:
            print("Unknown mode")
    return True


def main():
    # Non-interactive: argv passed (e.g. healthcheck, one-shot)
    if len(sys.argv) > 1:
        run_command(sys.argv[1], sys.argv[2:] if len(sys.argv) > 2 else None)
        return

    # Interactive CLI loop
    while True:
        print(MENU)
        choice = input("> ").strip().lower()
        if choice:
            run_command(choice)
        print()

if __name__ == "__main__":
    main()