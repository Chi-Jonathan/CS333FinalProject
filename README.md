# CS333FinalProject

This is a probabilistic packet marking simulator. This project simulates a network with the routers as nodes and having “packets” sent through each. A router marks a packet through probability, and an attacker’s route is found by having a conclusive path marked down, with each router having a significant amount of packets marked. When there is enough data to conclude an attacker’s course, the simulation stops, and then the data is returned with the number of packets marked from each router. There are two methods used in this packet marking simulator: node sampling and edge sampling. Node sampling can only detect a single attacker and builds a one-dimensional graph of the attacker’s route. Edge sampling can detect multiple attackers and makes a two-dimensional graph of the attackers’ routes. The only technology used was Python, with the random library imported.

The automatic testing of this application is done through GitHub actions. The building is done by creating a Docker image and deployment is done through Dockerhub at chijoni

This project isn't really all too showy, it's all just command line inputs and outputs.
