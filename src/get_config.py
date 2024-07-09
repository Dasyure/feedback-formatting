import yaml

# Gets constants needed for the scraper
with open("config.yaml", "r") as file:
    data = yaml.safe_load(file)

INPUT_FILE = data["INPUT_FILE"]
INPUT_FILE_CSV = data["INPUT_FILE_CSV"]
OUTPUT_FILE = data["OUTPUT_FILE"]
DEFAULT_COMMENT = data["DEFAULT_COMMENT"]
ENABLE_COLOUR_GRADES = data["ENABLE_COLOUR_GRADES"]
GRADE_COLOUR_RANGE = data["GRADE_COLOUR_RANGE"]
