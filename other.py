input2 = " dehedebdewhbdewhbdhewbdewbdkewbdhewbdhkewbdhewbhkbhfrehuigbreyuicernvuteryvtortuierlhtuirdvyt7oerbtuerlytuoery9eoy8"
import re
# Define the regular expression pattern for the title
title_pattern = re.compile(r'^(.*?)Stage', re.DOTALL)

# Define the regular expression pattern for the location
location_pattern = re.compile(r'Location(.*?)CIS Researcher', re.DOTALL)

# Search for the patterns in the input string
title_match = title_pattern.search(input2)
location_match = location_pattern.search(input2)

# Extract and print the title of the deal
if title_match:
    title_of_deal = title_match.group(1).strip()
    print("Title of the deal:", title_of_deal)
else:
    print("Title of the deal not found.")