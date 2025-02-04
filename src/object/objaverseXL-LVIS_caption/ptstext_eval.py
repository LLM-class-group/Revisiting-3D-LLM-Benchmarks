from pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.rouge.rouge import Rouge
from pycocoevalcap.cider.cider import Cider

class Ptstext_EvalCap:
    """
    Evaluate the performance of 3D-QA model
    """
    def __init__(self):
        self.eval = {}

    def evaluate(self, gts, res):
        print('setting up scorers...')
        scorers = [
            (Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]),
            (Rouge(), "ROUGE_L"),
            (Cider(), "CIDEr")
        ]

        for scorer, method in scorers:
            print('computing %s score...'%(scorer.method()))
            score, scores = scorer.compute_score(gts, res)
            print(f"score for method {method}: {score}")
            
            if type(method) == list:
                for sc, scs, m in zip(score, scores, method):
                    self.setEval(sc, m)
                    print("%s: %0.3f"%(m, sc))
            else:
                self.setEval(score, method)
                print("%s: %0.3f"%(method, score))

    def setEval(self, score, method):
        self.eval[method] = score


