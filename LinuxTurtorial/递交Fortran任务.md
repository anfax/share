# 在Linux上递交Fortran程序任务

在Linux上递交Fortran程序任务常用到的command-line有以下几种：

- `gfortran`：GNU Fortran编译器，是一个可以将Fortran源代码编译成可执行文件的命令。它需要一个或多个文件作为参数，并可以使用-o选项指定输出文件的名称。例如：

```shell
gfortran code.f90 -o code1
```

- `./`：运行可执行文件的命令，需要在文件名前加上`./`表示当前目录。例如：

```shell
./code1
```

- `ssh`：Secure Shell的缩写，是一个可以安全地连接到远程服务器并在上面运行命令的协议和命令。它需要一个用户名和一个远程主机的IP地址或主机名作为参数，并会要求输入密码进行验证。例如：

```shell
ssh -X username@I.P. address
```

- `mkdir`：make directory 的缩写，是一个可以创建目录的命令。它需要一个参数，即要创建的目录的路径。它有很多选项和参数，可以用来控制创建过程中的行为或权限设置。例如：

```shell
mkdir directoryname
```

- `sbatch`：submit batch job 的缩写，是一个可以递交批处理作业到集群系统的命令。它需要一个参数，即包含作业信息和命令的脚本文件。它有很多选项和参数，可以用来控制作业的资源需求，运行时间，输出文件等。例如：

```shell
sbatch job.sh
```

## 递交任务的脚本

```bash
#!/bin/sh
# 指定使用sh作为脚本的解释器

#SBATCH --nodes=1 --ntasks-per-node=2
# 指定使用1个节点，每个节点上运行2个任务

#SBATCH --partition=n20
# 指定使用n20分区，即使用20核的节点

#SBATCH --error=%J.stderr
# 指定将错误信息输出到以作业ID命名的stderr文件中

#SBATCH --output=%J.stdout
# 指定将正常信息输出到以作业ID命名的stdout文件中

# Assuming that you will use 64 bit compiler
source /apps/intel/2018u2/bin/compilervars.sh intel64
# 加载Intel编译器的环境变量，假设使用64位编译器

echo "--------------------------------------------------------"
echo "  JOBID: $SLURM_JOB_ID"
echo "  The job was started at `date`"
echo "  The job was running at $SLURM_JOB_NODELIST "
# 打印作业ID，开始时间和运行节点的信息

TMPDIR=/scr/tmp/$USER/$SLURM_JOB_ID
mkdir -p $TMPDIR
WORKDIR=$PWD
\cp -rf $WORKDIR/* $TMPDIR
cd $TMPDIR
# 创建一个临时目录，并将当前目录下的所有文件复制到临时目录中，然后切换到临时目录

# Run openmp Job
export OMP_NUM_THREADS=$SLURM_NTASKS_PER_NODE
ulimit -m unlimited
ulimit -s unlimited
./a.out
# 运行OpenMP作业，设置每个节点上的线程数为任务数，取消内存和栈的限制，执行可执行文件a.out

\cp -rf $TMPDIR/* $WORKDIR
# 将临时目录下的所有文件复制回当前目录

# Delete the tmp File
rm -rf $TMPDIR
# 删除临时目录

cd $WORKDIR
# 切换回当前目录

echo "  The job was finished at `date`"
echo "--------------------------------------------------------"
# 打印作业结束时间的信息
```

## 定制自己的脚本

如果你的程序不需要复制当前目录下的所有文件到临时目录，而只需要复制可执行文件和输入文件，你可以修改复制文件的命令，只复制需要的文件。这样可以节省磁盘空间和时间。例如，如果你的可执行文件叫`a.out`，输入文件叫`input.txt`，你可以修改这两行为：

```bash
\cp -f $WORKDIR/a.out $WORKDIR/input.txt $TMPDIR
\cp -f $TMPDIR/output.txt $WORKDIR
```

如果你的程序不需要输出任何信息到标准输出或标准错误，你可以修改输出文件的参数，将它们重定向到`/dev/null`。这样可以节省磁盘空间和避免不必要的信息。例如，你可以修改这两行为：

```bash
#SBATCH --error=/dev/null
#SBATCH --output=/dev/null
```

如果你的程序不需要打印作业的开始时间和结束时间，你可以删除打印信息的命令。这样可以简化代码和避免不必要的信息。例如，你可以删除这几行：

```bash
echo "--------------------------------------------------------"
echo "  JOBID: $SLURM_JOB_ID"
echo "  The job was started at `date`"
echo "  The job was running at $SLURM_JOB_NODELIST "
echo "  The job was finished at `date`"
echo "--------------------------------------------------------"
```

## 残缺数据传回

如果程序运行中途出错，或者任务被终止，你可以使用scp命令或者rsync命令将产生的数据从远程服务器传回本地。以下是一些使用方法：

`scp`：Secure Copy Protocol的缩写，是一个可以安全地复制文件和目录在两个位置之间的命令，通常是在Unix或Linux系统之间。该协议确保传输的文件是加密的，以防止有可疑意图的人获取敏感信息。要使用`scp`命令，你需要知道远程服务器的IP地址或主机名，以及你的用户名和密码。你也需要指定源文件或目录和目标文件或目录的路径。例如，如果你想从远程服务器10.10.0.2复制一个文件叫data.txt到本地目录/home/user，你可以使用这个命令：

```shell
scp user@10.10.0.2:/path/to/data.txt /home/user
```

`rsync`：remote synchronization的缩写，是一个可以同步文件和目录在两个位置之间的命令，通常是在Unix或Linux系统之间。该命令可以检测文件和目录的变化，并只传输有变化的部分，以节省时间和带宽。要使用`rsync`命令，你也需要知道远程服务器的IP地址或主机名，以及你的用户名和密码。你也需要指定源文件或目录和目标文件或目录的路径。例如，如果你想从远程服务器10.10.0.2同步一个目录叫data到本地目录`/home/user`，你可以使用这个命令：

```shell
rsync -avzh --stats --progress user@10.10.0.2:/path/to/data /home/user
```
