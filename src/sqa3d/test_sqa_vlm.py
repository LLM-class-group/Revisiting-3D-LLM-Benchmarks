from openai import OpenAI
from tqdm import tqdm
from simple_loader import load_test_data, BEV
from vlm3d import VLM3D, CONCURRENT_REQUESTS
import json
import os
from datetime import datetime

image_dir = "./data/sqa3d/images/bev" if BEV else "./data/sqa3d/images/mv"
answer_path = "./data/sqa3d/answer_dict.jsonl"
question_path = "./data/sqa3d/balanced/v1_balanced_questions_test_scannetv2.json"
annotation_path = "./data/sqa3d/balanced/v1_balanced_sqa_annotations_test_scannetv2.json"

log_response_file = "./log_openai/response-mv-outside.jsonl"
openai_client = OpenAI()
qwen_client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8002/v1"
)
judge_model = "gpt-4o-mini"


def get_prompt(question, situation, category, category_answers):
    prompt = f"""
        You are an AI agent situated in a 3D environment. You will be provided with:
        1. A bird's-eye view (BEV) image of the entire scene
        2. A text description of your specific situation in the scene

        First, understand your specific position, orientation, and surroundings based on both the BEV image and situation description. Then, reason about the spatial relationships from your perspective to answer questions.

        Example:
        BEV: A bird's-eye view of a room containing a bed, a sofa, and a coffee table.
        Situation: Sitting at the edge of the bed, facing the sofa.
        Question: Can I walk directly to the coffee table in front of me?
        Answer: no

        Response Guidelines:
        1. Locate your position and orientation in the scene
        2. Analyze spatial relationships with surrounding objects
        3. Provide a direct answer without explanation

        Current Situation: {situation}
        Question: {question}
        Answer: """ if BEV else f"""
        You are an AI agent situated in a 3D environment. You will be provided with:
        1. Multiple views of the scene from different angles
        2. A text description of your specific situation in the scene

        First, understand your specific position, orientation, and surroundings based on both the multi-view images and situation description. Then, reason about the spatial relationships from your perspective to answer questions.

        Example:
        Scene views: Multiple views of a room containing a bed, a sofa, and a coffee table.
        Situation: Sitting at the edge of the bed, facing the sofa.
        Question: Can I walk directly to the coffee table in front of me?
        Answer: no

        Response Guidelines:
        1. Locate your position and orientation in the scene
        2. Analyze spatial relationships with surrounding objects
        3. Provide a direct answer without explanation

        Current Situation: {situation}
        Question: {question}
        Answer:
        """ 
    return prompt


def is_answer_match(model_answer: str, correct_answer: str) -> bool:
    """
    Use LLM to check if the model's answer semantically matches the correct answer
    """
    model_answer = model_answer.lower()
    correct_answer = correct_answer.lower()
    
    # Return True for exact matches
    if model_answer.strip() == correct_answer.strip():
        return True
        
    # Construct prompt for LLM to judge answer equivalence
    prompt = f"""
    Your task is to determine if two answers are semantically equivalent.
    Please respond with only "yes" or "no".

    Examples:
    Ground truth: yes
    Model response: true
    Answer: yes

    Ground truth: one
    Model response: 1
    Answer: yes

    Ground truth: tables
    Model response: table
    Answer: yes

    Ground truth: three
    Model response: two
    Answer: no

    ---

    Ground truth: {correct_answer}
    Model response: {model_answer}
    Answer:"""

    try:
        response = openai_client.chat.completions.create(
            model=judge_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=0
        )

        llm_answer = response.choices[0].message.content.strip().lower()
        print(f"llm judge: {llm_answer}")
        return llm_answer == "yes"
    
    except Exception as e:
        print(f"Answer matching error: {e}")
        return False


