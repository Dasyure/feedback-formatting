'''
Description: formats spreadsheet feedback (both group and individual)
Instructions:
 - copy paste feedback into input.csv
 - run: python3 formatter.py
 - copy text from results.txt
'''
import csv
import copy
import re
INPUT_FILE = "input.csv"
OUTPUT_FILE = 'results.txt'
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
        if i % 2 != 0 and i != max_index:
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
        if i % 2 != 0 and i != max_index:
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
def copy_input():
    counter = 0
    with open(INPUT_FILE, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t')
        # GROUP: First two rows
        for row in csv_reader:
            counter += 1 if counter < 2 else None
            if (results == {}):
                populate_categories(row)
            else:
                populate_marks_comments(row)
            if (counter >= 2):
                break

        # INDIVIDUAL: Continues looping from 3rd row onwards
        list_of_names = []
        list_of_results = []
        template_individual_results = {}
        for row in csv_reader:
            if (row[0] == HASH_STR):
                template_individual_results = populate_categories_individual(row)
            elif(row[0] == ''):
                continue
            else:
                list_of_names.append(row[0])
                feedback = populate_marks_comments_individual(row[1:], template_individual_results)
                list_of_results.append(copy.deepcopy(feedback))
        for i, name in enumerate(list_of_names):
            individual_results[name] = list_of_results[i]

'''
Description: formats the final output
'''
def export_results(start_message, end_message):
    with open(OUTPUT_FILE, 'w') as textfile:
        # Start message
        textfile.write(f"{start_message[1:]}\n")
        # Group and Individual feedback
        for category in results:
            comments = "Nothing to comment on!" if results[category]['comments'] == '' else results[category]['comments']
            textfile.write(f"[{results[category]['mark']}] {category}: {comments}\n")
        textfile.write('\n** Additional individual comments **\n\n')
        for name in individual_results:
            textfile.write(f"{name}:\n")
            for cat in individual_results[name]:
                comments = "Nothing to comment on!" if individual_results[name][cat]['comments'] == '' else individual_results[name][cat]['comments']
                textfile.write(f"  • [{individual_results[name][cat]['mark']}] {cat}: {comments}\n")
        # End message
        textfile.write(f"\n{end_message[1:]}")



if __name__ == "__main__":
    start_message = """
Congrats on finishing iter1! Here’s my overall thoughts on how you did this iteration:
  • 
  • Reminder: I was lenient with marking this iteration, so make sure you read each comment even if I gave a perfect mark. 

Below is a very quick breakdown of each section of the manual mark portion of iter1. The majority of these marks come from style and git practices! If a section was done perfectly, I won’t have many comments. The marks range from [terrible/below average/average/good/great/perfect]:
"""
    end_message = """
Additional notes:
  • Please read any comments left in the feedback merge request. It should be called “Project Feedback: Iteration 1”. If you click on the “changes” tab and scroll through the unresolved threads, you can view my comments. If I notice a line of code with bad style, I only comment on the first instance of it, so make sure you apply the feedback everywhere. 
  • Final marks: the course will release these. If you find your marks differ slightly from your team mates, it’s completely normal! It’s due to the way peer review data is collected by the course. 
  • However, if your marks are significantly less than your team mates, I will message you individually on MS teams with reasons why. 
Goodluck with iter2, see you all in two weeks!
"""
    copy_input()
    export_results(start_message, end_message)
