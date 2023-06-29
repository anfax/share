# Import numpy for numerical calculations
import numpy as np

# Define some constants
hbar = 1.0545718e-34 # Reduced Planck constant in J*s
kB = 1.38064852e-23 # Boltzmann constant in J/K
I = 1e-46 # Moment of inertia of molecule in kg*m^2
T = 300 # Temperature in K
mu = 1e-30 # Electric dipole moment of molecule in C*m

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

# Define a function to calculate the density matrix element at t=0
def rho0(J,M,Jp,Mp,T):
    # Use Boltzmann distribution for coefficients
    cJM = np.sqrt((2*J+1)*np.exp(-E(J)/(kB*T))/Z(T))*(M==0)
    cJpMp = np.sqrt((2*Jp+1)*np.exp(-E(Jp)/(kB*T))/Z(T))*(Mp==0)
    return cJM*np.conj(cJpMp)


# Define a function to calculate the electric field of a laser pulse at time t
def Efield(t):
    # Use a Gaussian envelope with a carrier frequency
    E0 = 1e5 # Peak electric field in V/m
    omega = 1e15 # Carrier frequency in rad/s
    tau = 1e-12 # Pulse duration in s
    return E0*np.exp(-t**2/(2*tau**2))*np.cos(omega*t)

# Define a function to calculate the matrix element of the electric dipole operator
def muJM(J,M,Jp,Mp):
    # Use the Wigner-Eckart theorem
    if M == Mp:
        return mu*np.sqrt((2*J+1)*(2*Jp+1))*np.sqrt((J+M)*(J-M))*np.sqrt((Jp+Mp)*(Jp-Mp))/(2*(2*J-1))
    else:
        return 0

# Define a function to calculate the matrix element of the perturbation Hamiltonian in the interaction picture
def H1I(J,M,Jp,Mp,t):
    # Use the electric dipole interaction and the unitary transformation
    return -muJM(J,M,Jp,Mp)*Efield(t)*np.exp(-1j*(E(J)-E(Jp))*t/hbar)

# Define a maximum value of J to truncate the basis set
Jmax = 25

# Create an empty matrix to store the density matrix elements at t=0
rho_matrix0 = np.zeros(((Jmax+1)**2,(Jmax+1)**2),dtype=complex)

# Loop over the basis functions and fill the matrix elements at t=0
for J in range(Jmax+1):
    for M in range(-J,J+1):
        for Jp in range(Jmax+1):
            for Mp in range(-Jp,Jp+1):
                # Use a linear index to access the matrix elements
                i = J*(Jmax+1)+M
                j = Jp*(Jmax+1)+Mp
                # Calculate the matrix element using the function defined above
                rho_matrix0[i,j] = rho0(J,M,Jp,Mp,T)
print(np.trace(rho_matrix0))
# Define a function to calculate the matrix element of the total angular momentum squared operator
def J2(J,M,Jp,Mp):
    # Use the eigenvalue of J^2
    if J == Jp and M == Mp:
        return hbar**2*J*(J+1)
    else:
        return 0

# Create an empty matrix to store the matrix elements of J^2
J2_matrix = np.zeros_like(rho_matrix0)

# Loop over the basis functions and fill the matrix elements of J^2
for J in range(Jmax+1):
    for M in range(-J,J+1):
        for Jp in range(Jmax+1):
            for Mp in range(-Jp,Jp+1):
                # Use a linear index to access the matrix elements
                i = J*(Jmax+1)+M
                j = Jp*(Jmax+1)+Mp
                # Calculate the matrix element using the function defined above
                J2_matrix[i,j] = J2(J,M,Jp,Mp)

# Create an empty matrix to store the density matrix elements at t>0
rho_matrix = np.zeros_like(rho_matrix0)

# Define a time step for numerical integration
dt = 1e-15 # Time step in s

# Define a total time for numerical integration
tmax = 10e-12 # Total time in s

# Define an array of time points for numerical integration
t_array = np.arange(0,tmax,dt)

# Loop over the time points and update the density matrix elements using Euler's method
for t in t_array:
    # Loop over the basis functions and calculate the derivative of the density matrix elements
    for J in range(Jmax+1):
        for M in range(-J,J+1):
            for Jp in range(Jmax+1):
                for Mp in range(-Jp,Jp+1):
                    # Use a linear index to access the matrix elements
                    i = J*(Jmax+1)+M
                    j = Jp*(Jmax+1)+Mp
                    # Calculate the derivative using the Liouville-von Neumann equation in the interaction picture
                    drho_dt = -1j/hbar*(H1I(J,M,Jp,Mp,t)*rho_matrix0[i,j]-rho_matrix0[i,j]*H1I(Jp,Mp,J,M,t))
                    # Update the matrix element using Euler's method
                    rho_matrix[i,j] += drho_dt*dt
    print(np.trace(rho_matrix))
# Print the density matrix at t=tmax
print(rho_matrix)
