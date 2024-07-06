'''
Description: formats spreadsheet feedback (both group and individual)
Instructions:
 - copy paste feedback into input.csv
 - run: python3 formatter.py
 - copy text from results.txt
'''
import csv
import copy
INPUT_FILE = "input.csv"
START_AND_END_MSG = "iter1_message.md"
OUTPUT_FILE = 'results.md'
HASH_STR = '####'

'''
Data Structures Used
--------------------
results = {
    category1: {
        mark: Perfect,
        comments: Not bad!
    },
}
--------------------
individual_results = { name1: results_object, }
'''
results = {}
individual_results = {}
feedback = {
    'group': {},
    'individual': {}
}

class Feedback:
    '''
    self.feedback = {
        category1: {
            mark: Perfect,
            comments: Not bad!
        },
    }
    '''
    def __init__(self) -> None:
        self.feedback = {}
    def is_empty(self):
        return True if self.feedback == {} else False
    '''
    Description: populates itself with the categories
    '''
    def add_categories(self, categories) -> None:
        for category in categories:
            if category not in ['', HASH_STR]:
                self.feedback[category] = { 'mark': '', 'comments': ''}
    '''
    Description: returns list of categories
    '''
    def get_categories(self):
        return [category for category in self.feedback.keys()]
    '''
    Description: populates itself with the comments and mark for each category
    '''
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
    def print(self, raw = False) -> None:
        if raw:
            print(self.feedback)
        else:
            for category in self.feedback:
                print(f"  {category}:\n"
                    f"    • Mark: {self.feedback[category]['mark']}\n"
                    f"    • Comments: {self.feedback[category]['comments']}")

'''
Description: populates results with the categories
'''
def populate_categories(categories):
    for category in categories:
        if category != '':
            results[category] = { 'mark': '', 'comments': ''}

'''
Description: populates results with the comments and mark for each category
'''
def populate_marks_comments(row):
    keys = [key for key in results.keys()]
    max_index = len(keys) * 2 - 1
    curr_category = keys[0]
    curr_section = 'mark'
    category_counter = 0
    for i, item in enumerate(row):
        curr_section = 'mark' if i % 2 == 0 else 'comments'
        results[curr_category][curr_section] = item
        # If index is odd, change categories
        if i % 2 != 0 and i < max_index:
            category_counter += 1
            curr_category = keys[category_counter]
        if i == max_index:
            break

'''
Description: populates results with the categories
'''
def populate_categories_individual(categories):
    res = {}
    for category in categories:
        if category not in ['', HASH_STR]:
            res[category] = { 'mark': '', 'comments': ''}
    return res

'''
Description: populates results with the comments and mark for each category
'''
def populate_marks_comments_individual(row, results_template):
    keys = [key for key in results_template.keys()]
    max_index = len(keys) * 2 - 1
    curr_category = keys[0]
    curr_section = 'mark'
    category_counter = 0
    for i, item in enumerate(row):
        curr_section = 'mark' if i % 2 == 0 else 'comments'
        results_template[curr_category][curr_section] = item
        # If index is odd, change categories
        if i % 2 != 0 and i < max_index:
            category_counter += 1
            curr_category = keys[category_counter]
        if i == max_index:
            break
    return results_template

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
    counter = 0
    with open(INPUT_FILE, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        # GROUP: First two rows
        Group_feedback = Feedback()
        for row in csv_reader:
            counter += 1 if counter < 2 else None
            if (Group_feedback.is_empty()):
                # populate_categories(row)
                Group_feedback.add_categories(row)
            else:
                # populate_marks_comments(row)
                Group_feedback.add_marks_comments(row)
            if (counter >= 2):
                break

        # INDIVIDUAL: Continues looping from 3rd row onwards
        list_of_names = []
        list_of_feedback = []
        individual_feedback = Feedback()
        for row in csv_reader:
            if (row[0] == HASH_STR):
                individual_feedback = Feedback() # create new feedback each row
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
Description: formats the final output
'''
def export_results(start_message, end_message):
    with open(OUTPUT_FILE, 'w') as textfile:
        # Start message
        textfile.write(f"{start_message}")
        # Group feedback
        group_result = ''
        for category in results:
            comments = "Nothing to comment on!" if results[category]['comments'] == '' else results[category]['comments']
            group_result += f"  • [{results[category]['mark']}] {category}: {comments} \\\n"
        textfile.write(group_result[:-2])

        # Individual feedback
        individual_result = ''
        textfile.write('\n\n**Additional individual comments** \\\n')
        for name in individual_results:
            individual_result += f"{name}: \\\n"
            for cat in individual_results[name]:
                comments = "Nothing to comment on!" if individual_results[name][cat]['comments'] == '' else individual_results[name][cat]['comments']
                individual_result += f"  • [{individual_results[name][cat]['mark']}] {cat}: {comments} \\\n"
        textfile.write(individual_result[:-2])
        # End message
        textfile.write(f"\n\n{end_message}")

if __name__ == "__main__":
    parse_csv()
    # [start_message, end_message] = get_start_end_messages()
    # export_results(start_message, end_message)
