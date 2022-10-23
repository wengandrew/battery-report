from tkinter import W
import pandas as pd

# run file 
def main():	

	# # step 1: output the normalized csv file
	# filepath = "C:/Users/ljing/OneDrive - Tesla/Documents/10 Other/Battery Talent/h1b_output_2022_battery.csv"
	# df = import_file(filepath)
	# filepath_normalized_salary = "C:/Users/ljing/OneDrive - Tesla/Documents/10 Other/Battery Talent/h1b_output_2022_normalized.csv"
	# df = normalize_salary(df,filepath_normalized_salary)
	
	# # step 2: label irrelevant jobs
	# filepath_normalized_salary = "C:/Users/ljing/OneDrive - Tesla/Documents/10 Other/Battery Talent/h1b_output_2022_normalized.csv"
	# df = pd.read_csv(filepath_normalized_salary)
	# filepath_relevant = "C:/Users/ljing/OneDrive - Tesla/Documents/10 Other/Battery Talent/h1b_output_2022_relevant_v1.csv"
	# relevance(df,filepath_relevant)

	# step 3: label job levels
	filepath_normalized_salary = "C:/Users/ljing/OneDrive - Tesla/Documents/10 Other/Battery Talent/h1b_output_2022_relevant_v1.csv"
	df = pd.read_csv(filepath_normalized_salary)
	# filter relevant roles first 
	filepath_labeled = "C:/Users/ljing/OneDrive - Tesla/Documents/10 Other/Battery Talent/h1b_output_2022_label_v1.csv"
	levels(df,filepath_labeled)

	# step 3: label job categories
	filepath_labeled = "C:/Users/ljing/OneDrive - Tesla/Documents/10 Other/Battery Talent/h1b_output_2022_label_v1.csv"
	df = pd.read_csv(filepath_labeled)

	# filter relevant roles first 
	filepath_categorized = "C:/Users/ljing/OneDrive - Tesla/Documents/10 Other/Battery Talent/h1b_output_2022_category_v1.csv"
	categories(df,filepath_categorized)

def relevance(df, filepath_relevant):
	
	# convert company csv to list 
	company_list_df = pd.read_csv("C:/Users/ljing/OneDrive - Tesla/Documents/10 Other/Battery Talent/company_list.csv")
	company_list = company_list_df['Company'].to_list()
	company_list = [x.upper() for x in company_list]

	# remove salary above 900k and below 30k 
	df.loc[df['salary'] > 900000, 'category'] = 'Incorrect Values'
	df.loc[df['salary'] < 30000, 'category'] = 'Incorrect Values'

	for index, row in df.iterrows():
		# 0 is not relevant, 1 is relevant 
		if any([substring in row['title'] for substring in ['ACCOUNTANT','ART DIRECTOR', 'ACCOUNT','ASIC DESIGN','CELLULAR']]):
			df.at[index,['category']] = 'Irrelevant' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
			df.at[index,['relevance']] = 'Irrelevant' if pd.isnull(df.at[index,'relevance']) else df.at[index,'relevance']
		if any([substring in row['title'] for substring in ['BATTERY']]):
			df.at[index,['relevance']] = 'Battery' if pd.isnull(df.at[index,'relevance']) else df.at[index,'relevance']
		if any([substring in row['title'] for substring in ['VEHICLE']]):
			df.at[index,['relevance']] = 'Vehicle' if pd.isnull(df.at[index,'relevance']) else df.at[index,'relevance']
		if any([substring in row['company'] for substring in company_list]):
			df.at[index,['relevance']] = 'Relevant' if pd.isnull(df.at[index,'relevance']) else df.at[index,'relevance']
		if any([substring in row['company'] for substring in ['APPLE','OAK RIDGE','WAYMO','UT-BATTELLE','AC PROPULSION INC','ACRO SERVICE CORPORATION','AEROTEK INC','ALTAIR PRODUCTDESIGN INC','APTIV CORPORATION','BENDIX COMMERCIAL VEHICLE SYSTEMS LLC','CRUISE','NURO','SIRIUS XM CONNECTED VEHICLE SERVICES INC','TUSIMPLE','VISTEON CORPORATION','ZOOX','NATRON','BATTELLE MEMORIAL','YOTTA','ASCII GROUP','ALTAIR','AGGREKO LLC']]) and not any([substring in row['title'] for substring in ['BATTERY','CELL','VEHICLE']]):
			df.at[index,['relevance']] = 'Irrelevant' if pd.isnull(df.at[index,'relevance']) else df.at[index,'relevance']
		
	# fill the rest with not relevant 
	df['relevance'] = df[['relevance']].fillna(value=0)

	df.to_csv(filepath_relevant)

