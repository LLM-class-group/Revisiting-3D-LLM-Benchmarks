import json
import sys, os


from nltk.tokenize import word_tokenize

import numpy as np
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.spice.spice import Spice

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

sys.path.append(os.path.join(os.getcwd()))

data_dir = "data/scanqa"
input_dir = ""  # add path of input file
file_names = []  # file names of five different views: bev, south, east, north, west


def get_lemma(ss):
    return [lemmatizer.lemmatize(token) for token in ss.split()]


def simple_ratio(numerator, denominator):
    num_numerator = sum([1 if token in numerator else 0 for token in denominator])
    num_denominator = len(denominator)
    return num_numerator / num_denominator


def tokens_unigram_f_value(ref: str, pred: str) -> float:
    ref_lemma = get_lemma(ref)
    pred_lemma = get_lemma(pred)
    precision = simple_ratio(ref_lemma, pred_lemma)
    recall = simple_ratio(pred_lemma, ref_lemma)
    return (
        2 * (recall * precision) / (recall + precision)
        if recall + precision != 0.0
        else 0
    )


def tokens_score(ref: str, pred: str) -> float:
    return 1.0 if ref == pred else 0.0


def evals_json(gold_data, preds):
    score_list = ["Top1 (EM)", "Top10 (EM)", "Top1 (F-value)"]
    score = {s: [] for s in score_list}

    for ins in gold_data:
        question_id = ins["question_id"]
        ref_answers = ins["answers"]
        pred = preds[question_id]

        # top-1
        answer = pred["answer_top10"][0]
        if answer in ref_answers:
            score["Top1 (EM)"].append(1)
            score["Top1 (F-value)"].append(1)
        else:
            scores = [tokens_unigram_f_value(answer, ref) for ref in ref_answers]
            score["Top1 (EM)"].append(0)
            score["Top1 (F-value)"].append(max(scores))

        # top-10
        for answer in pred["answer_top10"]:
            if answer in ref_answers:
                score["Top10 (EM)"].append(1)
                break
        else:
            score["Top10 (EM)"].append(0)

    rlt = {}
    for k, v in score.items():
        assert len(v) == len(gold_data), len(v)
        print(k, np.mean(v) * 100)
        rlt[k] = np.mean(v) * 100
    return rlt


def eval_pycoco(gold_data, preds, use_spice=False):
    score_list = [
        "Top1 (EM)",
        "Top10 (EM)",
        "Top1 (F-value)",
        "BLEU-1",
        "BLEU-2",
        "BLEU-3",
        "BLEU-4",
    ]
    score = {s: [] for s in score_list}

    scorers = [
        (Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]),
        (Meteor(), "METEOR"),
        (Rouge(), "ROUGE_L"),
        (Cider(), "CIDEr"),
    ]
    if use_spice:
        scorers.append((Spice(), "SPICE"))

    detail = {}

    gts_m = {ins["question_id"]: ins["answers"] for ins in gold_data}
    res_m = {qid: [value["answer_top10"][0]] for qid, value in preds.items()}

    question = {ins["question_id"]: ins["question"] for ins in gold_data}

    for question_id in gts_m:
        if question_id not in detail:
            detail[question_id] = {}
        detail[question_id]["all_answers"] = preds[question_id]["answer_top10"]
        detail[question_id]["question_id"] = question_id
        detail[question_id]["question"] = question[question_id]
        detail[question_id]["gts"] = gts_m[question_id]
        detail[question_id]["res"] = res_m[question_id]
        if area[question_id] == 0:
            detail[question_id]["area"] = "bev"
        elif area[question_id] == 1:
            detail[question_id]["area"] = "00o/00i"
        elif area[question_id] == 2:
            detail[question_id]["area"] = "01o/01i"
        elif area[question_id] == 3:
            detail[question_id]["area"] = "10o/10i"
        elif area[question_id] == 4:
            detail[question_id]["area"] = "11o/11i"

    # pycocoeval
    gts = {
        ins["question_id"]: [{"caption": ans} for ans in ins["answers"]]
        for ins in gold_data
    }
    res = {qid: [{"caption": value["answer_top10"][0]}] for qid, value in preds.items()}

    gts = {
        k: [" ".join(word_tokenize(d["caption"])) for d in v] for k, v in gts.items()
    }
    res = {
        k: [" ".join(word_tokenize(d["caption"])) for d in v] for k, v in res.items()
    }

    # =================================================
    # Compute scores
    # =================================================
    rlt = {}
    for scorer, method in scorers:
        eprint("computing %s score..." % (scorer.method()))
        score, scores = scorer.compute_score(gts, res)
        if type(method) == list:
            for sc, scs, m in zip(score, scores, method):
                print("%s: %0.3f" % (m, sc * 100))
                rlt[m] = sc * 100
                for k, scc in zip(gts.keys(), scs):
                    detail[k][m] = round(scc * 100, 3)
                    # if (detail [k][m] < 1e-3):
                    #     detail[k][m] = 0
        else:
            print("%s: %0.3f" % (method, score * 100))
            rlt[method] = score * 100
            for k, scc in zip(gts.keys(), scores):
                detail[k][method] = scc * 100

    output_file = "./output_scores.txt"
    # keys_to_delete = [k for k, v in detail.items() if need_del(v['question'])]

    # for k in keys_to_delete:
    #     del detail[k]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(detail, f, indent=4, sort_keys=True)

    return rlt


def need_del(question):
    if "where" in question.lower():
        return False
    if "what shape" in question.lower():
        return False
    if "what type" in question.lower():
        return False
    if "what kind" in question.lower():
        return False
    if "what is" in question.lower():
        return False
    return True


QT = ["Place", "Number", "Color", "Object nature", "Object", "Other"]


def qclass1(question):
    lques = question
    if "where" in lques.lower():
        return "Place"
    if "how many" in lques.lower():
        return "Number"
    if "what color" in lques.lower() or "what is the color" in lques.lower():
        return "Color"
    if "what shape" in lques.lower():
        # return 'Shape'
        return "Object nature"
    if "what type" in lques.lower():
        # return 'Type'
        return "Object nature"
    if "what kind" in lques.lower():
        # return 'Kind'
        return "Object nature"
    if "what is" in lques.lower():
        return "Object"
    return "Other"


if __name__ == "__main__":

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--use_spice", help="no spice", action="store_true")
    parser.add_argument("--detailed", help="", action="store_true")
    args = parser.parse_args()

    SPLITS = ["val"]

    ds = {
        split: json.load(open(os.path.join(data_dir, f"ScanQA_v1.0_{split}.json")))
        for split in SPLITS
    }

    #
    # val
    #
    area = {}
    with open(
        "src/scene/evaluation/scanqa/output_areas.txt", "r", encoding="utf-8"
    ) as file:
        for line in file:
            question_id, area_value = line.strip().split(": ")
            area[question_id] = int(area_value)

    files = [
        json.load(open(os.path.join(input_dir, fn), "r", encoding="utf-8"))
        for fn in file_names
    ]

    # 根据 area 中的 question_id 选择对应的 response
    preds = {}
    for idx, item in enumerate(files[0]):
        question_id = item["question_id"]
        file_index = area[question_id]
        response = files[file_index][idx]["response"]
        preds[question_id] = {"answer_top10": response}

    score = evals_json(ds["val"], preds)
    eval_pycoco(ds["val"], preds, use_spice=args.use_spice)
    print()
    print()
