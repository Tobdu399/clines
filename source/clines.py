import os
import sys
import chardet
import pathlib

show_encoding = False

path = os.getcwd()
files = {}

# The name of the files will always be printed in the same X position as 'Lines' header
# Other values will just be printed in order (value at the corresponding index 1, 2, 3, 4...)
# The order is currently the same as in the 'headers' dictionary:
headers = {
    "AbleToRead":    (0,    "right"),
    "Lines":         (15,   "left"),
    "NonemptyLines": (22,   "right"),
    "File":          (40,   "right")
}

current_line = ""


def add_to_display(text_to_add, space_to_previous, direction):
    global headers
    pos = headers[list(headers.keys())[-1]][0] + space_to_previous
    headers[text_to_add] = (pos, direction)


def update_header_underline():
    global underline

    underline = ""
    for header in headers.keys():
        while headers[header][0] > len(underline):
            underline += " "
        underline += "-"*len(header)


def main():
    global current_line

    total_line_count           = 0
    total_nonempty_line_count  = 0
    amount_of_unreadable_files = 0

    for file in (f for f in os.listdir(path) if os.path.isfile(f)):
        line_count            = 0
        nonempty_line_count   = 0

        try:
            if os.access(f"{path}/{file}", os.R_OK):
                try:
                    current_file = open(f"{path}/{file}", "r", encoding="ISO-8859-1")
                    encoding = ""

                    if show_encoding:
                        rawdata  = open(f"{path}/{file}", "rb").read()
                        result   = chardet.detect(rawdata)
                        encoding = result["encoding"]
                        if encoding is None:
                            encoding = "-"

                    # Calculate the amount of lines
                    lines = current_file.readlines()
                    for line in lines:
                        formatted_line = line.replace("\n", "")
                        lines[lines.index(line)] = formatted_line

                        line_count += 1
                        if formatted_line != "":
                            nonempty_line_count += 1

                    files[file] = ("Yes", line_count, nonempty_line_count, encoding)
                    total_line_count += line_count
                    total_nonempty_line_count += nonempty_line_count

                except PermissionError:
                    gap = " " * (10 - len("No") - len("AD"))
                    files[file] = (f"No{gap}AD", 0, 0, encoding)
                    amount_of_unreadable_files += 1
            else:
                gap = " "*(10 - len("No") - len("AD"))
                files[file] = (f"No{gap}AD", 0, 0, encoding)
                amount_of_unreadable_files += 1
        except KeyboardInterrupt:
            gap = " " * (10 - len("No") - len("INT"))
            files[file] = (f"No{gap}INT", 0, 0, encoding)
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

    update_header_underline()
    header = ""

    for element in headers.keys():
        while len(header) < headers[element][0]:
            header += " "
        header += element

    print(header)
    print(underline)

    for file in files.keys():
        index = 0
        for header in headers.keys():
            header_pos = headers[header][0]
            header_length = len(header)
            if headers[header][1] == "left":
                space_between = header_pos + header_length - len(current_line) - len(str(files[file][index]))
            else:
                space_between = header_pos - len(current_line)

            if space_between < 0:
                extension = pathlib.Path(f"{path}/{file}").suffix
                length_visualizer = "...  " + extension

                while space_between < len(length_visualizer) + 5:
                    current_line = current_line[:-1]
                    space_between = header_pos - len(current_line)

                space_between -= len(length_visualizer)
                current_line += length_visualizer

            if header == "File":
                current_line += " "*space_between + str(file)
            else:
                current_line += " "*space_between + str(files[file][index])
                if index < len(files[list(files.keys())[0]])-1:
                    index += 1

        print(current_line)
        current_line = ""
    print("\n")


if __name__ == "__main__":
    arguments = sys.argv

    if "/e" in arguments:
        show_encoding = True
        add_to_display("Encoding", 25, "right")

    main()
