import re

# Define the regular expression patterns
title_pattern = re.compile(r'€\d+.*?-(.*?)(?:Stage|Updated|Open)', re.DOTALL)
location_pattern = re.compile(r'Location\s+(.*?)(?:\nLinked|CIS Researcher)', re.DOTALL)
developer_pattern = re.compile(r'Promoter\s*([\w\s]+)\s*Email', re.IGNORECASE)
total_units_pattern = re.compile(r'Total Res Units\s*[:\-]?\s*(\d+)', re.IGNORECASE)
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
    return title_match.group(1).strip() if title_match else "Title of the deal not found."

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
    primary_sector_pattern = re.compile(r'Primary sector\s*([\w\s]+)')
    primary_sector_match = primary_sector_pattern.search(input_text)
    primary_sector = primary_sector_match.group(1).strip() if primary_sector_match else ""

    houses_pattern = re.compile(r'Total Houses\s*(\d+)')
    apartments_pattern = re.compile(r'Total Apartments\s*(\d+)')

    houses_count = houses_pattern.search(input_text)
    apartments_count = apartments_pattern.search(input_text)

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
        if "Apartment" in primary_sector:
            unit_type = "Apartments"
        elif "House" in primary_sector:
            unit_type = "Houses"
        else:
            unit_type = primary_sector

    return unit_type

def extract_total_units(input_text):
    total_units_match = total_units_pattern.search(input_text)
    return total_units_match.group(1).strip() if total_units_match else "N/A(units)"

def main(input_text):
    title_of_deal = extract_title(input_text)
    area, location = extract_location(input_text)
    developer_name = extract_developer(input_text)
    unit_type = extract_unit_type(input_text)
    total_units = extract_total_units(input_text)
    
    formatted_output = f"{developer_name}    {title_of_deal}    {area}    {location}    {unit_type}    {total_units}"
    print(formatted_output)

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

main(input2)
