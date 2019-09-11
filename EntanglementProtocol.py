# Modified Lo-Chau
# based off page 596 of [1]

import numpy as np

#Quantum Gate Definitions
HadamardMatrix = 1/np.sqrt(2) * np.array([[1,1],[1,-1]])
NotMatrix = np.array([[0,1],[1,0]])
IdentityMatrix = np.array([[1,0],[0,1]])
CNotMatrix = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])

#let n  = 10 for this example
n = 10
# STEP 1
# Alice creates 2n EPR pairs in the Bell(00) state = 1/sqrt(2)(|00> + |11>)

BellPairs = []
for i in range(2*n):
    qubit1 = [1,0] # |0>
    qubit2 = [1,0] # |0>
    qubitpair = np.kron(qubit1,qubit2) #|00>
    #apply hadamard to first qubit in pair
    qubitpair = np.matmul(np.kron(HadamardMatrix,IdentityMatrix),qubitpair) # 1/sqrt(2)(|00> + |10>)
    #apply CNot
    entangledpair = np.matmul(CNotMatrix,qubitpair) # 1/sqrt(2)(|00> + |11>)
    BellPairs += [entangledpair]


#STEP 2 & 3
# Alice randomly generates a 2n classical bit string and performs a hadamard transform
# on the second qubit of each pair for which b is 1. 
# Then Alices selects n of the en EPR pairs to serve as checks for interference
# for simplicity, we will just take even indecies starting at 0 (i.e. 0,2,4,6...)

a_message = np.random.randint(2,size=2*n)

for i in range(2*n):
    if a_message[i]:
        BellPairs[i] = np.matmul(np.kron(IdentityMatrix,HadamardMatrix),BellPairs[i])
    
#STEP 4
#Alice sends the second qubit of each pair to Bob
#(Note: eventhough the qubits are separated by some distance, the mathematical representation
# of Bob performing an operation on his qubit is still described by this joint state matrix)

#STEP 5
#Bob receives the qubits and announces this information

#STEP 6
# Alice anounces the randomly chosen bitstring she used to decide which entangled pair underwent the additional 
# Hadamard transformation. She also anounces which entangled pairs she wants to use as a check.
# For simplicity, we set this to (0,2,4..)

b_message = a_message

#STEP 7
# Bob performs a Hadamard transformation on the qubits which Alice anounced she had.

for i in range(2*n):
    if b_message[i]:
        BellPairs[i] = np.matmul(np.kron(IdentityMatrix,HadamardMatrix),BellPairs[i])

#STEP 8,9,10
# Assuming some qubit in an entangled pair was properly received by Bob without any interference or noise
# then the pair maintains maximum correlation and whatever value Alice measures on her qubit of the pair,
# Bob will receive the same value with absolute certainty once he measures.
# Thus if there is high confidence that the entangled pairs arrive safely to Bob, then Alice
# and Bob can simply measure their own half of the pairs and use the resuling classical bitstring
# as the symmetric private key.
# To check the channel, Alice and Bob measure their check qubits of a pair and publically discuss the
# measured values. 