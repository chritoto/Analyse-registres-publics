import csv
from datetime import datetime
import matplotlib.pyplot as plt



sanctions = []

with open('/Users/christophebolduc/Documents/PickPick/sanctions.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    for i,row in enumerate(reader):
        if i == 0:
            continue
        print(row)
        datetime_object = datetime.strptime(row[1], '%Y-%m-%d')
        sanction = [row[0], datetime_object, row[2], row[3]]
        sanctions.append(sanction)

#1. Plot the number of sanctions per month
#2. Number of sanctions per month where mentionned "Une demande de réexamen a été reçue"
#3. Number of sanctions per month where mentionned " La sanction administrative pécuniaire est annulée" 

months = []
plot1 = []
for sanction in sanctions:
    number_months_since_2018_03_01 = (sanction[1] - datetime(2018, 3, 1)).days//30
    year_month = number_months_since_2018_03_01#int(sanction[1].strftime("%Y%m"))
    print(year_month)
    if year_month not in months:
        months.append(year_month)
        plot1.append(1)
    else:
        plot1[months.index(year_month)] += 1
    if "Une demande de réexamen a été reçue" in sanction[3]:
        #Plot 2
        pass
    if "La sanction administrative pécuniaire est annulée" in sanction[3]:
        #Plot 3
        pass
    
plt.xlabel('Months since 2018-03-01')
plt.ylabel('Number of sanctions per month')
plt.scatter(months, plot1)
plt.show()