import re

# Define patterns for extraction
title_pattern = re.compile(r'(€.*?)-(.*?)(?:Stage|Updated|Open)', re.DOTALL)
location_pattern = re.compile(r'Location\s+(.*?)(?:\nLinked|CIS Researcher)', re.DOTALL)
developer_pattern = re.compile(r'Promoter\s*([\s\S]*?)(?:\s*Contact|\s*Email|\s*Phone|\s*LinkedIn)', re.IGNORECASE)
total_units_pattern = re.compile(r'Total Res Units\s*[:\-]?\s*(\d+)', re.IGNORECASE)
hotel_bedrooms_pattern = re.compile(r'Hotel Bedrooms\s*[:\-]?\s*(\d+)', re.IGNORECASE)
square_meters_pattern = re.compile(r'Floor\s*Area\s*[:\-]?\s*(\d[\d,]*\.?\d*)\s*m2', re.IGNORECASE)
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

# Paste your extract functions here

def extract_title(input_text):
    title_match = title_pattern.search(input_text)
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
    developer_match = developer_pattern.search(input_text)
    return developer_match.group(1).strip() if developer_match else "Developer name not found."

def extract_unit_type(input_text):
    primary_sector_pattern = re.compile(r'Primary sector\s*([\w\s]+)')
    houses_pattern = re.compile(r'Total Houses\s*(\d+)')
    apartments_pattern = re.compile(r'Total Apartments\s*(\d+)')

    houses_count = houses_pattern.search(input_text)
    apartments_count = apartments_pattern.search(input_text)

    if houses_count and apartments_count:
        houses = int(houses_count.group(1))
        apartments = int(apartments_count.group(1))
        if houses > 0 and apartments > 0:
            return "Houses and Apartments"
        elif houses > 0:
            return "Houses"
        elif apartments > 0:
            return "Apartments"

    primary_sector_match = primary_sector_pattern.search(input_text)
    primary_sector = primary_sector_match.group(1).strip() if primary_sector_match else ""

    unit_types = [
        "Apartments", "Houses", "Houses and Apartments", "Office", 
        "Apartments & Creche Facility", "Co Living", "Film Studio", 
        "Hotel", "Hotel - Aparthotel", "Industrial", "Life Sciences", 
        "Mixed use", "Retail", "Student Accommodation", "University"
    ]

    for unit_type in unit_types:
        if unit_type.lower() in primary_sector.lower():
            return unit_type

    return primary_sector

def extract_total_units(input_text):
    total_units_match = total_units_pattern.search(input_text)
    if total_units_match:
        return total_units_match.group(1).strip()
    
    hotel_bedrooms_match = hotel_bedrooms_pattern.search(input_text)
    if hotel_bedrooms_match:
        return hotel_bedrooms_match.group(1).strip()
    
    return "N/A(units)"

def extract_total_square_feet(input_text):
    floor_area_match = square_meters_pattern.search(input_text)
    if floor_area_match:
        square_meters = float(floor_area_match.group(1).strip().replace(',', ''))
        square_feet = round(square_meters * 10.7639)
        return f"{square_feet}"
    
    return "N/A"

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
    }

    return stage_mapping.get(stage, stage)

def main(input_text):
    deals = input_text.split("""Search for projects by keyword or project ID
AnyAllExact
DashboardProject SearchCompany SearchTrackingExport
DL""")
    results = []

    # Skip the first split part if it's empty (text before the first "€ - ")
    for deal in deals[1:]:
        #deal = "€ - " + deal  # Add back the split part to each deal
        if deal.strip():
            title_of_deal = extract_title(deal)
            area, location = extract_location(deal)
            developer_name = extract_developer(deal)
            unit_type = extract_unit_type(deal)
            total_units = extract_total_units(deal)
            total_square_feet = extract_total_square_feet(deal)
            square_feet_per_unit = extract_square_feet_per_unit(deal)
            stage = extract_stage(deal)
            
            result = [
                developer_name, title_of_deal, area, location, unit_type,
                '', total_units, '', total_square_feet, square_feet_per_unit, '\t\t\t\t\t\t', stage
            ]
            results.append(result)

    # Print each result row
    for result in results:
        print("\t".join(map(str, result)))

# Multiline input handling
print("Please enter the input text (end with 'END' on a new line):")

input_lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    input_lines.append(line)

input_text = "\n".join(input_lines)

main(input_text)

