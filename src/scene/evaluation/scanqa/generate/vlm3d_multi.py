import os
import json
import argparse
from openai import OpenAI
from types import SimpleNamespace
from utils import *
from concurrent.futures import ThreadPoolExecutor, as_completed

DETAIL_OUTPUT = False
OVERWRITE_IMAGE = False  # 重新渲染图片
CONCURRENT_REQUESTS = 32  # VLM并发请求数
current_dir = os.path.dirname(os.path.abspath(__file__))
base64_dir = ""  # for cache
scanqa_val_dir = ""


class VLM3D:
    def __init__(self, client):
        self.client = client
        self.model_name = client.models.list().data[0].id
        print(f"Using model: {self.model_name}")

    def batch_response(
        self,
        prompts,
        image_paths=None,
        BEV=False,
        question_ids=None,
        view_mode="multi_view",
    ):
        """
        Support for 3D & 2D & pure text input with parallel processing
        """

        base64_images = [
            self.get_or_create_base64_image(image_path) for image_path in image_paths
        ]

        batch_messages = []
        for idx, (prompt, question_id) in enumerate(zip(prompts, question_ids)):
            messages = get_mllm_messages(
                prompt, base64_images[idx], view_mode=view_mode
            )
            batch_messages.append((messages, question_id))

        results = []
        ids = []
        completed = 0

        output_file = args.result_file

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

                # Write results in JSONL format
                with open(output_file, "a", encoding="utf-8") as outfile:
                    output_data = {"question_id": question_id, "response": result}
                    outfile.write(json.dumps(output_data, ensure_ascii=False) + "\n")

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

    parser = argparse.ArgumentParser(description="VLM3D System")
    parser.add_argument(
        "--result_file",
        type=str,
        default="",
        help="Path to save results",
    )
    parser.add_argument(
        "--image_dir",
        type=str,
        default="",
        help="Directory containing input images",
    )
    parser.add_argument(
        "--view_mode",
        type=str,
        default="combine",
        choices=["00", "01", "10", "11", "combine"],
        help="View mode for rendering",
    )

    args = parser.parse_args()
    client = OpenAI(api_key="EMPTY", base_url="http://localhost:8002/v1")
    vlm3d = VLM3D(client)

    prompts = []
    question_ids = []
    image_files = []

    # 读取已完成的问题ID
    finished_ids = set()
    try:
        with open(args.result_file, "r", encoding="utf-8") as outfile:
            for line in outfile:
                try:
                    finished_question = json.loads(line.strip())
                    finished_ids.add(finished_question["question_id"])
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        # 如果结果文件不存在，创建一个空文件
        with open(args.result_file, "w", encoding="utf-8") as f:
            pass

    # 读取JSON文件
    with open(
        os.path.join(scanqa_val_dir, "ScanQA_v1.0_val.json"),
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    images_dir = args.image_dir

    # 提取元素，跳过已完成的问题
    for item in data:
        question = item["question"]
        question_id = item["question_id"]
        scene_id = item["scene_id"]

        # 如果问题已经处理过，跳过
        if question_id in finished_ids:
            continue

        prompts.append(question)
        question_ids.append(question_id)
        if args.view_mode == "combine":
            image_files.append(f"{images_dir}/{scene_id}_4ei.png")
        elif args.view_mode == "00":
            image_files.append(f"{images_dir}/{scene_id}_00.png")
        elif args.view_mode == "01":
            image_files.append(f"{images_dir}/{scene_id}_01.png")
        elif args.view_mode == "10":
            image_files.append(f"{images_dir}/{scene_id}_10.png")
        elif args.view_mode == "11":
            image_files.append(f"{images_dir}/{scene_id}_11.png")

    print(f"Total questions: {len(data)}")
    print(f"Already processed: {len(finished_ids)}")
    print(f"Remaining to process: {len(prompts)}")

    responses, questions = vlm3d.batch_response(
        prompts,
        image_paths=image_files,
        question_ids=question_ids,
        view_mode=args.view_mode,
    )
