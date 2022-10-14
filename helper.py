from clip_client import Client
from docarray import Document, DocumentArray
import imagehash
from PIL import Image
import numpy as np


def get_keyframes_data(video_data: 'np.ndarray', cut_sim: float):
    # 切出视频片段 使用文字搜索 通过感知哈希的算法 去比较两个帧哈希值的相似度
    last_hash = imagehash.phash(Image.fromarray(video_data[0]))  # 初始化: 计算第一帧的哈希值
    key_frames = [0]  # 关键帧列表
    frame_num = 0
    for each_frame in video_data:
        frame_hash = imagehash.phash(Image.fromarray(each_frame))  # 当前帧的hash值
        similarity = 1 - (last_hash - frame_hash) / len(frame_hash.hash) ** 2  # 计算相似度
        if similarity < cut_sim:  # cut_sim 大约在0.44到0.6之间。数字越小，视频片段越长（精度越低）
            key_frames.append(frame_num)  # 抽出来所有的关键帧
        frame_num += 1
        last_hash = frame_hash  # 更新哈希值
    video_length = len(video_data)
    key_frames.append(video_length)
    # 把视频搜索任务 转换为图片搜索任务 拼接图片
    keyframes_data = [((i, key_frames[key_frames.index(i)+1]), video_data[i]) for i in key_frames if i != video_length]
    return keyframes_data


def search_frame(keyframe_data: list, prompt: str, topn: int, server_url: str):
    client = Client(server_url)
    da = DocumentArray([Document(tags={'left': str(tup[0][0]), 'right': str(tup[0][1])}, tensor=tup[1]) for tup in keyframe_data])
    d = Document(text=prompt, matches=da)
    r = client.rank([d])
    result = r['@m', ['tags', 'tensor', 'scores__clip_score__value']]
    return [each[:topn] for each in result]
