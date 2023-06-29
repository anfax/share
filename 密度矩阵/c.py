# Import numpy for numerical calculations
import numpy as np

# Define some constants
hbar = 1.0545718e-34 # Reduced Planck constant in J*s
kB = 1.38064852e-23 # Boltzmann constant in J/K
I = 1e-46 # Moment of inertia of molecule in kg*m^2
T = 300 # Temperature in K

# Define a function to calculate the rigid rotor energy
def E(J):
    return hbar**2/(2*I)*J*(J+1)

# Define a function to calculate the rotational partition function
def Z(T):
    J = 0 # Initial value of J
    Z = 0 # Initial value of Z
    while True:
        # Add the contribution of each J level
        Z += (2*J+1)*np.exp(-E(J)/(kB*T))
        # Stop when the contribution is negligible
        if (2*J+1)*np.exp(-E(J)/(kB*T)) < 1e-10:
            break
        # Increment J by 1
        J += 1
    return Z

# Define a function to calculate the density matrix element
def rho(J,M,Jp,Mp,T):
    # Use Boltzmann distribution for coefficients
    cJM = np.sqrt((2*J+1)*np.exp(-E(J)/(kB*T))/Z(T))*(M==0)
    cJpMp = np.sqrt((2*Jp+1)*np.exp(-E(Jp)/(kB*T))/Z(T))*(Mp==0)
    return cJM*np.conj(cJpMp)

# Define a maximum value of J to truncate the basis set
Jmax = 10

# Create an empty matrix to store the density matrix elements
rho_matrix = np.zeros(((Jmax+1)**2,(Jmax+1)**2),dtype=complex)

# Loop over the basis functions and fill the matrix elements
for J in range(Jmax+1):
    for M in range(-J,J+1):
        for Jp in range(Jmax+1):
            for Mp in range(-Jp,Jp+1):
                # Use a linear index to access the matrix elements
                i = J*(Jmax+1)+M
                j = Jp*(Jmax+1)+Mp
                # Calculate the matrix element using the function defined above
                rho_matrix[i,j] = rho(J,M,Jp,Mp,T)

# Print the density matrix
print(rho_matrix)
