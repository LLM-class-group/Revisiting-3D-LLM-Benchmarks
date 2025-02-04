import os
import json
from openai import OpenAI
from utils import *
from concurrent.futures import ThreadPoolExecutor, as_completed

DETAIL_OUTPUT = False
OVERWRITE_IMAGE = False  # 重新渲染图片
CONCURRENT_REQUESTS = 32  # VLM并发请求数
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, "cached_images")
base64_dir = ""  # for cache
scanqa_val_dir = ""


class VLM3D:
    def __init__(self, client):
        self.client = client
        self.model_name = client.models.list().data[0].id
        print(f"Using model: {self.model_name}")

    def batch_response(self, prompts, image_paths=None, BEV=False, question_ids=None):
        """
        Support for 3D & 2D & pure text input with parallel processing
        """

        base64_images = [
            self.get_or_create_base64_image(image_path) for image_path in image_paths
        ]

        batch_messages = []
        for idx, (prompt, question_id) in enumerate(zip(prompts, question_ids)):
            messages = get_mllm_messages(prompt, base64_images[idx])
            batch_messages.append((messages, question_id))

        results = []
        ids = []
        completed = 0
        with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
            futures = [
                executor.submit(self._get_response, message_tuple)
                for message_tuple in batch_messages
            ]
            # 等待所有任务完成并获取结果
            for future in as_completed(futures):
                completed += 1
                result, question_id = future.result()
                results.append(result)
                ids.append(question_id)
                print(f"Completed {completed}/{len(prompts)}")

                # 实时存储结果
                with open("temp_bev.json", "a", encoding="utf-8") as outfile:
                    output_data = {"question_id": question_id, "response": result}
                    json.dump(output_data, outfile, ensure_ascii=False, indent=4)
                    outfile.write("\n")  # 添加换行符以分隔每个 JSON 对象

        return results, ids

    def get_or_create_base64_image(self, image_path):
        """
        获取或创建 base64 编码的图像
        """
        # 确保 base64 缓存目录存在
        os.makedirs(base64_dir, exist_ok=True)
        base64_file_path = os.path.join(
            base64_dir, os.path.basename(image_path) + ".txt"
        )

        # 如果 base64 文件存在，读取并返回
        if os.path.exists(base64_file_path):
            with open(base64_file_path, "r", encoding="utf-8") as f:
                return f.read()

        # 否则，创建 base64 编码并存储到文件
        base64_image = encode_image(image_path)
        with open(base64_file_path, "w", encoding="utf-8") as f:
            f.write(base64_image)
        return base64_image

    def _get_response(self, messages_tuple):
        messages, question_id = messages_tuple
        completions = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=512,
            temperature=0.8,
            n=10,  # 采样10次
        )

        # 提取所有10个响应内容
        responses = [completion.message.content for completion in completions.choices]

        return responses, question_id


if __name__ == "__main__":
    client = OpenAI(api_key="EMPTY", base_url="http://localhost:8080/v1")
    vlm3d = VLM3D(client)

    # 读取JSON文件
    with open(
        os.path.join(scanqa_val_dir, "ScanQA_v1.0_val.json"), X, "r", encoding="utf-8"
    ) as file:
        data = json.load(file)

    prompts = []
    question_ids = []
    image_files = []
    # 提取元素
    output_data = []

    for item in data:
        question = item["question"]
        question_id = item["question_id"]
        scene_id = item["scene_id"]

        prompts.append(question)
        question_ids.append(question_id)

        bev_path = ""
        image_files.append(
            os.path.join(bev_path, f"{scene_id}_bird.png")
        )  # append the file path of bev image

    responses, questions = vlm3d.batch_response(
        prompts, image_paths=image_files, question_ids=question_ids
    )
    answers = {}
    for response, question in zip(responses, questions):
        answers[question] = response

    # 将responses逐条写入JSON文件
    output_data = []
    for item in data:
        output_data.append(
            {
                "question_id": item["question_id"],
                "scene_id": item["scene_id"],
                "question": item["question"],
                "answers": item["answers"],
                "object_ids": item["object_ids"],
                "object_names": item["object_names"],
                "response": answers[item["question_id"]],
            }
        )

    with open("bev.json", "w", encoding="utf-8") as outfile:
        json.dump(output_data, outfile, ensure_ascii=False, indent=4)
