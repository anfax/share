---
presentation:
  theme: serif.css
  mouseWheel: true
  width: 2560
  height: 1440
---
<!-- slide -->
# A DIRECT RELAXATION METHOD FOR CALCULATING EIGENFUNCTIONS AND EIGENVALUES OF THE SCHRODINGER EQUATION ON A GRID
<!-- slide -->
## Introduction
<!-- slide -->
### Grid Meteods for sovleing the time-dependent Schrodinger equation

- Modeling atom and molecule surface scattering
- reactive calculations
- decay of resonnance
<!-- slide -->
### The utility of grid meteods is dependent on

- the eigenvalues
- te eignefunctions

### the eigenfunctions are used as

- initial states for the time-dependent propagation
- for analying the final results after the time-dependent a perturbation
### Nethods for obataining eigenfunction on relaxation techniques

<!-- slide -->

## Description of the relaxation method

<!-- slide -->
Step one is setting up a grid and constructing on it an initial wavefunction.

Step two is the calculation of the Hamiltonian operation:
$$ \phi  =\hat{H} $$
$$ \hat{H} ={\hat{p}\over 2m} + \hat{V} \tag{1} $$

<!-- slide -->
$$\exp\left[ -i \hat{H} t\right] = a_n \phi_n {i \hat{H} t\over R}$$
$a_n= 2 J_n (R) $ for $n\neq0 $ and $a_0 = J_0 (R) $ ($J_n$ is the Bessel function of te first kind) $R$ is the upper bound for the range of eignvlues of the Hamiltionina represented on the grid multiplied by t:
$$ R= [V_{\mathrm{max}}-V_{\mathrm{min}}+\pi^2 ({1\over (\Delta x)^2}+{1\over (\Delta y)^2}+{1\over (\Delta z)^2})]t\tag{2}$$(for a 3-D  grid)

$$\phi_n(\hat{X}) = 2 \hat{X} \phi_{n-1}(\hat{X})+\phi_{n-2}(\hat{X}),\hat{X} = {-i \hat{H} t \over R },\phi_0 =(\hat{X}) =\hat{I},\phi_1(\hat{X})=\hat{X}\tag{3}$$
<!-- slide -->
$$\psi (\tau )=\exp[-\hat{H}t]\psi(0)$$