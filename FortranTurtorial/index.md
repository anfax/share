---
This quickstart tutorial gives an overview of the Fortran programming language
and its syntax for common structured programming concepts including:
types, variables, arrays, control flow and functions.

---

# Fortran Programming

---
In this part of the tutorial, we will write our first Fortran program: the ubiquitous ["Hello, World!"](https : //en.wikipedia.org/wiki/%22Hello,_World!%22_program) example.

However, before we can write our program, we need to ensure that we have
a Fortran compiler set up.

Fortran is a *compiled language*, which means that, once written, the source code must be passed through a
compiler to produce a machine executable that can be run.

## Compiler setup

In this tutorial, we'll work with the free and open source
[GNU Fortran compiler (gfortran)](https: //gcc.gnu.org/fortran/),
which is part of the
[GNU Compiler Collection (GCC)](https://gcc.gnu.org/).

To install gfortran on Linux, use your system package manager.
On macOS, you can install gfortran using [Homebrew](https://brew.sh/) or [MacPorts](https://www.macports.org/).
On Windows, you can get native binaries [here](http://www.equation.com/servlet/equation.cmd?fa=fortran).

To check if you have *gfortran* setup correctly, open a terminal and run the following command:

```fortran
shell
$> gfortran --version
```

this should output something like:

```shell
GNU Fortran 7.5.0
Copyright (C) 2017 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

## Hello worlds

Once you have set up your compiler, open a new file in your favourite code editor and enter the following:

```fortran
program hello
  ! This is a comment line; it is ignored by the compiler
  print *, 'Hello, World!'
end program hello
```

Having saved your program to `hello.f90`, compile at the command line with:

```shell
$> gfortran hello.f90 -o hello
```

`.f90` is the standard file extension for modern Fortran source files.
The 90 refers to the first modern Fortran standard in 1990.

To run your compiled program:

```shell
$> ./hello
Hello, World!
```

Congratulations, you've written, compiled and run your first Fortran program!
In the next part of this tutorial, we will introduce variables for storing data.

---

## Variables

Variables store information that can be manipulated by the program.
Fortran is a *strongly typed* language, which means that each variable
must have a type.

There are 5 built-in data types in Fortran:

* `integer` -- for data that represent whole numbers, positive or negative
* `real` -- for floating-point data (not a whole number)
* `complex` -- pair consisting of a real part and an imaginary part
* `character` -- for text data
* `logical` -- for data that represent boolean (true or false) values

Before we can use a variable, we must *declare* it; this tells the compiler
the variable type and any other variable attributes.

Fortran is a *statically typed* language, which means the type of each
variable is fixed when the program is compiled---variable types cannot change while the program is running.

### Declaring variables

The syntax for declaring variables is:

```shell
<variable_type> :: <variable_name>
```

where `<variable_type>` is one of the built-in variable types listed above and
`<variable_name>` is the name that you would like to call your variable.

Variable names must start with a letter and can consist of letters, numbers and underscores.
In the following example we declare a variable for each of the built-in types.

__Example:__ variable declaration

```fortran
program variables
  implicit none

  integer :: amount
  real :: pi
  complex :: frequency
  character :: initial
  logical :: isOkay

end program variables
```

Fortran code is __case-insensitive__; you don't have to worry about the
capitalisation of your variable names, but it's good practice to keep it consistent.

Note the additional statement at the beginning of the program: `implicit none`.
This statement tells the compiler that all variables will be explicitly declared; without
this statement variables will be implicitly typed according to the letter they begin with.

Always use the `implicit none` statement at
the beginning of each program and procedure. Implicit typing is considered bad practice in
modern programming since it hides information leading to more program errors.

Once we have declared a variable, we can assign and reassign values to it using the assignment operator `=`.

__Example:__ variable assignment

```fortran
amount = 10
pi = 3.1415927
frequency = (1.0, -0.5)
initial = 'A'
isOkay = .false.
```

Characters are surrounded by either single (`'`) or double quotes (`"`).

Logical or boolean values can be either `.true.` or `.false.`.

for assignment at declaration: `integer :: amount = 1`.
__This is NOT a normal initialisation;__ it implies the `save` attribute which means that the variable retains
its value between procedure calls. Good practice is to initialise your variables separately to their declaration.

## Standard input / output

In our *Hello World* example, we printed text to the command window.
This is commonly referred to as writing to `standard output` or `stdout`.

We can use the `print` statement introduced earlier to print variable values to `stdout`:

```fortran
print *, 'The value of amount (integer) is: ', amount
print *, 'The value of pi (real) is: ', pi
print *, 'The value of frequency (complex) is: ', frequency
print *, 'The value of initial (character) is: ', initial
print *, 'The value of isOkay (logical) is: ', isOkay
```

In a similar way, we can read values from the command window
using the `read` statement:

```fortran
program read_value
  implicit none
  integer :: age

  print *, 'Please enter your age: '
  read(*,*) age

  print *, 'Your age is: ', age

end program read_value
```

This input source is commonly referred to as `standard input` or `stdin`.

## Expressions

The usual set of arithmetic operators are available, listed in order or precedence:

| Operator &nbsp;  | Description    |
|:----------------:|----------------|
| `**`             | Exponent       |
| `*`              | Multiplication |
| `/`             | Division       |
| `+`              | Addition       |
| `-`              | Subtraction    |

__Example:__

```fortran
program arithmetic
  implicit none

  real :: pi
  real :: radius
  real :: height
  real :: area
  real :: volume

  pi = 3.1415927

  print *, 'Enter cylinder base radius:'
  read(*,*) radius

  print *, 'Enter cylinder height:'
  read(*,*) height

  area = pi * radius**2.0
  volume = area * height

  print *, 'Cylinder radius is: ', radius
  print *, 'Cylinder height is: ', height
  print *, 'Cylinder base area is: ', area
  print *, 'Cylinder volume is: ', volume

end program arithmetic
```

## Floating-point precision

The desired floating-point precision can be explicitly declared using a `kind` parameter.
The `iso_fortran_env` intrinsic module provides `kind` parameters for the common 32-bit and 64-bit floating-point types.

__Example:__ explicit real `kind`

```fortran
program float
  use, intrinsic :: iso_fortran_env, only: sp=>real32, dp=>real64
  implicit none

  real(sp) :: float32
  real(dp) :: float64

  float32 = 1.0_sp  ! Explicit suffix for literal constants
  float64 = 1.0_dp

end program float
```

Always use a `kind` suffix for floating-point literal constants.

__Example:__ C-interoperable `kind`s

```fortran
program float
  use, intrinsic :: iso_c_binding, only: sp=>c_float, dp=>c_double
  implicit none

  real(sp) :: float32
  real(dp) :: float64

end program float
```

In the next part we will learn how to use arrays for storing more than one
value in a variable.

---

## Arrays strings

---

More often than not, we need to store and operate on long lists of numbers as opposed to just the single scalar variables
that we have been using so far; in computer programming such lists are called  *arrays*.

Arrays are *multidimensional* variables that contain more than one value
where each value is accessed using one or more indices.

Arrays in Fortran are *one-based* by default; this means
that the first element along any dimension is at index 1.

### Array declaration

We can declare arrays of any type. There are two common notations for declaring array variables:
using the `dimension` attribute or by appending the array dimensions in parentheses to the variable name.

__Example:__ static array declaration

```fortran
program arrays
  implicit none

  ! 1D integer array
  integer, dimension(10) :: array1

  ! An equivalent array declaration
  integer :: array2(10)

  ! 2D real array
  real, dimension(10, 10) :: array3

  ! Custom lower and upper index bounds
  real :: array4(0:9)
  real :: array5(-5:5)

end program arrays
```

### Array slicing

A powerful feature of the Fortran language is its built-in support for array operations;
we can perform operations on all or part of an array using array *slicing* notation:

__Example:__ array slicing

```fortran
program array_slice
  implicit none

  integer :: i
  integer :: array1(10)  ! 1D integer array of 10 elements
  integer :: array2(10, 10)  ! 2D integer array of 100 elements

  array1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  ! Array constructor
  array1 = [(i, i = 1, 10)]  ! Implied do loop constructor
  array1(:) = 0  ! Set all elements to zero
  array1(1:5) = 1  ! Set first five elements to one
  array1(6:) = 1  ! Set all elements after five to one

  print *, array1(1:10:2)  ! Print out elements at odd indices
  print *, array2(:,1)  ! Print out the first column in a 2D array
  print *, array1(10:1:-1)  ! Print an array in reverse

end program array_slice
```

Fortran arrays are stored in *column-major* order; the first
index varies fastest.

### Allocatable (dynamic) arrays

So far we have specified the size of our array in our program code---this
type of array is known as a *static* array since its size is fixed when
we compile our program.

Quite often, we do not know how big our array needs to be until we run our program, for example, if we are reading data from a file of unknown size.

For this problem, we need `allocatable` arrays.
These are *allocated* while the program is running once we know how big the array needs to be.

__Example:__ allocatable arrays

```fortran
program allocatable
  implicit none

  integer, allocatable :: array1(:)
  integer, allocatable :: array2(:,:)

  allocate(array1(10))
  allocate(array2(10,10))

  ! ...

  deallocate(array1)
  deallocate(array2)

end program allocatable
```

Allocatable local arrays are deallocated automatically
when they go out of scope.

### Character strings

__Example:__ static character string

```fortran
program string
  implicit none

  character(len=4) :: first_name
  character(len=5) :: last_name
  character(10) :: full_name

  first_name = 'John'
  last_name = 'Smith'

  ! String concatenation
  full_name = first_name//' '//last_name

  print *, full_name

end program string
```

__Example:__ allocatable character string

```fortran
program allocatable_string
  implicit none

  character(:), allocatable :: first_name
  character(:), allocatable :: last_name

  ! Explicit allocation statement
  allocate(character(4) :: first_name)
  first_name = 'John'

  ! Allocation on assignment
  last_name = 'Smith'

  print *, first_name//' '//last_name

end program allocatable_string
```

### Array of strings

An array of strings can be expressed in Fortran as an array of `character` variables.
All elements in a `character` array have equal length.
However, strings of varying lengths can be provided as input to the array constructor, as shown in the example below.
They will be truncated or right-padded with spaces if they are longer or shorter, respectively, than the declared length of the `character` array.
Finally, we use the intrinsic function `trim` to remove any excess spaces when printing the values to the standard output.

__Example:__ string array

```fortran
program string_array
  implicit none
  character(len=10), dimension(2) :: keys, vals

  keys = [character(len=10) :: "user", "dbname"]
  vals = [character(len=10) :: "ben", "motivation"]

  call show(keys, vals)

  contains

  subroutine show(akeys, avals)
    character(len=*), intent(in) :: akeys(:), avals(:)
    integer                      :: i

    do i = 1, size(akeys)
      print *, trim(akeys(i)), ": ", trim(avals(i))
    end do

  end subroutine show

end program string_array
```

---

## Operators and flow control

One of the powerful advantages of computer algorithms, compared to simple mathematical formulae,
comes in the form of program *branching* whereby the program can decide which instructions to
execute next based on a logical condition.

There are two main forms of controlling program flow:

* *Conditional* (if): choose program path based on a boolean (true or false) value

* *Loop*: repeat a portion of code multiple times

### Logical operators

Before we use a conditional branching operator, we need to be able to form
a logical expression.

To form a logical expression, the following set of relational operators are available:

| Operator &nbsp;  | Alternative &nbsp;    | Description                                                     |
|:----------------:|:---------------------:|-----------------------------------------------------------------|
| `==`             | `.eq.`                | Tests for equality of two operands                              |
| `/=`             | `.ne.`                | Test for inequality of two operands                             |
| `>`             | `.gt.`                | Tests if left operand is strictly greater than right operand    |
| `<`             | `.lt.`                | Tests if left operand is strictly less than right operand       |
| `>=`             | `.ge.`                | Tests if left operand is greater than or equal to right operand |
| `<=`             | `.le.`                | Tests if left operand is less than or equal to right operand    |

as well as the following logical operators:

| Operator &nbsp;       | Description                                                          |
|:---------------------:|----------------------------------------------------------------------|
| `.and.`               | TRUE if both left and right operands are TRUE                        |
| `.or.`                | TRUE if either left or right or both operands are TRUE               |
| `.not.`               | TRUE if right operand is FALSE                                       |
| `.eqv.`               | TRUE if left operand has same logical value as right operand         |
| `.neqv.`              | TRUE if left operand has the opposite logical value as right operand |

### Conditional construct (`if`)

In the following examples, a conditional `if` construct is used to print out a
message to describe the nature of the `angle` variable:

__Example:__ single branch `if`

```fortran
if (angle < 90.0) then
  print *, 'Angle is acute'
end if
```

In this first example, the code within the `if` construct is *only executed if* the
test expression (`angle < 90.0`) is true.

**It is good practice to indent code within constructs such as `if` and `do`
to make code more readable.

We can add an alternative branch to the construct using the `else` keyword:

__Example:__ two-branch `if`-`else`

```fortran
if (angle < 90.0) then
  print *, 'Angle is acute'
else
  print *, 'Angle is obtuse'
end if
```

Now there are two *branches* in the `if` construct, but *only one branch is executed* depending
on the logical expression following the `if` keyword.

We can actually add any number of branches using `else if` to specify more conditions:

__Example:__ multi-branch  `if`-`else if`-`else`

```fortran
if (angle < 90.0) then
  print *, 'Angle is acute'
else if (angle < 180.0) then
  print *, 'Angle is obtuse'
else
  print *, 'Angle is reflex'
end if
```

When multiple conditional expressions are used, each conditional expression is tested only if none of the previous
expressions have evaluated to true.

### Loop constructs (`do`)

In the following example, a `do` loop construct is used to print out the numbers in
a sequence.
The `do` loop has an integer *counter* variable which is used to track which iteration of the loop
is currently executing. In this example we use a common name for this counter variable: `i`.

When we define the start of the `do` loop, we use our counter variable name followed by an equals (`=`) sign
to specify the start value and final value of our counting variable.

__Example:__ `do` loop

```fortran
integer :: i

do i = 1, 10
  print *, i
end do
```

__Example:__ `do` loop with skip

```fortran
integer :: i

do i = 1, 10, 2
  print *, i  ! Print odd numbers
end do
```

#### Conditional loop (`do while`)

A condition may be added to a `do` loop with the `while` keyword. The loop will be executed while the condition given
in `while()` evaluates to `.true.`.

__Example:__ `do while()` loop

```fortran
integer :: i

i = 1
do while (i < 11)
  print *, i
  i = i + 1
end do
! Here i = 11
```

#### Loop control statements (`exit` and `cycle`)

Most often than not, loops need to be stopped if a condition is met. Fortran provides two executable statements to deal
with such cases.

`exit` is used to quit the loop prematurely. It is usually enclosed inside an `if`.

__Example:__ loop with `exit`

```fortran
integer :: i

do i = 1, 100
  if (i > 10) then
    exit  ! Stop printing numbers
  end if
  print *, i
end do
! Here i = 11
```

On the other hand, `cycle` skips whatever is left of the loop and goes into the next cycle.

__Example:__ loop with `cycle`

```fortran
integer :: i

do i = 1, 10
  if (mod(i, 2) == 0) then
      cycle  ! Don't print even numbers
  end if
  print *, i
end do
```

When used within nested loops, the `cycle` and `exit` statements operate on the innermost loop.

#### Nested loop control: tags

A recurring case in any programming language is the use of nested loops. Nested loops refer to loops that exist within another loop. Fortran allows the programmer to *tag* or *name* each loop. If loops are tagged, there are two potential benefits:

1. The readability of the code may be improved (when the naming is meaningful).
2. `exit` and `cycle` may be used with tags, which allows for very fine-grained control of the loops.

__Example:__ tagged nested loops

```fortran
integer :: i, j

outer_loop: do i = 1, 10
  inner_loop: do j = 1, 10
    if ((j + i) > 10) then  ! Print only pairs of i and j that add up to 10
      cycle outer_loop  ! Go to the next iteration of the outer loop
    end if
    print *, 'I=', i, ' J=', j, ' Sum=', j + i
  end do inner_loop
end do outer_loop
```

#### Parallelizable loop (`do concurrent`)

The `do concurrent` loop is used to explicitly specify that the *inside of the loop has no interdependencies*; this informs the compiler that it may use parallelization/*SIMD* to speed up execution of the loop and conveys programmer intention more clearly. More specifically, this means
that any given loop iteration does not depend on the prior execution of other loop iterations. It is also necessary that any state changes that may occur must only happen within each `do concurrent` loop.
These requirements place restrictions on what can be placed within the loop body.

> Simply replacing a `do` loop with a `do concurrent` does not guarantee parallel execution.
The explanation given above does not detail all the requirements that need to be met in order to write a correct `do concurrent` loop.
Compilers are also free to do as they see fit, meaning they may not optimize the loop (e.g., a small number of iterations doing a simple calculation, like the below example).
In general, compiler flags are required to activate possible parallelization for `do concurrent` loops.

__Example:__ `do concurrent()` loop

```fortran
real, parameter :: pi = 3.14159265
integer, parameter :: n = 10
real :: result_sin(n)
integer :: i

do concurrent (i = 1:n)  ! Careful, the syntax is slightly different
  result_sin(i) = sin(i * pi/4.)
end do

print *, result_sin
```

---

## Organising code structure

Most programming languages allow you to collect commonly-used code into
*procedures* that can be reused by *calling* them from other sections of code.

Fortran has two forms of procedure:

* __Subroutine__: invoked by a `call` statement
* __Function__: invoked within an expression or assignment to which it returns a value

Both subroutines and functions have access to variables in the parent scope by *argument association*;
unless the `value` attribute is specified, this is similar to call by reference.

### Subroutines

The subroutine input arguments, known as *dummy arguments*, are specified in parentheses after the subroutine name;
the dummy argument types and attributes are declared within the body of the subroutine just like local variables.

__Example:__

```fortran
! Print matrix A to screen
subroutine print_matrix(n,m,A)
  implicit none
  integer, intent(in) :: n
  integer, intent(in) :: m
  real, intent(in) :: A(n, m)

  integer :: i

  do i = 1, n
    print *, A(i, 1:m)
  end do

end subroutine print_matrix
```

Note the additional `intent` attribute when declaring the dummy arguments; this optional attribute signifies to the compiler whether the argument
is ''read-only'' (`intent(in)`) ''write-only'' (`intent(out)`) or ''read-write'' (`intent(inout)`) within the procedure.
In this example, the subroutine does not modify its arguments, hence all arguments are `intent(in)`.

It is good practice to always specify the `intent` attribute for dummy arguments; this allows the compiler to check for unintentional errors and provides self-documentation.

We can call this subroutine from a program using a `call` statement:

```fortran
program call_sub
  implicit none

  real :: mat(10, 20)

  mat(:,:) = 0.0

  call print_matrix(10, 20, mat)

end program call_sub
```

This example uses a so-called *explicit-shape* array argument since we have passed additional variables to describe
the dimensions of the array `A`; this will not be necessary if we place our subroutine in a module as described later.

### Functions

```fortran
! L2 Norm of a vector
function vector_norm(n,vec) result(norm)
  implicit none
  integer, intent(in) :: n
  real, intent(in) :: vec(n)
  real :: norm

  norm = sqrt(sum(vec**2))

end function vector_norm
```

__In production code, the intrinsic function `norm2` should be used.__

To execute this function:

```fortran
program run_fcn
  implicit none

  real :: v(9)
  real :: vector_norm

  v(:) = 9

  print *, 'Vector norm = ', vector_norm(9,v)

end program run_fcn
```

It is good programming practice for functions not to modify their arguments---that is, all function arguments should be `intent(in)`.
Such functions are known as `pure` functions.
Use subroutines if your procedure needs to modify its arguments.

### Modules

Fortran modules contain definitions that are made accessible to programs, procedures, and other modules through the `use` statement.
They can contain data objects, type definitions, procedures, and interfaces.

* Modules allow controlled scoping extension whereby entity access is made explicit
* Modules automatically generate explicit interfaces required for modern procedures

It is recommended to always place functions and subroutines within modules.

__Example:__

```fortran
module my_mod
  implicit none

  private  ! All entities are now module-private by default
  public public_var, print_matrix  ! Explicitly export public entities

  real, parameter :: public_var = 2
  integer :: private_var

contains
    
  ! Print matrix A to screen
  subroutine print_matrix(A)
    real, intent(in) :: A(:,:)  ! An assumed-shape dummy argument

    integer :: i

    do i = 1, size(A,1)
      print *, A(i,:)
    end do

  end subroutine print_matrix

end module my_mod
```

Compare this `print_matrix` subroutine with [that written outside of a module](## subroutines);
we no longer have to explicitly pass the matrix dimensions and can instead take
advantage of *assumed-shape* arguments since the module will generate the required
explicit interface for us. This results in a much simpler subroutine interface.

To `use` the module within a program:

```fortran
program use_mod
  use my_mod
  implicit none

  real :: mat(10, 10)

  mat(:,:) = public_var

  call print_matrix(mat)

end program use_mod
```

__Example:__ explicit import list

```fortran
use my_mod, only: public_var
```

__Example:__ aliased import

```fortran
use my_mod, only: printMat=>print_matrix
```

Each module should be written in a separate `.f90` source file. Modules need to be compiled prior to any program units that `use` them.

---

## Derived types

As discussed previously in [Variables]({{site.baseurl}}/learn/quickstart/variables), there are five built-in data types in Fortran. A *derived type* is a special form of data type that can encapsulate other built-in types as well as other derived types. It could be considered equivalent to *struct* in the C and C++ programming languages.

### A quick take on derived types

Here's an example of a basic derived type:

```fortran
type :: t_pair
  integer :: i
  real :: x
end type
```

The syntax to create a variable of type `t_pair` and access its members is:

```fortran
! Declare
type(t_pair) :: pair
! Initialize
pair%i = 1
pair%x = 0.5
```

The percentage symbol `%` is used to access the members of a derived type.

In the above snippet, we declared an instance of a derived type and initialized its members explicitly.
You can also initialize derived type members by invoking the derived type constructor.

Example using the derived type constructor:

```fortran
pair = t_pair(1, 0.5)      ! Initialize with positional arguments
pair = t_pair(i=1, x=0.5)  ! Initialize with keyword arguments
pair = t_pair(x=0.5, i=1)  ! Keyword arguments can go in any order
```

Example with default initialization:

```fortran
type :: t_pair
  integer :: i = 1
  real :: x = 0.5
end type

type(t_pair) :: pair
pair = t_pair()       ! pair%i is 1, pair%x is 0.5
pair = t_pair(i=2)    ! pair%i is 2, pair%x is 0.5
pair = t_pair(x=2.7)  ! pair%i is 1, pair%x is 2.7
```

### Derived types in detail

The full syntax of a derived type with all optional properties is presented below:

```shell
type [,attribute-list] :: name [(parameterized-declaration-list)]
  [parameterized-definition-statements]
  [private statement or sequence statement]
  [member-variables]
contains
  [type-bound-procedures]
end type
```

### Options to declare a derived type

`attribute-list` may refer to the following:

* *access-type* that is either `public` or `private`
* `bind(c)` offers interoperability with C programming language
* `extends(`*parent*`)`, where *parent* is the name of a previously declared derived type from which the current derived type will inherit all its members and functionality
* `abstract` -- an object oriented feature that is covered in the advanced programming tutorial

If the attribute `bind(c)` or the statement `sequence` is used, then a derived type cannot have the attribute `extends` and vice versa.

The `sequence` attribute may be used only to declare that the following  members should be accessed in the same order as they are defined within the derived type.

Example with `sequence`:

```fortran
type :: t_pair
  sequence
  integer :: i
  real :: x
end type
! Initialize
type(t_pair) :: pair
pair = t_pair(1, 0.5)
```

The use of the statement `sequence` presupposes that the data types defined below are neither of `allocatable` nor of `pointer` type. Furthermore, it does not imply that these data types will be stored in memory in any particular form, i.e., there is no relation to the `contiguous` attribute.

The *access-type* attributes `public` and `private`, if used, declare that all member-variables declared below will be automatically assigned the attribute accordingly.

The attribute `bind(c)` is used to achieve compatibility between Fortran's derived type and C's struct.

Example with `bind(c)`:

```fortran
module f_to_c
  use iso_c_bindings, only: c_int
  implicit none

  type, bind(c) :: f_type
    integer(c_int) :: i
  end type

end module f_to_c
```

matches the following C struct type:

```c
struct c_struct {
  int i;
};
```

A fortran derived type with the attribute `bind(c)` cannot have the `sequence` and `extends` attributes. Furthermore it cannot contain any Fortran `pointer` or `allocatable` types.

`parameterized-declaration-list` is an optional feature. If used, then the parameters must be listed in place of `[parameterized-definition-statements]` and must be either `len` or `kind` parameters or both.

Example of a derived type with `parameterized-declaration-list` and with the attribute `public`:

 ```fortran
module m_matrix
  implicit none
  private

  type, public :: t_matrix(rows, cols, k)
    integer, len :: rows, cols
    integer, kind :: k = kind(0.0)
    real(kind=k), dimension(rows, cols) :: values
  end type

end module m_matrix

program test_matrix
  use m_matrix
  implicit none

  type(t_matrix(rows=5, cols=5)) :: m

end program test_matrix
 ```

In this example the parameter `k` has already been assigned a default value of `kind(0.0)` (single-precision floating-point). Therefore, it can be omitted, as is the case here in the declaration inside the main program.

By default, derived types and their members are public. However, in this example, the attribute `private` is used at the beginning of the module. Therefore, everything within the module will be by default `private` unless explicitly declared as `public`. If the type `t_matrix` was not given the attribute `public` in the above example, then the compiler would throw an error inside `program test`.

The attribute `extends` was added in the F2003 standard and introduces an important feature of the object oriented paradigm (OOP), namely inheritance. It allows code reusability by letting child types derive from extensible parent types: `type, extends(parent) :: child`. Here, `child` inherits all the members and functionality from `type :: parent`.

Example with the attribute `extends`:

```fortran
module m_employee
  implicit none
  private
  public t_date, t_address, t_person, t_employee
  ! Note another way of using the public attribute:
  ! gathering all public data types in one place.

  type :: t_date
    integer :: year, month, day
  end type

  type :: t_address
    character(len=:), allocatable :: city, road_name
    integer :: house_number
  end type

  type, extends(t_address) :: t_person
    character(len=:), allocatable :: first_name, last_name, e_mail
  end type

  type, extends(t_person)  :: t_employee
    type(t_date) :: hired_date
    character(len=:), allocatable :: position
    real :: monthly_salary
  end type

end module m_employee

program test_employee
  use m_employee
  implicit none
  type(t_employee) :: employee

  ! Initialization

  ! t_employee has access to type(t_date) members not because of extends
  ! but because a type(t_date) was declared within t_employee.
  employee%hired_date%year  = 2020  
  employee%hired_date%month = 1
  employee%hired_date%day   = 20

  ! t_employee has access to t_person, and inherits its members due to extends.
  employee%first_name = 'John'  
  employee%last_name  = 'Doe'
  
  ! t_employee has access to t_address, because it inherits from t_person,
  ! which in return inherits from t_address.
  employee%city         = 'London'
  employee%road_name    = 'BigBen'
  employee%house_number = 1

  ! t_employee has access to its defined members.
  employee%position       = 'Intern'
  employee%monthly_salary = 0.0

end program test_employee
```

### Options to declare members of a derived type

`[member-variables]` refers to the declaration of all the member data types. These data types can be of any built-in data type, and/or of other derived types, as already showcased in the above examples. However, member-variables can have their own extensive syntax, in form of:
`type [,member-attributes] :: name[attr-dependent-spec][init]`

`type`: any built-in type or other derived type

`member-attributes` (optional):

* `public` or `private` access attributes
* `protected` access attribute
* `allocatable` with or without `dimension` to specify a dynamic array
* `pointer`, `codimension`, `contiguous`, `volatile`, `asynchronous`

Examples of common cases:

```fortran
type :: t_example
  ! 1st case: simple built-in type with access attribute and [init]
  integer, private :: i = 0
  ! private hides it from use outside of the t_example's scope.
  ! The default initialization [=0] is the [init] part.

  ! 2nd case: protected
  integer, protected :: i
  ! In contrary to private, protected allows access to i assigned value outside of t_example
  ! but is not definable, i.e. a value may be assigned to i only within t_example.

  ! 3rd case: dynamic 1-D array
  real, allocatable, dimension(:) :: x
  ! the same as
  real, allocatable :: x(:)
  ! This parentheses' usage implies dimension(:) and is one of the possible [attr-dependent-spec].
end type
```

The following attributes: `pointer`, `codimension`, `contiguous`, `volatile`, `asynchronous` are advanced features that will not be addressed in the *Quickstart* tutorial. However, they are presented here, in order for the readers to know that these features do exist and be able to recognize them. These features will be covered in detail in the upcoming *Advanced programing* mini-book.

### Type-bound procedures

A derived type can contain functions or subroutines that are *bound* to it. We'll refer to them as *type-bound procedures*. Type-bound procedures follow the `contains` statement that, in turn, follows all member variable declarations.

It is impossible to describe type-bound procedures in full without delving into OOP features of modern Fortran. For now we'll focus on a simple example to show their basic use.

Here's an example of a derived type with a basic type-bound procedure:

```fortran
module m_shapes
  implicit none
  private
  public t_square

  type :: t_square
  real :: side
  contains
    procedure :: area  ! procedure declaration
  end type

contains

  ! Procedure definition
  real function area(self) result(res)
    class(t_square), intent(in) :: self
    res = self%side**2
  end function

end module m_shapes

program main
  use m_shapes
  implicit none

  ! Variables' declaration
  type(t_square) :: sq
  real :: x, side

  ! Variables' initialization
  side = 0.5
  sq%side = side

  x = sq%area()
  ! self does not appear here, it has been passed implicitly

  ! Do stuff with x...

end program main
```

What is new:

* `self` is an arbitrary name that we chose to represent the instance of the derived type `t_square` inside the type-bound function. This allows us to access its members and to automatically pass it as an argument when we invoke a type-bound procedure.
* We now use `class(t_square)` instead of `type(t_square)` in the interface of the `area` function. This allows us to invoke the `area` function with any derived type that extends `t_square`. The keyword `class` introduces the OOP feature polymorphism.

In the above example, the type-bound procedure `area` is defined as a function and can be invoked only in an expression, for example `x = sq%area()` or `print *, sq%area()`. If you define it instead as a subroutine, you can invoke it from its own `call` statement:

```fortran
! Change within module
contains
  subroutine area(self, x)
    class(t_square), intent(in) :: self
    real, intent(out) :: x
    x = self%side**2
  end subroutine

! ...

! Change within main program
call sq%area(x)

! Do stuff with x...
```

In contrast to the example with the type-bound function, we now have two arguments:

* `class(t_square), intent(in) :: self` -- the instance of the derived type itself
* `real, intent(out) :: x` -- used to store the calculated area and return to the caller
