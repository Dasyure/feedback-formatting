import csv
import copy
import pandas as pd

INPUT_FILE = "input/input.xls"
INPUT_FILE_CSV = "input/csv/input.csv"
INPUT_FILE_APPEND_MSG = "input/iter1_message.md"
OUTPUT_FILE = 'output/results.md'
ENABLE_COLOUR_GRADES = True
'''
Data Structure used:
feedback = {
    group: Feedback,
    individual: {
        name1: Feedback,
    }
}
'''
# Global variable
feedback = { 'group': {}, 'individual': {} }

class Feedback:
    '''
        feedback = {
            category1: {
                mark: Perfect,
                comments: Not bad!
            },
        }
    '''
    def __init__(self) -> None:
        self.feedback = {}
    def is_empty(self) -> bool:
        return True if self.feedback == {} else False
    def add_categories(self, categories) -> None:
        for category in categories:
            if category != '' and 'Unnamed' not in category:
                self.feedback[category] = { 'mark': '', 'comments': ''}
    def get_categories(self) -> list:
        return [category for category in self.feedback.keys()]
    def add_marks_comments(self, row) -> None:
        print(len(row))
        categories = self.get_categories()
        max_index = len(categories) * 2 - 1
        category_index = 0
        curr_category = categories[0]
        curr_section = 'mark'
        for i, mark_or_comment in enumerate(row):
            curr_section = 'mark' if i % 2 == 0 else 'comments'
            self.feedback[curr_category][curr_section] = mark_or_comment
            # If index is odd, change categories
            if i % 2 != 0 and i < max_index:
                category_index += 1
                curr_category = categories[category_index]
            if i == max_index:
                break
    def get_mark(self, category) -> str:
        return self.feedback[category]['mark']
    def get_comments(self, category) -> str:
        return self.feedback[category]['comments']
    def print(self, raw = False) -> None:
        if raw:
            print(self.feedback)
        else:
            for category in self.feedback:
                print(f"  {category}:\n"
                    f"    • Mark: {self.feedback[category]['mark']}\n"
                    f"    • Comments: {self.feedback[category]['comments']}")

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
        Group_feedback = Feedback()
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
        Individual_feedback = Feedback()
        for row in csv_reader:
            if (Individual_feedback.is_empty()):
                Individual_feedback = Feedback()
                Individual_feedback.add_categories(row[1:])
            elif(row[0] != ''):
                list_of_names.append(row[0])
                Individual_feedback.add_marks_comments(row[1:])
                list_of_feedback.append(copy.deepcopy(Individual_feedback))
        for i, name in enumerate(list_of_names):
            feedback['individual'][name] = list_of_feedback[i]

'''
Description: grabs the start_msg to add to the beginning of the output, then
    grab the end_msg to add to the end of the output. 
'''
def get_start_end_messages() -> list:
    with open(INPUT_FILE_APPEND_MSG, 'r') as textfile:
        start_message = ''
        end_message = ''
        flag = 'START'
        for line in textfile:
            if 'START_MESSAGE' in line:
                flag = 'START'
                continue
            elif 'END_MESSAGE' in line:
                flag = 'END'
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
    if (grade in ['Terrible', 'Below Average']):
        return f"<span style='color:red;'>{grade}</span>"
    elif (grade in ['Average', 'Good']):
        return f"<span style='color:orange;'>{grade}</span>"
    elif (grade == 'Really great'):
        return f"<span style='color:yellowgreen;'>{grade}</span>"
    elif (grade == 'Perfect'):
        return f"<span style='color:teal;'>{grade}</span>"
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
def export_results(start_message, end_message):
    global feedback
    with open(OUTPUT_FILE, 'w') as textfile:
        # Start message
        textfile.write(f"{start_message}")
        # Group feedback
        group_result = format_feedback_into_string(feedback['group'], group_feedback=True, show_header=True)
        textfile.write(group_result)
        # Individual feedback
        textfile.write('\n\\\n**Additional individual comments**\n')
        individual_result = ''
        for name in feedback['individual']:
            individual_result += f"- {name}:\n"
            individual_result += format_feedback_into_string(feedback['individual'][name])
        textfile.write(individual_result[:-2])
        # End message
        textfile.write(f"\n___\n {end_message}")

if __name__ == "__main__":
    # TODO: second argument to be the iteration, python3 feedback_formatter.py iter1
    # TODO: throw error if incorrect number of args passed to input.csv
    # TODO: config.yaml and classes.py
    dataframe = pd.read_excel(INPUT_FILE)
    dataframe.to_csv(INPUT_FILE_CSV, index=None, header=True) 
    parse_csv()
    [start_message, end_message] = get_start_end_messages()
    export_results(start_message, end_message)
    print(f"\n    Open '{OUTPUT_FILE}' to view the output!")
