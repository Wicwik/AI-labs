from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD, State
from pgmpy.sampling import BayesianModelSampling

model = BayesianNetwork([('T', 'W'), ('E', 'W'), ('T', 'S'), ('D', 'S')])

cpd_t = TabularCPD('T', 3, [[3/10], [1/5], [1/2]])
cpd_d = TabularCPD('D', 2, [[1/10], [9/10]])
cpd_e = TabularCPD('E', 2, [[6/18], [12/18]])
cdp_w = TabularCPD('W', 2, [
    [2/10, 2/10, 1, 9/10, 1/10, 0],
    [8/10, 8/10, 0, 1/10, 9/10, 1]
], evidence=['T', 'E'], evidence_card=[3,2])

cdp_s = TabularCPD('S', 2, [
    [1, 0, 0, 1, 0, 1],
    [0, 1, 1, 0, 1, 0]
], evidence=['T', 'D'], evidence_card=[3, 2])

model.add_cpds(cpd_t, cpd_d, cpd_e, cdp_w, cdp_s)
model.get_cpds()
model.check_model()

evidence = [State(var='E', state=0), State(var='W', state=0)]

inference = BayesianModelSampling(model)
data = inference.rejection_sample(evidence=evidence, size=1000)
model.fit(data)

print('Probabilities of trams for question 1 [4,5,9]:', model.get_cpds()[0].values)

model = BayesianNetwork([('T', 'W'), ('E', 'W'), ('T', 'S'), ('D', 'S')])
model.add_cpds(cpd_t, cpd_d, cpd_e, cdp_w, cdp_s)
model.get_cpds()
model.check_model()

evidence = [State(var='T', state=2)]

inference = BayesianModelSampling(model)
data = inference.rejection_sample(evidence=evidence, size=1000)
model.fit(data)

print('Probabilities of wagons for question 2 (first column means evening is true and seconds means evening is false):', model.get_cpds()[3].values)
