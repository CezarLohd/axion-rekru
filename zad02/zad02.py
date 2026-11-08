import numpy as np

#kety
ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

#macierz jednostkowa
gate_I = np.array([
    [1, 0],
    [0, 1]
], dtype=complex)


#macierz not
gate_X = np.array([
    [0, 1],
    [1, 0]
], dtype=complex)


#macierz zmiany fazy
gate_Z = np.array([
    [1, 0],
    [0, -1]
], dtype=complex)

#bramka hadamarda
gate_H = (1 / np.sqrt(2)) * np.array([
    [1, 1],
    [1, -1]
])

#bramka theta (zalezna od tej thety)
gate_Ry = lambda theta: np.array([
    [np.cos(theta/2), -np.sin(theta/2)],
    [np.sin(theta/2), np.cos(theta/2)]
], dtype=complex)


# cnot
gate_CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

def measure(state, shots=1000):
    probabilities = np.abs(state) ** 2 # vector prawdonodobienstw - |alfa_stan|^2

    labels = ['0', '1'] if len(state) == 2 else ['00', '01', '10', '11']


    choices = np.random.choice(labels, shots, True, probabilities)

    results = {}
    for choice in choices:
        results[choice] = results.get(choice, 0) + 1
        # 0 - fallback, jak choicea nie mam w results jeszcze

    return results

def main(): 
    print()
    print("---====<[   1: H @ H |0> = |0>   ]>====---")
    print()

    state_h = gate_H @ gate_H @ ket_0

    print(f"Stan wektorowy: {state_h}")
    print(f"Pomiar: {measure(state_h)}")
    print()
    print()

    print("---====<[   Stan Bella - (|00> + |11>) / sqrt(2)   ]>====---")
    print()

    state_00 = np.kron(ket_0, ket_0)

    # Na pierwszy kubit hadamard, a drugi zostaje nieruszony
    gate_H_na_pierwszy = np.kron(gate_H, gate_I) 

    state_after = gate_H_na_pierwszy @ state_00
    bell_state = gate_CNOT @ state_after

    print(f"Stan wektorowy: {bell_state}")
    print(f"Pomiar: {measure(bell_state)}")
    print()
    print()

    #Sprawdzmy tez thete since już tu jest
    print(f"---====<[   Ry(pi) |0>   ]>====---")
    print()

    state_Ry = gate_Ry(np.pi) @ ket_0

    print(f"Stan wektorowy: {np.round(state_Ry, 5)}")
    print(f"Pomiar: {measure(state_Ry)}")
    print()
    print()

    print(f"---====<[   Ry(pi/2) |0>   ]>====---")
    print()

    state_Ry_2 = gate_Ry(np.pi/2) @ ket_0

    print(f"Stan wektorowy: {np.round(state_Ry_2, 5)}")
    print(f"Pomiar: {measure(state_Ry_2)}")

if __name__ == "__main__":
    main()



