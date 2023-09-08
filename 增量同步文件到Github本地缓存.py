from dirsync import sync
import os
import subprocess
source = './'
target = 'D:\\GitHub\\share'
# 同步源文件夹到目标文件夹
# result = sync(source, target, 'update', twoway=False)
result = sync(source, target, 'sync',recursive=True, twoway=False)
# 同步目标文件夹到源文件夹
# sync(target, source, 'update', twoway=True)
print(target)
# 添加所有修改的文件到 git 的暂存区
# subprocess.run(['git', 'add', '-A'],cwd=target)
# 获取同步的文件和文件夹列表
if result:
    synced_list = list(result)
else:
    synced_list = []
# 将列表转换为字符串，用逗号分隔
synced_str = ', '.join(synced_list)
print('Synced List'+synced_str)
# 提交修改并添加一条信息，包含同步的文件和文件夹
# subprocess.run(['git', 'commit', '-m', f'Sync files: {synced_str}'],cwd=target)
# subprocess.run(['git', 'log', '-1'],cwd=target)