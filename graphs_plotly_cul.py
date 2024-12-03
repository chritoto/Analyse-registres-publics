import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import plotly.io as pio   
pio.kaleido.scope.mathjax = None


min_date = datetime.now()
#cutoff = datetime(2024, 7, 31)

sanctions = []

with open('/Users/christophebolduc/Documents/PickPick/culpabilites.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    for i,row in enumerate(reader):
        if i == 0:
            continue
        datetime_object = datetime.strptime(row[0], '%Y-%m-%d')
        sanction = [row[0], datetime_object, row[1].lower()]
        #if datetime_object <= cutoff:   
        sanctions.append(sanction)
        if datetime_object < min_date:
            min_date = datetime_object
            
months = []
today = datetime.today()
min_date = datetime(2018, 3, 1)
current = min_date
while current <= today:
    months.append(current)
    current += relativedelta(months=1)


plot1_y = []
for i in range(len(months)):
    plot1_y.append(0)
    

for sanction in sanctions:
    #Toutes les sanctions
    date_sanction = sanction[1]
    month = date_sanction.month
    year = date_sanction.year
    index = months.index(datetime(year, month, min_date.day))
    plot1_y[index] += 1
    
    
print("nombre de culpabilites total:", sum(plot1_y))
####### Plot 1 ########


color_0 = "rgb(0,0,0)"
color_1 = "rgb(200,200,200)"
cutoff = datetime(2024, 7, 31)
first_date = datetime(2018, 2, 1)

labels = []
mois_txt = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']

for month in months:
    
    if month.month == 1:
        labels.append(month.strftime(mois_txt[month.month-1]+"\n%Y"))
    else:
        labels.append(month.strftime(mois_txt[month.month-1]))

trace = go.Bar(
    x=months,
    y=plot1_y,
    marker=dict(
        color=color_0
    ),
    opacity=1.
)

layout = go.Layout(
    #title='Number of sanctions per month',
    height=800,
    width=1200,
    xaxis=dict(
        title='Mois'
    ),
    yaxis=dict(
        title='Nombre de déclarations de culpabilité'
    ),
    bargap=0.2,
)

data = [trace]

fig = go.Figure(data=data, layout=layout)
fig.update_xaxes(range=[first_date,cutoff])
# fig.update_xaxes(
#     dtick="M1",
#     #tickformat="%b %Y",
#     ticks="outside")
fig.update_xaxes(tickangle=90)

fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = months,
        ticktext = labels
    )
)
# fig.show()
fig.update_layout(template='plotly_white')
fig.write_image("graph4.pdf")