def test_with_vlm3d(data_dict, vlm3d, all_possible_answers):
    """测试VLM3D模型并记录每个问题的响应结果"""
    
    q_type_mapping = {
        0: 'what', 1: 'is', 2: 'how',
        3: 'can', 4: 'which', 5: 'other'
    }
    
    question_records = []
    cached_responses = []
    
    # 读取已缓存的responses
    if os.path.exists(log_response_file):
        with open(log_response_file, 'r') as f:
            cached_responses = f.readlines()
    
    try:
        # 准备所有prompts和需要新生成response的问题
        prompts = []
        new_questions_idx = []
        
        # 确定需要新生成response的问题
        start_idx = len(cached_responses)
        for idx, (q, s) in enumerate(zip(data_dict['questions'], data_dict['situations'])):
            if idx >= start_idx:
                prompt = get_prompt(q, s, None, None)
                prompts.append(prompt)
                new_questions_idx.append(idx)
        
        # 只对未缓存的问题调用模型
        if prompts:
            print(f"Generating responses for {len(prompts)} new questions...")
            BATCH_SIZE = CONCURRENT_REQUESTS
            
            with open(log_response_file, 'a') as f:
                for i in tqdm(range(0, len(prompts), BATCH_SIZE)):
                    batch_prompts = prompts[i:i + BATCH_SIZE]
                    batch_images = [data_dict['images'][idx] for idx in new_questions_idx[i:i + BATCH_SIZE]]
                    batch_responses = vlm3d.batch_response(batch_prompts, image_paths=batch_images)
                    
                    # 写入新的responses
                    for response in batch_responses:
                        f.write(f"{response}\n")
                        cached_responses.append(response + "\n")

        # 评估所有问题的结果
        for idx, (response, answer, q_type) in enumerate(zip(
            cached_responses,
            data_dict['answer_texts'],
            data_dict['q_types']
        )):
            is_correct = is_answer_match(response, answer)
            category = q_type_mapping.get(q_type, 'other')
            
            record = {
                'question': data_dict['questions'][idx],
                'situation': data_dict['situations'][idx],
                'image_path': data_dict['images'][idx],
                'model_answer': response.rstrip('\n'),
                'ground_truth': answer,
                'is_correct': is_correct,
                'category': category
            }
            question_records.append(record)
        
        total_correct = sum(1 for r in question_records if r['is_correct'])
        total_accuracy = total_correct / len(question_records)
        
        return total_accuracy, question_records

    except Exception as e:
        print(f"Error processing data: {e}")
        return 0, []


def collect_ground_truth_answers(data_dict):
    """收集所有实际出现的ground truth答案"""
    category_answers = {
        'what': set(),
        'is': set(),
        'how': set(),
        'can': set(),
        'which': set(),
        'other': set()
    }
    
    q_type_mapping = {
        0: 'what',
        1: 'is',
        2: 'how',
        3: 'can',
        4: 'which',
        5: 'other'
    }
    
    for answer, q_type in zip(data_dict['answer_texts'], data_dict['q_types']):
        category = q_type_mapping.get(q_type, 'other')
        category_answers[category].add(answer.strip().lower())
    
    return {k: sorted(list(v)) for k, v in category_answers.items()}


# Usage Example
if __name__ == "__main__":
    vlm3d = VLM3D(openai_client)
    # Load data
    data_dict, all_possible_answers = load_test_data(image_dir, answer_path, question_path, annotation_path)
    print("Total data count:", len(data_dict['images']))

    # Limit test samples
    test_size = None
    # for key in data_dict.keys():
    #     data_dict[key] = data_dict[key][:test_size]

    print(f"Testing with {len(data_dict['images'])} samples...")
    
    # 运行测试
    accuracy, question_records = test_with_vlm3d(data_dict, vlm3d, all_possible_answers)
    
    # 按类别统计准确率
    category_stats = {}
    for record in question_records:
        category = record['category']
        if category not in category_stats:
            category_stats[category] = {'correct': 0, 'total': 0}
        
        category_stats[category]['total'] += 1
        if record['is_correct']:
            category_stats[category]['correct'] += 1
    
    # 打印各类别准确率
    print("\n=== 分类准确率 ===")
    for category, stats in category_stats.items():
        acc = stats['correct'] / stats['total']
        print(f"{category}: {acc:.2%} ({stats['correct']}/{stats['total']})")
    
    print(f"\n整体准确率: {accuracy:.2%}")
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {
        'timestamp': timestamp,
        'test_size': test_size,
        'overall_accuracy': accuracy,
        'category_accuracy': {
            cat: stats['correct']/stats['total'] 
            for cat, stats in category_stats.items()
        },
        'category_stats': category_stats,
        'question_records': question_records
    }
    
    # 使用时间戳创建唯一的文件名
    result_file = f"./log_openai/questions_{timestamp}.json"
    with open(result_file, 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
