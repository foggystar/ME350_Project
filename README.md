# ME350_Project
UM-JI Joint Institute, ME3500J 2025su Project

## 使用流程

- 克隆仓库到本地并进入仓库
```bash
git clone git@github.com:foggystar/ME350_Project.git
cd ME350_Project
```

- 每次使用仓库前同步云端
```bash
git pull
```

- 完成当前修改后将修改的文件推送到云端([参见conventional Commit](conventionalCommit.md))
```bash
git add 修改过的文件的路径（可以用空给分开，添加多个文件，偷懒直接用 * ）
git commit -m "(type): 做了什么事情"
git push
```

## 项目结构说明

*   **`code/`**: 存放项目的主要源代码。
    - `main/`: 包含主程序代码，例如 `main.ino` Arduino 控制程序。
*   **`docs/`**: 存放项目的相关文档。
    - 项目规则 (`Game rule - Climbing Robot Challenge 2025-05-30.pdf`) 
    - 参考论文 (`SpiRobs_Logarithmic spiral-shaped robots-mono.pdf`, `SpiRobs_Logarithmic spiral-shaped robots.pdf`)。
*   **`mini_project/`**: 存放与`mini Project`验相关的文件。
    - 评分标准 (`(Rubric) Mini-project 1.docx`) 
    - Slides (`F-lab 1 2025-06-04.pptx`) 
    - 实验手册 (`Manual (F-Lab 1) Synthesis and prototyping of a self-locking robotic clamp.docx`)。
*   **`model/`**: 存放项目相关的3D模型和设计文件。
    - 包含各种 SolidWorks 等3D模型文件，
        - 舵机模型
        - 方案一（环形升降机）
        - 方案二（两段式同步带抱紧）
        - 公共零件：铝型材等。
*   **`process/`**: 存放与加工制造过程相关的文件。
    - `.3MF` 3D打印文件 
    - `.DXF` 激光切割文件
*   **`refer.md`**: 参考资料或笔记。

