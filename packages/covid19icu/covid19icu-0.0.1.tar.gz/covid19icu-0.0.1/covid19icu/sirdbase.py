from scipy.integrate import odeint, RK45, solve_ivp
from numpy import array, sqrt, linspace, insert, cumsum
from numpy.random import normal
from scipy.ndimage.filters import uniform_filter1d
from pylab import *
import sys
import cma

color_dict = {
	#("susceptibles", 0) : "#FF0000",
	("positives", 0) : "#FF0000",
	("deaths", 0) : "navy",
	("recovered", 0) : "yellow",
	("acutecare", 0): "#FF00FF",

	#("susceptibles", 1) : "994444",
	("positives", 1) : "#FF8C00",
	("deaths", 1) : "navy",
	("recovered", 1) : "orange",
	("acutecare", 1): "#AA77ff",
	
	#("susceptibles", 2) : "darkgreen",
	("positives", 2) : "#77DD00",
	("deaths", 2) : "navy",
	("recovered", 2) : "orange",
	("acutecare", 2): "#66CCCC",	

	#("susceptibles", 3) : "darkgreen",
	("positives", 3) : "#220000",
	("deaths", 3) : "navy",
	("recovered", 3) : "orange",
	("acutecare", 3): "#339933",	
}

def generate_dates(begin, end):
	import datetime
	if isinstance(end, str):
		start_date = datetime.date.fromisoformat(begin) 
		end_date = datetime.date.fromisoformat(end) 
		delta = end_date-start_date
		print_dates = [start_date + datetime.timedelta(i) for i in range(delta.days)]
		return print_dates
	elif isinstance(end, int):
		start_date = datetime.date.fromisoformat(begin) 
		print_dates = [start_date + datetime.timedelta(i) for i in range(end)]
		return print_dates


def fitness2(x, arguments, normalize=False, verbose=False):
	if verbose:
		import time
		start = time.time()
	x0 = arguments['x0']
	tmax = arguments['tmax']
	sampling_time = arguments['sampling_time']
	integrator = arguments['integrator']
	beta,gamma,delta, S = x
	x0[0] = S
	SM = SIRDsim()
	tsT, tsS, tsI, tsR, tsD = SM.simulate(x0, beta=beta, 
		gamma=gamma, delta=delta, tmax=tmax,  
		sample=arguments['sampling_time'], integrator=integrator)
	if len(tsI)!=len(arguments['positive']):
		print("Error ###")
		return sys.float_info.max
		exit()
	N = len(sampling_time)
	if normalize:
		 RMSE_I = abs(tsI - arguments['positive'])/(1+arguments['positive'])
		 RMSE_R = abs(tsR - arguments['recovered'])/(1+arguments['recovered'])
		 RMSE_D = abs(tsD - arguments['dead'])/(1+arguments['dead'])

		 RMSE_I = sum(RMSE_I)/N
		 RMSE_R = sum(RMSE_R)/N
		 RMSE_D = sum(RMSE_D)/N

	else:
		RMSE_I = sqrt(sum((tsI - arguments['positive'])**2)/N)
		RMSE_R = sqrt(sum((tsR - arguments['recovered'])**2)/N)
		RMSE_D = sqrt(sum((tsD - arguments['dead'])**2)/N)
	final_fitness = (RMSE_I + RMSE_R + RMSE_D)/3
	if verbose:
		end = time.time()
		print ("- calculated fitness: %.3f [%.2f s]" % (final_fitness, end-start))
	return final_fitness


def _SIRD_simulation_step(t, x0, beta, gamma, delta, tau=1.):

	# unpack current state
	S, I, R, D = x0
	
	# susceptible
	dS = (-beta*S*I)*tau

	# infected (officially)
	dI = (beta*S*I-gamma*I-delta*I)*tau

	# removed (cured)
	dR = (gamma*I)*tau

	# removed (cured + dead)
	dD = (delta*I)*tau

	return array([dS, dI, dR, dD])



def _SIRD_simulation_step_lsoda(x0, t, beta, gamma, delta):

	# unpack current state
	S, I, R, D = x0

	# susceptible
	dS = -beta*S*I

	# infected (officially)
	dI = beta*S*I-gamma*I-delta*I

	# removed (cured)
	dR = gamma*I

	# removed (cured + dead)
	dD = delta*I

	return array([dS, dI, dR, dD])

