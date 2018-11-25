from scipy.stats import norm
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
import random
import numpy as np
import collections


"""
pred_data = [ collections.deque(maxlen=30) for i in range(96)]
pred_data[0].append(10)
pred_data[0].append(8)
pred_data[0].append(7.5)
pred_data[0].append(7.5)
pred_data[0].append(7.5)
pred_data[0].append(2)

N = 100
np.random.seed(1)
#X = np.concatenate((np.random.normal(0, 1, int(0.3 * N)),
#                    np.random.normal(5, 1, int(0.7 * N))))[:, np.newaxis]

X = np.array(pred_data[0]).reshape(-1,1)

X_plot = np.linspace(-5, 10, 1000)[:, np.newaxis]

true_dens = (0.3 * norm(0, 1).pdf(X_plot[:, 0])
             + 0.7 * norm(5, 1).pdf(X_plot[:, 0]))

fig, ax = plt.subplots()
ax.fill(X_plot[:, 0], true_dens, fc='black', alpha=0.2,
        label='input distribution')


kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(X)
log_dens = kde.score_samples(X_plot)
ax.plot(X_plot[:, 0], np.exp(log_dens), '-',
        label="kernel = '{0}'".format('gaussian'))

ax.text(6, 0.38, "N={0} points".format(N))

ax.legend(loc='upper left')
ax.plot(X[:, 0], -0.005 - 0.01 * np.random.random(X.shape[0]), '+k')

#ax.set_xlim(-4, 9)
#ax.set_ylim(-0.02, 0.4)

print(kde.sample([10]))
plt.show()

"""

class kde_model():
    def __init__(self, time_slots, queue_len):
        self.time_slots = time_slots
        self.queue_len = queue_len
        self.pred_data = [collections.deque(maxlen=self.queue_len) for i in range(self.time_slots)]


    def add_observation(self, time_slot, value):
        self.pred_data[time_slot].append(value)
        return True

    def get_prediction(self, time_slot):
        if len(self.pred_data[time_slot]) > 0:
            kde = KernelDensity(kernel='gaussian', bandwidth=5).fit(np.array(self.pred_data[time_slot]).reshape(-1,1))
            return kde.sample(1)
        else:
            return False





if __name__ == '__main__':

    mdl = kde_model(96,5)

    mdl.add_observation(1, 55)
    mdl.add_observation(1, 54)
    mdl.add_observation(1, 25)
    mdl.add_observation(1, 55)
    mdl.add_observation(1, 10)
    mdl.add_observation(1, 10)
    mdl.add_observation(1, 10)
    mdl.add_observation(1, 10)
    mdl.add_observation(1, 10)
    mdl.add_observation(1, 10)


    print(mdl.get_prediction(1))
    print(mdl.get_prediction(0))


