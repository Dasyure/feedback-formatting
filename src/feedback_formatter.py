import pandas as pd
import csv
import copy
import sys
from classes import Feedback

INPUT_FILE = "input/input.xlsx"
INPUT_FILE_CSV = "input/csv/input.csv"
OUTPUT_FILE = 'output/results.md'
ENABLE_COLOUR_GRADES = True
# Used for colouring grades (can only have 4 colours)
GRADE_RANGE = {
    'tier1': ['Perfect'],
    'tier2': ['Really great'],
    'tier3': ['Average', 'Good'],
    'tier4': ['Terrible', 'Below Average'],
}
# Global variable
'''
feedback = {
    group: Feedback,
    individual: {
        name1: Feedback,
    }
}
'''
feedback = { 'group': {}, 'individual': {} }

'''
Description: converts given xls file into csv file. Input is originally xls
    since it looks better and retains formatting.
'''
def convert_xls_csv() -> None:
    dataframe = pd.read_excel(INPUT_FILE)
    dataframe.to_csv(INPUT_FILE_CSV, index=None, header=True) 

'''
Description: parses CSV input into data structures (results and individual_results)
    CSV is expected to be in this format:
    Header1 | Header2 | Header3 | Header4
    Mark | Description | Mark | Description | Mark | Description | Mark | Description  
    #### | Header1 | Header2 | Header3
    Name | Mark | Description | Mark | Description | Mark | Description
    Name | Mark | Description | Mark | Description | Mark | Description
    Name | Mark | Description | Mark | Description | Mark | Description
    Name | Mark | Description | Mark | Description | Mark | Description
    Name | Mark | Description | Mark | Description | Mark | Description
'''
def parse_csv() -> None:
    global feedback
    with open(INPUT_FILE_CSV, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        # GROUP FEEDBACK: First two rows
        Group_feedback = Feedback(INPUT_FILE)
        for row in csv_reader:
            if (Group_feedback.is_empty()):
                Group_feedback.add_categories(row[1:])
            else:
                Group_feedback.add_marks_comments(row[1:])
                break
        feedback['group'] = Group_feedback

        # INDIVIDUAL FEEDBACK: Continues looping from 3rd row onwards
        list_of_names = []
        list_of_feedback = []
        Individual_feedback = Feedback(INPUT_FILE)
        for row in csv_reader:
            if (Individual_feedback.is_empty()):
                Individual_feedback = Feedback(INPUT_FILE)
                Individual_feedback.add_categories(row[1:])
            elif(row[0] != ''):
                list_of_names.append(row[0])
                Individual_feedback.add_marks_comments(row[1:], is_group = False)
                list_of_feedback.append(copy.deepcopy(Individual_feedback))
        for i, name in enumerate(list_of_names):
            feedback['individual'][name] = list_of_feedback[i]

'''
Description: grabs the start_msg to add to the beginning of the output, then
    grab the end_msg to add to the end of the output. 
'''
def get_start_end_messages(iteration_num) -> list:
    input_file_append_msg = f"input/iter{iteration_num}_message.md"
    with open(input_file_append_msg, 'r') as textfile:
        start_message = ''
        end_message = ''
        flag = 'START'
        for line in textfile:
            if ('START_MESSAGE' in line) or ('END_MESSAGE' in line):
                flag = 'START' if 'START_MESSAGE' in line else 'END'
                continue
            start_message += line if flag == 'START' else ''
            end_message += line if flag == 'END' else ''
    return [start_message, end_message]

'''
Description: adds colour to the grade on markdown
'''
def colour_grade(grade):
    if (not ENABLE_COLOUR_GRADES):
        return grade
    if (grade in GRADE_RANGE['tier1']):
        return f"<span style='color:teal;'>{grade}</span>"
    elif (grade in GRADE_RANGE['tier2']):
        return f"<span style='color:yellowgreen;'>{grade}</span>"
    elif (grade in GRADE_RANGE['tier3']):
        return f"<span style='color:orange;'>{grade}</span>"
    elif (grade in GRADE_RANGE['tier4']):
        return f"<span style='color:red;'>{grade}</span>"
    return grade

'''
Description: turns feedback into a formatted string.
    Group feedback uses markdown table, Individual feedback uses dot points
'''
def format_feedback_into_string(Feedback, group_feedback = False, show_header = False):
    result = ''
    if group_feedback:
        if (show_header):
            result += '| Mark | Category | Comments |\n'
        else:
            result += '|  |  |  |\n'
        result += '| ---- | ---- | ---- |\n'
    for category in Feedback.get_categories():
        mark = colour_grade(Feedback.get_mark(category))
        comments = "Nothing to comment on!" if Feedback.get_comments(category) == '' else Feedback.get_comments(category)
        if group_feedback:
            result += f"| {mark} | {category} | {comments} |\n"
        else:
            result += f"  - {mark} {category}: {comments} \n"
    return result

'''
Description: formats the final output
'''
def export_results(start_message, end_message, iteration_num):
    global feedback
    with open(OUTPUT_FILE, 'w') as textfile:
        # Start message
        textfile.write(f"{start_message}")
        # Group feedback
        group_result = format_feedback_into_string(feedback['group'], group_feedback=True, show_header=True)
        textfile.write(group_result)
        # Individual feedback
        if iteration_num != 0:
            textfile.write('\n\\\n**Additional individual comments**\n')
        individual_result = ''
        for name in feedback['individual']:
            individual_result += f"- {name}:\n"
            individual_result += format_feedback_into_string(feedback['individual'][name])
        textfile.write(individual_result[:-2])
        # End message
        textfile.write(f"\n___\n {end_message}")

if __name__ == "__main__":
    iterations = [0, 1, 2, 3]
    correct_usage = ("    Correct usage: 'python3 src/feedback_formatter.py ITERATION_NUM'\n"
                     f"               e.g 'python3 src/feedback_formatter.py 2'")
    if (len(sys.argv) != 2):
        print(f'\n    Error: incorrect number of arguments passed!\n{correct_usage}')
    elif(not sys.argv[1].isdigit()):
        print(f'\n    Error: ITERATION_NUM must be 0, 1, 2 or 3.\n{correct_usage}')
    elif(int(sys.argv[1]) not in iterations):
        print(f'\n    Error: ITERATION_NUM must be 0, 1, 2 or 3.\n{correct_usage}')
    else:
        iteration_num = int(sys.argv[1])
        convert_xls_csv()
        parse_csv()
        [start_message, end_message] = get_start_end_messages(iteration_num)
        export_results(start_message, end_message, iteration_num)
        print(f"\n    Open '{OUTPUT_FILE}' to view the output!")
