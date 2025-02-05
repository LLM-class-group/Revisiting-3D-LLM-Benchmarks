import json
from ptstext_eval import Ptstext_EvalCap

def format_data(ground_truth_data, result_data):
    """Format the data"""

    gts = {}
    res = {}
    id_mapping = {}
    
    # Create ID mapping
    for idx, item in enumerate(ground_truth_data, 1):  # Start numbering from 1
        object_id = item["object_id"]
        id_mapping[object_id] = str(idx)  # Convert the index to a string
        gts[str(idx)] = item["captions"]
    
    # Process result data and number according to ground truth order
    for item in result_data:
        pcd_id = item["object_id"]
        if pcd_id in id_mapping:
            new_id = id_mapping[pcd_id]
            res[new_id] = [item["description"]]
    
    # Sort the results
    gts = dict(sorted(gts.items(), key=lambda x: int(x[0])))
    res = dict(sorted(res.items(), key=lambda x: int(x[0])))
    
    return gts, res

def evaluate_and_report():
    """Format data and evaluate the results"""
    
    # Read the ground truth data
    with open('./data/objaverseXL-LVIS_caption/annotations/cap3d_caption_test.json', 'r', encoding='utf-8') as f:
        ground_truth_data = json.load(f)
    
    # Read the result data
    with open('./data/objaverseXL-LVIS_caption/result/result.json', 'r', encoding='utf-8') as f:
        result_data = json.load(f)

    # Format the data
    gts, res = format_data(ground_truth_data, result_data)

    # Evaluate using Ptstext_EvalCap
    ptstext_evalcap = Ptstext_EvalCap()
    ptstext_evalcap.evaluate(gts, res)

    # Output the evaluation results
    for metric, score in ptstext_evalcap.eval.items():
        print(f"{metric}: {score:.3f}")
    
    # Write the evaluation results to the log file
    log_stats = {"test": {k: v for k, v in ptstext_evalcap.eval.items()}}
    with open('./data/objaverseXL-LVIS_caption/result/evaluate.txt', "a") as f:
        f.write(json.dumps(log_stats) + "\n")


if __name__ == "__main__":
    evaluate_and_report()