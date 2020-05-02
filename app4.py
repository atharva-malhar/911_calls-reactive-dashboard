def main():
	import streamlit as st
	import pandas as pd
	import matplotlib.pyplot as plt
	import seaborn as sns
	import os

	# Title
	st.title("911 Calls Analysis App")
	st.header("Built with streamlit")

	#EDA
	my_dataset = 'C:/Users/Lenovo/kossine/capstone#1-Reactive-Dashboard/src/911_calls.csv'

	#Function to load dataset
	@st.cache(persist=True)
	def explore_data(dataset):
		df = pd.read_csv(r'src/911_calls.csv')
		return df

	df = explore_data(my_dataset)

	if st.checkbox("Preview Dataset"):	
		if st.button("Head"):
			st.write(df.head())
		elif st.button("Tail"):
			st.write(df.tail())
		else :
			st.write(df.head(3))	

	# #Show entire dataset
	# if st.checkbox("Show the entire dataset"):
	# 	st.write(data)		Not working in this case since the data is very large

	#Show column names
	if st.checkbox("Show column names"):
		st.write(df.columns)	

	#Show Dimensions
	df_dim = st.radio("What dimensions do you want to see?",("Rows","Columns","All"))
	if df_dim == "Rows":
		st.text("Showing rows")
		st.write(df.shape[0])
	elif df_dim	== "Columns":
		st.text("Showing columns")
		st.write(df.shape[1])
	else:
		st.text("Showing shape of the dataset")
		st.write(df.shape)

	#Show Summary	
	if st.checkbox("Show summary of Dataset"):
		st.write(df.describe())

	#Select a column
	col_option = st.selectbox("Select column",("lat","lng","desc","zip","title","timeStamp","twp","addr","e"))
	if col_option == "lat":
		st.write(df['lat'])
	elif col_option == "lng":
		st.write(df['lng'])
	elif col_option == "desc":
		st.write(df['desc'])
	elif col_option == "zip":
		st.write(df['zip'])
	elif col_option == "title":
		st.write(df['title'])
	elif col_option == "timeStamp":
		st.write(df['timeStamp'])
	elif col_option == "twp":
		st.write(df['twp'])
	elif col_option == "addr":
		st.write(df['addr'])
	elif col_option == "e":
		st.write(df['e'])

	if st.checkbox("Show top 5 zipcodes for 911 calls"):
		st.write(df['zip'].value_counts().head(5))	

	if st.checkbox("Show top 5 townships for 911 calls"):
		st.write(df['twp'].value_counts().head(5))

	if st.checkbox("Number of unique title codes"):
		st.write(len(df['title'].unique()))

	#We create another column named reason, reason being grabbed from the title column
	#We use the apply function of pandas and lambda funtion to actually apply the required condition to all the data points
	df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])

	#Now we just plot the numbers obtained above using a count plot
	#Y axis for a countplot is count by default so you dont need to specify that
	st.subheader("Countplot using seaborn")
	st.write(sns.countplot(x='Reason',data=df))
	st.pyplot()

	df['timeStamp'] = pd.to_datetime(df['timeStamp'])

	#Now, since we've got a datetime object, we can grab various attributes from that object.
	#We'll use the apply funtion to create 3 new columns called Hour, Month and Day of week.
	df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
	df['Month'] = df['timeStamp'].apply(lambda time: time.month)
	df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)

	#Now, the day of week column looks a bit weird, so we actually map values to a string using the map function 
	dmap = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
	df['Day of Week'] = df['Day of Week'].map(dmap)

	# #Now we create a countplot using seaborn for the Day of Week column
	# st.write(sns.countplot(x='Day of Week',data = df))
	# #We observe that there's a drop on Sunday

	#Now we add a hue to the plot, which adds a legend based on another categorical data column
	st.subheader("Countplot using seaborn for Days of week with a hue")
	st.write(sns.countplot(x='Day of Week',data = df,hue = 'Reason'))
	st.pyplot()
	#Could've actually done it in the same step
	#To relocate the position of the legend we use the doumentation code
	plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)

	byMonth = df.groupby('Month').count()

	#Observe the trend of change in the values
	st.subheader("Simple line graph showing the trend of change in values")
	st.write(byMonth['lat'].plot())
	st.pyplot()

	#Now we use seaborn's lmplot() to create a linear fit on the number of calls per month
	#We also need to reset the index here
	st.subheader("A linear model showing a relationship between month and township")
	st.write(sns.lmplot(x='Month',y='twp',data = byMonth.reset_index()))
	st.pyplot()
	#So we get a linear model

	#We create another column named date that contains the date from the timeStamp column
	# df['Date'] = df['timeStamp'].apply(lambda t:t.date())

	# #Doesn't look nice though
	# st.write(df.groupby('Date').count()['lat'].plot())
	# plt.tight_layout()
	# st.pyplot()




