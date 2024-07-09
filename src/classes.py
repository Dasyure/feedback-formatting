from get_config import INPUT_FILE

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
    def len_feedback(self, row) -> int:
        num = 0
        for i, item in enumerate(row):
            if (i % 2 == 0 and item != ''):
                num += 1
        return num
    def add_marks_comments(self, row, is_group = True) -> None:
        categories = self.get_categories()
        max_index = len(categories) * 2 - 1
        num_categories = len(categories)
        num_marks = self.len_feedback(row)
        # Warning if there are missing categories or marks
        if(num_categories != num_marks):
            section = 'group' if is_group else 'individual'
            missing_item = 'marks' if num_categories > num_marks else 'categories'
            missing_num = num_marks if num_categories > num_marks else num_categories
            correct_item = 'categories' if num_categories > num_marks else 'marks'
            correct_num = num_categories if num_categories > num_marks else num_marks
            print(f"\n    Warning: You forgot to copy paste some {missing_item} into the {section} section!"
                  f"\n    There's {correct_num} {correct_item} but only"
                  f" {missing_num} {missing_item}. Some fields may be missing. Open '{INPUT_FILE}' and try again. ")
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
