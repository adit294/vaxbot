import json


def get_info_from_json(filename):
	"""
	Reads JSON from cowin and extracts relevant info
	"""
	vax_info = json.load(open(filename, "r"))
	try:
		centers = vax_info["centers"]
		all_center_available = 0
		available_locations = {}
		for center in centers:
			center_id = center["center_id"]
			name = center["name"]
			address = center["address"]
			sessions = center["sessions"]
			total_available = 0
			for session in sessions:
				try:
					capacity = session["available_capacity"]
					total_available += capacity
				except:
					continue
			all_center_available += total_available
			if total_available > 0:
				available_locations[center_id] = {"name" : name, "address" : address, "availability": total_available, "center_id":center_id}
		result = {"total_availability": all_center_available, "details": available_locations}
		return result
	except:
		log_file = open("logger.txt", "a")
		log_file.write("get_info_from_json failed \n")
		log_file.close()
		return {}


def compare_availability_to_prev(new_availability, availability_filepath):
	"""
	Compares recently fetched availability to previous availability
	to determine if there is any increase or new availability.
	"""
	log_file = open("logger.txt", "a")
	try:
		old_availability = json.load(open(availability_filepath, "r"))
	except:
		log_file.write("Couldn't open old availability file")
		old_availability = {"total_availability":0,'details':{}} 

	try:
		total_diff = new_availability["total_availability"] - old_availability["total_availability"]
		new_sessions = new_availability["details"]
		old_sessions = old_availability["details"]
		diff_sessions = {}
		additional_availability = 0
		existing_availability = 0
		for center_id in new_sessions:
			if str(center_id) not in old_sessions:
				diff_sessions[center_id] = new_sessions[center_id]
				additional_availability += new_sessions[center_id]["availability"]
			else:
				if new_sessions[center_id]["availability"] > old_sessions[str(center_id)]["availability"]:
					additional_availability += (new_sessions[center_id]["availability"] - old_sessions[str(center_id)]["availability"])
					existing_availability += old_sessions[str(center_id)]["availability"]
					diff_sessions[center_id] = new_sessions[center_id]
				else:
					existing_availability += new_sessions[center_id]["availability"]
		# don't tweet if there was only a small increase (very few cancellations for example)
		if additional_availability > 50 or (additional_availability > 0 and new_availability["total_availability"] < 30):
			return additional_availability + existing_availability, diff_sessions
		else:
			return 0, diff_sessions
	except:
		log_file.write("compare_availability_to_prev failed \n")
		log_file.close()
		return 0, {}
