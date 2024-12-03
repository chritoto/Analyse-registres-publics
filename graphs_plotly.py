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

with open('/Users/christophebolduc/Documents/PickPick/sanctions.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    for i,row in enumerate(reader):
        if i == 0:
            continue
        datetime_object = datetime.strptime(row[1], '%Y-%m-%d')
        sanction = [row[0], datetime_object, row[2], row[3].lower()]
        #if datetime_object <= cutoff:   
        sanctions.append(sanction)
        if datetime_object < min_date:
            min_date = datetime_object
            
#1. Plot the number of sanctions per month
#2. Number of sanctions per month where mentionned "Une demande de réexamen a été reçue"
#3. Number of sanctions per month where mentionned " La sanction administrative pécuniaire est annulée" 

months = []
today = datetime.today()
min_date = datetime(2018, 3, 1)
current = min_date
while current <= today:
    months.append(current)
    current += relativedelta(months=1)


plot1_y = []
plot2_1y = []
plot2_2y = []
plot3_1y = []
plot3_2y = []
for i in range(len(months)):
    plot1_y.append(0)
    plot2_1y.append(0)
    plot2_2y.append(0)
    plot3_1y.append(0)
    plot3_2y.append(0)
    

count = 0
for sanction in sanctions:
    #Toutes les sanctions
    date_sanction = sanction[1]
    month = date_sanction.month
    year = date_sanction.year
    index = months.index(datetime(year, month, min_date.day))
    plot1_y[index] += 1
    
    
    admise_cond = "n'est pas admise" in sanction[3] or "ne peut être admise" in sanction[3]
    if "une demande de réexamen" in sanction[3] and not admise_cond:
        print(sanction[3])
        count += 1

    
    # if "une demande de réexamen" in sanction[3] and "une requête a été déposée au tribunal" not in sanction[3] and not admise_cond:
    #     plot2_1y[index] += 1
    # if "une demande de réexamen" in sanction[3] and "une requête a été déposée au tribunal" not in sanction[3] and not admise_cond and "est annulée" in sanction[3]:
    #     plot2_2y[index] += 1
        
    if "une demande de réexamen" in sanction[3] and not admise_cond:
        plot2_1y[index] += 1
    if "une demande de réexamen" in sanction[3] and "une requête a été déposée au tribunal" not in sanction[3] and not admise_cond and "est annulée" in sanction[3]:
        plot2_2y[index] += 1
    
    if "tribunal" in sanction[3] and "désistement" not in sanction[3] and "desistement" not in sanction[3]:
        plot3_1y[index] += 1
    if "tribunal" in sanction[3] and "est annulée" in sanction[3] and "désistement" not in sanction[3] and "desistement" not in sanction[3]:
        plot3_2y[index] += 1
    
print("nombre de sanctions total:", sum(plot1_y))
print("nombre de réexamen:",count)

print("nombre demande:", sum(plot2_1y))
print("nombre demande annulée:", sum(plot2_2y))

print("nombre tribunal:", sum(plot3_1y))
print("nombre tribunal annulée:", sum(plot3_2y))
####### Plot 1 ########


color_0 = "rgb(0,0,0)"
color_1 = "rgb(200,200,200)"
cutoff = datetime(2024, 7, 31)
first_date = datetime(2018, 2, 1)

labels = []
mois_txt = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
index_aout_2023 = months.index(datetime(2023, 8, 1))
index_dec_2022 = months.index(datetime(2022, 12, 1))

print("moyenne demande réexamen jusqu'a aout 2023:", sum(plot2_1y[:index_aout_2023])/len(plot2_1y[:index_aout_2023]))
print("moyenne de pourcentage des demandes annulées jusqu'a aout 2023:", sum(plot2_2y[:index_aout_2023])/sum(plot2_1y[:index_aout_2023]) * 100)
print("moyenne demandes tribunal jusqu'a decembre 2022:" , sum(plot3_1y[:index_dec_2022])/len(plot3_1y[:index_dec_2022]))
print("moyenne de pourcentage des demandes annulées tribunal jusqu'a decembre 2022:", sum(plot3_2y[:index_dec_2022])/sum(plot3_1y[:index_dec_2022]) * 100)

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
        title='Nombre de sanctions'
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
fig.write_image("graph1.pdf")

####### Plot 2 ########

trace1 = go.Bar(
    x=months,
    y=plot2_1y,
    marker=dict(
        color=color_0
    ),
    opacity=1.0,
    name="Demandes de réexamen"
)

trace2 = go.Bar(
    x=months,
    y=plot2_2y,
    marker=dict(
        color=color_1
    ),
    opacity=1,
    name="Demandes ayant menées à une annulation de la SAP"
)

layout = go.Layout(
    #title='Number of sanctions per month demande de réexament pas de tribunal',
    height=800,
    width=1200,
    xaxis=dict(
        title='Mois'
    ),
    yaxis=dict(
        title='Nombre de demandes de réexamen'
    ),
    bargap=0.2,
    barmode='overlay'
)

data = [trace1, trace2]

fig = go.Figure(data=data, layout=layout)
fig.update_xaxes(range=[first_date,cutoff])
# fig.update_xaxes(
#     dtick="M1",
#     tickformat="%b\n%Y")
fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = months,
        ticktext = labels
    )
)
#fig.show()
fig.update_layout(template='plotly_white')
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.99
))
fig.write_image("graph2.pdf")

####### Plot 3 ########

trace1 = go.Bar(
    x=months,
    y=plot3_1y,
    marker=dict(
        color=color_0
    ),
    opacity=1.0,
    name="Reqêtes au TAQ"
)

trace2 = go.Bar(
    x=months,
    y=plot3_2y,
    marker=dict(
        color=color_1
    ),
    opacity=1,
    name="Requêtes ayant menées à une annulation de la SAP"
)

layout = go.Layout(
    #title='Number of sanctions per month pour tribunal',
    height=450,
    width=1200,
    xaxis=dict(
        title='Mois'
    ),
    yaxis=dict(
        title='Nombre de requêtes au TAQ'
    ),
    bargap=0.2,
    barmode='overlay'
)

data = [trace1, trace2]

fig = go.Figure(data=data, layout=layout)
fig.update_xaxes(range=[first_date,cutoff])
# fig.update_xaxes(
#     dtick="M1",
#     tickformat="%b\n%Y")
fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = months,
        ticktext = labels
    )
)
#fig.show()
fig.update_layout(template='plotly_white')
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.99
))
fig.write_image("graph3.pdf")