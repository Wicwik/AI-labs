import pandas as pd
from pgmpy.models import NaiveBayes
from pgmpy.inference import VariableElimination

#Lod dataset
exams = pd.read_csv('exams.csv')


# First question
model = NaiveBayes()
#add all independent evidence features
model.add_edges_from([('passed', 'has_time'), ('passed','wants_to'), ('passed', 'studying')])

#train the model to classify the 'passed' variable
#for other variables you meight want to change the model
model.fit(exams, 'passed')

#predict most probable outcome based on evidence
inference = VariableElimination(model)
prediction = inference.map_query(['passed'], evidence = {'has_time':1,'wants_to':1,'studying':1})
print("Prediction (passed1):", prediction)

print()

# Second question
inference = VariableElimination(model)
prediction = inference.map_query(['passed'], evidence = {'has_time':0,'wants_to':1,'studying':0})
print("Prediction (passed2):", prediction)

for cpd in model.get_cpds():
    print(cpd)

print()

# Third question
model = NaiveBayes()
model.add_edges_from([('has_time', 'passed'), ('has_time','wants_to'), ('has_time', 'studying')])

model.fit(exams, 'has_time')
inference = VariableElimination(model)
prediction = inference.map_query(['has_time'], evidence = {'passed':1,'wants_to':0,'studying':0})
print("Prediction (has_time):", prediction)

for cpd in model.get_cpds():
    print(cpd)

print()

# Fourth question
model = NaiveBayes()
model.add_edges_from([('wants_to', 'has_time'), ('wants_to','passed'), ('wants_to', 'studying')])

model.fit(exams, 'wants_to')
inference = VariableElimination(model)
prediction = inference.map_query(['wants_to'], evidence = {'passed':0,'has_time':1,'studying':2})
print("Prediction (wants_to):", prediction)

for cpd in model.get_cpds():
    print(cpd)

print()

# Fifth question
model = NaiveBayes()
model.add_edges_from([('studying', 'has_time'), ('studying','wants_to'), ('studying', 'passed')])

model.fit(exams, 'studying')
inference = VariableElimination(model)
prediction = inference.map_query(['studying'], evidence = {'passed':1,'has_time':1,'wants_to':0})
print("Prediction (studying):", prediction)

for cpd in model.get_cpds():
    print(cpd)