class SIRDsim(object):

	def __init__(self):
		pass

	def simulate(self, x0, beta, gamma, delta, tmax, event=None, 
		sample=None, integrator="Euler", tau=1e-4):
		
		if integrator == "LSODA":
			sol = odeint(
				_SIRD_simulation_step_lsoda, x0, sample, 
				atol=1, rtol=1e-3, 
				args=(beta, gamma, delta)).T

		elif integrator == "Euler":

			t = sample[0]
			ts_S = []
			ts_I = []
			ts_R = []
			ts_D = []
			ts_T = []
			snum = 0

			x=x0[:]

			while(t<tmax):
				x += _SIRD_simulation_step(t, x0, beta=beta, gamma=gamma, delta=delta, tau=tau)
				
				if snum<len(sample):
					if t>sample[snum]:
						ts_S.append(x[0])
						ts_I.append(x[1])
						ts_R.append(x[2])
						ts_D.append(x[3])
						ts_T.append(t)
						snum+=1

				t += tau
			return array([ts_T, ts_S, ts_I, ts_R, ts_D])
		elif integrator=="RK45":

			sol = solve_ivp(
				_SIRD_simulation_step, 
				t_span=(sample[0], sample[-1]),
				t_eval=sample, 
				y0=x0,
				args=(beta, gamma, delta)
				)
			
			sol = sol.y

		else:
			raise Exception("Integration method not supported")
			exit()

		return array([sample, sol[0], sol[1], sol[2], sol[3]])