def levels(df, filepath_labeled):
	# case 
	for index, row in df.iterrows():
		# start from higher level	
		if any([substring in row['title'] for substring in ['CHIEF TECHNOLOGY OFFICER','CHIEF BRAND OFFICER','CHIEF MARKETING OFFICER','CHIEF EXECUTIVE OFFICER','CHIEF STRATEGY OFFICER','CHIEF FINANCIAL OFFICER']]):
			df.at[index,['level']] = 'C-Suite' if pd.isnull(df.at[index,'level']) else df.at[index,'level']
		if any([substring in row['title'] for substring in ['DIRECTOR','VICE PRESIDENT', 'VP OF']]):
			df.at[index,['level']] = 'Director' if pd.isnull(df.at[index,'level']) else df.at[index,'level']
		if any([substring in row['title'] for substring in ['MANAGER','SENIOR MANAGER']]) and not any([substring in row['title'] for substring in ['PROGRAM MANAGER','PROJECT MANAGER','GLOBAL SUPPLY MANAGER','PRODUCT MANAGER','STRATEGY MANAGER','SOURCING MANAGER','SUPPLY CHAIN MANAGER','DISTRIBUTION MANAGER','MANAGER PLANNER', 'IT MANAGER','SUPERVISOR']]):			
			df.at[index,['level']] = 'Manager' if pd.isnull(df.at[index,'level']) else df.at[index,'level']
		if any([substring in row['title'] for substring in ['STAFF', 'CHIEF','PRINCIPAL']]) and not any([substring in row['title'] for substring in ['MEMBER OF','CHIEF OF STAFF']]):
			df.at[index,['level']] = 'Staff' if pd.isnull(df.at[index,'level']) else df.at[index,'level']
		if any([substring in row['title'] for substring in ['SENIOR', 'SENIOR ASSOCIATE', 'SR.', 'SR ','LEAD']]):
			df.at[index,['level']] = 'Senior' if pd.isnull(df.at[index,'level']) else df.at[index,'level']
		if any([substring in row['title'] for substring in ['ASSOCIATE','JUNIOR']]):
			df.at[index,['level']] = 'Junior' if pd.isnull(df.at[index,'level']) else df.at[index,'level']
		else:
			df.at[index,['level']] = 'Junior' if pd.isnull(df.at[index,'level']) else df.at[index,'level']

	df.to_csv(filepath_labeled)

