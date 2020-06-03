import random
import math
import scipy.stats

def day_analysis(time, arr_total ,arr_home, arr_pickup, deliveries_paid, deliveries_oc, deliveries_pickup, locker, home, pickup, oc_reward):
	acc_pf = 0
	acc_oc = 0 
	acc_lckr = 0
	acc_costs = 0

	print("\n\nDAY   |  NEW PACKAGES (10-50) |       DELIVERIES       | ACCUMULATED DELIVERIES |           COSTS            | LOCKER STATUS         |")
	print(" t    |  total   home   lckr  |   pf      oc     lckr  |   pf      oc     lckr  |  pf           oc       ACC |  home    lckr   total |")
	print("----- | --------------------- | ---------------------- | ---------------------- | -------------------------- | --------------------- |")
	for i in range(0, time+1):
		acc_pf = acc_pf + deliveries_paid[i]
		acc_oc = acc_oc + deliveries_oc[i]
		acc_lckr = acc_lckr + deliveries_pickup[i]
		acc_costs = acc_costs + calculate_cost_oc(i,deliveries_oc, oc_reward) + calculate_cost_paid(i,deliveries_paid)

		print("%3d   |   %3d    %3d    %3d   |   %3d     %3d     %3d  |  %5d   %5d   %5d |%7.2f   %7.2f   %7.2f | %4d   %4d     %4d  |" %
			(i, arr_total[i], arr_home[i], arr_pickup[i], deliveries_paid[i], deliveries_oc[i], deliveries_pickup[i], acc_pf, acc_oc, acc_lckr, 
			# costs and locker status
			calculate_cost_paid(i,deliveries_paid), calculate_cost_oc(i,deliveries_oc, oc_reward) , acc_costs , home[i], pickup[i], locker[i]))

	#print("INVENTORY: ","locker:",locker[day], "home:", home[day],"pickup:", pickup[day])
	#print("DEPARTURES:", "pickup:", del_pickup[day],"(oc:" ,deliveries_oc[day], ")", " and paid", deliveries_paid[day])

	return

def estimated_package_arrivals():
	return round(random.uniform(10,50))

def calculate_cost_paid(i, deliveries_paid):
	cost = 0;
	if deliveries_paid[i] < 11:
		cost = cost + deliveries_paid[i]
	else:
		cost = 10 + cost + 2 * (deliveries_paid[i] - 10) 
	return cost

def calculate_cost_oc(i, deliveries_oc, oc_reward):
	return deliveries_oc[i] * oc_reward


def calculate_cost(i, deliveries_paid, deliveries_oc, oc_reward):
	cost = 0;
	if deliveries_paid[i] < 11:
		cost = cost + deliveries_paid[i]
	else:
		cost = 10 + cost + 2 * (deliveries_paid[i] - 10) 
	cost = cost + deliveries_oc[i] * oc_reward
	return cost

def calculate_cost_oc(i, deliveries_oc, oc_reward):
	return deliveries_oc[i] * oc_reward

	
	
def prob_pickup_or_home():
	if random.random() < 0.5:
		return 0
	else: return 1

def prob_pickup(pickup_rate):
	if random.random() < pickup_rate:
		return 1
	else: return 0

def prob_oc(oc_probability):
	if random.random() < oc_probability:
		return 1
	else: return 0


