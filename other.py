import re

# Define the regular expression patterns
title_pattern = re.compile(r'€.*?-(.*?)\s*Stage', re.DOTALL)
location_pattern = re.compile(r'Location\s+(.*?)(?:\nLinked|CIS Researcher)', re.DOTALL)
developer_pattern = re.compile(r'Promoter\s*(.*?)(?:\s*Contact|\s*Email|\s*County)', re.IGNORECASE | re.DOTALL)
total_units_pattern = re.compile(r'Total Res Units\s*[:\-]?\s*(\d+)', re.IGNORECASE)
hotel_bedrooms_pattern = re.compile(r'Hotel Bedrooms\s*[:\-]?\s*(\d+)', re.IGNORECASE)
floor_area_pattern = re.compile(r'Floor Area\s*[:\-]?\s*(\d+\.?\d*)\s*m2', re.IGNORECASE)
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
    title_match = title_pattern.search(input_text)
    return title_match.group(0).strip() if title_match else "Title of the deal not found."

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
    
    formatted_output = f"{developer_name}    {title_of_deal}    {area}    {location}    {unit_type}    {total_units}    {total_square_feet}"
    print(formatted_output)

input2 = '''
€12.7m - Hotel/Restaurant/Office Development, Dublin 2
Stage Plans Granted

Updated 03/07/2024

Open with

Primary sector
Hospitality  Hotels
Location
5, 6 & 7 George's Quay & 1A, 1, 3, 5, 7, 9, 11, 13 and 15 Tara Street, & No. 11 Poolbeg Street, Dublin 2 D02 Y662, Co. Dublin
Linked projects
€18.4m - Hotel/Office/Restaurant Development
CIS Researcher

Clare Lennon
Do you have questions or require further information on this project? Please contact me.
CIS Next review
Dec 2024
Description
3rd July 2024: It should be noted that this planning approval expires in December 2024.

A decision to grant planning permission was issued by Dublin City Council on 16/09/2019 to Greybirch Limited for the proposed development consisting of the demolition of existing structures at the following addresses: Nos. 5, 6 & 7 George's Quay, Nos. 1a, 1, 3, 5, 7, 9, 11. 13 and 15 Tara Street and No. 11 Poolbeg Street and the construction of a mixed-use development ranging in height from three to eight storeys, including rooftop plant.

The total gross floor area above ground on this building will be circa 4740 square metres and the gross floor area including basement is 5,284 square metres. the site area is 0.799 ha. The ground floor includes a hotel reception/bar/restaurant totalling 150 square metres, a co-working reception and cafe totalling 163 square metres and a cafe/restaurant/retail unit totalling 74 square metres.

The first floor comprises a co-working office space with circa 490 square metres of nett office space. The second to seventh floor levels inclusive comprise of hotel use with a total of 116 hotel bedrooms. A breakfast room/bar associated with the hotel is located on the sixth floor opening onto a roof terrace.

Three private roof terraces will be provided to hotel bedrooms: one located at fourth floor to the north elevation and two to the south elevation located at third and sixth floors. one basement level, floor area 540 square metres provides ancillary uses to the hotel and retail uses of the building, including plant, bicycle storage, staff amenities and a commercial kitchen. the gross floor area including basement is 5,284 square metres.

The proposed development also includes for provision of hotel/retail/cafe/restaurant signage, associated site servicing (foul and surface water drainage, water supply and electricity supply), and all other associated site excavation and site development works above
'''

main(input2)
