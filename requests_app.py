import requests
from bs4 import BeautifulSoup
import time
from tabulate import tabulate

calendarIDList = [['Alexandria - 2681 Mill Road', '4024318'],
					['Arlington - 4150 South Four Mile Run Drive', '3871953'],
					['Arlington Metro at Va. Square - 3434 North Washington Blvd. Suite RET01', '4190501'],
					['Culpeper - 18505 Crossroad Parkway', '4190315'],
					['East Henrico - 5517 South Laburnum Avenue', '4190288'],
					['Fairfax/Westfields - 14950 Northridge Drive', '3885876'],
					['Fair Oaks Mall - 11805 Fair Oaks Mall', '4371737'],
					['Franconia - 6306 Grovedale Drive', '3874886'],
					['Fredericksburg -  5700 Southpoint Centre Blvd', '3885990'],
					['Front Royal - 15 Water Street', '4023722'],
					['Leesburg - 945 Edwards Ferry Road NE', '3885966'],
					['Lorton - 7714 Gunston Plaza', '4315650'],
					['Prince William/Manassas - 11270 Bulloch Drive', '3874953'],
					['Richmond Central - 2300 West Broad Street', '3871818'],
					['Stafford - 874 Garrisonville Road', '4371766'],
					['Sterling - 100 Free Court Sterling', '4307300'],
					['Sterling - S. Sterling Boulevard, Unit D112 (NEW LOCATION)', '4888651'],
					['Tappahannock - 750 Richmond Beach Road', '4176704'],
					['Tysons Corner - 1968 Gallows Road', '3874778'],
					['Warrenton - 94 Alexandria Pike', '4254581'],
					['West Henrico - 9237 Quioccasin Road', '4315911'],
					['Winchester - 4050 Valley Pike', '4254611'],
					['Woodbridge - 2731 Caton Hill Road', '3886018']]

def postRequest(calendarID):
	# payload = {'type': '14002959', 'calendar': calendarID, 'skip': 'true', 'options[qty]': '1', 'options[numDays]': '5',
	# 		'ignoreAppointment': '', 'appointmentType': '', 'calendarID': ''}
	payload = {'type': '14002959', 'calendar': calendarID, 'skip': 'true', 'options[qty]': '1', 'options[numDays]': '5'}
	r = requests.post('https://vadmvappointments.as.me/schedule.php?action=showCalendar&fulldate=1&owner=19444409&template=monthly', data=payload)
	return r


# payload = {'type': '14002959', 'calendar': '3871993', 'skip': 'true', 'options[qty]': '1', 'options[numDays]': '5',
# 			'ignoreAppointment': '', 'appointmentType': '', 'calendarID': ''}
def original():
	start = time.time()
	# r = requests.post('https://vadmvappointments.as.me/schedule.php?action=showCalendar&fulldate=1&owner=19444409&template=monthly', data=payload)
	r = postRequest('3871953')
	end = time.time()
	soup = BeautifulSoup(r.content, 'html.parser')

	f = open('response.html', 'w')
	f.write(soup.prettify())
	f.close()

	openMonth = soup.find('option', {'selected': 'selected'}).text.split()[0]
	openYear = soup.find('option', {'selected': 'selected'}).text.split()[1]
	openDates = soup.findAll('td', {'class': 'scheduleday activeday'})

	print("Time for request: " + str(end-start) + " seconds")
	print("Response payload written to file response.html")
	for d in openDates:
		print(openMonth + " " + d.text + " " + openYear + "\n\n")

	for l in calendarIDList:
		print(l[0] + "\t" + l[1])

def main():
	locationDates = []
	totalTime = 0
	for i in range(len(calendarIDList)):
		locationDates.append([calendarIDList[i][0]])
		start = time.time()
		req = postRequest(calendarIDList[i][1])
		end = time.time()
		totalTime += end - start
		print(calendarIDList[i][0].split()[0] + " - " + str(req.status_code))
		soup = BeautifulSoup(req.content, 'html.parser')
		openMonth = soup.find('option', {'selected': 'selected'}).text.split()[0]
		openYear = soup.find('option', {'selected': 'selected'}).text.split()[1]
		openDays = soup.findAll('td', {'class': 'scheduleday activeday'})
		dayList = []
		for day in openDays:
			combDay = openMonth + " " + day.text + " " + openYear
			dayList.append(combDay)
		locationDates[i].append(dayList)
	print(tabulate(locationDates, headers=['Location', 'Date(s)'], tablefmt='presto'))
	print("Average time per request: " + str(totalTime / len(calendarIDList)) + " seconds\n\n")

main()




