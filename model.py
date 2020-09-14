import pandas as pd
import numpy as np 
import re
import datetime as dt

import controller


class PolicyHolder():
	Genders = ["Male", "Female"]
	Allergies = ['Drug','Food','Insect','Latex','Mold','Pet','Pollen', 'NA'] 


	def __init__(self, gender, DOB, SSN, is_smoker, allergies, med_conditions):
		self.gender = gender
		self.DOB = controller.is_valid_date(DOB)
		self.SSN = SSN
		self.is_smoker = is_smoker
		self.allergies = allergies
		self.med_conditions = med_conditions
		self.holder_schema_check()


	def holder_schema_check(self):
		if self.gender not in self.Genders:
			raise ValueError("Gender value error")

		if not isinstance(self.DOB, dt.datetime):
			raise TypeError("Please check if the date of birth has (MM/DD/YYYY) format.")

		reg_SSN = re.compile("^(?!000|666)[0-8][0-9]{2}-(?!00)[0-9]{2}-(?!0000)[0-9]{4}$")
		if not reg_SSN.findall(self.SSN):
			raise ValueError("Please check if the SSN has 000-00-0000 format.")
				
		if self.is_smoker not in ["Y", "N"]:
			raise ValueError("Is_smoker should be Y or N.")

		al_list = self.allergies.split('/')
		for a in al_list:
			if a not in self.Allergies:
				raise ValueError("One or More (or NA) Allergy should be chosen from the allergiy list with separator '/'. ")


		med_con_list = self.med_conditions.split('/')
		reg_med_con = re.compile("[A-TV-Z][0-9][0-9AB]\.?[0-9A-TV-Z]{0,4}")
		for m in med_con_list:
			if not reg_med_con.findall(m):
				raise ValueError("Medical condition should be one or more ICD-10 code(s) (or NA) with separator '/'. ")



class Claim():
	Claim_Types = ['Hospital stays','Prescription medications','Surgeries', 'Emergency medical care', 'NA']
	# https://www.arnolditkin.com/insurance-claims/types-of-insurance-claims/

	def __init__(self, PolicyHolderID, date_of_inc, claim_type, billed_amount, covered_amount):
		self.PolicyHolderID = PolicyHolderID
		self.date_of_inc = controller.is_valid_date(date_of_inc)
		self.claim_type = claim_type
		self.billed_amount = billed_amount
		self.covered_amount = covered_amount 

		try:
			self.billed_amount = float(self.billed_amount)
		except:
			raise TypeError("Billed amount should be a numerical value.")
		try:
			self.covered_amount = float(self.covered_amount)
		except:
			raise TypeError("Covered amount should be a numerical value.")
		self.claim_check_schema()


	def claim_check_schema(self):
		if not isinstance(self.date_of_inc, dt.datetime):
			raise TypeError("Please check if the date of incidence has (MM/DD/YYYY) format.")

		if self.claim_type not in self.Claim_Types:
			raise TypeError("One or More (or NA) Claim Type should be chosen from the claim type list with separator '/'. ")
 
