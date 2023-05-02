import main
import random

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
graph = main.build_network(main.get_network(filename))
attackers, users = main.randomize_attacker(graph, num_attackers)
if method == 0:
  packets_marked, packets_sent = main.node_sampling(graph, attackers, users, probability, rate)
  packets_marked = sorted(packets_marked.items(), key=lambda x:x[1])
  print("Node sampling: ")
  print(packets_marked)
  print("Number of packets:", packets_sent)
else:
  packets_marked, packets_sent, users_costs, attackers_costs = main.edge_sampling(graph, attackers, users, probability, rate)
  packets_marked = sorted(packets_marked.items(), key=lambda x:x[1])
  print("Edge sampling: ")
  print(packets_marked)
  print("Number of packets:", packets_sent)
  print(users_costs)
  print(attackers_costs)

print(attackers)
print(users)
