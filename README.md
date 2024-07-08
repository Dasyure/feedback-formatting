TODO:
- instructions, with pictures / video recording
- remove the need for ####, remove counter use a flag instead
- rearrange order of start and end message? <<< nah
- use "___" as a break


Instructions:
- Row 1: copy paste headers for group feedback


Group Feedback Instructions:
- Copy paste row (from TestCoverage to WhitespaceIndentation) into `group-input.txt`
- Copy paste row (individual tab: from IssueBoard to Meetings) into the line below in `group-input.txt`
- Copy start and end message into `announcements.txt` in the form of `START_MESSAGE: ....\n END_MESSAGE: ....`
- Run `python3 group-formatter.py`
- `group-input.txt` will have your changes

Individual Feedback Instructions:
- Copy paste column names (e.g. Zhanxin Ye, Jyne Nakamura, Eric Liu, Tiffany Lin, Caroline Liu) into `individual-input-names.txt`
- Copy paste columns and rows result (top left corner for commits, bottom right corner for testBeforeImplementation) into `individual-input-results.txt`
- Copy start and end message into `announcements.txt` in the form of `START_MESSAGE: ....\n END_MESSAGE: ....`
- Run `python3 individual-formatter.py`
- `individual-input-results.txt` will have your changes

Description: formats spreadsheet feedback (both group and individual)
Instructions:
 - copy paste feedback into INPUT_FILE
 - copy paste start and end messages into START_AND_END_MSG
 - run: python3 formatter.py