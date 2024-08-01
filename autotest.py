import re


input2 = '''
€63m - Office Development, Dublin 2
Stage Plans Granted

Updated 23/07/2024

Open with

Primary sector
Commercial  Office
Location
Setanta Centre, 6-15 Nassau Street, Dublin 2 and including a building at No.44 Kildare Street (know, as Transport House - at the junction of Setanta Place and Kildare Street)., Dublin 2 D02 XK75, Co. Dublin
Linked projects
€63m - Office Development, Kildare Street
CIS Researcher

Judith Irvine
Do you have questions or require further information on this project? Please contact me.
CIS Next review
Oct 2024
Description
23/07/2024: A decision to grant planning permission was issued by Dublin City Council on 18/07/2024 to Ternary Limited for a proposed development site extends to 5,857 square metres in area and will have a gross floor area of 37,722 square metres, including basement areas of 14,970 square metres. the application site is bounded by nassau street to the north and the rear of buildings fronting nassau street, setanta place to the south (including existing basement levels beneath setanta place street level), to the east by kildare street and the rear of the buildings fronting kildare street, and to the west by the rear of buildings fronting frederick street south. the planning applications relates to development which adjoins the rear of protected structures fronting 22 - 30 frederick street south, the rear of no. 5 and 16 - 19 nassau street and the rear of 45- 46 kildare street.

The number of storeys on the existing buildings on the site varies up to a maximum of 8 storeys with roof-top plant and equipment over 2 basement levels. the development will consist of the demolition, excavation and clearance of all existing buildings and structures on the site including basements other than the existing kilkenny design store and annex 1,455 square metres and associated basement areas of 1,432 square metres (notated on the planning application drawings as 'sg1' and 'sg2' at b-1) which do not form part of the demolition/construction proposals. the western boundary walls to the rear of the protected structures fronting frederick street south and rear of 5 and 16-19 nassau street will be demolished and new boundary walls constructed. in addition to the demolition of the buildings, the development also provides for the demolition of the two existing basements (excluding the basement levels beneath setanta place which are retained and remodelled internally), and car park ramps from setanta place.

Following the above demolitions, excavations and site clearance the development provides for the construction a new office building extending to 8 storeys in height including setbacks at 6th, 7th and 8th storey over 4 basement levels (the two basement levels beneath setanta place which are retained and remodelled and are notated on the planning application drawings as 'sg1' and 'sg2' at basement level b-1) and new car park access/egress ramps off setanta place. the existing vehicular connection beneath setanta place between the application site and public car parking spaces in the building known as 10-11 molesworth street will be reinstated. the proposed basement levels will contain 211 car parking spaces (of which 141 will be for public use with the balance i.e. 70 for private use). the number of onsite car parking spaces on the overall site will be reduced from the existing 319 spaces to 211 spaces.

The basement areas will also contain300 bicycle parking spaces along with associated drying areas, bicycle repair facilities, showers and locker/changing/storage areas, accessed via a dedicated cycle access/egress ramp off setanta place, circulation, waste receptacle areas, plant and equipment and tenant facilities. service and deliveries will be from nassau street and setanta place and via basement areas. a swimming pool and gymnasium are proposed at ground and b-1 levels. the development incorporates sustainable development measures including roof mounted photovoltaic cells (500sq.m), green roof areas, rain water harvesting, air-sourced heat-pumps and attenuation tank. the pedestrian link between nassau street and setanta place will be repositioned and upgraded. it is also proposed to relocate the existing mosaic mural known as the "tain wall" for the western boundary wall forward towards nassau street. the proposal includes roof terraces at 5th floor level to the northern, eastern and western elevations facing towards nassau street, south frederick street and kildare street respectively. the main entrance to the proposed development will be off nassau street, with secondary entrances off the pedestrian link and setanta place.

A pedestrian entrance is also provided off kildare street. the proposed development provides for 1 no. double esb substation fronting setanta place along with all associated site development works including landscaping and boundary treatments and air intake and out-let fans and ducts/vents including screened roof top mounted plant and equipment including zone for communications equipment (satellite dishes/aerials) at seventh and eight storeys.

Please see linked project for information on original planning application.
Key details
Value
€63.7m
(Estimated)
Project ID
1348811
Planning Stage
Plans Granted
CIS Next Review
Oct 2024
Floor Area
37,722 m2
Funding Type
Private
Construction Type
New Build
Planning Information
Authority
Dublin City Council
Planning Reference
2407/18/X1
Decision Date
18 Jul 2024
Application Date
27 May 2024
SiteArea
0.59 ha
Links and Files
Documents
Planning documents
Additional Information
Storeys
8
Requires Demolition
Y
Postcode
D02 XK75
Structures
1
CompaniesMaterialsTrackingHistory
Promoter
Ternary Limited
CountyDublin 2

Planning Consultant
Stephen Ward Town Planning and Development Consultants
Emailplanning@wardconsult.com

Phone+353429329791

CountyCo. Louth

LinkedIn

'''
'''
print("Enter your text (type 'END' on a new line to finish):")
input_lines = []
while True:
    line = input()
    if line == "END":
        break
    input_lines.append(line)
input2 = "\n".join(input_lines)
'''

