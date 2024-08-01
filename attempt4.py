import re
'''
# Define the regular expression patterns
title_pattern = re.compile(r'€\d+.*?-(.*?)(?:Stage|Updated|Open)', re.DOTALL)
location_pattern = re.compile(r'Location\s+(.*?)(?:\nLinked|CIS Researcher)', re.DOTALL)
developer_pattern = re.compile(r'Promoter\s*([\w\s]+)\s*Email', re.IGNORECASE)
total_units_pattern = re.compile(r'Total Res Units\s*[:\-]?\s*(\d+)', re.IGNORECASE)
eircode_pattern = re.compile(r'\b[A-Z]\d{2}(\s*[A-Z0-9]{2,4})?\b')
'''

title_pattern = re.compile(r'€.*?-(.*?)(?:Stage|Updated|Open)', re.DOTALL)
location_pattern = re.compile(r'Location\s+(.*?)(?:\nLinked|CIS Researcher)', re.DOTALL)
developer_pattern = re.compile(r'Promoter\s*(.*?)(?:\s*Contact|\s*Email|\s*County)', re.IGNORECASE | re.DOTALL)
total_units_pattern = re.compile(r'Total Res Units\s*[:\-]?\s*(\d+)', re.IGNORECASE)
hotel_bedrooms_pattern = re.compile(r'Hotel Bedrooms\s*[:\-]?\s*(\d+)', re.IGNORECASE)
square_meters_pattern = re.compile(r'Floor Area\s*[:\-]?\s*(\d+\.?\d*)\s*m2', re.IGNORECASE)
eircode_pattern = re.compile(r'\b[A-Z]\d{2}(\s*[A-Z0-9]{2,4})?\b')

# Define all counties
counties = [
    "Carlow", "Cavan", "Clare", "Cork", "Donegal", "Dublin", "Galway",
    "Kerry", "Kildare", "Kilkenny", "Laois", "Leitrim", "Limerick",
    "Longford", "Louth", "Mayo", "Meath", "Monaghan", "Offaly",
    "Roscommon", "Sligo", "Tipperary", "Waterford", "Westmeath",
    "Wexford", "Wicklow", "Antrim", "Armagh", "Down", "Fermanagh",
    "Derry", "Tyrone"
]

def extract_title(input_text):
    # Define a pattern to match from the first euro sign to the word "Stage"
    title_pattern = re.compile(r'(€.*?)-(.*?)(?:Stage|Updated|Open)', re.DOTALL)
    
    # Search for the pattern in the input text
    title_match = title_pattern.search(input_text)
    
    # Extract and clean the title
    if title_match:
        title = f"{title_match.group(1).strip()} - {title_match.group(2).strip()}"
        return title
    else:
        return "Title of the deal not found."

def extract_location(input_text):
    location_match = location_pattern.search(input_text)
    if not location_match:
        return "Area not found", "Location not found"
    
    full_location = location_match.group(1).strip()
    cleaned_location = eircode_pattern.sub('', full_location)
    location_components = [comp.strip() for comp in cleaned_location.split(',')]

    area = "Area not found"
    location = "Location not found"
    
    for i, component in enumerate(location_components):
        for county in counties:
            if county in component:
                # Check if there's a district code (one or two digits) following the county
                county_with_code = re.search(rf'\b{county}\b\s*\d{{1,2}}', component)
                if county_with_code:
                    location = county_with_code.group(0)
                else:
                    location = county
                area = location_components[i - 1] if i > 0 else "Area not found"
                break
        if location != "Location not found":
            break

    return area, location

def extract_developer(input_text):
    developer_pattern = re.compile(r'Promoter\s*(.*?)(?:\s*Contact|\s*Email|\s*County)', re.IGNORECASE | re.DOTALL)
    developer_match = developer_pattern.search(input_text)
    return developer_match.group(1).strip() if developer_match else "Developer name not found."

def extract_unit_type(input_text):
    # Define patterns for primary sector and unit counts
    primary_sector_pattern = re.compile(r'Primary sector\s*([\w\s]+)')
    houses_pattern = re.compile(r'Total Houses\s*(\d+)')
    apartments_pattern = re.compile(r'Total Apartments\s*(\d+)')

    # Extract counts of houses and apartments
    houses_count = houses_pattern.search(input_text)
    apartments_count = apartments_pattern.search(input_text)

    # Determine unit type based on counts
    if houses_count and apartments_count:
        houses = int(houses_count.group(1))
        apartments = int(apartments_count.group(1))
        if houses > 0 and apartments > 0:
            return "Houses and Apartments"
        elif houses > 0:
            return "Houses"
        elif apartments > 0:
            return "Apartments"

    # If counts are not conclusive, use primary sector
    primary_sector_match = primary_sector_pattern.search(input_text)
    primary_sector = primary_sector_match.group(1).strip() if primary_sector_match else ""

    # Define unit types to search for in the primary sector
    unit_types = [
        "Apartments", "Houses", "Houses and Apartments", "Office", 
        "Apartments & Creche Facility", "Co Living", "Film Studio", 
        "Hotel", "Hotel - Aparthotel", "Industrial", "Life Sciences", 
        "Mixed use", "Retail", "Student Accommodation", "University"
    ]

    # Check for specific keywords in the primary sector
    for unit_type in unit_types:
        if unit_type.lower() in primary_sector.lower():
            return unit_type

    # Fallback to primary sector itself if no specific type is found
    return primary_sector

