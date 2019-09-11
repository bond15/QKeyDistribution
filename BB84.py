# BB84 protocol
import numpy as np

#Quantum Gate Definitions
HadamardMatrix = 1/np.sqrt(2) * np.array([[1,1],[1,-1]])
NotMatrix = np.array([[0,1],[1,0]])

def Hadamard (qubit):    
    return np.matmul(HadamardMatrix,qubit)

def Not (qubit):
    return np.matmul(NotMatrix,qubit)

#Quantum Measurement simulation (no noise)(computational basis measurement)
# for a qubit in a general state |Psi> = a|0> + b|1> we say that the (projective) measurement
# of |Psi> will result in state |0> with probablity a^2 and result in state |1> with probability b^2
# Measurment of a qubit is a transformation from quantum information to classical information

# for this project, a qubit is only in 4 possible states:
# |0> --(0 with 100% chance),
# |1> --(1 with 100% chance),
# |+>= 1/(sqrt(2))(|0> + |1>)  --(1 with 50% chance, 0 with 50% chance),
# |->= 1/(sqrt(2))(|0> - |1>)  --(1 with 50% chance, 0 with 50% chance)

def Measure(qubit):
    if qubit[0]: # |0>
        return 0
    if qubit[1]: # |1>
        return 1
    return np.random.randint(2) #|+> or |->
    
    
'''
Folling the BB84 algorithm as it appears on page 588 of 
Nielsen, M., & Chuang, I. (2010). Quantum information theory. 
In Quantum Computation and Quantum Information: 10th Anniversary Edition (pp. 528-607). 
Cambridge: Cambridge University Press. doi:10.1017/CBO9780511976667.016
'''
#STEP 1 
#Alice chooses a message to send.
a_message = np.array(list(map(int,"110011101101101000110010110100101010")))

#STEP 2
# Alice chooses randomly between the Computational and Hadamard basis with equal probabability
# for all bits in her message. She then encodes each bit in her message in a qubit according to the random basis 
# she chose. Let 0 denote Computational basis and 1 denote Hadamard basis.
a_basis = np.random.randint(2,size=len(a_message))

a_qubits = []
for i in range(len(a_message)):
    qubit = np.array([1,0]) # qubit initially in state |0>
    
    #check encoding
    if a_basis[i]: # Hadamard basis
        if a_message[i]: # ith bit is a one
            a_qubits += [Hadamard(Not(qubit))]
        else: # ith bit is a zero
            a_qubits += [Hadamard(qubit)]
    else: #Computational basis
        if a_message[i]: # ith bit is a one
            a_qubits += [Not(qubit)]
        else: # ith bit is a zero
            a_qubits += [qubit]

#STEP 3
# Alice sends the prepped qubits to Bob
b_qubits = a_qubits

#STEP 4
# Upon receiving the qubits, Bob chooses randomly between basis for each qubit and performs a measurement.
# (Note: the Measurement function is implemented for the Computational basis, to measure in the Hadamard basis
# a Hadamard transformation is first applied, then the output is measured in the computational basis)

# randomly choose measure basis
b_basis = np.random.randint(2,size=len(b_qubits))

b_message = []
# measure qubits according to basis
for i in range(len(b_qubits)):
    if b_basis[i]: # Hadamard basis
        #first perform transform
        b_message += [Measure(Hadamard(b_qubits[i]))] #equivalent to measuring in hadamard basis
    
    else: # Computational basis
        b_message += [Measure(b_qubits[i])] 

#STEP 5
# Allice publically announces the basis she used to encode her message. 
# Bob looks at the basis he chose and identifies which he actually chose correctly
# he then relays this information to Alice

#Alice's public anouncement of basis choice received by Bob
b_a_basis = a_basis 

# Bob finds which bits in the message were decoded properly
b_correct_indicies = []
for i in range(len(b_qubits)):
    if b_basis[i] == b_a_basis[i]:
        b_correct_indicies += [i]

# Bob sends Alice the list of qubits he decoded correctly
a_b_correct_indicies = b_correct_indicies

#STEP 6
# Both Bob and Alice discard the bits in their copies of the message that didnt have the same basis for encoding and decoding
# If the original message length was (4+delta)n, then it is desireable 2n bits remained in the filtered message after 
# Alice and Bob filter on correct indicies. Delta being the parameter used to increase/decrease the liklihood of 2n bits remaining

# Alice discards bits
a_message_filtered = []
for i in range(len(a_message)):
    if i in a_b_correct_indicies:
        a_message_filtered += [a_message[i]]

# Bob discards bits
b_message_filtered = []
for i in range(len(b_qubits)):
    if i in b_correct_indicies:
        b_message_filtered += [b_message[i]]
        
# Alice decides if there are enough filtered values to continue the protocol
if len(a_message_filtered)*2 < len(a_message):
    print("END, Not enough filtered values")

# STEP 7-9
# At this point, Alice and Bob both have a copy of the message that is correct by proper encoding-decoding pair. 
# However, even though the indicies are now correct, it may be the case that the message values at those indicies arent
# due to noise in the channel or from a disturbance due to eavesdropping on the qubit channel. 
# Alice would then randomly select n indicies of her message to compare the value with bobs. If a sufficent number 
# are correct between Alice and Bob at those indicies, then the algorithm transitions to the Privacy amplification
# and information reconsilation stage as mentioned on page 584 of the mentioned text. 
# 
# Here there are no eavesdroppers and the simulated quantum behavior is not sophisticated enough to model the 
# types of error expectations seen in practice. 



print("original message", a_message)
print("len", len(a_message))
print("a_basis",a_basis)
print("b_basis",b_basis)
print("indicies",b_correct_indicies)
print("a", a_message_filtered)
print("b", b_message_filtered)
print("flen",len(a_message_filtered))