def categories(df,filepath_categories):

	for index, row in df.iterrows():
		if any([substring in row['title'] for substring in ['PRODUCT MANAGER','PROJECT MANAGER', 'PROGRAM MANAGER','COORDINATOR','PRODUCT OWNER','PRODUCT DESIGN']]):
			df.at[index,['category']] = 'PM' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
		if any([substring in row['title'] for substring in ['SOFTWARE','DATA','STACK','ALGORITHM','PROGRAMMER', 'AI SCIENTIST', 'MACHINE LEARNING', 'ARTIFICIAL INTELLIGENCE','COMPUTER','DEEP LEARNING','USER EXPERIENCE','UX','COMPUTAT', 'MODELING','LIFETIME','PREDICT','SIMULATION','CLOUD','PLATFORM','WEB','NETWORK','DIGITAL','AUTOMAT','JAVA','USER INTERFACE','MODEL','HADOOP','VISION','ANDROID']]):
			df.at[index,['category']] = 'Software' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
		if any([substring in row['title'] for substring in ['RESEARCH','R&D','SCIENTIST','CHEMIST']]) and not any([substring in row['title'] for substring in ['RESEARCH ANALYST']]):
			df.at[index,['category']] = 'Research' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
		if any([substring in row['title'] for substring in ['MANUFACTUR','PROCESS','DEVELOPMENT','INDUSTRIAL','ARCHITECT']]):
			df.at[index,['category']] = 'Manufacturing' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
		if any([substring in row['title'] for substring in ['MECHANICAL','CAD','HARDWARE','CAE','CFD','CATIA','FEA','MODULE','DESIGN AND RELEASE','DESIGN RELEASE']]):
			df.at[index,['category']] = 'Mechanical' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
		if any([substring in row['title'] for substring in ['VALIDATION','TEST','QUALITY','QA','CHARACTERIZATION','APPLICATION','STRESS','VERIFICATION']]):
			df.at[index,['category']] = 'Test/QA' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
		if any([substring in row['title'] for substring in ['BUSINESS','SUPPLY CHAIN','FINANC','GLOBAL SUPPLY','BUYER','PURCHAS','CHIEF OF STAFF','MARKET','RISK','STRATEGIC','SALES','SOURCING','RECRUITER','TALENT','STRATEGY','PROCURE']]):
			df.at[index,['category']] = 'Business' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
		if any([substring in row['title'] for substring in ['ELECTRIC','CONTROL','SYSTEM','FIRMWARE','ELECTRONIC','SENSOR','PERCEPTION','PCB']]):
			df.at[index,['category']] = 'Electrical' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
		if any([substring in row['title'] for substring in ['SAFETY','THERMAL','RELIAB', 'HEAT']]):
			df.at[index,['category']] = 'Safety/Thermal' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
		if any([substring in row['title'] for substring in ['BATTERY','CELL','MATERIALS']]):
			df.at[index,['category']] = 'Battery General' if pd.isnull(df.at[index,'category']) else df.at[index,'category']		
		if any([substring in row['title'] for substring in ['VEHICLE','POWERTRAIN','AUTOMOTIVE','BODY','CHASIS','CHASSIS','MOTOR','ASSEMBLY','CRASH','CLOSURE','EXTERIOR','INTERIOR','TRANSMISSION']]):
			df.at[index,['category']] = 'Vehicle' if pd.isnull(df.at[index,'category']) else df.at[index,'category']		
		if any([substring in row['title'] for substring in ['PRINCIPAL ENGINEER','ASSOCIATE ENGINEER','TECHNICAL STAFF','SENIOR ENGINEER','PRODUCT ENGINEER','STAFF ENGINEER','ENGINEERING MANAGER','PROJECT LEAD','TECHNICAL LEAD','PROJECT ENGINEER','SR. ENGINEER','ENGINEER I','ENGINEER II','ENGINEER III']]):
			df.at[index,['category']] = 'General' if pd.isnull(df.at[index,'category']) else df.at[index,'category']
		if not pd.isnull(row['level']):
			if any([substring in row['level'] for substring in ['Manager','Director','C-Suite']]):
				df.at[index,['category']] = 'General' if pd.isnull(df.at[index,'category']) else df.at[index,'category']

	df.to_csv(filepath_categories)


def import_file(filepath):
	df = pd.read_csv(filepath)

	# clean df
	df['year'] = pd.DatetimeIndex(df['start date']).year
	df['salary'] = df["salary"].str.replace(",","").astype(float)
	return (df)

def normalize_salary(df,filepath_normalized_salary):
	# https://www.usinflationcalculator.com/inflation/consumer-price-index-and-annual-percent-changes-from-1913-to-2008/
	current_cpi = 277.948 #CPI from November
	cpi_dict = {'2021':277.948, '2020': 260.474, '2019':256.974,'2018':251.233,'2017':246.524,'2016':241.432,'2015':236.525,'2014':234.812,'2013':233.049,'2012':229.601,'2011':225.672} # use values from December
	cpi_pct = cpi_dict.copy()
	for key, value in cpi_pct.items():
		cpi_pct[key] = current_cpi/value
	df_cpi_pct = pd.DataFrame.from_dict(cpi_pct,orient='index',columns=['cpi_pct'])
	df_cpi_pct['year']=df_cpi_pct.index.astype(int)
	df = df.merge(df_cpi_pct, how='left', on='year')
	df['salary_normalized'] = round(df['salary'] * df['cpi_pct'],0)
	df['level'] = None
	df['category'] = None
	df['relevance'] = None
	df.to_csv(filepath_normalized_salary)
	return(df)
	

# output file

if __name__ == "__main__":
	main()