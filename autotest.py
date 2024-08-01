import re

# Define the pattern for developer extraction
developer_pattern = re.compile(r'Promoter\s*([\s\S]*?)(?:\s*Contact|\s*Email|\s*Phone|\s*LinkedIn)', re.IGNORECASE)

def extract_developer(input_text):
    developer_match = developer_pattern.search(input_text)
    return developer_match.group(1).strip() if developer_match else "Developer name not found."


# Test input text
test_input_text = """

Search for projects by keyword or project ID
AnyAllExact
DashboardProject SearchCompany SearchTrackingExport
DL
€15m - Residential Development
Stage Tender

Updated 01/08/2024

Open with

Primary sector
Residential  Housing Developments
Location
Oldtown Mill Road, Celbridge, Co. Kildare
CIS Researcher

Adam Dargan
Do you have questions or require further information on this project? Please contact me.
CIS Next review
Aug 2024
Description
1st August 2024: Tenders are currently being sought from contractors for this development as part of the €270 million Social Housing PPP - Bundle 4.Construction work is expected to commence in Q3/Q4 2025.

PROCUREMENT TYPE:
Works

TIME-LIMIT FOR RECEIPT OF TENDERS OR REQUESTS TO PARTICIPATE:
10/09/2024 12:00

END OF CLARIFICATION PERIOD:
27/08/2024 12:00

TENDERS OPENING DATE:
11/09/2024 00:00

CONTRACT DURATION IN MONTHS OR YEARS, INCLUDING ANY OPTIONS AND RENEWALS:
27 years


25/03/2024: A part 8 planning application was submitted by Kildare County Council on 21/03/2024 for this project.

The proposed development includes:

60 no. residential units including 40 no. houses and 20 no. apartments comprising 20 no. one bed units; 15 no. two bed units; 21 no. three bed units; and 4 no. four bed units; with renewable energy design measures (which may be provided externally) for each housing unit.Rear garden sheds serving the residential units;

Landscaping works including provision of (a) open space and kick about areas; (b) natural play features; and (c) new pedestrian and cycle connections;
Associated site and infrastructural works including provision for (a) 2 no. ESB substations and switchrooms; (b) car and bicycle parking; (d) public lighting; (e) bin storage; (f) temporary construction signage; (g) estate signage; and (h) varied site boundary treatment comprising walls and fencing; and
all associated site development works, including removal of existing spoil from the site in advance of construction works.


Key details
Value
€15m
(Estimated)
Project ID
1337365
Planning Stage
Plans Submitted
Contract Stage
Tender
CIS Next Review
Aug 2024
Funding Type
PPP
Construction Type
New Build
Schedule of Works
Start Date
04 Aug 2025
Planning Information
Authority
Kildare County Council
Planning Reference
Part 8 - 1337365
Application Date
21 Mar 2024
Tender Information
Tender Deadline
10/09/2024 12:00
Is part of framework?
N
Links and Files
Documents
Part 8 Planning Application
Documents
Tender Documents
Documents
TED Europa
Additional Information
Two Bed Houses
15
Three Bed Houses
21
Four Plus Bed Houses
4
Total Houses
40
One Bed Apartments
20
Total Apartments
20
Total Res Units
60
CompaniesTrackingHistory
Promoter
Kildare County Council
Emailcustomercare@kildarecoco.ie

Phone+35345980200

CountyCo. Kildare

LinkedIn

 Website
Co-Promoter
National Development Finance Agency
Emailinfo@ndfa.ie

ContactLaura McElduff

Contact EmailLaura.McElduff@ntma.ie

Phone+35312384000

CountyDublin 1

LinkedIn

 Website
Architect
Sean Harrington Architects
Emailinfo@sha.ie

Phone+35318733422

CountyDublin 1

 Website
Architect
McCrossan O'Rourke Manning Architects
Emailarch@mcorm.com

Phone+35314788700

CountyDublin 8

LinkedIn

 Website
Architect
Coady Partnership Architects
Emailadmin@coady.ie

ContactStephan Carter

Phone+35314976766

CountyDublin 6

LinkedIn

 Website
Project Manager
Turner & Townsend
Emaildublin@turntown.com

Phone+35314003300

CountyDublin 2

LinkedIn

 Website
Planning Consultant
HRA Planning Chartered Town Planning Consultants
Emailinfo@hraplanning.ie

ContactMary Hughes

Phone+35387 6443389

CountyDublin 7

 Website
Planning Consultant
MacCabe Durney Barnes
Emailplanning@mdb.ie

ContactRichard Hamilton

Phone+35316762594

CountyDublin 2

LinkedIn

 Website
Quantity Surveyor
Currie & Brown
Emailenquires@curriebrown.com

Phone+35312843300

CountyDublin 8

 Website
Mech & Elec Engineer
Semple and McKillop
Emailinfo@semplemckillop.com

Phone+353429749570

CountyCo. Monaghan

LinkedIn

 Website
Site Investigation Consultant
IGSL Limited
Emailinfo@igsl.ie

Phone+35345846176

CountyCo. Kildare

LinkedIn

 Website
Civil & Structural Engineer
Malone O'Regan Consulting Engineers
Emaildublin@morce.ie

ContactDouglas Weir

Contact Emaildweir@morce.ie

Phone+35312602655

CountyDublin 14

LinkedIn

 Website
Mapbox
Map
Satellite
+
−
Draw a polyline
Draw a rectangle
Draw a circle
Leaflet | © Mapbox © OpenStreetMap
Hey,
How may I help you today ?


"""

# Run the test
print(extract_developer(test_input_text))  # Expected
