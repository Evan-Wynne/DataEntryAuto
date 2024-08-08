import re
# Define patterns for extraction
title_pattern = re.compile(r'€.*?-(.*?)(?:Stage|Updated|Open)', re.DOTALL)
location_pattern = re.compile(r'Location\s+(.*?)(?:\nLinked|CIS Researcher)', re.DOTALL)
developer_pattern = re.compile(r'Promoter\s*(.*?)(?:\s*Contact|\s*Email|\s*County)', re.IGNORECASE | re.DOTALL)
total_units_pattern = re.compile(r'Total Res Units\s*[:\-]?\s*(\d+)', re.IGNORECASE)
hotel_bedrooms_pattern = re.compile(r'Hotel Bedrooms\s*[:\-]?\s*(\d+)', re.IGNORECASE)
square_meters_pattern = re.compile(r'Floor Area\s*[:\-]?\s*(\d+\.?\d*)\s*m2', re.IGNORECASE)
stage_pattern = re.compile(r'Stage\s*(.*?)\n', re.IGNORECASE)
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
    # Define the pattern to capture floor area in square meters
    floor_area_pattern = re.compile(r'Floor\s*Area\s*[:\-]?\s*(\d[\d,]*\.?\d*)\s*m2', re.IGNORECASE)
    
    # Search for total square meters
    floor_area_match = floor_area_pattern.search(input_text)
    if floor_area_match:
        square_meters = float(floor_area_match.group(1).strip().replace(',', ''))
        # Convert to square feet
        square_feet = round(square_meters * 10.7639)
        return f"{square_feet}"
    
    # Return N/A if square meters are not found
    return "N/A(sq ft)"

def extract_square_feet_per_unit(input_text):
    total_square_feet = extract_total_square_feet(input_text)
    total_units = extract_total_units(input_text)
    
    if total_square_feet != "N/A" and total_units != "N/A(units)":
        total_square_feet = int(total_square_feet)
        total_units = int(total_units)
        square_feet_per_unit = round(total_square_feet / total_units)
        return square_feet_per_unit
    return "N/A"

def extract_stage(input_text):
    stage_match = stage_pattern.search(input_text)
    if not stage_match:
        return "Stage not found"

    stage = stage_match.group(1).strip()

    stage_mapping = {
        "Plans Granted": "Planning Approved",
        "Plans Withdrawn": "Withdrawn",
        "Tender": "Tender",
        "Plans Submitted": "Seeking Planning Approval",
        # Add other mappings as needed
    }

    return stage_mapping.get(stage, stage)

def main(input_text):
    title_of_deal = extract_title(input_text)
    area, location = extract_location(input_text)
    developer_name = extract_developer(input_text)
    unit_type = extract_unit_type(input_text)
    total_units = extract_total_units(input_text)
    total_square_feet = extract_total_square_feet(input_text)
    square_feet_per_unit = extract_square_feet_per_unit(input_text)
    stage = extract_stage(input_text)
    
    formatted_output = f"{developer_name}\t{title_of_deal}\t{area}\t{location}\t{unit_type}\t\t{total_units}\t\t{total_square_feet}\t{square_feet_per_unit}\t\t\t\t\t\t\t\t{stage}"
    print(formatted_output)

