import os

path = os.getcwd()
files = {}


def main():
    total_line_count           = 0
    total_nonempty_line_count  = 0
    amount_of_unreadable_files = 0

    for file in (f for f in os.listdir(path) if os.path.isfile(f)):
        line_count            = 0
        nonempty_line_count   = 0

        try:
            if os.access(f"{path}/{file}", os.R_OK):
                try:
                    current_file = open(f"{path}/{file}", encoding="ISO-8859-1")

                    # Calculate the amount of lines
                    lines = current_file.readlines()
                    for line in lines:
                        formatted_line = line.replace("\n", "")
                        lines[lines.index(line)] = formatted_line

                        line_count += 1
                        if formatted_line != "":
                            nonempty_line_count += 1

                    files[file] = ("Yes", line_count, nonempty_line_count)
                    total_line_count += line_count
                    total_nonempty_line_count += nonempty_line_count

                except PermissionError:
                    gap = " " * (10 - len("No") - len("AD"))
                    files[file] = (f"No{gap}AD", 0, 0)
                    amount_of_unreadable_files += 1
            else:
                gap = " "*(10 - len("No") - len("AD"))
                files[file] = (f"No{gap}AD", 0, 0)
                amount_of_unreadable_files += 1
        except KeyboardInterrupt:
            gap = " " * (10 - len("No") - len("INT"))
            files[file] = (f"No{gap}INT", 0, 0)
            amount_of_unreadable_files += 1

        finally:
            current_file.close()

    print(f"\n\n    Directory: {path}")
    print(f"    Summary:   {total_line_count} line(s)")
    print(f"               {total_nonempty_line_count} nonempty line(s)")
    if amount_of_unreadable_files > 0:
        print(f"               {amount_of_unreadable_files} unreadable file(s)\n")
    else:
        print()

    print("AbleToRead     Lines  NonemptyLines     File")
    print("----------     -----  -------------     ----")

    for file in files.keys():
        first_gap   = " "*(20 - len(files[file][0]) - len(str(files[file][1])))
        second_gap  = " "*(18 - len(str(files[file][2])))

        print(f"{files[file][0]}{first_gap}{files[file][1]}  {files[file][2]}{second_gap}{file}")

    print("\n")


if __name__ == "__main__":
    main()
