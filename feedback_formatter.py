import csv
import copy

INPUT_FILE = "input.csv"
START_AND_END_MSG = "iter1_message.md"
OUTPUT_FILE = 'results.md'
HASH_STR = '####'
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

'''
    self.feedback = {
        category1: {
            mark: Perfect,
            comments: Not bad!
        },
    }
'''
class Feedback:
    def __init__(self) -> None:
        self.feedback = {}
    def is_empty(self):
        return True if self.feedback == {} else False
    def add_categories(self, categories) -> None:
        for category in categories:
            if category not in ['', HASH_STR]:
                self.feedback[category] = { 'mark': '', 'comments': ''}
    def get_categories(self):
        return [category for category in self.feedback.keys()]
    def add_marks_comments(self, row):
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
    def get_mark(self, category):
        return self.feedback[category]['mark']
    def get_comments(self, category):
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
def parse_csv():
    global feedback
    with open(INPUT_FILE, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        # GROUP FEEDBACK: First two rows
        Group_feedback = Feedback()
        for row in csv_reader:
            if (Group_feedback.is_empty()):
                Group_feedback.add_categories(row)
            else:
                Group_feedback.add_marks_comments(row)
                break
        feedback['group'] = Group_feedback

        # INDIVIDUAL FEEDBACK: Continues looping from 3rd row onwards
        list_of_names = []
        list_of_feedback = []
        individual_feedback = Feedback()
        counter = 0
        for row in csv_reader:
            if (row[0] == HASH_STR):
                individual_feedback = Feedback()
                individual_feedback.add_categories(row)
            elif(row[0] != ''):
                list_of_names.append(row[0])
                individual_feedback.add_marks_comments(row[1:])
                list_of_feedback.append(copy.deepcopy(individual_feedback))
        for i, name in enumerate(list_of_names):
            feedback['individual'][name] = list_of_feedback[i]

'''
Description: grabs the start_msg to add to the beginning of the output, then
    grab the end_msg to add to the end of the output. 
'''
def get_start_end_messages():
    with open(START_AND_END_MSG, 'r') as textfile:
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
Description: turns feedback into a formatted string
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
            result += f"  • {mark} {category}: {comments} \\\n"
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
        textfile.write('\n___\n**Additional individual comments** \\\n')
        individual_result = ''
        for name in feedback['individual']:
            individual_result += f"{name}:\\\n"
            individual_result += format_feedback_into_string(feedback['individual'][name])
        textfile.write(individual_result[:-2])
        # End message
        textfile.write(f"\n___\n {end_message}")

if __name__ == "__main__":
    parse_csv()
    [start_message, end_message] = get_start_end_messages()
    export_results(start_message, end_message)
    print("\n    Open 'results.md' to view the output!")