input2 = '''
€11m - The July ApartHotel Development, Dublin 7
Stage Plans Granted

Updated 30/07/2024

Open with

Primary sector
Hospitality  Hotels
Location
162-164a (inclusive) Capel Street and 33-36 (inclusive) Strand Street Little, Dublin 7 D07 F861, Co. Dublin
CIS Researcher

Clare Lennon
Do you have questions or require further information on this project? Please contact me.
CIS Next review
Sep 2024
Description
30th July 2024: According to reports An Bord Pleanála has granted planning permission for an eight-storey hotel on Dublin’s Capel Street, undercutting Dublin City Council’s de facto ban on the construction of new hotels in parts of the city. In January 2023, The July group, a Dutch hospitality company, was told by Dublin City Council it cannot build a 105-bedroom hotel on a derelict site on Capel Street. The company appealed the decision and the local council’s initial ruling has now been overturned by An Bord Pleanála. (Source: Business Post).

Originally a decision to refuse planning permission was issued by Dublin City Council on 10/05/2023 to City ID for this project. The modification application lodged in April 2023 by City ID Capel Limited was also refused planning permission by Dublin City Council. The successful appeal was lodged in June 2023 - Appeal Reference: ABP-317264-23.

Demolition works have already taken place on the site at 33-36 Strand Street Little (Working Men's Club) and buildings to the rear of the shop at 162 Capel Street, Dublin 7 to allow for over construction of this project.
     
This site was sold in 2022 to City ID, the Dutch hospitality group. They scaled back the planned 142-bedroom hotel to create a 105-unit aparthotel instead with each featuring fully equipped kitchens and living spaces. The group plans a €1 billion investment over the next 5 years to grow its international platform of aparthotels across major European cities.

Proposed modifications to facilitate the 105-suite aparthotel include the following:

Basement: internal reconfigurations at permitted basement level to provide revised plant areas and spa/wellness area.

Ground Floor: alterations to the rear of the ground floor of No. 162 Capel Street, providing access to the aparthotel and an enclosed events space in this location; relocation of bicycle parking from basement level to ground floor with access to same from the laneway located on Strand Street Little; general layout modifications to the reception/restaurant/bar area.

Upper Floors: internal reconfigurations from first to eight floor to facilitate 105 No. aparthotel suites and ancillary services areas; build out of setback at fifth to eight floors levels on western elevation (rear of Capel Street) and northern elevation (rear of Strand Street Little); part build out of set back at fifth and sixth floor levels on eastern elevation; inclusion of private glazed balconies on the southern side at seventh floor level; amendments to facade at street level, including the provision of retractable awnings on both the Capel Street and Strand Street Little frontages; amendments to fenestration at all levels; all associated amendments to plant, site works and services.

Previous Plans: On the 6th of September 2021 An Bord Pleanala overturned Dublin City Council’s decision to refuse planning permission to Ringline Investments Limited for the hotel project. (An Bord Pleanala Ref. 309215). The project was to include the demolition of building and redevelopment of partly vacant site for a hotel with ancillary bar/cafe lobby fronting Capel Street/Strand Street Little junction and shop in 162 Capel Street. (Plan Ref: 3609/20) The new plans were then submitted by City ID Capel Limited: Permission for modifications to planning permission granted for a 5-9 storey 142 No. bedroom hotel under ref. 3609/20 (abp-309215-21) to facilitate its reconfiguration as a 105-suite aparthotel.
Key details
Value
€10.9m
(Estimated)
Project ID
1130190
Planning Stage
Plans Granted
CIS Next Review
Sep 2024
Floor Area
5,215 m2
Funding Type
Private
Construction Type
New Build
Schedule of Works
Duration
24 months
Planning Information
Authority
Dublin City Council
Planning Reference
5526/22
Decision Date
10 May 2023
Application Date
22 Dec 2022
SiteArea
0.08 ha
Appeal status
Approved After Appeal
Links and Files
Documents
Appeal Url
Documents
Planning documents
Additional Information
Hotel Bedrooms
105
Storeys
8
Requires Demolition
Y
Postcode
D07 F861
CompaniesMaterialsTrackingHistory
Promoter
City ID
Emailinfo@cityidgroup.com

ContactArieke Bollemeijer

Phone+310207239090

 Website
Architect
C+W O’Brien Architects
Emailinfo@cwoarchitects.ie

ContactArthur O'Brien

Contact Emailaobrien@cwoarchitects.ie

Phone+35315180170

CountyDublin 7

LinkedIn

 Website
Planning Consultant
Simon Clear and Associates
Emailadmin@clearconsult.ie

ContactPaula Shannon

Contact Emailpaula@clearconsult.ie

Phone+35314569084

CountyDublin 12

 Website
Consulting Engineer
CORA Consulting Engineers
Emailinfo@cora.ie

ContactJohn Casey

Contact Emailjohn.casey@cora.ie

Phone+35316611100

CountyDublin 2

LinkedIn

 Website
Demolition Contractor
Breffni Group
Emailinfo@breffnigroup.ie

ContactRory Flynn

Phone+35318644586

CountyCo. Dublin

'''


main(input2)