######TITLE OF THE DEAL########
# Define the regular expression pattern for the title
title_pattern = re.compile(r'^(.*?)Stage', re.DOTALL)

# Define the regular expression pattern for the location
location_pattern = re.compile(r'Location(.*?)CIS Researcher', re.DOTALL)

# Search for the patterns in the input string
title_match = title_pattern.search(input2)
location_match = location_pattern.search(input2)

# Extract the title of the deal
if title_match:
    title_of_deal = title_match.group(1).strip()

######LOCATION OF THE DEAL########
# List of all 32 counties in Ireland
counties = [
    "Carlow", "Cavan", "Clare", "Cork", "Donegal", "Dublin", "Galway",
    "Kerry", "Kildare", "Kilkenny", "Laois", "Leitrim", "Limerick",
    "Longford", "Louth", "Mayo", "Meath", "Monaghan", "Offaly",
    "Roscommon", "Sligo", "Tipperary", "Waterford", "Westmeath",
    "Wexford", "Wicklow", "Antrim", "Armagh", "Down", "Fermanagh",
    "Derry", "Tyrone"
]
# Define all necessary regex patterns at the start
location_pattern = re.compile(r'Location\n(.*?)\nCIS Researcher', re.DOTALL)
eircode_pattern = re.compile(r'\b[A-Z]\d{2}(\s*[A-Z0-9]{2,4})?\b')
title_pattern = re.compile(r'^(.*?)Stage', re.DOTALL)
developer_pattern = re.compile(r'Promoter\s*([\w\s]+)\s*Email', re.IGNORECASE)

# Extract the full location
location_match = location_pattern.search(input2)
full_location = location_match.group(1).strip() if location_match else "Location info not found."

# Remove Eircodes and split the location string
cleaned_location = eircode_pattern.sub('', full_location)
location_components = cleaned_location.split(',')

# Initialize variables
area = "Area not found"
location = "Location not found"

# Extract area and location based on components
if len(location_components) >= 2:
    area = location_components[-2].strip()
    location = location_components[-1].strip().replace('Co. ', '')

# Extract title of the deal
title_match = title_pattern.search(input2)
title_of_deal = title_match.group(1).strip() if title_match else "Title of the deal not found."

# Extract developer's name
developer_match = developer_pattern.search(input2)
developer_name = developer_match.group(1).strip() if developer_match else "Developer name not found."



#####Promoter name#####
# Define the regular expression pattern to find the developer's name
developer_pattern = re.compile(r'Promoter\s*([\w\s]+)\s*Email', re.IGNORECASE)

# Search for the pattern in the input string
developer_match = developer_pattern.search(input2)

# Print the developer's name
if developer_match:
    developer_name = developer_match.group(1).strip()
    
else:
    print("Developer name not found.")

#unit type:
# Regular expressions to find counts and primary sector
houses_pattern = re.compile(r'Total Houses\s*(\d+)')
apartments_pattern = re.compile(r'Total Apartments\s*(\d+)')
primary_sector_pattern = re.compile(r'Primary sector\s*([\w\s]+)')

# Find counts of houses and apartments
houses_count = houses_pattern.search(input2)
apartments_count = apartments_pattern.search(input2)

# Extract primary sector
primary_sector_match = primary_sector_pattern.search(input2)
primary_sector = primary_sector_match.group(1).strip() if primary_sector_match else ""

# Determine unit type based on counts and primary sector
unit_type = ""
if houses_count and apartments_count:
    houses = int(houses_count.group(1))
    apartments = int(apartments_count.group(1))
    if houses > 0 and apartments > 0:
        unit_type = "Houses and Apartments"
    elif houses > 0:
        unit_type = "Houses"
    elif apartments > 0:
        unit_type = "Apartments"
else:
    # Fallback to primary sector if counts are not conclusive
    if "Apartment" in primary_sector:
        unit_type = "Apartments"
    elif "House" in primary_sector:
        unit_type = "Houses"
    else:
        # Additional mapping for other unit types could be added here
        unit_type = primary_sector


# Define regex for total residential units
total_units_pattern = re.compile(r'Total Res Units\s*[:\-]?\s*(\d+)', re.IGNORECASE)

# Search for total units in the input string
total_units_match = total_units_pattern.search(input2)
total_units = int(total_units_match.group(1)) if total_units_match else "Total number of units not found."

# Assuming the rest of your script has correctly populated these variables:
developer_name = developer_name.strip()  # Removing extra spaces and newlines
title_of_deal = title_of_deal.strip()
area = area.strip()
location = location.strip()
unit_type = unit_type.strip()
total_units = str(total_units).strip()  # Convert to string if not already and strip

# Prepare the output with exactly four spaces between each piece of information
formatted_output = f"{developer_name}    {title_of_deal}    {area}    {location}    {unit_type}    {total_units}"
print(formatted_output)