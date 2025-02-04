import json
import sys, os
import copy


from nltk.tokenize import word_tokenize


import numpy as np


from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider
from pycocoevalcap.spice.spice import Spice

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

sys.path.append(os.path.join(os.getcwd()))

DETAILED_EVAL = False
data_path = ""
input_path = ""


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def file_write(str, file_name=""):
    with open(file_name, "a") as file:
        file.write(str + "\n")


def convert_numpy_int64_to_int(obj):
    if isinstance(obj, np.int64):
        return int(obj)
    raise TypeError


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
        answer = pred["response"][0]
        if answer in ref_answers:
            score["Top1 (EM)"].append(1)
            score["Top1 (F-value)"].append(1)
        else:
            scores = [tokens_unigram_f_value(answer, ref) for ref in ref_answers]
            score["Top1 (EM)"].append(0)
            score["Top1 (F-value)"].append(max(scores))

        # top-10
        for answer in pred["response"]:
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


def evals_json(gold_data, preds, avg=False):

    ## todo 10 次采样结果，如何对 EM 和 F1 进行平均?

    score_list = ["Top1 (EM)", "Top10 (EM)", "Top1 (F-value)"]
    score = {s: [] for s in score_list}

    for ins in gold_data:
        question_id = ins["question_id"]
        ref_answers = ins["answers"]
        pred = preds[question_id]

        # top-1
        answer = pred["response"][0]
        if answer in ref_answers:
            score["Top1 (EM)"].append(1)
            score["Top1 (F-value)"].append(1)
        else:
            scores = [tokens_unigram_f_value(answer, ref) for ref in ref_answers]
            score["Top1 (EM)"].append(0)
            score["Top1 (F-value)"].append(max(scores))

        # top-10
        for answer in pred["response"]:
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


def evals_json_multi(gold_data, preds_list, avg=False):
    for mode, preds in preds_list.items():
        evals_json(gold_data, preds, avg=avg)


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
    res_m = {qid: [value["response"][0]] for qid, value in preds.items()}

    question = {ins["question_id"]: ins["question"] for ins in gold_data}

    meteor_score = 0
    for question_id in gts_m:
        if question_id not in detail:
            detail[question_id] = {}
        detail[question_id]["question_id"] = question_id
        detail[question_id]["question"] = question[question_id]
        detail[question_id]["ground_truth"] = gts_m[question_id]
        detail[question_id]["response"] = res_m[question_id]
        detail[question_id]["meteor"] = score * 100

    # pycocoeval
    gts = {
        ins["question_id"]: [{"caption": ans} for ans in ins["answers"]]
        for ins in gold_data
    }
    res = {qid: [{"caption": value["response"][0]}] for qid, value in preds.items()}

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
    print(len(gts), len(res))
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

    output_file = "./output_scores.json"
    keys_to_delete = [k for k, v in detail.items() if need_del(v["question"])]

    for k in keys_to_delete:
        del detail[k]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(detail, f, indent=4, sort_keys=True)

    return rlt


