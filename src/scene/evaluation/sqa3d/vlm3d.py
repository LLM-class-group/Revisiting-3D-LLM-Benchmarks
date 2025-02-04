from openai import OpenAI
import os
from render import render
from types import SimpleNamespace
from utils import *
from concurrent.futures import ThreadPoolExecutor, as_completed

DETAIL_OUTPUT = False
OVERWRITE_IMAGE = False     # 重新渲染图片
CONCURRENT_REQUESTS = 256     # VLM并发请求数
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, 'cached_images')


class VLM3D:
    def __init__(self, client):
        self.client = client
        self.model_name = "gpt-4o"
        # self.model_name = client.models.list().data[0].id
        print(f"Using model: {self.model_name}")

    def response(self, prompt, point_file=None, image_path=None, BEV=False):
        """
        Support for 3D & 2D & pure text input
        """
        if point_file:
            image_path = self.render(point_file, BEV)

        base64_image = encode_image(image_path)
        messages = get_mllm_messages(prompt, base64_image)
        return self._get_response(messages)

    def batch_response(self, prompts, point_files=None, image_paths=None, BEV=False):
        """
        Support for 3D & 2D & pure text input with parallel processing
        """
        DETAIL_OUTPUT = True

        if image_paths is None and point_files is None:
            batch_messages = [get_mllm_messages(prompt) for prompt in prompts]
        else:
            if image_paths is None:
                image_paths = [self.render(point_file, BEV) for point_file in point_files]
            
            base64_images = [encode_image(image_path) for image_path in image_paths]
            if DETAIL_OUTPUT:
                print(f"\nBatching {len(base64_images)} images")

            batch_messages = [get_mllm_messages(prompt, base64_image)
                          for prompt, base64_image in zip(prompts, base64_images)]

        results = [None] * len(batch_messages)  # 预分配结果列表
        with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
            # 创建future到索引的映射
            future_to_index = {
                executor.submit(self._get_response, messages): i 
                for i, messages in enumerate(batch_messages)
            }
            # 按完成顺序获取结果，但存储到正确的位置
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                results[index] = future.result()

        return results

    def render(self, point_file, BEV=False):
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

            if BEV:
                config.view = [0, 0, 2]
                config.rot = [90, 0, 20]

            # 加载点云数据
            pcl = load(point_file, separator=",")
            # 标准化点云
            pcl, center, scale = standardize_bbox(config, pcl)
            # 设置点云颜色
            pcl = color_map(config, pcl)
            # 渲染点云
            render(config, pcl, BEV)
            if DETAIL_OUTPUT:
                print(f"Rendered {point_file} to {image_path}")
        elif DETAIL_OUTPUT:
            print(f"Image {image_path} already exists")
        return image_path

    def _get_response(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=512,
            temperature=0.8
        )
        return completion.choices[0].message.content


if __name__ == "__main__":
    # Example use of VLM3D
    client = OpenAI()
    vlm3d = VLM3D(client)
    point_file =  "./data/example/instrument.npy"
    point2_file = "./data/example/turkle.pkl"
    prompt = "This is a point cloud of"
    responses = vlm3d.batch_response([prompt, prompt], [point_file, point2_file])
    for response in responses:
        print(response)
