# Some questions

## persion loss

### calculate order casue the persion loss
  
```fortran

double persion:: a, b, c
double persion:: sum1, sum2 
sum1= 0.50d0 * (a+b)/c
sum2= 0.50d0 * (a/c+b/c)
write(*,'(f15.7)')sum1, sum2

```

sum1 is no equate to sum2 caused persion loss.  
