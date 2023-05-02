import random

#This function builds the network
def get_network(filename):
  f = open(filename, "r")
  network = []
  connection = ("", "")
  while connection[1] != "V":
    #Turns each router connection into tuples
    connection = tuple(f.readline()[:-1].split("|"))
    network.append(connection)
  f.close()
  return network

def build_network(network):
  graph = {}
  for connection in network:
    graph[connection[0]] = connection[1]
  return graph

def node_sampling(graph, attackers, users, probability, rate):
  #Sets up the packets marked dictionary with each router having its id as a key and the amount of packets marked in its name as its value
  packets_marked = {}
  for key in graph:
    packets_marked[key] = 0


  #to_be_marked is the packet that is the last packet marked
  to_be_marked = ""
  num_packets = 0
  current_packet = ""

  #Puts the attackers' routes in a list in order
  attackers_routes = []
  for _ in range(len(attackers)):
    attackers_routes.append([])
  current_index = 0
  for attacker in attackers:
    key = attacker
    while "V" != key:
      attackers_routes[current_index].append(key)
      key = graph[key]
    current_index+=1

  # Gets all the user nodes
  user_nodes = []
  all_attackers =  [attacker for sublist in attackers_routes for attacker in sublist]
  for key in graph:
    if key not in all_attackers:
      user_nodes.append(key)

  # print(attackers_routes)
  # print(user_nodes)
  #Iterates until the routers are in the correct order, this makes sure that it is accurate
  finished = False
  while True:
    # print(packets_marked)
    for route in attackers_routes:
      for i in range(len(route)-1):
        if packets_marked[route[i]] >= packets_marked[route[i+1]]:
          finished = False
          break
        else:
          finished = True
      if not finished:
        break
    #Checks if attackers have sent a greater number of packets than any innocent routers
    for attacker in attackers:
      for user_node in user_nodes:
        if packets_marked[user_node] > packets_marked[attacker]:
          finished = False
          break
      if not finished:
        break
    

    if 0 in packets_marked.values():
      finished = False

    if finished:
      break

    # print(packets_marked)
      

    
    #Sends the packets
    for user in users:
      to_be_marked = ""
      num_packets+=1
      current_packet = user

      #Traverses graph from user to victim
      while "V" != current_packet:
        if random.random() < probability:
          to_be_marked = current_packet
        current_packet = graph[current_packet]
      if to_be_marked != "":
        packets_marked[to_be_marked] += 1

    for _ in  range(rate):
      # print(packets_marked)
      for attacker in attackers:
        to_be_marked = ""
        num_packets+=1
        current_packet = attacker

        #Traverses graph from user to victim
        while "V" != current_packet:
          if random.random() < probability:
            to_be_marked = current_packet
          current_packet = graph[current_packet]
        if to_be_marked != "":
          packets_marked[to_be_marked] += 1
  

  return packets_marked, num_packets

######################################################################################################################################################

def edge_sampling(graph, attackers, users, probability, rate):
  packets_marked = {}
  for key in graph:
    packets_marked[key + " | " + graph[key]] = 0

  #Puts the attackers' routes in a list in order
  attackers_routes = []
  for _ in range(len(attackers)):
    attackers_routes.append([])
  current_index = 0
  for attacker in attackers:
    current_attacker = attacker
    while "V" != current_attacker:
      attackers_routes[current_index].append(current_attacker + " | " + graph[current_attacker])
      current_attacker = graph[current_attacker]
    current_index+=1


  users_routes = []
  for _ in range(len(users)):
    users_routes.append([])
  current_index = 0
  for user in users:
    current_user = user
    while "V" != current_user:
      users_routes[current_index].append(current_user + " | " + graph[current_user])
      current_user = graph[current_user]
    current_index+=1

  attackers_costs = {}
  users_costs = {}

  for route in attackers_routes:
    attackers_costs[route[0]] = 0
  for route in users_routes:
    users_costs[route[0]] = 0

  # print(attackers_routes)

  current_cost = 0
  num_packets = 0

  finished = False
  while True:

    for route in attackers_routes:
      costs_key = route[0]
      current_cost = 0
      for node in route:
        current_cost += packets_marked[node]
      attackers_costs[costs_key] = current_cost
    for route in users_routes:
      costs_key = route[0]
      current_cost = 0
      for node in route:
        current_cost += packets_marked[node]
      users_costs[costs_key] = current_cost

    for a_cost in attackers_costs:
      for u_cost in users_costs:
        if attackers_costs[a_cost] > users_costs[u_cost]:
          finished = True
        else:
          finished = False
          break
      if not finished:
        break


    for route in attackers_routes:
      for i in range(len(route)-1):
        if packets_marked[route[i]] >= packets_marked[route[i+1]]:
          finished = False
          break
        else:
          finished = True
      if not finished:
        break

    if 0 in packets_marked.values():
      finished = False


    if finished:
      break
      
    
    #Sends the packets
    for user in users:
      num_packets+=1
      current_packet = user
      to_be_marked = ""

      #Traverses graph from user to victim
      while "V" != current_packet:
        edge = current_packet+" | "+graph[current_packet]
        if random.random() < probability:
          to_be_marked = edge
        current_packet = graph[current_packet]
      if to_be_marked != "":
        packets_marked[to_be_marked] += 1

    for _ in range(rate):
      for attacker in attackers:
        to_be_marked = ""
        num_packets+=1
        current_packet = attacker

        #Traverses graph from user to victim
        while "V" != current_packet:
          edge = current_packet+" | "+graph[current_packet]
          if random.random() < probability:
            to_be_marked = edge
          current_packet = graph[current_packet]
        if to_be_marked != "":
          packets_marked[to_be_marked] += 1

  return packets_marked, num_packets, users_costs, attackers_costs



# def get_users(graph, attackers):
#   users = []
#   for connection in graph:
#     if 'U' in connection and connection not in attackers:
#       users.append(connection)     
#   return attackers, users  

def randomize_attacker(graph, num_attackers):
  attackers = []
  users = []
  for connection in graph:
    if 'U' in connection:
      users.append(connection)
  for _ in range(num_attackers):
    attacker = random.choice(users)
    users.remove(attacker)
    attackers.append(attacker)
  return attackers, users
  
  



probability = float(input("\nPacket mark probability (0.2, 0.4, 0.5, 0.6, 0.8): "))
rate = int(input("Input x times more packets than the normal user the attacker should pump (x = 10, 100, 1000): "))
method = int(input("Input '0' for node sampling and '1' for edge sampling: "))
net = int(input("Input '3' for 3 branch network, '4' for 4 branch, and '5' for 5 branch: "))
num_attackers = int(input("Input the amount of attackers you want (should be less than number of branches): "))
print()

if net == 3:
  filename = "branch3.txt"
elif net == 4:
  filename = "branch4.txt"
else:
  filename = "branch5.txt"
graph = build_network(get_network(filename))
attackers, users = randomize_attacker(graph, num_attackers)
if method == 0:
  packets_marked, packets_sent = node_sampling(graph, attackers, users, probability, rate)
  packets_marked = sorted(packets_marked.items(), key=lambda x:x[1])
  print("Node sampling: ")
  print(packets_marked)
  print("Number of packets:", packets_sent)
else:
  packets_marked, packets_sent, users_costs, attackers_costs = edge_sampling(graph, attackers, users, probability, rate)
  packets_marked = sorted(packets_marked.items(), key=lambda x:x[1])
  print("Edge sampling: ")
  print(packets_marked)
  print("Number of packets:", packets_sent)
  print(users_costs)
  print(attackers_costs)

print(attackers)
print(users)

