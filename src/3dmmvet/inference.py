from openai import OpenAI
import os
import json
from tqdm import tqdm
import shortuuid
from sqa3d.utils import load, standardize_bbox, color_map
from sqa3d.render import render
from types import SimpleNamespace
import argparse
import base64

images_dir = './data/3dmmvet/images'
client = OpenAI()


def render_point_cloud_to_image(point_file):
    # 确保输出目录存在
    os.makedirs(images_dir, exist_ok=True)
    # 构建输出路径
    output_file_name = os.path.splitext(os.path.basename(point_file))[0] + '-2.png'
    output_path = os.path.join(images_dir, output_file_name)
    # 如果图片已存在则直接返回
    if os.path.exists(output_path):
        return output_path

    # 创建配置对象
    config = SimpleNamespace(
        workdir='temp_render',  # 临时工作目录
        output=output_path,  # 输出文件名
        path=point_file,  # 输入文件名
        res=[768, 768],        # 渲染分辨率
        radius=0.025,          # 点的半径
        contrast=0.0004,       # 对比度
        type="point",          # 渲染类型
        view=[2.75, 2.75, 2.75],  # 视角位置
        translate=[0, 0, 0],   # 平移参数
        scale=[1, 1, 1],       # 缩放参数
        white=False,            # 使用白色渲染
        RGB=[],                # RGB颜色设置（空表示使用默认）
        rot=[],                # 旋转参数（空表示使用默认）
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
        
    return output_path


def process_questions(point_folder, question_file, output_file, model):
    # 读取问题
    with open(question_file, "r") as f:
        questions = [json.loads(line) for line in f]
    
    # 检查输出文件是否包含目录路径
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # 读取已经处理过的问题ID
    processed_ids = set()
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            for line in f:
                try:
                    answer = json.loads(line)
                    processed_ids.add(answer["question_id"])
                except:
                    continue
    
    # 处理每个问题并写入答案
    with open(output_file, "a") as ans_file:
        for q in tqdm(questions):
            # 跳过已处理的问题
            if q["question_id"] in processed_ids:
                continue
                
            # 渲染点云图像
            point_path = os.path.join(point_folder, q["point"])
            image_path = render_point_cloud_to_image(point_path)
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            messages = get_mllm_messages(q["text"], base64_image)
            response = client.chat.completions.create(
                model=model,
                messages=messages
            ).choices[0].message.content

            # 保存结果
            answer = {
                "question_id": q["question_id"],
                "prompt": q["text"],
                "text": response,
                "answer_id": shortuuid.uuid(),
                "model_id": model,
                "metadata": {}
            }
            ans_file.write(json.dumps(answer) + "\n")
            ans_file.flush()


def get_mllm_messages(instruction, base64_image):
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
                {
                    "type": "text",
                    "text": instruction
                },
            ],
        },
    ]
    return messages


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--point-folder", type=str, default="./data/3dmmvet/points")
    parser.add_argument("--question-file", type=str, default="./data/3dmmvet/question.jsonl")
    parser.add_argument("--answers-file", type=str, default="./data/3dmmvet/answers/gpt-4o.jsonl")
    parser.add_argument("--model", type=str, default="gpt-4o")
    args = parser.parse_args()

    process_questions(args.point_folder, args.question_file, args.answers_file, args.model)
