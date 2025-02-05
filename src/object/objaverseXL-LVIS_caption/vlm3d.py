import os
import json
from openai import OpenAI
from render import render
from types import SimpleNamespace
from utils import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from prompt import prompt

DETAIL_OUTPUT = True
OVERWRITE_IMAGE = False     # re-render images
CONCURRENT_REQUESTS = 16    # VLm concurrent requests

images_dir = './data/objaverseXL-LVIS_caption/images'
result_file = './data/objaverseXL-LVIS_caption/result/result2.json'

class VLM3D:
    def __init__(self, client):
        self.client = client

        if USE_OPENAI:
            self.model_name = "gpt-4o"
        else:
            self.model_name = client.models.list().data[0].id

        print(f"Using model: {self.model_name}")

    def response(self, prompt, point_file=None, image_path=None):
        """
        Support for 3D & 2D & pure text input
        """
        if point_file:
            image_path = self.render(point_file)

        base64_image = encode_image(image_path)
        messages = get_mllm_messages(prompt, base64_image)
        return self._get_response(messages)

    def batch_response(self, prompts, object_ids, point_files):
        """
        Support for 3D & 2D & pure text input with parallel processing
        """
        image_paths = [self.render(point_file) for point_file in point_files]
        base64_images = [encode_image(image_path)
                         for image_path in image_paths]

        batch_messages = []
        for idx, prompt in enumerate(prompts):
            object_id = object_ids[idx]
            base64_image = base64_images[idx]
            # 创建一个包含 messages 和 object_id 的元组
            messages = get_mllm_messages(prompt, base64_image)
            batch_messages.append((messages, object_id))
            
        results = []
        completed = 0
        with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
            futures = [executor.submit(self._get_response, message_tuple) 
                      for message_tuple in batch_messages]
            # 等待所有任务完成并获取结果
            for future in as_completed(futures):
                completed += 1
                print(f"{completed}/{len(point_files)} ({completed/len(point_files)*100:.1f}%)")
                results.append(future.result())

        return results
    

    def single_response(self, prompt, object_id, image_path):
        """
        Support for 3D & 2D & pure text input with parallel processing
        """
        base64_images = encode_image(image_path)
        
        messages = get_mllm_messages(prompt, base64_images)
        message_tuple = ((messages, object_id))
        response_text, object_id = self._get_response(message_tuple)
            
    def render(self, point_file):
        """
        Render point cloud to image

        Returns: image path
        """
        # 确保输出目录存在
        os.makedirs(images_dir, exist_ok=True)
        # 构建图片路径
        image_file_name = os.path.splitext(
            os.path.basename(point_file))[0] + '.png'
        image_path = os.path.join(images_dir, image_file_name)
        # 如果图片不存在
        if not os.path.exists(image_path) or OVERWRITE_IMAGE:
            # 渲染图片
            # 创建配置对象
            config = SimpleNamespace(
                workdir='temp_render',  # 临时工作目录
                output=image_path,     # 输出文件名
                path=point_file,       # 输入文件名
                res=[768, 768],        # 渲染分辨率
                radius=0.025,          # 点的半径
                contrast=0.0004,       # 对比度
                type="point",          # 渲染类型
                view=[2.75, 2.75, 2.75],  # 视角位置
                translate=[0, 0, 0],   # 平移参数
                scale=[1, 1, 1],       # 缩放参数
                white=False,           # 使用白色渲染
                RGB=[],                # RGB颜色设置（空表示使用默认）
                rot=[0, 0, 180],        # 旋转参数（空表示使用默认）
                median=None,           # 中值滤波
                separator=",",         # 文本分隔符
                mask=False,            # 点云遮罩
                bgr2rgb=False,         # BGR 转 RGB
                single_view=False,     # 单视图点云
                upsample=1,            # 点云上采样
                num=float('inf'),      # 下采样点数
                knn=False,             # 是否使用KNN颜色映射
                center_num=24,         # KNN中心点数量
                part=False,            # 是否进行KNN聚类并分段渲染
                render=True,           # 使用mitsuba渲染
                tool=False,            # 是否使用实时点云可视化工具
                bbox='none'            # 实时工具边界框可视化
            )

            # 加载点云数据
            pcl = load(point_file, separator=",")
            # 标准化点云
            pcl, center, scale = standardize_bbox(config, pcl)
            # 设置点云颜色
            pcl = color_map(config, pcl)
            # 渲染点云
            render(config, pcl)
            if DETAIL_OUTPUT:
                print(f"Rendered {point_file} to {image_path}")
        elif DETAIL_OUTPUT:
            print(f"Image {image_path} already exists")
        return image_path

    def _get_response(self, message_tuple):
        messages, object_id = message_tuple  # 解包元组

        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=512,
            temperature=0.8
        )
        response_text = completion.choices[0].message.content
        # print(f"result for {object_id}: {response_text}")
        return response_text, object_id





USE_OPENAI = True

if __name__ == "__main__":
    # Example use of VLM3D
    
    if USE_OPENAI:
        api_key=""
        base_url=""
    else:
        api_key = "EMPTY"
        base_url="http://localhost:8002/v1"
    
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    vlm3d = VLM3D(client)
    point_folder = "./data/objaverseXL-LVIS_caption/point_cloud"
    point_files = [os.path.join(point_folder, f) for f in os.listdir(point_folder)]
    object_ids = [os.path.splitext(f)[0] for f in os.listdir(point_folder)]
    prompts = [prompt] * len(point_files)

    responses = vlm3d.batch_response(prompts, object_ids, point_files)
    results = []
    for response in responses:
        results.append({"object_id": response[1], "description": response[0]})

    with open(result_file, 'w') as f:
        json.dump(results, f, indent=4)
    
    # For single response
    # vlm3d.single_response(prompt, "a0c493acb14047a4b8524b92c829cde5", "./data/objaverseXL-LVIS_caption/images/0a1be4094d844d72b225de98da809b02.png")



