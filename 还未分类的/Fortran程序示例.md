# Fortran程序示例

## 源码

```fortran
program main !程序的开始
implicit none !关掉fortran默认的变量类型设置
real:: a,b,c !定义变量
!a = 1.0 !赋值给变量
!b = 2.0
read(*,*) a !从键盘读取变量
read(*,*) b
c = a+b  !计算
print*, 'a=',a !将结果输出到屏幕 
print*, 'b=',b
print*, 'c=',c
end program !结算程序
```

## 编译

```shell
ifort *f90
```

## 运行

```shell
./a.exe
```
