module DM
implicit none
type density_matrix
  integer :: dim ! dimension of the matrix
  complex, allocatable :: data(:,:) ! matrix elements
end type density_matrix


contains

  subroutine init_rho(rho, dim)

    type(density_matrix), intent(out) :: rho ! output density matrix
    integer, intent(in) :: dim ! input dimension
    allocate(rho%data(dim,dim)) ! allocate memory for matrix elements
    rho%data = 0.0 ! initialize matrix elements to zero
    rho%dim = dim ! assign dimension
  end subroutine init_rho

  subroutine trace_rho(rho, tr)
    type(density_matrix), intent(in) :: rho ! input density matrix
    complex, intent(out) :: tr ! output trace
    integer :: i
    tr = 0.0 ! initialize trace to zero
    do i = 1, rho%dim ! loop over diagonal elements
      tr = tr + rho%data(i,i) ! add to trace
    end do
  end subroutine trace_rho

  subroutine eigen_rho(rho, eval, evec)
   !use eispack
    type(density_matrix), intent(in) :: rho ! input density matrix
    real, allocatable, intent(out) :: eval(:) ! output eigenvalues
    complex, allocatable, intent(out) :: evec(:,:) ! output eigenvectors
    allocate(eval(rho%dim)) ! allocate memory for eigenvalues
    allocate(evec(rho%dim,rho%dim)) ! allocate memory for eigenvectors
    call eispack(rho%data,rho%dim,eval,evec) ! call external routine to solve eigenvalue problem
  end subroutine eigen_rho

end module DM

module density_matrix_module
  use DM!density_matrix_type ! use the defined data type and operations
  implicit none
  type(density_matrix) :: rho_0 ! initial density matrix
  type(density_matrix) :: rho_t ! time-dependent density matrix
contains
  subroutine init_density_matrix()
    integer :: dim ! dimension of the Hilbert space
    complex :: c1, c2 ! coefficients of the initial state
    dim = 2! ... ! assign dimension according to your problem
    call init_rho(rho_0,dim) ! initialize rho_0 with dimension dim
    c1 = 0.5_8 ! assign coefficient of the first basis state
    c2 = 0.5_8 ! assign coefficient of the second basis state
    rho_0%data(1,1) = c1*conjg(c1) ! assign diagonal element of rho_0 corresponding to the first basis state
    rho_0%data(2,2) = c2*conjg(c2) ! assign diagonal element of rho_0 corresponding to the second basis state
    rho_0%data(1,2) = c1*conjg(c2) ! assign off-diagonal element of rho_0 corresponding to the coherence between the first and second basis states
    rho_0%data(2,1) = c2*conjg(c1) ! assign off-diagonal element of rho_0 corresponding to the coherence between the second and first basis states

  end subroutine init_density_matrix

  subroutine evolve_density_matrix(t)
    real, intent(in) :: t ! input time
    type(density_matrix) :: H_t ! time-dependent Hamiltonian matrix

    call init_rho(rho_t,rho_0%dim) ! initialize rho_t with the same dimension as rho_0

    call build_Hamiltonian(t,H_t) ! build the Hamiltonian matrix at time t according to your problem

    call expm(H_t,rho_t) ! compute the exponential of the Hamiltonian matrix and store it in rho_t

    call matmul(rho_t,rho_0,rho_t) ! multiply rho_t by rho_0 and store the result in rho_t

    call matmul(rho_0,rho_t,rho_t) ! multiply rho_0 by rho_t and store the result in rho_t

  end subroutine evolve_density_matrix

end module density_matrix_module


program density_matrix_main
  use density_matrix_module ! use the defined module
  implicit none

  real :: t, dt, tmax ! time variables
  complex :: tr ! trace of the density matrix
  real, allocatable :: eval(:) ! eigenvalues of the density matrix
  complex, allocatable :: evec(:,:) ! eigenvectors of the density matrix

  call init_density_matrix() ! initialize the density matrix

  t = 0.0 ! initial time
  dt = 0.01 ! time step
  tmax = 10.0 ! maximum time

  do while (t <= tmax) ! loop over time

    call evolve_density_matrix(t) ! evolve the density matrix at time t

    call trace_rho(rho_t,tr) ! compute the trace of the density matrix at time t

    call eigen_rho(rho_t,eval,evec) ! compute the eigenvalues and eigenvectors of the density matrix at time t

    write(*,*) 'Time = ', t ! write time to standard output
    write(*,*) 'Trace = ', tr ! write trace to standard output
    write(*,*) 'Eigenvalues = ', eval ! write eigenvalues to standard output
    write(*,*) 'Eigenvectors = ', evec ! write eigenvectors to standard output

    t = t + dt ! increment time

  end do

end program density_matrix_main





