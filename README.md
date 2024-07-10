## Purpose
While I like to use the feedback merge request, I also like to give feedback on MS Teams. This script converts the marking spreadsheet feedback into a nice format that can be given to groups on MS Teams.

### Why use this script?
- **Takes less than a minute to do!**
- In your MyExperience feedback, students wished for more feedback
- Appends a message to the start and end of the feedback
- Pretty colourful output that summarises everything

### Video Demo
**Click below to watch!** Real student names and groups are hidden for privacy reasons. 
[![Watch the video](assets/feedback_formatting_thumbnail.png)](https://youtu.be/id39xWO5gwk)

## Setup
- Optional: setup a virtual environment first:
  - `python3 -m venv env`
  - `source env/bin/activate`
- `pip install -r requirements.txt`

## Instructions
### Quick instructions
- Copy input into `input/input.xlsx` just like in the video above!
- Run the script `python3 src/feedback_formatter.py ITER_NUM`
- Open `output/results.md`, hold `cmd + shift + v` to preview the markdown file.
- Copy paste the text from the markdown file to give to your classes.

### Detailed instructions
Open `input/input.xlsx` and get the following:
<details>
  <summary>1. Group categories</summary>

![Copy group categories](assets/1.1-copy-group-categories.png)
![Paste group categories](assets/1.2-paste-categories.png)
</details>
<details>
  <summary>2. Group feedback</summary>

![Copy group feedback](assets/1.3-copy-group-feedback.png)
![Paste group feedback](assets/1.4-paste-group-feedback.png)
</details>
<details>
  <summary>3. Individual names</summary>

![Copy names](assets/2.1-copy-names.png)
![Paste names](assets/2.2-paste-names.png)
</details>
<details>
  <summary>4. Individual categories</summary>

![Copy individual categories](assets/2.3-copy-categories.png)
![Paste individual categories](assets/2.4-paste-categories.png)
</details>
<details>
  <summary>5. Individual feedback</summary>

![Copy individual feedback](assets/2.5-copy-feedback.png)
![Paste individual feedback](assets/2.6-paste-feedback.png)
</details>
Optionally: you can group together individual categories as group categories
  <details>
    <summary>Instructions</summary>

  ![Copy group categories](assets/3.1-copy-group-categories.png)
  ![Copy additional group categories](assets/3.2-optionally-copy-more-group-categories.png)
  ![Paste additional group categories](assets/3.3-paste-categories.png)
  ![Copy group feedback](assets/3.4-copy-group-feedback.png)
  ![Copy additional group feedback](assets/3.5-copy-addition-group-feedback.png)
  ![Paste additional group feedback](assets/3.6-paste-extra-feedback.png)
  </details>

___

After everything has been copied in:
- Run the script `python3 src/feedback_formatter.py ITER_NUM`
- Open `output/results.md`, hold `cmd + shift + v` to preview the markdown file.
- Copy paste the text from the markdown file to give to your classes.

## Customising the output
- The contents of the `start message` and the `end message` can be changed in the markdown files in `/input`
- Settings can be configured in `config.yaml`.
  - If no comment is left for a mark, the default comment is: `Nothing to comment on!`.
  - Each grade is coloured either green, light green, yellow or red
