import subprocess
import os
from multiprocessing import Pool


def run_blender_script(input_output_pair):
    input_ply, output_image = input_output_pair
    blender_path = ""  # 修改为你的 Blender 可执行文件路径
    script_path = "./bev.py"
    cmd = [
        blender_path,
        "--background",
        "--python",
        script_path,
        "--",
        input_ply,
        output_image,
    ]
    subprocess.run(cmd)


if __name__ == "__main__":
    scene_file = ""  # .txt file that records the ID of the scene to be rendered
    input_directory = ""
    output_directory = ""
    os.makedirs(output_directory, exist_ok=True)

    with open(scene_file, "r", encoding="utf-8") as f:
        scenes = [line.strip() for line in f.readlines()]

    input_output_pairs = []
    for scene in scenes:
        input_ply = os.path.join(input_directory, f"{scene}_vh_clean_2.ply")

        output_image = os.path.join(output_directory, f"{scene}_bird.png")
        if not os.path.exists(output_image):  # 检查文件是否存在
            input_output_pairs.append((input_ply, output_image))

    with Pool(processes=4) as pool:  # 设置并行进程数
        pool.map(run_blender_script, input_output_pairs)
