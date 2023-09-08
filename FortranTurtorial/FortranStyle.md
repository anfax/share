# Style of Fortran prgram

## Code -> exe -> run

```shell
gfortran  module.f90 function.f90 subroutine.f90 main.f90
```

```shell
./a.out
```

## module

```fortran

module mod1
implicit none
! Common variables

integer, parameter:: rp = selected_real_kind(15,307)
real(rp),parameter:: constant1=1.0_rp
real(rp):: var1

private
public:: sub1, fun1
contains
subroutine sub1(a,b,c)
    real(rp),intent(in)::a,b
real(rp),intent(out):: c
c=a+b
end subroutine sub1

function fun1(a,b) result(c)
real(rp),intent(in)::a,b
real(rp)::c
c=a+b
end function fun1

end module mod1

```
