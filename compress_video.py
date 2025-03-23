import os
import subprocess
from datetime import datetime

# 获取当前目录
current_dir = os.getcwd()

# 获取当前日期和时间，用于命名输出文件
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# 扫描当前目录中的所有 .mp4 文件
for filename in os.listdir(current_dir):
    if filename.endswith(".mp4"):
        # 获取文件的完整路径
        input_file = os.path.join(current_dir, filename)

        # 构建输出文件的名称（原文件名 + 当前日期时间）
        output_file = os.path.join(
            current_dir, f"{os.path.splitext(filename)[0]}_{current_time}.mp4"
        )

        # FFmpeg 命令：使用 H.265 (HEVC) 编码进行压缩，保持较好的质量
        command = [
            "ffmpeg",
            "-i",
            input_file,
            "-c:v",
            "hevc_nvenc",  # 使用 CUDA 加速的 HEVC 编码器（H.265）
            "-crf",
            "30",  # 设置压缩质量，30 比 35 更高质量
            "-preset",
            "medium",  # 使用中等压缩速度的预设，平衡速度和质量
            "-b:v",
            "1000k",  # 增加比特率至 1000kbps，避免画质过度压缩
            "-c:a",
            "aac",  # 使用 AAC 编码音频
            "-b:a",
            "128k",  # 降低音频比特率为 128kbps
            "-threads",
            "8",  # 使用多线程加速
            output_file,
        ]

        # 执行 FFmpeg 命令
        subprocess.run(command)

        print(f"文件 {filename} 已压缩并保存为 {output_file}")
