import unittest
import main

class unit_test_sampling_algorithms(unittest.TestCase):
    def setUp(self):
        self.network=[('U1', 'R14'), ('R14', 'R11'), ('R11', 'R8'), ('R8', 'R5'), ('R5', 'R3'), ('R3', 'R2'), ('R2', 'R1'), ('U2', 'R15'), ('R15', 'R12'), ('R12', 'R9'), ('R9', 'R6'), ('R6', 'R3'), ('U3', 'R17'), ('R17', 'R16'), ('R16', 'R13'), ('R13', 'R10'), ('R10', 'R7'), ('R7', 'R4'), ('R4', 'R2'), ('R1', 'V')]
        self.graph={'U1': 'R14', 'R14': 'R11', 'R11': 'R8', 'R8': 'R5', 'R5': 'R3', 'R3': 'R2', 'R2': 'R1', 'U2': 'R15', 'R15': 'R12', 'R12': 'R9', 'R9': 'R6', 'R6': 'R3', 'U3': 'R17', 'R17': 
'R16', 'R16': 'R13', 'R13': 'R10', 'R10': 'R7', 'R7': 'R4', 'R4': 'R2', 'R1': 'V'}
        self.attackers=["U2"]
        self.users=["U1","U3"]
        self.probability=0.2
        self.rate=10
        self.attackers_route_node=["U2","R15","R12","R9","R6","R3","R2","R1"]
        self.attackers_route_edge=['U2 | R15', 'R15 | R12', 'R12 | R9', 'R9 | R6', 'R6 | R3', 'R3 | R2', 'R2 | R1', 'R1 | V']
    
    def test_get_network(self):
        self.assertEqual(main.get_network("branch3.txt"), self.network)

    def test_build_network(self):
        self.assertEqual(main.build_network(self.network), self.graph)

    def test_randomize_attacker(self):
        attackers, users = main.randomize_attacker(self.graph, 1)
        self.assertEqual(len(attackers), 1)
        self.assertEqual(len(users), 2)
        self.assertIn(attackers[0], ["U1","U2","U3"])
        self.assertIn(users[0], ["U1","U2","U3"])
        self.assertIn(users[1], ["U1","U2","U3"])

    def test_node_sampling(self):
        packets_marked, packets_sent = main.node_sampling(self.graph,self.attackers,self.users,self.probability,self.rate)
        packets_marked = sorted(packets_marked.items(), key=lambda x:x[1])
        p_route=[]
        for n in range(12,len(packets_marked)):
            p_route.append(packets_marked[n][0])
        self.assertEqual(p_route, self.attackers_route_node)
        p_sent=0
        for packet in packets_marked:
            p_sent+=packet[1]
        self.assertTrue(p_sent<=packets_sent)

    def test_edge_sampling(self):
        packets_marked, packets_sent, users_costs, attackers_costs = main.edge_sampling(self.graph, self.attackers, self.users, self.probability, self.rate)
        packets_marked = sorted(packets_marked.items(), key=lambda x:x[1])
        p_route=[]
        for n in range(12,len(packets_marked)):
            p_route.append(packets_marked[n][0])
        self.assertEqual(p_route, self.attackers_route_edge)
        p_sent=0
        for packet in packets_marked:
            p_sent+=packet[1]
        self.assertTrue(p_sent<=packets_sent)
        self.assertTrue(attackers_costs["U2 | R15"]>users_costs["U1 | R14"])
        self.assertTrue(attackers_costs["U2 | R15"]>users_costs["U3 | R17"])
 
class integration_test_sampling_algorithms(unittest.TestCase):
    def setUp(self):
        self.network=[('U1', 'R14'), ('R14', 'R11'), ('R11', 'R8'), ('R8', 'R5'), ('R5', 'R3'), ('R3', 'R2'), ('R2', 'R1'), ('U2', 'R15'), ('R15', 'R12'), ('R12', 'R9'), ('R9', 'R6'), ('R6', 'R3'), ('U3', 'R17'), ('R17', 'R16'), ('R16', 'R13'), ('R13', 'R10'), ('R10', 'R7'), ('R7', 'R4'), ('R4', 'R2'), ('R1', 'V')]
        self.graph={'U1': 'R14', 'R14': 'R11', 'R11': 'R8', 'R8': 'R5', 'R5': 'R3', 'R3': 'R2', 'R2': 'R1', 'U2': 'R15', 'R15': 'R12', 'R12': 'R9', 'R9': 'R6', 'R6': 'R3', 'U3': 'R17', 'R17': 
'R16', 'R16': 'R13', 'R13': 'R10', 'R10': 'R7', 'R7': 'R4', 'R4': 'R2', 'R1': 'V'}
        self.attackers=["U2"]
        self.users=["U1","U3"]
        self.probability=0.2
        self.rate=10
        self.attackers_route_node=["U2","R15","R12","R9","R6","R3","R2","R1"]
        self.attackers_route_edge=['U2 | R15', 'R15 | R12', 'R12 | R9', 'R9 | R6', 'R6 | R3', 'R3 | R2', 'R2 | R1', 'R1 | V']

if __name__ == '__main__':
    unittest.main()