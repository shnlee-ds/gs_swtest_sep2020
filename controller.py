import pandas as pd
import numpy as np 
import os
import re
import datetime as dt
from hashlib import sha1

import model


def is_valid_date(date):
        reg_date = re.compile("^(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])/[0-9]{4}$")
        if not reg_date.findall(date):
            raise ValueError("Wrong input. Date format should be 'mm/dd/yyyy'")
        m,d,y = int(date[:2]), int(date[3:5]), int(date[6:])
        return dt.datetime(y, m, d)


def write_data(data_name):
	if data_name == 'Claim_Data':
		cols = ['PolicyHolderID', 'Claim ID', 'Date of Incidence', 'Claim Type', 'Billed Amount', 'Covered Amount']

	elif data_name == 'Policy_Holder_Data':
		cols = ['PolicyHolderID', 'Gender', 'Date of Birth', 'SSN', 'Smoking', 'Allergies', 'Medical Condition']

	path = data_name + '.csv'
	if not os.path.isfile(path):
		data = pd.DataFrame(columns = cols)
		data.to_csv(path, index = None, encoding = 'utf-8')

for d in ['Policy_Holder_Data', 'Claim_Data']:
	write_data(d)

def read_data(data_name):
	data = pd.read_csv(data_name, encoding = 'utf-8', date_parser = True)
	if 'Date of Incidence' in data.columns:
		data['Date of Incidence'] = pd.to_datetime(data["Date of Incidence"])

	if 'Date of Birth' in data.columns:
		data['Date of Birth'] = pd.to_datetime(data["Date of Birth"])

	return data

def add_new(data, new):
	if isinstance(new, model.Claim):
		updated_data = data["Claim_Data"]
		ref_ID = len(updated_data)
		line = {'Claim ID':ref_ID,
				'PolicyHolderID': new.PolicyHolderID,
				'Date of Incidence': new.date_of_inc,
				'Claim Type': new.claim_type,
				'Billed Amount': new.billed_amount,
				'Covered Amount':new.covered_amount}
		if new.PolicyHolderID not in data["Policy_Holder_Data"].PolicyHolderID.values:
			raise KeyError("Cannot find the given policy holder. Please add the policy holder first.")

	if isinstance(new, model.PolicyHolder):
		updated_data = data["Policy_Holder_Data"]
		PolicyHolderID = str(sha1(str(new.SSN).encode("UTF-8")).hexdigest()) ########## Unique ID
		ref_ID = PolicyHolderID
		line = {'PolicyHolderID': PolicyHolderID,
				'Gender': new.gender, 
				'Date of Birth': new.DOB, 
				'SSN': new.SSN, 
				'Smoking': new.is_smoker, 
				'Allergies': new.allergies, 
				'Medical Condition': new.med_conditions}

	if ref_ID not in updated_data.iloc[:,0].values:
		updated_data = updated_data.append(line, ignore_index = True)
	else:
		raise KeyError("Policy holder already exists. PolicyHolderID: " + PolicyHolderID)

	return updated_data



def save_data(data, data_name):
	data.to_csv(data_name + '.csv', index = None, encoding = "utf-8")


def list_holders(holder_data):
	return holder_data.drop("SSN", axis=1)

def list_claims(PolicyHolderID, claim_data):
	return claim_data[claim_data["PolicyHolderID"] == PolicyHolderID]


def billed_sum_calc(claim_data):
	return claim_data["Billed Amount"].sum()

def covered_sum_calc(claim_data):
	return claim_data["Covered Amount"].sum()


def age_calc(bd):
	today = dt.date.today()
	return today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day)) 


def avg_age_calc(holder_data):
	if len(holder_data) == 0:
		raise ValueError("Policy holder list is empty.")
	else:
		holder_data["Age"] = holder_data["Date of Birth"].apply(age_calc)
		return str(np.mean(list(holder_data["Age"])))

def clm_cnt_by_year(claim_data):
	if len(claim_data) == 0:
		raise ValueError("Claim list is empty.")
	else:
		return claim_data.groupby(claim_data['Date of Incidence'].map(lambda x: x.year)).count()["Claim ID"].to_string()
	