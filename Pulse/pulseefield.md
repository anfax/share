# 脉冲电场

## 升余弦脉冲

升余弦脉冲的表达式是：
$$f(t)=E_0 \frac{1+\cos(πt/τ)​}{2} \,(0≤∣t∣≤τ)$$
其中E为脉冲幅度，τ为脉冲宽度。升余弦脉冲的半高全宽为τ。

## 三角形脉冲

三角形脉冲的表达式是：
$$f(t)=E_0 \left(1−\frac{∣t∣}{\tau}​\right)\,(∣t∣<T)$$
其中A为脉冲幅度，T为脉冲宽度。三角形脉冲的半高全宽为T。

```fortran
program plot_spectrum
  implicit none
  integer, parameter :: n = 1024 ! number of samples
  real, parameter :: w = 0.2 ! pulse width
  real, parameter :: dt = 0.01 ! time step
  real :: t(n) ! time array
  real :: x(n) ! pulse array
  complex :: y(n) ! spectrum array
  real :: f(n) ! frequency array
  real :: mag(n) ! magnitude array
  integer :: i ! loop index

  ! generate the triangular pulse in time domain
  do i = 1, n
    t(i) = (i - n/2 - 1)*dt ! center the pulse at t = 0
    x(i) = tripuls(t(i), w) ! use the subroutine defined before
  end do

  ! compute the FFT of the pulse using FFTPACK library
  call drfft(x, y, n)

  ! compute the frequency and magnitude arrays
  do i = 1, n/2 + 1
    f(i) = (i - 1)/(n*dt) ! positive frequencies only
    mag(i) = abs(y(i))/n ! normalize the magnitude
  end do

  ! plot the magnitude spectrum using PGPLOT library
  call pgopen('spectrum.png') ! open a PNG file for output
  call pgenv(0.0, f(n/2 + 1), 0.0, maxval(mag), 0, 0) ! set the axes limits
  call pglabel('Frequency', 'Magnitude', 'Spectrum of Triangular Pulse') ! add labels
  call pgline(n/2 + 1, f, mag) ! plot the line graph
  call pgclos() ! close the file

end program plot_spectrum

! include the subroutine for tripuls here or in a separate module
```
