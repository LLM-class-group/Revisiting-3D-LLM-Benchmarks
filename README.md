# Revisiting 3D LLM Benchmarks: Are We Really Testing 3D Capabilities?

<p align="center"><img width="540" src="docs/2d cheating.png"></p>

This is the official repository of our paper “**Revisiting 3D LLM Benchmarks: Are We Really Testing 3D Capabilities?**” by [Jiahe Jin](https://github.com/zizi0123), [Yanheng He](https://github.com/henryhe0123), and [Mingyan Yang](https://github.com/fircube).

## Abstract
In this work, we identify the "2D-Cheating" problem in 3D LLM evaluation, where these tasks might be easily solved by VLMs with rendered images of point clouds, exposing ineffective evaluation of 3D LLMs' unique 3D capabilities. We test VLM performance across multiple 3D LLM benchmarks and, using this as a reference, propose principles for better assessing genuine 3D understanding. We also advocate explicitly separating 3D abilities from 1D or 2D aspects when evaluating 3D LLMs.

## Usage

<p align="center"><img width="540" src="docs/benchmark overview.png"></p>

We conducted experiments on the above benchmarks. See the commands for reproducing each experiment as follows:

### 3D MM-Vet

#### **Generating Results**
To generate results using the model, run the following command:

```bash
python ./src/object/3dmmvet/inference.py
```

#### **Evaluating Results**
To evaluate the generated results, run the following command:

```bash
python ./src/object/3dmmvet/eval.py
```

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

#### **Rendering scene point cloud**

##### Render bev images
```bash
python ./src/scene/render/parallel_render_bev.py
```

##### Render multi view images
```bash
python ./src/scene/render/parallel_render_multi.py
```

#### **Generating Results**
To generate results using the model, run the following command:

##### Generate bev results
```bash
python ./src/scene/evaluation/scanqa/generate/vlm3d.py
```

##### Generate multi view results
```bash
bash ./src/scene/evaluation/scanqa/generate/generate.sh
```

#### **Evaluating Results**

To evaluate the generated captions against ground truth data, run the following command:

##### Evaluate single view results
```bash
python ./src/scene/evaluation/scanqa/evaluation/test.py
```

##### Evaluate HIS results of 5 views
```bash
python ./src/scene/evaluation/scanqa/evaluation/test_HIS.py
```

##### Evaluate BoN results
```bash
python ./src/scene/evaluation/scanqa/evaluation/test_BoN.py
```

### SQA3D

To test the model’s performance on SQA3D, run the following command:

```bash
python ./src/scene/evaluation/sqa3d/test_sqa_vlm.py
```

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

## Acknowledgement
We would like to express our sincere gratitude to Prof. Yonglu Li for his valuable guidance and support throughout this research, from topic selection to the final writing. His insightful discussions and feedback have been essential to the completion of this work. We would also like to thank Ye Wang for kindly sharing the viewpoint dataset in ScanNet.