def extract_total_units(input_text):

    # Define the patterns for total residential units and hotel bedrooms
    total_units_pattern = re.compile(r'Total Res Units\s*[:\-]?\s*(\d+)', re.IGNORECASE)
    hotel_bedrooms_pattern = re.compile(r'Hotel Bedrooms\s*[:\-]?\s*(\d+)', re.IGNORECASE)
    
    # Search for total residential units
    total_units_match = total_units_pattern.search(input_text)
    if total_units_match:
        return total_units_match.group(1).strip()
    
    # Search for hotel bedrooms if total residential units not found
    hotel_bedrooms_match = hotel_bedrooms_pattern.search(input_text)
    if hotel_bedrooms_match:
        return hotel_bedrooms_match.group(1).strip()
    
    # Return N/A if neither pattern is found
    return "N/A(units)"



def extract_total_square_feet(input_text):
    # Search for total square meters using the provided format
    floor_area_pattern = re.compile(r'Floor Area\s*[:\-]?\s*(\d+\.?\d*)\s*m2', re.IGNORECASE)
    floor_area_match = floor_area_pattern.search(input_text)
    
    if floor_area_match:
        square_meters = float(floor_area_match.group(1).strip())
        # Convert to square feet
        square_feet = square_meters * 10.7639
        return f"{square_feet:.2f} sq ft"
    
    # Return N/A if square meters are not found
    return "N/A(sq ft)"

def main(input_text):
    title_of_deal = extract_title(input_text)
    area, location = extract_location(input_text)
    developer_name = extract_developer(input_text)
    unit_type = extract_unit_type(input_text)
    total_units = extract_total_units(input_text)
    total_square_feet = extract_total_square_feet(input_text)
    
    formatted_output = f"{developer_name}    {title_of_deal}    {area}    {location}    {unit_type}\t\t{total_units}\t{total_square_feet}"
    print(formatted_output)

input2 = '''
€33m - LRD Student Accommodation Development, Dublin 7
Stage Plans Granted

Updated 13/06/2024

Open with

Primary sector
Residential  Student Accommodation
Location
Former IDA Centre, Prussia Street, Dublin 7, Co. Dublin
CIS Researcher

Adam Dargan
Do you have questions or require further information on this project? Please contact me.
CIS Next review
Nov 2024
Description
On the 7th of June 2024 an appeal was lodged with An Bord Pleanala against Dublin City Council's decision to grant planning permission to Lyonshall Limited for a scheme comprises permission the proposed development will consist of the demolition of the existing 4 warehouse structures to provide for the construction of a 373 bedroom purpose-built student accommodation development, a ground floor cafe, and all ancillary site development works. The proposed development will be provided in 2 apartment blocks ranging in height from 3-5 storeys over basement and a single terrace of own door studio units, including 43 apartments ranging in size from 4-6 bedrooms (250 bedroom spaces), 123 studio apartments all served by bicycle parking in a dedicated bike store, bin store, plant rooms, outdoor amenity spaces and internal student amenity facilities, esb substation, rooftop mounted plant and photovoltic panels.

The primary access to the proposed development will be provided from prussia street to the east. The proposed development also provides for the alterations of section of the western boundary wall to provide for fencing and a gate to facilitate a maintenance access for dublin city council from drumalee court.
Key details
Value
€33.4m
(Estimated)
Project ID
1336925
Planning Stage
Plans Granted
CIS Next Review
Nov 2024
Floor Area
11,659.9 m2
Funding Type
Private
Construction Type
New Build
Planning Information
Authority
Dublin City Council
Planning Reference
LRD6050/24-S3
Decision Date
09 May 2024
Application Date
15 Mar 2024
SiteArea
0.58 ha
Appeal status
Is Under Appeal
Links and Files
Documents
Appeal Url
Documents
Planning documents
Additional Information
One Bed Apartments
123
Four Bed Apartments
3
Five and greater bed apartments
40
Total Apartments
166
Student Bed spaces
448
Storeys
5
Requires Demolition
Y
Total Res Units
166
Structures
2
CompaniesMaterialsTrackingHistory
Promoter
Lyonshall Limited
ContactKieran Coughlan

CountyCo. Cork

Architect
O'Mahony Pike Architects
Emailinfo@omp.ie

ContactSolene Vermount

Phone+353214272775

CountyCo. Cork

LinkedIn

 Website
Planning Consultant
HW Planning
Emailinfo@hwplanning.ie

ContactHarry Walsh

Phone+353214873250

CountyCo. Cork

LinkedIn

 Website
Consulting Engineer
MHL & Associates Limited
Emailinfo@mhl.ie

ContactKen Manley

Contact Emailkmanley@mhl.ie

Phone+353214840214

CountyCo. Cork

LinkedIn

 Website
Consulting Engineer
Horgan Lynch & Partners
Emailcork@horganlynch.ie

ContactNiall Fitzgerald

Contact Emailniall.fitzgerald@horganlynch.ie

Phone+353214936100

CountyCo. Cork

LinkedIn


'''

main(input2)


# total res units or hotel bedrooms