def eval_pycoco_multi(
    gold_data, preds_dict_origin, use_spice=False, all_sample_num=10, used_sample_num=1
):

    file_write(f"\nEvaluating {used_sample_num} samples for each question...")

    preds_dict = copy.deepcopy(preds_dict_origin)  # 深拷贝，防止修改原字典

    ## 仅仅取前 used_sample_num 个采样结果进行评估
    for mode, preds in preds_dict.items():
        for qid, value in preds.items():
            value["response"] = value["response"][:used_sample_num]
            for response in value["response"]:
                response = response.lower()

    detail_results = {}
    result = {}

    questions = {ins["question_id"]: ins["question"] for ins in gold_data}
    answers = {ins["question_id"]: ins["answers"] for ins in gold_data}

    for question_id in questions.keys():
        if question_id not in detail_results:
            detail_results[question_id] = {}
            detail_results[question_id]["response"] = {}
            detail_results[question_id]["mode"] = {}
            detail_results[question_id]["question_id"] = question_id
            detail_results[question_id]["question"] = questions[question_id]
            detail_results[question_id]["ground_truth"] = answers[question_id]

    # reformat for pycocoeval
    gts = {
        ins["question_id"]: [{"caption": ans} for ans in ins["answers"]]
        for ins in gold_data
    }
    gts = {
        k: [" ".join(word_tokenize(d["caption"])) for d in v] for k, v in gts.items()
    }

    reformat_preds_dict = {}
    for mode, preds in preds_dict.items():
        reformat_preds_dict[mode] = []
        for idx in range(used_sample_num):
            sample_results = {
                qid: [{"caption": value["response"][idx]}]
                for qid, value in preds.items()
            }  # mode 下的第 idx 次采样的所有结果
            reformat_preds_dict[mode].append(sample_results)
            reformat_preds_dict[mode][idx] = {
                k: [" ".join(word_tokenize(d["caption"])) for d in v]
                for k, v in reformat_preds_dict[mode][idx].items()
            }

    # ## ------------------------------------------------
    # ### BLEU
    # ## ------------------------------------------------

    # blue_scorer = Bleu(4)
    # blue_method = ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]
    # blue_best = {}
    # blue_score = {}
    # for idx, res in enumerate(res_list):
    #     score, scores = blue_scorer.compute_score(gts, res)
    #     for sc, scs, m in zip(score, scores, blue_method):
    #         if m != "Bleu_1":
    #             continue
    #         for k, scc in zip(gts.keys(), scs):
    #             if k not in blue_score:
    #                 blue_score[k] = scc
    #                 blue_best[k] = idx
    #             else:
    #                 blue_score[k] = max(blue_score[k], scc)
    #                 blue_best[k] = idx if blue_score[k] == scc else blue_best[k]

    # blue_res = {k: res_list[v][k] for k, v in blue_best.items()}
    # score, scores = blue_scorer.compute_score(gts, blue_res)
    # eprint("computing %s score..." % (blue_scorer.method()))
    # for sc, scs, m in zip(score, scores, blue_method):
    #     print("%s: %0.3f" % (m, sc * 100))
    #     result[m] = sc * 100
    #     for k, scc in zip(gts.keys(), scs):
    #         detail_results[k][m] = round(scc * 100, 3)
    #         detail_results[k]["response"][m] = blue_res[k]
    #         detail_results[k]["mode"][m] = filenames[int(blue_best[k])]

    ## ------------------------------------------------
    ## Meteor, ROUGE, CIDEr, SPICE
    ## ------------------------------------------------

    scorers = [
        (Meteor(), "METEOR"),
        (Rouge(), "ROUGE_L"),
        (Cider(), "CIDEr"),
    ]
    if use_spice:
        scorers.append((Spice(), "SPICE"))

    for scorer, method in scorers:
        file_write(f"computing {scorer.method()} score...")

        max_modes = ["bev"] * len(gts)
        max_avg_scores = [0] * len(gts)

        for mode in preds_dict.keys():  # 遍历所有视角模式
            score_list = []
            scores_list = []
            avg_scores = []
            all_sample_results = reformat_preds_dict[mode]
            for sample_results in all_sample_results:  # 遍历所有采样结果
                score, scores = scorer.compute_score(gts, sample_results)
                score_list.append(score)
                scores_list.append(scores)

            for k in range(len(scores_list[0])):  # 遍历所有问题
                avg_score = sum([scores[k] for scores in scores_list]) / len(
                    scores_list
                )
                avg_scores.append(avg_score)

            for k, avg_score in enumerate(avg_scores):
                if avg_score > max_avg_scores[k]:
                    max_avg_scores[k] = avg_score
                    max_modes[k] = mode

        final_score = sum(max_avg_scores) / len(max_avg_scores)
        file_write(f"{method}: {final_score * 100}")
        result[method] = final_score * 100

        for question_id, score, mode in zip(gts.keys(), max_avg_scores, max_modes):
            detail_results[question_id][method] = score * 100
            detail_results[question_id]["response"][method] = preds_dict[mode][
                question_id
            ]["response"]
            detail_results[question_id]["mode"][method] = mode

    return result


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

    SPLITS = ["val"]

    dataset = {
        split: json.load(open(os.path.join(data_path, f"ScanQA_v1.0_{split}.json")))
        for split in SPLITS
    }

    if DETAILED_EVAL:
        for split in ["val"]:
            preds_list = []
            for filename in [".json"]:  # add filenames here
                with open(
                    os.path.join(input_path, f"{filename}"), "r", encoding="utf-8"
                ) as file:
                    preds = json.load(file)
                preds_list.append(
                    {
                        item["question_id"]: {"response": item["response"]}
                        for item in preds
                    }
                )

            golds = dataset[split]
            scores = {}

            preds_ = {k: {} for k in QT}
            golds_ = {k: [] for k in QT}
            # for qid,g in golds.items():
            for g in golds:
                qid = g["question_id"]
                preds_[qclass1(g["question"])][qid] = preds[qid]
                golds_[qclass1(g["question"])].append(g)

            for qt in QT:
                score = evals_json(golds_[qt], preds_[qt])
                print()
                score2 = eval_pycoco(golds_[qt], preds_[qt], use_spice=args.use_spice)
                score.update(score2)
                scores[f"{split}.{qt}"] = score
            print(split, scores)
            json.dump(
                scores, open("./eval.detailed.json", "w"), indent=4, sort_keys=True
            )

    else:
        preds_dict = {}  # 初始化一个字典，用于存储每个文件的预测结果
        modes = ["bev", "00", "10", "01", "11"]

        selected_modes = modes[0:1]

        file_write(f"------ Selected modes: {selected_modes} -------")

        for mode in selected_modes:
            with open(
                os.path.join(input_path, f"{mode}_merge.json"),
                "r",
                encoding="utf-8",
            ) as file:
                preds = json.load(file)
                preds_dict[mode] = {
                    item["question_id"]: {"response": item["response"]}
                    for item in preds
                }

        ## Top1 (EM), Top10 (EM), Top1 (F-value)
        # score = evals_json_multi(dataset["val"], preds_dict)
        eval_pycoco_multi(
            dataset["val"],
            preds_dict,
            use_spice=False,
            all_sample_num=20,
            used_sample_num=20,
        )

        # ## BLEU-1, BLEU-2, BLEU-3, BLEU-4, ROUGE_L, CIDEr
        # for used_sample_num in range(2, 21, 2):
        #     eval_pycoco_multi(dataset["val"], preds_dict, use_spice=False, all_sample_num=20, used_sample_num=used_sample_num)
