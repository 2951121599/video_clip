# video_clip
GUI搜索关键信息进行短视频搜索剪辑。

## Basic Usage
### 1. Install requirements
```bash
pip install -r requirements.txt
```

### 2. Run the streamlit GUI
```bash
streamlit run app.py
```

## Parameters
### Text Prompt
使用提示描述信息搜索想要的场景，将返回几个与其相关的剪辑视频。
### Top N
要返回的视频剪辑数。
### Cut Sim
大约在0.44到0.6之间。数字越小，视频片段越长（精度越低）。
### CLIP-as-service Server
CLIP作为服务服务器的url。默认值是一个加载了Jina.ai提供的ViT-L/14-336px的演示服务器。您还可以运行自己的[CLIP as service](https://github.com/jina-ai/clip-as-service)服务器。