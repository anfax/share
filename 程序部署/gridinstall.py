# 一键部署grid-model项目的python脚本
# 作者：Bing
# 日期：2023-05-12
# 注意：这个脚本是自动生成的，可能有错误或不完善的地方，请在使用之前仔细检查和测试

# 导入需要的模块
import os
import subprocess
import sys

# 定义一些常量
REPO_URL = "https://github.com/annehutter/grid-model.git" # 项目的github地址
REPO_NAME = "grid-model" # 项目的名称
REPO_DIR = os.path.join(os.getcwd(), REPO_NAME) # 项目的本地目录
ENV_NAME = "grid-env" # 虚拟环境的名称
ENV_DIR = os.path.join(REPO_DIR, ENV_NAME) # 虚拟环境的目录
REQ_FILE = os.path.join(REPO_DIR, "requirements.txt") # 依赖包的文件

# 定义一些辅助函数
def run_command(cmd):
    """运行一个命令，并打印输出和错误"""
    print(f"Running: {cmd}")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())
    return process.returncode

def check_git():
    """检查是否安装了git，并返回git的路径"""
    git_path = shutil.which("git")
    if not git_path:
        print("Error: git is not installed. Please install git first.")
        sys.exit(1)
    return git_path

def check_python():
    """检查是否安装了python，并返回python的路径"""
    python_path = shutil.which("python")
    if not python_path:
        print("Error: python is not installed. Please install python first.")
        sys.exit(1)
    return python_path

def check_pip():
    """检查是否安装了pip，并返回pip的路径"""
    pip_path = shutil.which("pip")
    if not pip_path:
        print("Error: pip is not installed. Please install pip first.")
        sys.exit(1)
    return pip_path

def check_venv():
    """检查是否安装了venv，并返回venv的路径"""
    venv_path = shutil.which("venv")
    if not venv_path:
        print("Error: venv is not installed. Please install venv first.")
        sys.exit(1)
    return venv_path

def clone_repo():
    """克隆项目到本地目录"""
    if os.path.exists(REPO_DIR):
        print(f"Warning: {REPO_DIR} already exists. Skipping cloning.")
    else:
        git_path = check_git()
        cmd = f"{git_path} clone {REPO_URL}"
        ret = run_command(cmd)
        if ret != 0:
            print(f"Error: failed to clone {REPO_URL}. Please check the error message and try again.")
            sys.exit(1)

def create_env():
    """创建虚拟环境"""
    if os.path.exists(ENV_DIR):
        print(f"Warning: {ENV_DIR} already exists. Skipping creating environment.")
    else:
        python_path = check_python()
        venv_path = check_venv()
        cmd = f"{python_path} -m {venv_path} {ENV_DIR}"
        ret = run_command(cmd)
        if ret != 0:
            print(f"Error: failed to create virtual environment {ENV_NAME}. Please check the error message and try again.")
            sys.exit(1)

def activate_env():
    """激活虚拟环境"""
    activate_file = os.path.join(ENV_DIR, "bin", "activate")
    if not os.path.exists(activate_file):
        print(f"Error: {activate_file} does not exist. Please check the environment creation and try again.")
        sys.exit(1)
    cmd = f"source {activate_file}"
    ret = run_command(cmd)
    if ret != 0:
        print(f"Error: failed to activate virtual environment {ENV_NAME}. Please check the error message and try again.")
        sys.exit(1)

def install_req():
    """安装依赖包"""
    if not os.path.exists(REQ_FILE):
        print(f"Error: {REQ_FILE} does not exist. Please check the repository and try again.")
        sys.exit(1)
    pip_path = check_pip()
    cmd = f"{pip_path} install -r {REQ_FILE}"
    ret = run_command(cmd)
    if ret != 0:
        print(f"Error: failed to install requirements. Please check the error message and try again.")
        sys.exit(1)

def main():
    """主函数"""
    print("Starting to deploy grid-model project...")
    clone_repo()
    create_env()
    activate_env()
    install_req()
    print("Finished deploying grid-model project. Enjoy!")

if __name__ == "__main__":
    main()
