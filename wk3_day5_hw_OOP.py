import requests
from datetime import datetime, timedelta
from operator import itemgetter

# Make API Request
data1 = requests.get("https://ct-mock-tech-assessment.herokuapp.com/").json()

data = {}

# Meeting Class
class Meeting:
    def __init__(self, country):
        
        self.country = country
        self.list_of_available_dates_by_person = []
        self.valid_start_dates = []
        self.date_counter = {}
        self.attendee_count = 0
        self.attendee_emails = []
        self.start_date = ''
        self.country_dictionary = {
            'attendee count': len(self.attendee_emails),
            'attendee emails': [],
            'country': country,
            'start date': self.start_date
        }
    # Function to find dates and attendees
    def attendees_info(self):
        list_of_available_dates_by_person = []
        valid_start_date_by_person = []
        date_counter = {}
        start_date = ''
        number_of_attendees = 0
        
        # Get list of available dates for each individual
        for num in range(233):
            if data1['partners'][num]['country'] == country:
                list_of_available_dates_by_person.append(data1['partners'][num]['availableDates'])
        # print(f"List of Available Dates By Person: {country}, {list_of_available_dates_by_person}")
        # List only valid start dates that can accomodate day 2 for each person 
        for each in list_of_available_dates_by_person:
            for idx in range(1, len(each)):
                current_date = datetime.strptime(each[idx], "%Y-%m-%d")
                previous_date = datetime.strptime(each[idx-1], "%Y-%m-%d")
                # checking for 1 day time difference
                if (current_date-previous_date).days == 1:
                    valid_start_date_by_person.append(each[idx-1])
        # print(f"List of Valid Start Dates by Person: {country}, {valid_start_date_by_person}")

        # Count number of individuals available for each date
        for each in valid_start_date_by_person:
            if each not in date_counter:
                date_counter[each] = 1
            else:
                date_counter[each] += 1
        # print(f"Date Counter: {country}, {date_counter}")

        # Pick the start date that maximizes number of available attendees
        day_1_date = max(date_counter, key=date_counter.get)
        attendee_count = date_counter[day_1_date]
        # print(f'Attendee Count: {country}, {attendee_count}')
        # print(f"Day 1 Date: {country}, {day_1_date}")
        
        # Assign day 2 date
        day_1_day_as_integer = int(day_1_date[-1])
        # print(f"Day 1 day as integer: {country}, {day_1_day_as_integer}")
        day_2_day_as_integer = day_1_day_as_integer + 1
        # print(f"Day 2 day as integer: {country}, {day_2_day_as_integer}")
        day_2_date = ''
        if day_2_day_as_integer == 10 and day_1_date[-2] == '0':
            for num in range(len(day_1_date)-2):
                day_2_date += day_1_date[num]
            day_2_date += str(10)
        elif day_2_day_as_integer == 10 and day_1_date[-2] == '1':
            for num in range(len(day_1_date)-2):
                day_2_date += day_1_date[num]
            day_2_date += str(20)
        elif day_2_day_as_integer == 10 and day_1_date[-2] == '2':
            for num in range(len(day_1_date)-2):
                day_2_date += day_1_date[num]
            day_2_date += str(30)
        else:    
            for num in range(len(day_1_date)-1):
                day_2_date += day_1_date[num]
            day_2_date += str(day_2_day_as_integer)
        # print(f"Day 1: {country}, {day_1_date}")
        # print(f"Day 2: {country}, {day_2_date}")

        # Compile attendee list
        attendee_list = []
        for num in range(233):        
            if data1['partners'][num]['country'] == country:
                if day_1_date in data1['partners'][num]['availableDates'] and day_2_date in data1['partners'][num]['availableDates']:
                    attendee_list.append(data1['partners'][num]['email'])
        # print(f"Attendee List: {attendee_list}")

        # Compile info in dictionary for each country
        Country_Dictionary = {
            'attendee count': len(attendee_list),
            'attendee emails': attendee_list,
            'country': country,
            'start date': day_1_date
        }
        # print(f"{country} Dictionary: {Country_Dictionary}\n")

        # Add each country dictionary to 1 complete international dictionary
        data[f"{country} Dictionary"] = Country_Dictionary

# Compile list of countries and Instantiate a Meeting for each country
countries = []
for num in range(233):
    country = data1['partners'][num]['country']
    if country not in countries:
        countries.append(country)
        meeting = Meeting(country)
        Meeting.attendees_info(country)

print(data)

r = requests.post("https://ct-mock-tech-assessment.herokuapp.com/", json = data)
print(r.text)

