import requests
from bs4 import BeautifulSoup
import time
from tabulate import tabulate

calendarIDList = [['Abingdon - 25552 Lee Highway', '3871993'],
					['Alexandria - 2681 Mill Road', '4024318'],
					['Altavista - 1301 H Main Street', '4190296'],
					['Arlington - 4150 South Four Mile Run Drive', '3871953'],
					['Arlington Metro at Va. Square - 3434 North Washington Blvd. Suite RET01', '4190501'],
					['Bedford - 1128 E. Lynchburg Salem Turnpike', '4315680'],
					['Charlottesville -  2055 Abbey Road', '3886298'],
					['Chesapeake - 813 Greenbrier Parkway', '3886173'],
					['Chester - 12100 Branders Creek Drive', '3886199'],
					['Chesterfield - 610 Johnston Willis Drive', '3875784'],
					['Christiansburg - 385 Arbor Drive', '3886276'],
					['Clintwood - 2311 Dickenson Hwy.', '4190420'],
					['Courtland - 27426 Southampton Parkway', '4344200'],
					['Covington - 121 Mall Road', '4176686'],
					['Culpeper - 18505 Crossroad Parkway', '4190315'],
					['Danville - 126 Sandy Court, Suite C', '4151244'],
					['East Henrico - 5517 South Laburnum Avenue', '4190288'],
					['Emporia - 103 Commonwealth Blvd', '3886241'],
					['Fairfax/Westfields - 14950 Northridge Drive', '3885876'],
					['Fair Oaks Mall - 11805 Fair Oaks Mall', '4371737'],
					['Farmville - 300 North Virginia Street', '4024334'],
					['Franconia - 6306 Grovedale Drive', '3874886'],
					['Fredericksburg -  5700 Southpoint Centre Blvd', '3885990'],
					['Front Royal - 15 Water Street', '4023722'],
					['Galax - 7565 Carrollton Pike', '3885835'],
					['Gate City - 382 Jones Street, Suite 101', '4085803'],
					['Gloucester - 2348 York Crossing Drive', '3886055'],
					['Hampton - 8109 Roanoke Avenue', '3875096'],
					['Harrisonburg - 3281 Peoples Drive', '3875897'],
					['Hopewell - 4401 Crossings Boulevard', '4344252'],
					['Jonesville - 195 Hill Street', '4188697'],
					['Kilmarnock - 110 DMV Drive', '4315629'],
					['Lebanon - 567 W. Main Street', '4151211'],
					['Leesburg - 945 Edwards Ferry Road NE', '3885966'],
					['Lexington - 110 East Midland Trail', '4984822'],
					['Lorton - 7714 Gunston Plaza', '4315650'],
					['Lynchburg - 3236 Odd Fellows Road', '3963680'],
					['Marion - 1595 North Main Street', '4344203'],
					['Martinsville - 310 Starling Avenue', '4023812'],
					['Newport News - 12730 Patrick Henry Drive', '3886129'],
					['Norfolk/Military Circle - 5745 Poplar Hall Drive', '4023785'],
					['Norfolk/Widgeon Road - 850 Widgeon Road', '4254699'],
					['North Henrico - 9015 Brook Road', '3886217'],
					['Norton - 1729 Park Avenue S.W.', '4151218'],
					['Onancock - 20 North Street', '3875561'],
					['Petersburg - 120 Wagner Road', '4190459'],
					['Portsmouth -  6400 Bickford Parkway', '3919684'],
					['Prince William/Manassas - 11270 Bulloch Drive', '3874953'],
					['Pulaski - 1901 Bobwhite Boulevard', '4315660'],
					['Richmond Central - 2300 West Broad Street', '3871818'],
					['Roanoke - 5220 Valleypark Drive', '3875811'],
					['Rocky Mount  - 305 Tanyard Road', '4254370'],
					['South Boston -  2039 Hamilton Blvd', '3920204'],
					['South Hill - 206 South Brunswick Avenue', '4190383'],
					['Stafford - 874 Garrisonville Road', '4371766'],
					['Staunton - 17 First Street', '4344176'],
					['Sterling - 100 Free Court Sterling', '4307300'],
					['Sterling - S. Sterling Boulevard, Unit D112 (NEW LOCATION)', '4888651'],
					['Suffolk - 1040 Centerbrooke Lane', '4254598'],
					['Tappahannock - 750 Richmond Beach Road', '4176704'],
					['Tazewell - 1151 Tazewell Avenue', '3963753'],
					['Tysons Corner - 1968 Gallows Road', '3874778'],
					['VA Beach-Buckner - 3551 Buckner Boulevard', '3875662'],
					['VA Beach-Hilltop - 1712 Donna Drive', '4254734'],
					['Vansant - 1657 Lovers Gap Road', '4176713'],
					['Warrenton - 94 Alexandria Pike', '4254581'],
					['Waynesboro - 998 Hopeman Parkway', '4024300'],
					['West Henrico - 9237 Quioccasin Road', '4315911'],
					['Williamsburg - 5235 John Tyler Highway', '4254652'],
					['Winchester - 4050 Valley Pike', '4254611'],
					['Woodbridge - 2731 Caton Hill Road', '3886018'],
					['Woodstock - 714-A North Main Street', '4023845'],
					['Wytheville - 800 East Main Street, Suite 100', '4024345']]

def postRequest(calendarID):
	payload = {'type': '14002959', 'calendar': calendarID, 'skip': 'true', 'options[qty]': '1', 'options[numDays]': '5'}
	r = requests.post('https://vadmvappointments.as.me/schedule.php?action=showCalendar&fulldate=1&owner=19444409&template=monthly', data=payload)
	return r

def main():
	locationDates = []
	totalTime = 0
	for i in range(len(calendarIDList)):
		locationDates.append([calendarIDList[i][0]])
		start = time.time()
		req = postRequest(calendarIDList[i][1])
		end = time.time()
		totalTime += end - start
		print(calendarIDList[i][0].split('-')[0] + " - " + str(req.status_code))
		soup = BeautifulSoup(req.content, 'html.parser')
		openMonth = soup.find('option', {'selected': 'selected'}).text.split()[0]
		openYear = soup.find('option', {'selected': 'selected'}).text.split()[1]
		openDays = soup.findAll('td', {'class': 'scheduleday activeday'})
		
		if openDays:
			dateStr = ""
			for day in openDays:
				dateStr += openMonth + " " + day.text + " " + openYear + "\n"
			locationDates[i].append(dateStr.rstrip())

	print("\n")
	print(tabulate(locationDates, headers=['Location', 'Date(s)'], tablefmt='presto'))
	print("Average time per request: " + str(totalTime / len(calendarIDList)) + " seconds\n\n")

main()




