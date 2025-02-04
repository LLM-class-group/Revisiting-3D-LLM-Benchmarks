import json
import os
from PIL import Image

MULTI_VIEW = False
BEV = True

def load_test_data(image_dir, answer_path, question_path, annotation_path):
    """
    加载测试数据
    Args:
        image_dir: BEV图像目录
        answer_path: 答案字典文件路径
        question_path: 问题文件路径
        annotation_path: 标注文件路径
    Returns:
        data_dict: 包含所有数据的字典
        all_answers: 所有可能的答案文本列表
    """
    # 加载答案字典
    with open(answer_path, 'r') as f:
        answer_dict = json.load(f)
        ans2id = answer_dict[0]  # 答案到ID的映射
        id2ans = answer_dict[1]  # ID到答案的映射
        all_answers = list(ans2id.keys())  # 获取所有可能的答案文本
    
    # 加载问题数据
    with open(question_path, 'r') as f:
        data = json.load(f)
        questions = data['questions']  # 获取questions数组

    # 加载标注数据
    with open(annotation_path, 'r') as f:
        annotations = json.load(f)['annotations']
        
    # 创建问题ID到标注ID的映射
    qid2annoid = {}
    for i in range(len(annotations)):
        qid2annoid[annotations[i]["question_id"]] = i
    
    # 构建数据字典
    data_dict = {
        'images': [],
        'image_prefixes': [],     
        'questions': [],   
        'situations': [],  
        'answers': [],     
        'answer_texts': [],
        'q_types': []     
    }
    
    # 问题类型映射
    type_mapping = {
        'what': 0,
        'is': 1,
        'how': 2,
        'can': 3,
        'which': 4,
        'other': 5
    }
    
    # 填充数据字典
    for q in questions:
        # 获取图像路径
        image_path = os.path.join(image_dir, q['scene_id'] + '_bird.png' if BEV else q['scene_id'] + '.png')
        image_path_prefix = os.path.join(image_dir, q['scene_id'])
        if not os.path.exists(image_path) and not MULTI_VIEW:
            print(f"警告: 图像不存在 {image_path}")
            continue
            
        # 添加数据
        data_dict['images'].append(image_path)
        data_dict['image_prefixes'].append(image_path_prefix)
        data_dict['questions'].append(q['question'])
        data_dict['situations'].append(q['situation'])
        
        # 获取答案
        q_id = q['question_id']
        if q_id in qid2annoid:
            answer_text = annotations[qid2annoid[q_id]]["answers"][0]["answer"]
            # 保存答案文本
            data_dict['answer_texts'].append(answer_text)
            # 使用答案字典获取答案ID
            if answer_text not in ans2id:
                answer_id = len(ans2id)  # 对于未知答案，使用最后一个类别
            else:
                answer_id = ans2id[answer_text]
            data_dict['answers'].append(answer_id)
        else:
            data_dict['answers'].append(-1)  # 对于没有答案的情况使用-1
            data_dict['answer_texts'].append('')  # 对于没有答案的情况使用空字符串
        
        # 获取问题类型
        first_word = q['question'].lower().split()[0]
        q_type = type_mapping.get(first_word, 5)  # 默认为 'other'
        data_dict['q_types'].append(q_type)
    
    return data_dict, all_answers

def get_batch(data_dict, start_idx, batch_size=1):
    """
    获取一个批次的数据
    Args:
        data_dict: 数据字典
        start_idx: 起始索引
        batch_size: 批次大小
    Returns:
        batch_dict: 包含一个批次数据的字典
    """
    end_idx = min(start_idx + batch_size, len(data_dict['images']))
    
    batch_dict = {
        'images': [],
        'questions': [],
        'answers': [],
        'answer_texts': [],
        'q_types': []
    }
    
    for i in range(start_idx, end_idx):
        # 加载图像
        image = Image.open(data_dict['images'][i])
        
        # 添加数据到批次
        batch_dict['images'].append(image)
        batch_dict['questions'].append(data_dict['questions'][i])
        batch_dict['answers'].append(data_dict['answers'][i])
        batch_dict['answer_texts'].append(data_dict['answer_texts'][i])
        batch_dict['q_types'].append(data_dict['q_types'][i])
    
    return batch_dict

# 使用示例
if __name__ == "__main__":
    # 设置数据路径
    split = 'test'
    image_dir = "./data/sqa3d/images/bev" if BEV else "./data/sqa3d/images/mv"
    answer_path = "./data/sqa3d/answer_dict.json"
    question_path = f"./data/sqa3d/balanced/v1_balanced_questions_{split}_scannetv2.json"
    annotation_path = f"./data/sqa3d/balanced/v1_balanced_sqa_annotations_{split}_scannetv2.json"
    
    # 加载数据
    data_dict, all_possible_answers = load_test_data(image_dir, answer_path, question_path, annotation_path)
    
    # 打印一些基本信息
    print(f"总共加载了 {len(data_dict['images'])} 个样本")
    if len(data_dict['images']) > 0:
        id = 1
        print("\n示例数据:")
        print(f"场景ID: {os.path.basename(data_dict['images'][id]).replace('.png', '')}")
        print(f"情境: {data_dict['situations'][id]}")
        print(f"问题: {data_dict['questions'][id]}")
        print(f"答案: {data_dict['answers'][id]}")
        print(f"答案文本: {data_dict['answer_texts'][id]}")
        print(f"问题类型: {data_dict['q_types'][id]}") 
    
    # 打印所有可能的答案
    print(f"\n所有可能的答案 ({len(all_possible_answers)} 个):")
    # print(all_possible_answers)