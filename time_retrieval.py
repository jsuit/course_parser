import re
import urllib2
import json

# Read list of courses from json list generated by parser.py
# Courses need to have college and id
course_data = open("courses.json", "r")
courses = json.load(course_data)
course_data.close()

all_sections = []

for course in courses:
	# print "Loading sections for course: " + course["college"] + " " + course["id"]

	#Retrieve source code
	url = "https://oscar.gatech.edu/pls/bprod/bwckctlg.p_disp_listcrse?term_in=201308&subj_in=" + course["college"] + "&crse_in=" + course["id"] + "&schd_in=%"
	urlsoc = urllib2.urlopen(url)
	sourcedata = urlsoc.read()
	urlsoc.close()

	# Splits code into pieces that should each have one section, except the first which is discarded
	section_code_list = sourcedata.split("<th CLASS=\"ddheader\" scope=\"col\" >Type</th>")[1:]

	sections = []
	for section_code in section_code_list:
		# Gets start time, end time, day, room
		class_regex = "<td CLASS=\"dddefault\">Class</td>\n<td CLASS=\"dddefault\">(.*?) - (.*?)</td>\n<td CLASS=\"dddefault\">(.*?)</td>\n<td CLASS=\"dddefault\">(.*?)</td>"
		raw_meetings = re.findall(class_regex, section_code)
		if raw_meetings:
			meetings = [ { "start_time": raw_meeting[0], "end_time": raw_meeting[1], "days": list(raw_meeting[2]), "location": raw_meeting[3] } for raw_meeting in raw_meetings ]
			section = {"college": course["college"], "id": course["id"], "meetings": meetings}
			sections.append(section)

	# Currently treating sections as independent and not grouping by course
	all_sections = all_sections + sections

# # Yay printing
# for section in all_sections:
# 	print section["college"], " ", section["id"]
# 	print "---"
# 	for meeting in section["meetings"]:
# 		print meeting["days"], meeting["start_time"] + " - " + meeting["end_time"]
# 	print ""

# Putting sections in json
sections_json = json.dumps(all_sections)
f = open("sections.json", "w")
f.write(sections_json)
f.close()



# ------- SAMPLE MEETING TIME HTML -------
# <td CLASS="dddefault">Class</td>
# <td CLASS="dddefault">4:35 pm - 5:55 pm</td>
# <td CLASS="dddefault">M</td>
# <td CLASS="dddefault">Klaus 1456</td>