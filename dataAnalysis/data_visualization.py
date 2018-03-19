import plotly
import plotly.graph_objs as go
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

cv_set = 'bank-crossvalidation_new.csv'

COLUMNS = ["age","job","marital","education","default","balance","housing","loan","contact","day","month","duration",
           "campaign","pdays","previous","poutcome","y"]

df = pd.read_csv(cv_set)

df_yes = df[df.y=='yes']
df_no = df[df.y=='no']

fig = {
    'data': [
  		{
  			'x': df_yes.duration,
        	'y': df_yes.age,
        	'text': df_yes.y,
        	'mode': 'markers',
        	'name': 'yes'},
        {
        	'x': df_no.duration,
        	'y': df_no.age,
        	'text': df_no.y,
        	'mode': 'markers',
        	'name': 'no'}
    ],
    'layout': {
        'xaxis': {'title': 'Duration of call'},
        'yaxis': {'title': "Age of client"}
    }
}

plotly.offline.plot(fig)

'''
yes_t = df_yes.size
no_t = df_no.size
fig_pie = {
    'data': [{'labels': ['Yes', 'No '],
              'values': [yes_t, no_t],
              'type': 'pie'}],
    'layout': {'title': 'How many deposits were issued'}
     }

plotly.offline.plot(fig_pie)
'''