def simulate(time, pickup_rate,oc_probability, oc_reward):
	
	locker = []
	home = []
	pickup = []
	# deliviries list
	del_oc = []	
	del_paid = []
	del_pickup = []
	#arrival list
	arr_home = []
	arr_pickup = []
	arr_total = []

	for i in range(0, time+3 ):
		locker.append(0)
		home.append(0)
		pickup.append(0)

		del_oc.append(0)
		del_paid.append(0)
		del_pickup.append(0)
		
		arr_home.append(0)
		arr_pickup.append(0)
		arr_total.append(0)
	
	# Contador total_packages é responsavel por contar quantas encomendas passam pela loja.
	total_packages = 0

	#simulation starts
	for i in range(1,time+1):
		# Dia começa por assumir as encomendas no fechar da loja para o dia seguinte.
		# Apos isso, chegam as encomendas aleatorias
		pickup[i] = pickup[i-1] + pickup[i]
		home[i] = home[i-1] + home[i]
		locker[i] = locker[i-1] + locker[i]

		# +++ ARRIVAL of PACKAGES +++
		# é gerado um numero aleatorio de encomendas a chegar
		epa = estimated_package_arrivals()
		total_packages = total_packages + epa
		locker[i] = locker[i] + epa
		arr_total[i] = epa
		# por cada encomenda j é randomizada a probabilidade 
		# de ser home or pickup conforme o enunciado.
		pickups_day=0
		home_day=0
		for j in range(0,epa):
			if prob_pickup_or_home():
				home_day = home_day + 1
			else: pickups_day = pickups_day + 1

		arr_pickup[i] = home_day
		arr_home[i] = pickups_day
		home[i] = home[i] + home_day
		pickup[i] = pickup[i] + pickups_day
		
		# Neste momento, numero max de encomendas atingidas no dia. 
		# A partir de aqui, as encomendas comecam a ser entregues.

		# --- DEPARTURES --- #
		# por cada encomenda para pickup, e randomizado a prob de ser levantanda.

		pu_size = pickup[i]
		for k in range(1,pu_size):
			if prob_pickup(pickup_rate):
				pickup[i] = pickup[i] - 1 
				locker[i] = locker[i] - 1
				del_pickup[i] = del_pickup[i] + 1

				# encomenda é levantada
				# Se existirim encomendas para serem entregues em casa
				if(home[i] + home[i+1] > 0):
					# E o pickup aceitar ser oc 
					if(prob_oc(oc_probability)):
						home[i] = home[i] - 1
						del_oc[i] = del_oc[i] + 1
						locker[i] = locker[i] - 1
						# pickup (oc) faz uma entrega em casa
					
					else: 
						#delivered by paid fleep
						#senao a encomenda é entregue no dia seguinte pela frota paga
						home[i+1] = home[i+1] - 1
						del_paid[i+1] = del_paid[i+1] + 1
						locker[i+1] = locker[i+1] - 1

		# DIA Termina apos todas as probabilidades de pickup serem calculadas
	
	
	day_analysis(i,arr_total, arr_home, arr_pickup, del_paid, del_oc, del_pickup, locker, home, pickup, oc_reward)
	#simulation ends
	#print("\nmax locker packages at closing:", max(locker))
	#print("total packages counter equal to total arrivals?:", sum(arr_total) == total_packages, "\n" ,total_packages ," - ", sum(arr_total))
	# total cost: 
	total_cost = 0
	oc_cost = 0
	paid_cost = 0
	for h in range(1,time+1):
		total_cost = total_cost + calculate_cost_oc(h,del_oc, oc_reward) + calculate_cost_paid(h,del_paid)
		oc_cost = oc_cost + calculate_cost_oc(h,del_oc, oc_reward)
		paid_cost = paid_cost +  calculate_cost_paid(h,del_paid)
	#print("total cost until day", h,":" , round(total_cost,3))
	return total_packages, total_cost , max(locker), oc_cost, paid_cost;

def mean_confidence_interval(data,alpha):
		n = len(data)
		m = float(sum(data))/n
		var = sum([(x-m)**2 for x in data]) / float(n-1)
		tfact = scipy.stats.t._ppf(1-alpha/2., n-1)
		h = tfact * math.sqrt(var/n)
		return m-h, m+h

if __name__ == "__main__":
	time = 120
	pickup_prob = .75
	oc_probab = [.01, .25, .5, .6,  .75]
	oc_cost = [0, 0.5, 1, 1.5, 1.8]

	confidence = .99
	alpha = 1 - confidence
	observations = 10000
	

	results_total_packages =[]
	results_total_cost=[]
	results_max_locker = []
	results_expected_reward_total =[]
	results_expected_pf_total =[]

	for k in range(0,5):

		for i in range(observations):
			x = simulate(time, pickup_prob, oc_probab[k], oc_cost[k])
			results_total_packages.append(x[0])
			results_total_cost.append(x[1])
			results_max_locker.append(x[2])
			results_expected_reward_total.append(x[3])
			results_expected_pf_total.append(x[4])

		print("\n\n*****************************************",  file=open("solution", "a"))
		print("PICKUP being OC Probability:" , oc_probab[k],"\nOC Compensation:" ,oc_cost[k],  file=open("solution", "a"))

		print("*****************************************",  file=open("solution", "a"))
		print ("1 (A)",  file=open("solution", "a"))
		#print("\nMean confidence interval of total OC compesantion: " ,mean_confidence_interval(results_expected_reward_total,alpha),  file=open("solution", "a"))
		#print("Mean confidence interval of total PAID FLEET cost: " ,mean_confidence_interval(results_expected_pf_total,alpha),  file=open("solution", "a"))
		print("Mean total cost: " ,mean_confidence_interval(results_total_cost,alpha),  file=open("solution", "a"))
		print("Max total cost: " ,max(results_total_cost)) #,  file=open("solution", "a"))

		print ("1 (B)",  file=open("solution", "a"))
		print("Mean  confidence interval of max locker capacity: " ,mean_confidence_interval(results_max_locker,alpha),  file=open("solution", "a"))
		print("Maximum locker capacity in all simulations: " , max(results_max_locker),  file=open("solution", "a"))

		#print ("\n\nOTHER IMPORTANT DATA",  file=open("solution", "a"))
		#print("\nMean confidence interval of packages handled: " , mean_confidence_interval(results_total_packages,alpha),  file=open("solution", "a"))
		#print("\nMax total OC compesantion: " ,max(results_expected_reward_total),  file=open("solution", "a"))
		#print("Min total OC compesantion: " ,min(results_expected_reward_total),  file=open("solution", "a"))
		#print("\nMax total PAID FLEET cost: " ,max(results_expected_pf_total),  file=open("solution", "a"))
		#print("Min total PAID FLEET cost: " ,min(results_expected_pf_total),  file=open("solution", "a"))

		results_total_packages =[]
		results_total_cost=[]
		results_max_locker = []
		results_expected_reward_total =[]
		results_expected_pf_total =[]
