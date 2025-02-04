#!/bin/bash

# 基础路径设置
RESULT_DIR=""
BASE_IMAGE_DIR=""

# 定义所有需要运行的view_mode
VIEW_MODES=("00" "01" "10" "11")

# 依次执行每个view_mode
for view_mode in "${VIEW_MODES[@]}"; do
   echo "Processing view_mode: $view_mode"
   
   # 根据view_mode设置不同的image_dir
   if [ "$view_mode" = "combine" ]; then
       IMAGE_DIR=""
   else
       IMAGE_DIR="${BASE_IMAGE_DIR}"
   fi
   
   python vlm3d_multi.py \
       --result_file "${RESULT_DIR}/inside_${view_mode}.jsonl" \
       --image_dir "${IMAGE_DIR}" \
       --view_mode "$view_mode"
   
   # 等待当前任务完成，并检查是否成功
   if [ $? -eq 0 ]; then
       echo "Successfully completed $view_mode"
   else
       echo "Error processing $view_mode"
   fi
   
   echo "-----------------------------------"
done

echo "All view modes processed"