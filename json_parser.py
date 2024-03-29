import json


def get_info_from_json(filename):
	"""
	Reads JSON from cowin and extracts relevant info
	"""
	vax_info = json.load(open(filename, "r"))
	try:
		centers = vax_info["centers"]
		all_center_available = 0
		covishield_dose1_available_18 =0
		covishield_dose2_available_18 =0
		covaxin_dose1_available_18 =0
		covaxin_dose2_available_18 =0
		covishield_dose1_available_45 =0
		covishield_dose2_available_45 =0
		covaxin_dose1_available_45 =0
		covaxin_dose2_available_45 =0
		# dose1_available=0
		# dose2_available=0
		# dose1_available_45=0
		# dose2_available_45=0
		available_18=0
		available_45=0
		available_locations = {}
		for center in centers:
			center_id = center["center_id"]
			name = center["name"]
			address = center["address"]
			sessions = center["sessions"]
			total_available = 0
			# total_shield=0
			# total_covaxin=0
			# total_shield_18=0
			# total_covaxin_18=0
			# total_shield_45=0
			# total_covaxin_45=0
			# total_dose1=0
			# total_dose2=0
			# total_dose1_45=0
			# total_dose2_45=0
			total_18=0
			total_45=0
			total_dose1_covi_18=0
			total_dose2_covi_18=0
			total_dose1_covax_18=0
			total_dose2_covax_18=0
			total_dose1_covi_45=0
			total_dose2_covi_45=0
			total_dose1_covax_45=0
			total_dose2_covax_45=0
			for session in sessions:
				try:
					capacity = session["available_capacity"]
					capacity_dose1 = session["available_capacity_dose1"]
					capacity_dose2 = session["available_capacity_dose2"]
					total_available += capacity
					# total_dose1 += capacity_dose1
					# total_dose2 += capacity_dose2
					if session["vaccine"]=="COVISHIELD" and session["min_age_limit"]==18:
						# total_shield_18 += capacity
						total_dose1_covi_18 +=capacity_dose1
						total_dose2_covi_18 +=capacity_dose2
					if session["vaccine"]=="COVAXIN" and session["min_age_limit"]==18:
						# total_covaxin_18 += capacity
						total_dose1_covax_18 +=capacity_dose1
						total_dose2_covax_18 +=capacity_dose2
					if session["vaccine"]=="COVISHIELD" and session["min_age_limit"]==45:
						# total_shield_45 += capacity
						total_dose1_covi_45 +=capacity_dose1
						total_dose2_covi_45 +=capacity_dose2
					if session["vaccine"]=="COVAXIN" and session["min_age_limit"]==45:
						# total_covaxin_45 += capacity
						total_dose1_covax_45 +=capacity_dose1
						total_dose2_covax_45 +=capacity_dose2
					if session["min_age_limit"]==18:
						total_18+= capacity
						# total_dose1 +=capacity_dose1
						# total_dose2 +=capacity_dose2
						# total_shield_18 += total_shield
						# total_covaxin_18 += total_covaxin
					if session["min_age_limit"]==45:	
						# total_dose1_45+=capacity_dose1
						# total_dose2_45+=capacity_dose2
						total_45+= capacity
						# total_shield_45 += total_shield
						# total_covaxin_45 += total_covaxin
				except:
					continue
			all_center_available += total_available
			covishield_dose1_available_18 +=total_dose1_covi_18
			covishield_dose2_available_18 +=total_dose2_covi_18
			covaxin_dose1_available_18 +=total_dose1_covax_18
			covaxin_dose2_available_18 +=total_dose2_covax_18
			covishield_dose1_available_45 +=total_dose1_covi_45
			covishield_dose2_available_45 +=total_dose2_covi_45
			covaxin_dose1_available_45 +=total_dose1_covax_45
			covaxin_dose2_available_45 +=total_dose2_covax_45
			# dose1_available_45+=total_dose1_45
			# dose2_available_45+=total_dose2_45
			# covishield_available_18 += total_shield_18
			# covaxin_available_18 += total_covaxin_18
			# covishield_available_45 += total_shield_45
			# covaxin_available_45 += total_covaxin_45
			available_18 += total_18
			available_45 += total_45
			if total_available > 0:
				available_locations[center_id] = {"name" : name, "address" : address, "availability": total_available, "center_id":center_id}
		result = {"total_availability": all_center_available, "covishield_dose1_availability_18": covishield_dose1_available_18, "covishield_dose2_availability_18": covishield_dose2_available_18,"covaxin_dose1_availability_18": covaxin_dose1_available_18,"covaxin_dose2_availability_18": covaxin_dose2_available_18, "covishield_dose1_availability_45": covishield_dose1_available_45,"covishield_dose2_availability_45":covishield_dose2_available_45,"covaxin_dose1_availability_45":covaxin_dose1_available_45,"covaxin_dose2_availability_45":covaxin_dose2_available_45,"availability_18": available_18, "availability_45": available_45,"details": available_locations}
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
		covishield_dose1_availablee_18 = new_availability["covishield_dose1_availability_18"]
		covishield_dose2_availablee_18 = new_availability["covishield_dose2_availability_18"]
		covaxin_dose1_availablee_18 = new_availability["covaxin_dose1_availability_18"]
		covaxin_dose2_availablee_18 = new_availability["covaxin_dose2_availability_18"]
		covishield_dose1_availablee_45 = new_availability["covishield_dose1_availability_45"]
		covishield_dose2_availablee_45 = new_availability["covishield_dose2_availability_45"]
		covaxin_dose1_availablee_45 = new_availability["covaxin_dose1_availability_45"]
		covaxin_dose2_availablee_45 = new_availability["covaxin_dose2_availability_45"]
		# covishield_availablee_45 = new_availability["covishield_availability_45"]
		# covaxin_availablee_45 = new_availability["covaxin_availability_45"]
		avaiablee_18 = new_availability["availability_18"]
		avaiablee_45 = new_availability["availability_45"]
		# dose1_availablee = new_availability["dose1_availability"]
		# dose2_availablee = new_availability["dose2_availability"]
		# dose1_availablee_45 = new_availability["dose1_availability_45"]
		# dose2_availablee_45 = new_availability["dose2_availability_45"]
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
		# tweet only if additional availability is greater than 10% of total availability
		if additional_availability > (0.1 * new_availability["total_availability"]):
			return additional_availability + existing_availability,covishield_dose1_availablee_18,covishield_dose2_availablee_18 ,covaxin_dose1_availablee_18,covaxin_dose2_availablee_18,covishield_dose1_availablee_45,covishield_dose2_availablee_45,covaxin_dose1_availablee_45,covaxin_dose2_availablee_45, avaiablee_18,avaiablee_45, diff_sessions 
		else:
			return 0,0,0,0,0,0,0,0,0,0,0, diff_sessions
	except:
		log_file.write("compare_availability_to_prev failed \n")
		log_file.close()
		return 0,0,0,0,0,0,0,0,0, {}