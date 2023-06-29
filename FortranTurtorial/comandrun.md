# Fortran Hello World Example: How To Write and Execute Fortran Program on Linux OS

## Step 1: Write a Hello World Fortran Program

Create a file named `hello.f90` with the following content:

```fortran


! This program prints "Hello World" to the screen 
program HelloWorld
print *, "Hello World" ! print statement 
end program ! end statement 
```

## Step 2: Compile the Fortran Program

Use the `gfortran` command to compile the program:

```fortran
gfortran hello.f90 -o hello 
```

This will create an executable file named `hello`.

## Step 3: Execute the Fortran Program

Use the `./` prefix to execute the program:

```shell
./hello 
```

This will print `Hello World` to the screen.

## Step 4: Debug the Fortran Program

To debug the program, you need to compile it with the `-g` option to generate debugging information:

```shell
gfortran -g hello.f90 -o hello 
```

You can also use the `-fcheck=all` option to check for runtime errors:

```shell
gfortran -g -fcheck=all hello.f90 -o hello 
```

Then use the gdb command to start the debugger:

```shell
gdb hello 
```

You can use various commands in gdb to control the debugging process, such as:

- `run`: start or restart the program execution.
- `break`: set a breakpoint at a specified line or function.
- `next`: execute the next line of code, stepping over function calls.
- `print`: print the value of a variable or expression.
- `quit`: exit gdb.

For example, you can set a breakpoint at line 3 and print the value of `*` after running the program:

```shell
(gdb) break 3 Breakpoint 1 at 0x4004c4: file hello.f90, line 3. 
 
(gdb) run 
 
Starting program: /home/user/hello 
 
Breakpoint 1, MAIN__ () at hello.f90:3
 
3 print *, "Hello World" ! print statement 

(gdb)

print * 

$1 = (character(kind=4) *) 0x7ffff7f9c010 <_IO_2_1_stdout_>

(gdb) quit 

A debugging session is active. 

Inferior 1 [process 1234] will be killed. 

Quit anyway? (y or n) y

```
