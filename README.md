Here’s the complete `README.md` for your repository based on the provided content and structure:

---

# Revisiting 3D LLM Benchmarks: Are We Really Testing 3D Capabilities?

<p align="center"><img width="540" src="docs/2d cheating.png"></p>

This is the official repository of our paper **Revisiting 3D LLM Benchmarks: Are We Really Testing 3D Capabilities?** by [Jiahe Jin](https://github.com/zizi0123), [Yanheng He](https://github.com/henryhe0123), and [Mingyan Yang](https://github.com/fircube).

## Abstract
In this work, we identify the "2D-Cheating" problem in 3D LLM evaluation, where these tasks might be easily solved by VLMs with rendered images of point clouds, exposing ineffective evaluation of 3D LLMs' unique 3D capabilities. We test VLM performance across multiple 3D LLM benchmarks and, using this as a reference, propose principles for better assessing genuine 3D understanding. We also advocate explicitly separating 3D abilities from 1D or 2D aspects when evaluating 3D LLMs.

## Usage

<p align="center"><img width="540" src="docs/benchmark overview.png"></p>

We conducted experiments on the above benchmarks. See the commands for reproducing each experiment as follows:

### 3D MM-Vet

### ObjaverseXL-LVIS Caption

#### **Generating Results**
To generate captioning results using the model, run the following command:


```bash
python ./src/object/objaverseXL-LVIS_caption/vlm3d.py
```

#### **Evaluating Results**

To evaluate the generated captions against ground truth data, run the following command:

```bash
python ./src/object/objaverseXL-LVIS_caption/evaluate.py
```
### ScanQA

### SQA3D


## Citation
If you find this work useful, please cite our paper:

```
@article{jin2025revisiting,
  title={Revisiting 3D LLM Benchmarks: Are We Really Testing 3D Capabilities?},
  author={Jin, Jiahe and He, Yanheng and Yang, Mingyan},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025}
}
```
