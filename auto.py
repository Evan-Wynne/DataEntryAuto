import re
####finding the approx total unit number#####
input2 ='''€75m - Ballymany SHD Development, Newbridge
Stage On Site

Updated 31/07/2024

Open with

Primary sector
Residential  Housing Developments
Location
Ballymany, Newbridge W12 YR65, Co. Kildare
CIS Researcher

Adam Dargan
Do you have questions or require further information on this project? Please contact me.
CIS Next review
Research Complete
Description
31/07/2024: Works are expected to commence imminently on site on the construction of apartment block (Du1), 07A&B, 08A&B, 09A&B, and 10A&B Stables Green, Curragh Farm, Ballymany, Newbridge, Co. Kildare, with all associated site works.

24th July 2024: Work is expected to commence imminently on the construction of apartment block (Du1), 17A&B, 18A&B, 19A&B, and 20A&B Stables Green, Curragh Farm, Ballymany, Newbridge, Co. Kildare, with all associated site works.

03/07/2024: Works are expected to commence imminently on site on the construction of phase 2 at Curragh Farm, Ballymany, Newbridge, Co. Kildare, including all associated site works.

01/05/2024: Works are expected to commence imminently on site on the construction of apartment block (Du1), 25A&B, 26A&B, 27A&B , 28A&B, 29A&B, 30A&B, 31A&B, and 32A&B at Roan Gates, Curragh Farm, Ballymany, Newbridge, Co. Kildare, with all associated site works.

03/01/2024: Works are expected to commence imminently on site on the construction of Phase 2 (Houses No.9-47) Beechtree Place, Phase 2 (Houses No.11-16) Stables Green & Phase 1 (Houses 33-36) Roan Gates at Curragh Farm, Ballymany, Newbridge, Co. Kildare under planning permission number APB-312704-22, along with all associated site works.

06/12/2023: Works are expected to commence imminently on site on the construction of three 2 storey, own door apartment buildings, Type Du3 with 4 No. units 64A to 65B, 4 No. units 66A to 67B and 4 No. units 68A to 69B at Rosetree Green at Curragh Farm, under planning permission number APB-312704-22.

10/11/2023: We understand that the mechanical and electrical subcontractors have been appointed.

08/11/2023: We understand that works are underway on the construction of Phase 1 (House No.56-73) Beechtree Place and Phase 1 (House No.21-30) Stables Green at Curragh Farm, Ballymany, Newbridge, Co. Kildare under planning permission number APB-312704-22, along with all associated site works.

12/04/2023: Works are expected to commence imminently on site on the construction of 16 No 1 Own Door Apartment units 30A to 37B Rosetree Green, Curragh Farm, in a 2 storey building and all associated siteworks at Ballymany, Newbridge, Co. Kildare under planning permission number ABP-312704-22

21/03/2023: We understand that works are underway to complete phase 1 of 40 residential dwellings at Rosetree Green SHD, Ballymany, Newbridge, Co. Kildare under planning permission number ABP-312704-22

15th September 2022: This project has been approved planning.

Briargate Developments Newbridge Limited have lodged a Strategic Housing Development with An Bord Pleanála for the following development:

The application site is bounded to the north by Standhouse Road and the rear of dwellings fronting that road; to the south by Ballymany Road (R445); to the east by the gardens of houses in the Elms housing development and a playing field’ and to the west by agricultural fields of Ballymany Studfarm.

The development will consist of future phases of a residential development of which Phase 1 (54 no. units and Link Road) is currently under construction on foot of planning Ref. 16/658 (ABP REF. PL09.249038), which provided for 280 dwelling units, creche, nursing home and Link Road. The overall development will provide 390 no. units and creche on completion.

In summary the proposed development will consist of the following:-

Construction of 336 no. residential units consisting of 245 no. houses, 27 no. apartments and 64 no. duplexes;
The apartments are located in a part 3-storey and part 4-storey building and the duplexes are located across 6 no. 2 to 3-storey buildings;
A 2-storey creche;
Car parking, bicycle parking, internal roads, services infrastructure, bin stores and bicycle stores;
Landscaping, open spaces, play areas, boundary treatment and public lighting;
Footpath improvements along Standhouse Road and all associated site works and services.
Key details
Value
€75.8m
(Estimated)
Project ID
1214061
Planning Stage
Plans Granted
Contract Stage
On Site
CIS Next Review
Research Complete
Floor Area
34,799.95 m2
Funding Type
Private
Construction Type
New Build
Schedule of Works
Start Date
21 Mar 2023
Finish Date
13 Mar 2028
Duration
60 months
Planning Information
Authority
Kildare County Council
Planning Reference
ABPREF312704
Decision Date
06 Sep 2022
Application Date
11 Feb 2022
SiteArea
11.4 ha
Links and Files
Documents
An Bord Pleanala
Documents
Planning Documents
Additional Information
Units Commenced
217
Units Complete
29
Two Bed Houses
17
Three Bed Houses
184
Four Plus Bed Houses
44
Total Houses
245
One Bed Apartments
45
Two Bed Apartments
29
Three Bed Apartments
17
Total Apartments
91
Storeys
4
Postcode
W12 YR65
Total Res Units
336
CompaniesMaterialsTrackingHistory
Promoter
Briargate Developments
Emailinfo@anthonyneville.ie

Phone+353539142386

CountyCo. Wexford

 Website
Promoter
Anthony Neville Homes
Emailinfo@anthonyneville.ie

Phone+353539142386

CountyCo. Wexford

 Website
Architect
Reddy Architecture and Urbanism
Emaildublin@reddyarchitecture.com

ContactMark Kennedy

Contact Emailmkennedy@reddyarchitecture.com

Phone+35314987000

CountyDublin 6

LinkedIn

'''

# Regex to find "Total Res Units" followed by a number
total_units_pattern = re.compile(r'Total Res Units\s*(\d+)', re.IGNORECASE)

# Search for the pattern in the input text
total_units_match = total_units_pattern.search(input2)

# Output the result
if total_units_match:
    total_units = 0
    total_units = int(total_units_match.group(1))
    print(f"Total Number of Units: {total_units}")
else:
    print("Total number of units not found.")