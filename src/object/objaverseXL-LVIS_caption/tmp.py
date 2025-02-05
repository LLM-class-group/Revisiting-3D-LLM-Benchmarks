import os

dir_path = '/Users/jinjiahe/Desktop/学习与课程/大三/计算机视觉/Revisiting-3D-LLM-Benchmarks/data/objaverseXL-LVIS_caption/images'

# 遍历文件夹里的所有文件，如果是以'_2.png' 结尾，则删除
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith('_2.png'):
            os.remove(os.path.join(root, file))