class SIRD_model(object):

	def __init__(self):
		self._dates = None
		self._tspositives = None
		self._tsrecovered = None
		self._tsdeaths = None
		self._tsacutecare = None
		self._S = 0
		self._simulator = SIRDsim()

		self._beta = None
		self._gamma = None
		self._delta = None

		self._phi = 0.08
		self._tau = 5

		self._x0 = [0,0,0,0]

		self._model_simulator = SIRDsim()


	def import_data(self, 
		pop_size,
		ts_positives,
		ts_recovered,
		ts_deaths,
		ts_acutecare = None,
		acute_care_beds = None,
	):
		self._dates = range(len(ts_positives))
		self._tspositives = ts_positives
		self._tsrecovered = ts_recovered
		self._tsdeaths    = ts_deaths
		self._tsacutecare = ts_acutecare
		self._acute_care_beds = acute_care_beds

		self._x0 = [pop_size, self._tspositives[0], self._tsrecovered[0], self._tsdeaths[0]]


	def calibrate(self, max_iter=150, 
		swarm_size=150, excludepoints=None, use_fstpso=True,
		integrator="LSODA"):	
		
		from fstpso import FuzzyPSO

		lts = len(self._tspositives[:excludepoints])

		all_data = {
			'positive': self._tspositives[:excludepoints],
			'recovered': self._tsrecovered[:excludepoints],
			'dead': self._tsdeaths[:excludepoints],
			'sampling_time': range(lts),
			'x0': self._x0,
			'tmax': lts,
			'integrator': integrator
		}

		self._S = self._x0[0]

		# heuristic for search space
		min_positive = max(self._tspositives[:excludepoints])*10
		max_positive = self._x0[0]*.1

		if use_fstpso: 
			FS = FuzzyPSO()
			FS.set_fitness(fitness2, arguments=all_data)
			FS.set_search_space([
				[1e-10, 1e-3],  			# S->I
				[1e-7, 1e0], 
				[1e-7, 1e0], 
				[min_positive, max_positive]] 
				)

			FS.set_swarm_size(swarm_size)
			FS.disable_fuzzyrule_minvelocity()

			res, fit = FS.solve_with_fstpso(max_iter=max_iter, 
				creation_method={'name': 'logarithmic'},
				)
		

		self._beta  = res.X[0]
		self._gamma = res.X[1]
		self._delta = res.X[2]
		self._x0[0] = res.X[3]

		print("Result: beta=%e, gamma=%e, delta=%e, S0=%e" % (self._beta, self._gamma, self._delta, self._x0[0]), "with fitness:", fit)
		print("Calibrated model ready to simulate.")
		return array([self._beta, self._gamma, self._delta, self._x0[0], fit])

	def simulate_model(self, x0, tmax, samples=None, events=[], integrator="Euler"):	
		x0[0] = self._x0[0]
		
		if samples is None:	samples = linspace(0, tmax, 1000)

		updated_events = events + [[tmax, 0]] # dummy termination event
		
		simulation_data = None; countevents = 0; t0 = 0

		local_beta = self._beta

		for event_time, ratio in updated_events:
			
			chunk_time = [z for z in samples if (z>=t0  and z<=event_time)]
			
			result_chunk = self._model_simulator.simulate(
				x0, 
				beta=local_beta, 
				gamma=self._gamma, 
				delta=self._delta, 
				tmax=event_time, 
				sample=chunk_time, 
				integrator=integrator)

			if simulation_data is None: 
				simulation_data = result_chunk
			else:
				simulation_data = concatenate((simulation_data, result_chunk), axis=1)
			countevents +=1
			
			t0 = result_chunk[0][-1]
			x0 = [result_chunk[1][-1], result_chunk[2][-1], result_chunk[3][-1], result_chunk[4][-1]]
			
			if event_time!=tmax: local_beta *= ratio
				
		return array(simulation_data)


	def _est_acutecare(self, infected):
		return [infected[0]*self._phi]*self._tau + list(infected*self._phi)[:-self._tau]


	def plot_fit(self, ax, tmax, 
		samples=None, hide=[], events=[], 
		integrator="LSODA",
		excludepoints=None, comment="", style=0 ):

		x0 = self._x0

		#x0[0] = self._x0[0]
		tt, susc, infe, reco, deat = self.simulate_model(x0, tmax=tmax, samples=samples, events=events, integrator=integrator)

		acutecare = self._est_acutecare(infe)	

		from scipy.signal import savgol_filter

		if not "Infected" in hide:
			ax.plot(tt,infe, label="Infected (simulated) %s" % comment, color=color_dict[("positives", style)])
		if not "Recovered" in hide:
			ax.plot(tt,reco, label="Recovered (simulated) %s" % comment, color=color_dict[("recovered", style)])
		if not "Deaths" in hide:
			ax.plot(tt,deat, label="Deceased (simulated) %s" % comment, color=color_dict[("deaths", style)])
		if not "Estacutecare" in hide:
			ax.plot(tt,acutecare, "--", label="ICU patients (estimated) %s" % comment, color=color_dict[("acutecare", style)])

		# scatter plot experimental data
		if not "Positives-data" in hide:
			ax.scatter(list(self._dates)[:excludepoints], list(self._tspositives)[:excludepoints], label="Infected (real data)", edgecolor="gray", c=color_dict[("positives", style)])
			#ax.scatter(list(self._dates)[:], list(self._tspositives)[:], label="Infected (real data)", edgecolor="gray", c=color_dict[("positives", style)])
		if not "Recovered-data" in hide:
			ax.scatter(list(self._dates[:excludepoints]), list(self._tsrecovered)[:excludepoints], label="Recovered (real data)", linewidth=0.5, edgecolor="gray", c=color_dict[("recovered", style)])
		if not "Deaths-data" in hide:
			ax.scatter(list(self._dates[:excludepoints]), list(self._tsdeaths)[:excludepoints], label="Deceased (real data)", linewidth=0.5, edgecolor="gray", c=color_dict[("deaths", style)])
		if not "Acutecare-data" in hide:
			if self._tsacutecare is not None:
				ax.scatter(list(self._dates[:excludepoints]), list(self._tsacutecare)[:excludepoints], label="ICU patients (real data)", linewidth=0.5, edgecolor="gray", c=color_dict[("acutecare", style)])
		
		if not "Limit" in hide:
			if self._acute_care_beds is not None:
				ax.axhline(self._acute_care_beds, linestyle=":", linewidth=0.5, color="black", label="Limit ICU beds", alpha=0.8)

		if not "Halflimit" in hide:
			if self._acute_care_beds is not None:
				ax.axhline(self._acute_care_beds/2, linestyle="-", linewidth=0.5, color="black", label="Limit ICU beds (for COVID-19 patients)", alpha=0.8)

		ax.set_ylabel("Number of individuals")
		ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

		return tt, susc, infe, reco, deat,  acutecare

if __name__ == '__main__':
	pass 