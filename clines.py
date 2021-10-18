import pathlib
import os
import threading
from   lib.progressbar import progressbar
import colorama
import time
import sys


total_amount_of_lines          = 0
total_amount_of_nonempty_lines = 0


def summary_and_quit():
    print(f"\n\n    Summary: {total_amount_of_lines} line(s)\n             {total_amount_of_nonempty_lines} nonempty line(s)\n\n")
    progressbar.stop()
    sys.exit()


def clines():
    global total_amount_of_lines, total_amount_of_nonempty_lines

    try:
        colorama.init()

        threading.Thread(target=progressbar.show).start()
        time.sleep(0.5)

        path       = os.getcwd()
        all_items  = [item for item in os.listdir(path)]
        folders    = [f"{folder}/" for folder in all_items if pathlib.Path(folder).is_dir()]
        files      = [file for file in all_items if pathlib.Path(file).is_file()]

        total_amount_of_files          = len(all_items)
        files_read                     = 0

        filename_max_length = 30
        name_gap            = (2 + max([len(item) for item in all_items]))

        if name_gap > filename_max_length:
            name_gap = filename_max_length

        directory       = f"\n\n    Directory: {path}\n\n"
        title           = f"Name{' ' * name_gap}Items/Lines NonemptyLines"
        title_underline = f"----{' ' * name_gap}----------- -------------"

        interrupted_text = " PROCESS INTERRUPTED "

        # Get the position where to print the amount of lines
        lines_text_location = title.find("Items/Lines") + len("Items/Lines")

        print(directory)
        print(title)
        print(title_underline)

        # Read folders --------------------------------------------------
        for current_folder in folders:
            foldername_to_print = current_folder
            if len(foldername_to_print) > filename_max_length:
                foldername_to_print = current_folder[:filename_max_length - 4] + ".../"

            try:
                progressbar.current_process = foldername_to_print

                amount_of_subitems = len([subitem for subitem in os.listdir(f"{path}/{current_folder}")])
                print(f"\033[33m📁\033[0m {foldername_to_print}{' ' * (lines_text_location - 3 - len(foldername_to_print) - len('Items/Lines'))}{amount_of_subitems}")

            except PermissionError:
                print(f"\033[33m📁\033[0m {foldername_to_print}{' ' * (lines_text_location - 3 - len(foldername_to_print) - len('Items/Lines'))}-                        \033[31mACCESS DENIED\033[0m")
            except KeyboardInterrupt:
                summary_and_quit()
            finally:
                files_read += 1
                progressbar.progress = (files_read / total_amount_of_files) * 100

        # Read files ----------------------------------------------------
        for current_file in files:
            filename_to_print = current_file
            if len(filename_to_print) > filename_max_length:
                filename_to_print = filename_to_print[:filename_max_length - 3 - len(filename_to_print[(filename_to_print.rfind(".")):])] + "..." + filename_to_print[(filename_to_print.rfind(".")):]

            try:
                with open(current_file, "r", encoding="iso-8859-15") as file:
                    # Update the progressbar "current file" text
                    progressbar.current_process = filename_to_print

                    lines = file.readlines()

                    total_lines    = len(lines)
                    nonempty_lines = 0
                    current_line   = 0

                    for line in lines:
                        if len(str(line).replace(" ", "").strip("\n")) > 0:
                            nonempty_lines += 1
                        current_line += 1

                    print(f"\033[36m📄\033[0m {filename_to_print}{' ' * (lines_text_location-(3+len(filename_to_print)+len(str(total_lines))))}{total_lines} {nonempty_lines}")

                    total_amount_of_lines          += total_lines
                    total_amount_of_nonempty_lines += nonempty_lines

                    file.close()

            except PermissionError:
                print(f"\033[36m📄\033[0m {filename_to_print}{' ' * (lines_text_location - (4 + len(filename_to_print)))}- -            \033[31mACCESS DENIED\033[0m")
            except KeyboardInterrupt:
                print(f"\n\033[31m{'-' * int((len(title)/2)-(len(interrupted_text)/2))}{interrupted_text}{'-' * int((len(title)/2)-(len(interrupted_text)/2))}\033[0m")
                summary_and_quit()
            finally:
                files_read += 1
                progressbar.progress = (files_read / total_amount_of_files) * 100

        time.sleep(0.5)
        summary_and_quit()

    except KeyboardInterrupt:
        progressbar.stop()


if __name__ == '__main__':
    clines()
