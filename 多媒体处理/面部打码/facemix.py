#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
人脸马赛克处理工具
================

功能:自动检测并处理图片和视频中的人脸区域

作者:YourName
版本:1.0.0
日期:2025-02-23
"""
import time 
import cv2
import numpy as np
import os
from pathlib import Path
from tqdm import tqdm
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor
import subprocess

# 添加更健壮的依赖检查
try:
    import ffmpeg
except ImportError:
    print("警告: ffmpeg-python 库未安装,音频处理功能将不可用")
    print("请运行: pip install ffmpeg-python")
    ffmpeg = None

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    print("警告: moviepy 库未安装,视频信息提取功能将受限")
    print("请运行: pip install moviepy")
    VideoFileClip = None

print(cv2.cuda.getCudaEnabledDeviceCount())  # 如果>0则CUDA可用

class FaceMosaic:
    def __init__(self, effect_type='mosaic', effect_param=15, use_gpu=True, 
                 cpu_limit=0.7, gpu_memory_limit=0.8, max_workers=4):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.effect_type = effect_type
        self.effect_param = effect_param
        self.supported_images = {'.jpg', '.jpeg', '.png', '.bmp'}
        self.supported_videos = {'.mp4', '.avi', '.mov'}
        
        # 改进 GPU 检测方法
        try:
            if use_gpu and cv2.cuda.getCudaEnabledDeviceCount() > 0:
                self.use_gpu = True
                self.gpu_stream = cv2.cuda.Stream()
                print(f"已启用GPU加速 - 设备: {cv2.cuda.getDevice()}")
            else:
                self.use_gpu = False
                print("使用CPU处理")
        except Exception as e:
            print(f"GPU初始化失败: {e}")
            self.use_gpu = False
            print("使用CPU处理")
            
        # emoji 表情路径
        self.emoji_path = Path(__file__).parent / "emoji.png"
        if not self.emoji_path.exists():
            print("警告: emoji.png 文件不存在,将使用默认的马赛克效果")
            self.effect_type = 'mosaic'
        
        # 添加资源限制参数
        self.cpu_limit = cpu_limit  # CPU使用率上限(0-1)
        self.gpu_memory_limit = gpu_memory_limit  # GPU显存使用率上限(0-1)
        self.max_workers = max_workers  # 最大工作线程数
        
        # 创建线程池
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        
        if self.use_gpu:
            # 设置CUDA设备内存限制
            try:
                total_memory = cv2.cuda.DeviceInfo().totalMemory()
                allowed_memory = int(total_memory * self.gpu_memory_limit)
                cv2.cuda.setMemoryFraction(allowed_memory / total_memory)
            except Exception as e:
                print(f"设置GPU内存限制失败: {e}")

        # 检查FFmpeg是否可用
        try:
            subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.ffmpeg_available = True
            print("FFmpeg 可用 - 将保留视频声音")
        except (subprocess.SubprocessError, FileNotFoundError):
            self.ffmpeg_available = False
            print("警告: FFmpeg 不可用 - 处理后的视频将没有声音")

    def process_image(self, image_path, output_path):
        """处理单张图片"""
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"无法读取图片: {image_path}")
            return False
        
        processed_img = self.process_frame(img)
        return cv2.imwrite(str(output_path), processed_img)

    def process_video(self, video_path, output_path):
        """处理视频文件 - 修改版本"""
        video_path_str = str(video_path)
        output_path_str = str(output_path)
        
        # 创建临时目录用于存放帧
        temp_dir = Path(output_path_str).parent / f"temp_{Path(output_path_str).stem}"
        temp_dir.mkdir(exist_ok=True)
        temp_video = str(temp_dir / "temp_video.mp4")
        
        try:
            # 获取视频信息
            video_info = self._get_video_info(video_path_str)
            if not video_info:
                print(f"无法获取视频信息: {video_path}")
                return False
            
            fps, width, height, total_frames = video_info
            
            # 处理视频帧
            success = self._process_video_frames(video_path_str, temp_video, fps, width, height, total_frames)
            if not success:
                if temp_dir.exists():
                    import shutil
                    shutil.rmtree(temp_dir)
                return False
            
            # 如果FFmpeg可用,合并音频
            if self.ffmpeg_available:
                has_audio = self._check_video_has_audio(video_path_str)
                if has_audio:
                    print("合并音频...")
                    final_output = self._merge_audio_video(video_path_str, temp_video, output_path_str)
                    if final_output:
                        print("视频处理完成(含音频)")
                    else:
                        print("音频合并失败,输出无音频视频")
                        if os.path.exists(temp_video) and os.path.exists(output_path_str):
                            os.remove(output_path_str)
                        os.rename(temp_video, output_path_str)
                else:
                    print("原视频无音频,直接输出处理后的视频")
                    if os.path.exists(output_path_str):
                        os.remove(output_path_str)
                    os.rename(temp_video, output_path_str)
            else:
                # 没有FFmpeg,直接使用处理后的视频
                if os.path.exists(output_path_str):
                    os.remove(output_path_str)
                os.rename(temp_video, output_path_str)
            
            # 清理临时文件
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir)
            
            return True
            
        except Exception as e:
            print(f"视频处理过程中出现错误: {str(e)}")
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir)
            return False

    def _get_video_info(self, video_path):
        """获取视频信息"""
        try:
            # 尝试使用MoviePy获取更准确的视频信息
            clip = VideoFileClip(video_path)
            fps = clip.fps
            width, height = clip.size
            total_frames = int(clip.duration * clip.fps)
            clip.close()
            return fps, width, height, total_frames
        except:
            try:
                # 回退到OpenCV
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    return None
                fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()
                return fps, width, height, total_frames
            except:
                return None

    def _process_video_frames(self, video_path, output_path, fps, width, height, total_frames):
        """处理视频帧 - 优化版本"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False

        try:
            # 自动尝试多种编码器
            available_codecs = ['avc1', 'H264', 'mp4v', 'XVID']
            chosen_codec = None

            for codec in available_codecs:
                try:
                    fourcc = cv2.VideoWriter_fourcc(*codec)
                    test_path = output_path + ".test"
                    test_out = cv2.VideoWriter(
                        test_path,
                        fourcc,
                        fps,
                        (width, height),
                        True
                    )
                    
                    if test_out.isOpened():
                        test_out.release()
                        if os.path.exists(test_path):
                            os.remove(test_path)
                        chosen_codec = codec
                        print(f"选择编码器: {codec}")
                        break
                except Exception:
                    continue

            if not chosen_codec:
                print("无法找到可用的视频编码器，将使用默认编码器")
                chosen_codec = 'avc1'
                
            # 使用选定的编码器
            fourcc = cv2.VideoWriter_fourcc(*chosen_codec)
            
            out = cv2.VideoWriter(
                output_path,
                fourcc,
                fps,
                (width, height),
                True
            )
            
            # 设置高比特率
            if hasattr(out, 'set'):
                out.set(cv2.VIDEOWRITER_PROP_QUALITY, 100)
            
            # 避免丢帧的处理逻辑
            frames_processed = 0
            frames_missed = 0
            
            # 使用更大的批处理大小来提高效率
            batch_size = min(30, int(total_frames / 100) + 1)
            
            with tqdm(total=total_frames, desc="处理视频帧") as pbar:
                while True:
                    batch_frames = []
                    batch_indices = []
                    
                    # 读取一批帧
                    for _ in range(batch_size):
                        ret, frame = cap.read()
                        if not ret:
                            break
                        batch_indices.append(frames_processed)
                        batch_frames.append(frame)
                        frames_processed += 1
                    
                    if not batch_frames:
                        break  # 视频读取完毕
                    
                    # 处理每一帧
                    results = []
                    for idx, frame in enumerate(batch_frames):
                        try:
                            processed = self.process_frame(frame.copy())
                            results.append(processed)
                        except Exception as e:
                            print(f"\n处理第 {batch_indices[idx]} 帧时出错: {str(e)}")
                            results.append(frame)  # 使用原始帧
                            frames_missed += 1
                    
                    # 写入处理后的帧
                    for frame in results:
                        out.write(frame)
                        
                    pbar.update(len(batch_frames))
            
            cap.release()
            out.release()
            
            print(f"\n处理完成: 总帧数 {frames_processed}, 成功处理 {frames_processed - frames_missed} 帧")
            print(f"处理成功率: {(frames_processed - frames_missed) / frames_processed * 100:.2f}%")
            
            return True
            
        except Exception as e:
            print(f"视频帧处理错误: {str(e)}")
            cap.release()
            if 'out' in locals():
                out.release()
            return False
    
    def _check_video_has_audio(self, video_path):
        """检查视频是否有音频流"""
        try:
            probe = ffmpeg.probe(video_path)
            audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
            return len(audio_streams) > 0
        except:
            return False
    
    def _merge_audio_video(self, original_video, processed_video, output_path):
        """合并音频和视频"""
        try:
            # 方法一：使用ffmpeg-python的正确语法
            # 提取原始视频的音频
            ffmpeg.input(original_video).audio.output(f"{output_path}.temp.aac", 
                                                   codec='aac').run(quiet=True, overwrite_output=True)
            
            # 合并处理后的视频和原始音频
            video_stream = ffmpeg.input(processed_video).video
            audio_stream = ffmpeg.input(f"{output_path}.temp.aac").audio
            
            ffmpeg.output(video_stream, audio_stream, output_path, 
                        codec='copy', acodec='aac', vcodec='copy',
                        strict='experimental').run(quiet=True, overwrite_output=True)
            
            # 删除临时音频文件
            if os.path.exists(f"{output_path}.temp.aac"):
                os.remove(f"{output_path}.temp.aac")
                
            return True
        except Exception as e:
            print(f"音频合并失败: {str(e)}")
            print("尝试备用方法合并音频...")
            try:
                # 方法二：使用subprocess直接调用ffmpeg命令行
                subprocess.run([
                    'ffmpeg', '-i', processed_video, 
                    '-i', original_video, '-c:v', 'copy',
                    '-map', '0:v:0', '-map', '1:a:0?',
                    '-shortest', output_path
                ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # 删除临时音频文件
                if os.path.exists(f"{output_path}.temp.aac"):
                    os.remove(f"{output_path}.temp.aac")
                    
                return True
            except Exception as e2:
                print(f"备用方法合并失败: {str(e2)}")
                # 清理临时文件
                if os.path.exists(f"{output_path}.temp.aac"):
                    os.remove(f"{output_path}.temp.aac")
                return False

    def process_frame(self, frame):
        """处理单帧图像"""
        if self.use_gpu:
            # 将图像上传到GPU
            gpu_frame = cv2.cuda_GpuMat()
            gpu_frame.upload(frame)
            
            # 转换为灰度图
            gpu_gray = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)
            gray = gpu_gray.download()
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if self.use_gpu:
            for (x, y, w, h) in faces:
                roi = frame[y:y+h, x:x+w]
                gpu_roi = cv2.cuda_GpuMat()
                gpu_roi.upload(roi)
                
                if self.effect_type == 'blur':
                    gpu_processed = cv2.cuda.GaussianBlur(gpu_roi, 
                        (self.effect_param, self.effect_param), 0)
                    roi = gpu_processed.download()
                else:
                    # 对于马赛克和emoji效果仍使用CPU处理
                    roi = self.apply_effect(roi)
                    
                frame[y:y+h, x:x+w] = roi
        else:
            for (x, y, w, h) in faces:
                roi = frame[y:y+h, x:x+w]
                roi = self.apply_effect(roi)
                frame[y:y+h, x:x+w] = roi
                
        return frame

    def apply_effect(self, image):
        """应用不同的打码效果"""
        if self.effect_type == 'mosaic':
            return self.apply_mosaic(image)
        elif self.effect_type == 'blur':
            return self.apply_blur(image)
        elif self.effect_type == 'emoji':
            return self.apply_emoji(image)
        return image

    def apply_mosaic(self, image):
        """应用马赛克效果"""
        h, w = image.shape[:2]
        temp = cv2.resize(image, (self.effect_param, self.effect_param))
        return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

    def apply_blur(self, image):
        """应用模糊效果"""
        return cv2.GaussianBlur(image, (self.effect_param, self.effect_param), 0)

    def apply_emoji(self, image):
        """应用emoji表情效果"""
        try:
            emoji = cv2.imread(str(self.emoji_path), cv2.IMREAD_UNCHANGED)
            if emoji is None:
                print("警告: 无法读取emoji图片,使用马赛克效果替代")
                return self.apply_mosaic(image)
            
            # 调整emoji大小以适应人脸区域
            h, w = image.shape[:2]
            if h <= 0 or w <= 0:  # 添加尺寸检查
                return self.apply_mosaic(image)
                
            emoji = cv2.resize(emoji, (w, h))
            
            # 如果emoji有alpha通道,进行alpha混合
            if emoji.shape[2] == 4:
                alpha = emoji[:, :, 3] / 255.0
                alpha = np.clip(alpha, 0, 1)  # 确保alpha值在0-1之间
                result = image.copy()
                for c in range(3):
                    result[:, :, c] = image[:, :, c] * (1 - alpha) + emoji[:, :, c] * alpha
                return result
            else:
                return emoji[:, :, :3]
                
        except Exception as e:
            print(f"应用emoji失败: {e},使用马赛克效果替代")
            return self.apply_mosaic(image)

    def _limit_cpu_usage(self):
        """限制CPU使用率"""
        import win32process
        import win32api
        import win32con
        import time
        
        try:
            # 获取当前进程
            p = psutil.Process()
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, p.pid)
            
            while True:
                cpu_percent = psutil.cpu_percent(interval=1)
                if cpu_percent > self.cpu_limit * 100:
                    # 设置为低优先级
                    win32process.SetPriorityClass(handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
                    # 设置CPU亲和性来限制使用的CPU核心数
                    max_cores = int(psutil.cpu_count() * self.cpu_limit)
                    max_cores = max(1, max_cores)  # 至少保留一个核心
                    mask = (1 << max_cores) - 1  # 创建CPU掩码
                    win32process.SetProcessAffinityMask(handle, mask)
                else:
                    # 恢复正常优先级
                    win32process.SetPriorityClass(handle, win32process.NORMAL_PRIORITY_CLASS)
                    # 恢复使用所有CPU核心
                    mask = (1 << psutil.cpu_count()) - 1
                    win32process.SetProcessAffinityMask(handle, mask)
                
                time.sleep(1)
                
        except Exception as e:
            print(f"CPU限制设置失败: {e}")

    def process_directory(self, input_dir):
        """处理整个目录"""
        # 启动CPU限制监控线程
        cpu_monitor = threading.Thread(target=self._limit_cpu_usage, daemon=True)
        cpu_monitor.start()
        
        input_path = Path(input_dir)
        if not input_path.exists():
            print(f"错误:目录 {input_dir} 不存在")
            return

        # 收集所有需要处理的文件
        tasks = []
        for file_path in input_path.iterdir():
            suffix = file_path.suffix.lower()
            out_path = file_path.parent / f"{file_path.stem}_masked{suffix}"
            
            if suffix in self.supported_images:
                tasks.append((self.process_image, file_path, out_path))
            elif suffix in self.supported_videos:
                tasks.append((self.process_video, file_path, out_path))

        # 使用线程池并发处理文件
        try:
            futures = []
            for func, *args in tasks:
                future = self.thread_pool.submit(func, *args)
                futures.append((future, args[0]))
            
            # 等待所有任务完成并显示结果
            for future, file_path in futures:
                try:
                    success = future.result()
                    if success:
                        print(f"已处理: {file_path.name}")
                    else:
                        print(f"处理失败: {file_path.name}")
                except Exception as e:
                    print(f"处理 {file_path.name} 时出错: {str(e)}")
                    
        finally:
            self.thread_pool.shutdown()

def check_cuda_availability():
    """检查CUDA是否可用"""
    try:
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            device_name = cv2.cuda.getDevice()
            print(f"找到CUDA设备: {device_name}")
            print(f"CUDA版本: {cv2.cuda.getComputeCapability()}")
            return True
        else:
            print("未找到CUDA设备")
            return False
    except Exception as e:
        print(f"CUDA检查失败: {e}")
        return False

def download_openh264():
    """下载并安装OpenH264库"""
    try:
        import urllib.request
        import zipfile
        import shutil
        import sys
        
        openh264_url = "https://github.com/cisco/openh264/releases/download/v1.8.0/openh264-1.8.0-win64.dll.bz2"
        dll_path = os.path.join(os.path.dirname(sys.executable), "openh264-1.8.0-win64.dll")
        
        if os.path.exists(dll_path):
            print("OpenH264库已存在,无需下载")
            return True
            
        print("正在下载OpenH264库...")
        temp_file = "openh264-1.8.0-win64.dll.bz2"
        urllib.request.urlretrieve(openh264_url, temp_file)
        
        print("正在解压OpenH264库...")
        import bz2
        with bz2.BZ2File(temp_file, 'rb') as f_in, open(dll_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
        os.remove(temp_file)
        print(f"OpenH264库已成功安装到: {dll_path}")
        return True
    except Exception as e:
        print(f"下载OpenH264库失败: {e}")
        print("您可以手动下载安装: https://github.com/cisco/openh264/releases/download/v1.8.0/openh264-1.8.0-win64.dll.bz2")
        return False

def main():
    # 添加此行，确保OpenH264库被下载
    download_openh264()
    
    while True:
        input_dir = input("请输入需要处理的文件夹路径: ").strip()
        if input_dir:
            break
        print("路径不能为空,请重新输入")
    
    print("\n请选择打码效果:")
    print("1. 马赛克 (默认)")
    print("2. 模糊")
    print("3. Emoji表情")
    
    choice = input("请输入选择 (1-3): ").strip()
    
    # 设置默认效果参数
    effect_type = 'mosaic'
    effect_param = 15
    
    if choice == '2':
        effect_type = 'blur'
        effect_param = 25
    elif choice == '3':
        effect_type = 'emoji'
        effect_param = 15
    
    # 检查GPU可用性
    use_gpu = False
    if input("\n是否使用GPU加速? (y/n): ").lower().startswith('y'):
        use_gpu = check_cuda_availability()
    
    # 添加资源限制选项
    cpu_limit = float(input("\n请输入CPU使用率上限(0.1-1.0): ").strip() or "0.7")
    gpu_memory_limit = float(input("请输入GPU显存使用率上限(0.1-1.0): ").strip() or "0.8")
    max_workers = int(input("请输入最大工作线程数(1-16): ").strip() or "4")
    
    try:
        processor = FaceMosaic(
            effect_type=effect_type,
            effect_param=effect_param,
            use_gpu=use_gpu,
            cpu_limit=cpu_limit,
            gpu_memory_limit=gpu_memory_limit, 
            max_workers=max_workers
        )
        processor.process_directory(input_dir)
        print("\n处理完成!")
    except Exception as e:
        print(f"\n处理过程中出现错误: {str(e)}")
        print("请确保输入路径正确且具有足够的访问权限.")

if __name__ == "__main__":
    main()