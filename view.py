import pandas as pd
import numpy as np 
import re
import datetime as dt
from hashlib import sha1

import model
import controller

class Command_Line_Interface:

	def __init__(self):
		self.holder_data = controller.read_data("Policy_Holder_Data.csv")
		self.claim_data = controller.read_data("Claim_Data.csv")
		self.Data = {"Policy_Holder_Data": self.holder_data, 
					 "Claim_Data": self.claim_data}


	def add_new_holder(self):

		msg = ["Gender(Male / Female): ",
		"Date of Birth (MM/DD/YYYY): ",
		"Social Security Number (XXX-XX-XXXX): ",
		"Smoking status (Y/N): ",
		"Allergies (please input one or more of the options below. Multiple option available with separator '/'.)\n\
		- Drug\n\
		- Food\n\
		- Insect\n\
		- Latex\n\
		- Mold\n\
		- Pet\n\
		- Pollen\n\
		- NA\n:",
		"Medical Conditions (ICD-10 Code). You can iput multiple codes with '/' as a separator.: "]

		try: 
			gender, DOB, SSN, is_smoker, allergies, med_conditions = [str(input(i)) for i in msg]

			holder = model.PolicyHolder(gender, DOB, SSN, is_smoker, allergies, med_conditions)
			self.holder_data = controller.add_new(self.Data, holder)
			self.Data = {"Policy_Holder_Data": self.holder_data, "Claim_Data": self.claim_data}
			PolicyHolderID = sha1(str(SSN).encode("UTF-8")).hexdigest()
			print("Policy holder has been added - Unique ID: {}".format(PolicyHolderID))

		except Exception as e:
			self.err_msg("Wrong Input, check error: " + str(e))


		self.holder_data["Age"] = self.holder_data["Date of Birth"].apply controller.age_calc)
	 controller.save_data(self.holder_data, "Policy_Holder_Data")
	 controller.save_data(self.claim_data, "Claim_Data")


	def add_new_claim(self):


		msg = ["Social Security Number (XXX-XX-XXXX): ",
		"Date of Incidence (MM/DD/YYYY): ",
		"Type of Issue (please input one or more of the options below. Multiple option available with separator '/'.)\n\
		\t- Hospital stays\n\
		\t- Prescription medications\n\
		\t- Surgeries\n\
		\t- Emergency medical care\n\
		\t- NA\n:",
		"Billed Amount: $", 
		"Covered Amount: $"]


		try:
			SSN, date_of_inc, claim_type, billed_amount, covered_amount = [str(input(i)) for i in msg]
			PolicyHolderID = sha1(str(SSN).encode("UTF-8")).hexdigest()
			billed_amount = billed_amount
			covered_amount = covered_amount
			claim = model.Claim(PolicyHolderID, date_of_inc, claim_type, billed_amount, covered_amount)
			self.claim_data = controller.add_new(self.Data, claim)
			self.Data = {"Policy_Holder_Data": self.holder_data, "Claim_Data": self.claim_data}
			print("Claim successfully added on Unique ID - {}".format(PolicyHolderID))			 

		except Exception as e:
			self.err_msg("Wrong Input, check error: " + str(e))

		self.holder_data["Age"] = self.holder_data["Date of Birth"].apply controller.age_calc)
	 controller.save_data(self.holder_data, "Policy_Holder_Data")
	 controller.save_data(self.claim_data, "Claim_Data")



	def check_ID(self):
		try:
			SSN = str(input("Policy Holder's SSN (000-00-0000): "))
			reg_SSN = re.compile("^(?!000|666)[0-8][0-9]{2}-(?!00)[0-9]{2}-(?!0000)[0-9]{4}$")
			if not reg_SSN.findall(SSN):
				raise ValueError("Please check if the SSN has 000-00-0000 format.")
			PolicyHolderID = sha1(str(SSN).encode("UTF-8")).hexdigest()
			print("The unique ID for given SSN: {}".format(PolicyHolderID))

		except Exception as e:
			self.err_msg("Wrong Input. ")


	def view_holder_list(self):
		try:
			l = controller.list_holders(self.holder_data)
			if l.empty:
				raise ValueError("No policy holder exists.")
			else:
				print(l.to_string(index=False))
		except Exception as e:
			self.err_msg("Error: " + str(e))

	def view_claim_list(self):
		try:
			SSN = input("Policy Holder's SSN (000-00-0000): ")
			reg_SSN = re.compile("^(?!000|666)[0-8][0-9]{2}-(?!00)[0-9]{2}-(?!0000)[0-9]{4}$")
			if not reg_SSN.findall(SSN):
				raise ValueError("Please check if the SSN has 000-00-0000 format.")
			PolicyHolderID = sha1(str(SSN).encode("UTF-8")).hexdigest()
			l = controller.list_claims(PolicyHolderID, self.claim_data)
			if l.empty:
				raise ValueError("No claim data exists with the given policy holder.")
			else:
				print(l.to_string(index=False))
		except Exception as e:
			self.err_msg("Error: " + str(e))


	def view_billed_sum(self):
		amt = controller.billed_sum_calc(self.claim_data)
		print("Total sum of billed amount: $" + str(amt))


	def view_covered_sum(self):
		amt = controller.covered_sum_calc(self.claim_data)
		print("Total sum of covered amount: $" + str(amt))


	def view_avg_age(self):
		try:
			avg = controller.avg_age_calc(self.holder_data)
			print('Average age of policy holders: ' + avg)
		except Exception as e:
			self.err_msg("Error: " + str(e))
	

	def view_clm_cnt_by_year(self):
		try:
			print controller.clm_cnt_by_year(self.claim_data))
		except Exception as e:
			self.err_msg("Error: " + str(e))

	def err_msg(self, msg):
		print(msg)


run = Command_Line_Interface()
while True:
    print("\t\t============================================================")
    print("\t\t\t\t\tCLAIM DATA MANAGER")
    print("\t\t\t  Please select one of the option numbers below.\n")
    print("\t\t  Add new data")
    print("\t\t\t1. Add a new policy holder")
    print("\t\t\t2. Add a new claim")
    print("\t\t\t3. Check a policy holder's unique ID")
    print("\n\t\t  Statistics")
    print("\t\t\t4. List of policy holders")
    print("\t\t\t5. List of claims by policy holder's unique ID")
    print("\t\t\t6. Statistics of Billed amount")
    print("\t\t\t7. Statistics of Covered amount")
    print("\t\t\t8. Total Number of Claims by year")
    print("\t\t\t9. Statistics of Policy Holders")
    print("\n\t\t0. Exit")
    print("\t\t============================================================")
    c = input()	
    if c == "0":
        break
    c_dict = {"1": run.add_new_holder,
    "2": run.add_new_claim,
    "3": run.check_ID,
    "4": run.view_holder_list,
    "5": run.view_claim_list,
    "6": run.view_billed_sum,
    "7": run.view_covered_sum,
    "8": run.view_clm_cnt_by_year,
    "9": run.view_avg_age}
    c_dict[c]()
        


