"""
File structure:
-> convert_xls_csv
-> parse_csv
-> get_start_end_messages
-> export_results
  -> format_feedback_into_string
    -> colour_grade
-> print_results_for_fun
"""

import pandas as pd
import csv
import copy
import sys
from classes import Feedback, Store_Feedback
from get_config import (
    INPUT_FILE,
    INPUT_FILE_CSV,
    OUTPUT_FILE,
    DEFAULT_COMMENT,
    ENABLE_COLOUR_GRADES,
    GRADE_COLOUR_RANGE,
)


def convert_xls_csv() -> None:
    """
    Description: converts given xlsx file into csv file. Input is originally xlsx
        since it looks better and retains formatting.
    """
    dataframe = pd.read_excel(INPUT_FILE)
    dataframe.to_csv(INPUT_FILE_CSV, index=None, header=True)


def parse_csv(Datastore) -> None:
    """
    Description: parses CSV input into data structures
    """
    # global feedback
    with open(INPUT_FILE_CSV, "r") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        # GROUP FEEDBACK: First two rows
        Group_feedback = Feedback()
        for row in csv_reader:
            if Group_feedback.is_empty():
                Group_feedback.add_categories(row[1:])
            else:
                Group_feedback.add_marks_comments(row[1:])
                break
        Datastore.add_group_feedback(Group_feedback)

        # INDIVIDUAL FEEDBACK: Continues looping from 3rd row onwards
        list_of_names = []
        list_of_feedback = []
        Individual_feedback = Feedback()
        for row in csv_reader:
            if Individual_feedback.is_empty():
                Individual_feedback = Feedback()
                Individual_feedback.add_categories(row[1:])
            elif row[0] != "":
                list_of_names.append(row[0])
                Individual_feedback.add_marks_comments(row[1:], is_group=False)
                list_of_feedback.append(copy.deepcopy(Individual_feedback))
        for i, name in enumerate(list_of_names):
            Datastore.add_individual_feedback(name, list_of_feedback[i])


def get_start_end_messages(iteration_num) -> list:
    """
    Description: grabs the start_msg to add to the beginning of the output, then
        grab the end_msg to add to the end of the output.
    """
    input_file_append_msg = f"input/iter{iteration_num}_message.md"
    with open(input_file_append_msg, "r") as textfile:
        start_message = ""
        end_message = ""
        flag = "START"
        for line in textfile:
            if ("START_MESSAGE" in line) or ("END_MESSAGE" in line):
                flag = "START" if "START_MESSAGE" in line else "END"
                continue
            start_message += line if flag == "START" else ""
            end_message += line if flag == "END" else ""
    return [start_message, end_message]


def colour_grade(grade):
    """
    Description: adds colour to the grade on markdown
    """
    if not ENABLE_COLOUR_GRADES:
        return grade
    tiers = list(GRADE_COLOUR_RANGE.keys())
    for tier in tiers:
        if grade in GRADE_COLOUR_RANGE[tier]["grades"]:
            return f"<span style='color:{GRADE_COLOUR_RANGE[tier]['colour']};'>{grade}</span>"
    return grade


def format_feedback_into_string(Feedback, group_feedback=False, show_header=False):
    """
    Description: turns feedback into a formatted string.
        Group feedback uses markdown table, Individual feedback uses dot points
    """
    result = ""
    if group_feedback:
        if show_header:
            result += "| Mark | Category | Comments |\n"
        else:
            result += "|  |  |  |\n"
        result += "| ---- | ---- | ---- |\n"
    for category in Feedback.get_categories():
        mark = colour_grade(Feedback.get_mark(category))
        comments = (
            f"{DEFAULT_COMMENT}"
            if Feedback.get_comments(category) == ""
            else Feedback.get_comments(category)
        )
        if group_feedback:
            result += f"| {mark} | {category} | {comments} |\n"
        else:
            result += f"  - {mark} {category}: {comments} \n"
    return result


def export_results(Datastore, start_message, end_message, iteration_num):
    """
    Description: formats the final output
    """
    # global feedback
    with open(OUTPUT_FILE, "w") as textfile:
        # Start message
        textfile.write(f"{start_message}")
        # Group feedback
        group_result = format_feedback_into_string(
            Datastore.get_group_feedback(), group_feedback=True, show_header=True
        )
        textfile.write(group_result)
        # Individual feedback
        if iteration_num != 0:
            textfile.write("\n\\\n**Additional individual comments**\n")
        individual_result = ""
        # for name in feedback['individual']:
        for name in Datastore.get_individual_list():
            individual_result += f"- {name}:\n"
            individual_result += format_feedback_into_string(
                Datastore.get_individual_feedback(name)
            )
        textfile.write(individual_result[:-2])
        # End message
        textfile.write(f"\n___\n {end_message}")


def print_results_for_fun(Datastore) -> None:
    """
    Description: not needed for functionality, just for fun and debugging
    """
    Datastore.print()


if __name__ == "__main__":
    iterations = [0, 1, 2, 3]
    correct_usage = (
        "    Correct usage: 'python3 src/feedback_formatter.py ITERATION_NUM'\n"
        f"               e.g 'python3 src/feedback_formatter.py 2'"
    )
    if len(sys.argv) != 2:
        print(f"\n    Error: incorrect number of arguments passed!\n{correct_usage}")
    elif not sys.argv[1].isdigit():
        print(f"\n    Error: ITERATION_NUM must be 0, 1, 2 or 3.\n{correct_usage}")
    elif int(sys.argv[1]) not in iterations:
        print(f"\n    Error: ITERATION_NUM must be 0, 1, 2 or 3.\n{correct_usage}")
    else:
        iteration_num = int(sys.argv[1])
        Datastore = Store_Feedback()

        convert_xls_csv()
        parse_csv(Datastore)
        [start_message, end_message] = get_start_end_messages(iteration_num)
        export_results(Datastore, start_message, end_message, iteration_num)
        # print_results_for_fun(Datastore)
        print(f"\n    Run the command 'open {OUTPUT_FILE}' to view the output!")
