import json
import os
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def download_video_clip(youtube_id, start_time, end_time, output_path):
    try:
        video_url = f"https://www.youtube.com/watch?v={youtube_id}"
        yt = YouTube(video_url)

        # 选择最高质量的视频流
        video_stream = yt.streams.get_highest_resolution()

        # 下载视频
        video_stream.download(output_path=output_path, filename=f"{youtube_id}.mp4")
        
        # 剪裁视频
        input_path = os.path.join(output_path, f"{youtube_id}.mp4")
        output_filename = f"{youtube_id}_{start_time}_{end_time}.mp4"
        output_path = os.path.join(output_path, output_filename)

        video_clip = VideoFileClip(input_path).subclip(start_time, end_time)
        
        # 提取音频流
        audio_clip = AudioFileClip(input_path).subclip(start_time, end_time)
        
        # 将音频流添加到视频剪辑中
        video_clip = video_clip.set_audio(audio_clip)
        
        # 保存剪裁后的视频
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    except Exception as e:
        error_message = f"Error processing train video {input_path}: {e}\n"
        print(error_message)
        with open("/Users/yussiiy/code/video_music/error_ids.txt", "a") as error_file:
            error_file.write(error_message)
            
    try:
        os.remove(input_path)
    except OSError as e:
        error_message = f"Error deleting train video {input_path}: {e}"
        print(error_message)
        with open("/Users/yussiiy/code/video_music/error_ids.txt", "a") as error_file:
            error_file.write(error_message)

def download_video(youtube_id,output_path):

    video_url = f'https://www.youtube.com/watch?v={youtube_id}'
    print(f"Downloading video with ID: {youtube_id}")

    try:
        # 创建YouTube对象
        yt = YouTube(video_url)
                
        # 选择要下载的视频流（可以根据需要选择不同质量的视频流）
        video_stream = yt.streams.get_highest_resolution()
                
        # 下载视频
        video_stream.download(output_path=output_path, filename=f"{youtube_id}.mp4")
                
        print(f"Downloaded video with ID: {youtube_id}")
    except Exception as e:
        error_message=f"Error downloading video with ID {youtube_id}: {e}"
        print(error_message)
        with open("/Users/yussiiy/code/video_music/error_ids.txt", "a") as error_file:
            error_file.write(error_message)

    print("Download complete.")


if __name__ == "__main__":
    # json_path="/workspace/CondFoleyGen/data/countixAV_train.json"
    # with open(json_path, 'r') as file:
    #     data = json.load(file)

    # output_path = "/workspace/CondFoleyGen/data/ImpactSet/countixAV/train"

    # for item in data:
    #     youtube_id = item[:11]  # 提取YouTube ID
    #     start_time = item[12:16]  # 提取开始秒数
    #     end_time = item[17:]  # 提取结束秒数
        
    #     print(f'id:{youtube_id},start:{start_time},end:{end_time}')

    #     download_video_clip(youtube_id, start_time, end_time, output_path)
        
        # 打开并读取文本文件
    file_path = '/Users/yussiiy/code/video_music/video_list.txt'
    output_path="/Users/yussiiy/code/video_music/data"
    with open(file_path, 'r') as file:
        for line in file:
            video_id = line.strip()  # 去除行尾的换行符和空格
            download_video(video_id,output_path)