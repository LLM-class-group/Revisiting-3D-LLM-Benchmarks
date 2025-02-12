# Revisiting 3D LLM Benchmarks: Are We Really Testing 3D Capabilities?

<p align="center"><img width="540" src="assets/2d cheating.png"></p>

This is the official repository of our paper “**Revisiting 3D LLM Benchmarks: Are We Really Testing 3D Capabilities?**” by [Jiahe Jin](https://github.com/zizi0123), [Yanheng He](https://github.com/henryhe0123), and [Mingyan Yang](https://github.com/fircube).

## Abstract
In this work, we identify the "2D-Cheating" problem in 3D LLM evaluation, where these tasks might be easily solved by VLMs with rendered images of point clouds, exposing ineffective evaluation of 3D LLMs' unique 3D capabilities. We test VLM performance across multiple 3D LLM benchmarks and, using this as a reference, propose principles for better assessing genuine 3D understanding. We also advocate explicitly separating 3D abilities from 1D or 2D aspects when evaluating 3D LLMs.

## Usage

<p align="center"><img width="540" src="assets/benchmark overview.png"></p>

We conducted experiments on the above benchmarks. See the commands for reproducing each experiment as follows:

### 3D MM-Vet

#### **Generating Results**

```bash
python ./src/object/3dmmvet/inference.py
```

#### **Evaluating Results**

```bash
python ./src/object/3dmmvet/eval.py
```

### ObjaverseXL-LVIS Caption

#### **Generating Results**

```bash
python ./src/object/objaverseXL-LVIS_caption/vlm3d.py
```

#### **Evaluating Results**

```bash
python ./src/object/objaverseXL-LVIS_caption/evaluate.py
```

### **Rendering Scene Point Cloud**

##### Render BEV Images
```bash
python ./src/scene/render/parallel_render_bev.py
```

##### Render Multi View Images
```bash
python ./src/scene/render/parallel_render_multi.py
```

### ScanQA


#### **Generating Results**

##### Generate BEV Results

```bash
python ./src/scene/evaluation/scanqa/generate/vlm3d.py
```

##### Generate Multi View Results

```bash
bash ./src/scene/evaluation/scanqa/generate/generate.sh
```

#### **Evaluating Results**

##### Evaluate Single View Results
```bash
python ./src/scene/evaluation/scanqa/evaluation/test.py
```

##### Evaluate HIS Results 
```bash
python ./src/scene/evaluation/scanqa/evaluation/test_HIS.py
```

##### Evaluate BoN Results
```bash
python ./src/scene/evaluation/scanqa/evaluation/test_BoN.py
```

### SQA3D

To test VLM’s performance on SQA3D, run the following command:

```bash
python ./src/scene/evaluation/sqa3d/test_sqa_vlm.py
```

## Acknowledgement
We would like to express our sincere gratitude to Prof. Yonglu Li for his valuable guidance and support throughout this research, from topic selection to the final writing. His insightful discussions and feedback have been essential to the completion of this work. We would also like to thank Ye Wang for kindly sharing the viewpoint dataset in ScanNet.

## Data Attribution
This project uses data from:
- [GPT4Point](https://github.com/Pointcept/GPT4Point) (MIT License)
- [ShapeLLM](https://github.com/qizekun/ShapeLLM) (Apache 2.0 License)

## Citation
If you find this work useful, please cite our paper:

```
@misc{revisit3dllmbenchmark,
  author       = {Jiahe Jin and Yanheng He and Mingyan Yang},
  title        = {Revisiting 3D LLM Benchmarks: Are We Really Testing 3D Capabilities?},
  year         = {2025},
  organization = {GitHub},
  url          = {https://github.com/LLM-class-group/Revisiting-3D-LLM-Benchmarks},
}
```


