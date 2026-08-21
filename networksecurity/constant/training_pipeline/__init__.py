# os 用来拼接路径，避免手写 "/" 或 "\" 导致 Windows/Mac 路径不兼容。
# 例子：os.path.join("Artifacts", "data_ingestion") 会得到正确的系统路径。
import os

# numpy 这里主要用 np.nan，表示缺失值。
# 后面的 KNNImputer 会把 np.nan 这种缺失值补上。
import numpy as np


# =========================
# 通用训练流水线常量
# =========================

# 目标列，也就是模型最后要预测的那一列。
TARGET_COLUMN = "Result"

# 训练流水线的名字，用来标识整个项目/流程。
# 例子：日志、配置、产物目录里可以看到这个项目叫 NetworkSecurity。
PIPELINE_NAME: str = "NetworkSecurity"

# 所有中间产物的总文件夹名。
# 例子：运行一次训练后，数据文件、模型文件、报告文件都会放到 Artifacts 下面。
ARTIFACT_DIR: str = "Artifacts"

# 原始 CSV 文件名。
# 例子：从 MongoDB 导出的原始数据会保存成 phisingData.csv。
FILE_NAME: str = "phisingData.csv"

# 切分数据后，训练集文件名。
# 例子：80% 数据保存到 train.csv，用来训练模型。
TRAIN_FILE_NAME: str = "train.csv"

# 切分数据后，测试集文件名。
# 例子：20% 数据保存到 test.csv，用来评估模型效果。
TEST_FILE_NAME: str = "test.csv"

# 数据 schema 文件路径。
# schema.yaml 通常用来规定有哪些列、每列类型是什么、哪些列需要删除等。
SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

# 最终保存模型的目录。
# 例子：训练完成后，最终可用的模型可能会被复制到 saved_models/。
SAVED_MODEL_DIR = os.path.join("saved_models")

# 模型文件名。
# pkl 是 Python 常见的序列化格式，保存训练好的模型对象。
MODEL_FILE_NAME = "model.pkl"


# =========================
# Data Ingestion 数据摄取阶段常量
# =========================
# Data Ingestion Dir
# └── feature_store
#     └── NetworkData.csv   ← Feature Store File Path
# └── ingested
#     ├── train.csv
#     └── test.csv

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "BIHAO"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2


# =========================
# Data Validation 数据验证阶段常量
# =========================
# Data Validation Dir
# ├── validated
# │   ├── train.csv   ← Valid Train File Path
# │   └── test.csv    ← Valid Test File Path
# ├── invalid
# │   ├── train.csv   ← Invalid Train File Path
# │   └── test.csv    ← Invalid Test File Path
# └── drift_report
#     └── report.yaml ← Drift Report File Path


DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

# 数据预处理对象文件名。
# 例子：缺失值填充器、标准化器等预处理对象会保存成 preprocessing.pkl。
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"


# =========================
# Data Transformation 数据转换阶段常量
# =========================

# Data Transformation 阶段自己的文件夹名。
# 例子：Artifacts/时间戳/data_transformation/
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"

# 转换后的数据保存目录名。
# 例子：CSV 转成模型更容易读取的 numpy 数组后，会放到 transformed/。
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"

# 转换器/预处理对象保存目录名。
# 例子：KNNImputer 训练好之后会保存到 transformed_object/。
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

# KNNImputer 的参数，用来填补缺失值。
# missing_values=np.nan：把 np.nan 当成缺失值。
# n_neighbors=3：用最相近的 3 条数据来推算缺失值。
# weights="uniform"：3 个邻居的权重一样。
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

# 转换后的训练数据文件名。
# npy 是 numpy 数组文件，比 CSV 更适合直接喂给模型训练。
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

# 转换后的测试数据文件名。
DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"


# =========================
# Model Trainer 模型训练阶段常量
# =========================

# Model Trainer 阶段自己的文件夹名。
# 例子：Artifacts/时间戳/model_trainer/
MODEL_TRAINER_DIR_NAME: str = "model_trainer"

# 训练好的模型保存目录名。
# 例子：Artifacts/时间戳/model_trainer/trained_model/model.pkl
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"

# 训练好的模型文件名。
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"

# 模型最低期望分数。
# 例子：0.6 表示模型准确率/评分至少要达到 60%，否则认为训练结果不合格。
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6

# 判断过拟合/欠拟合的阈值。
# 例子：训练集分数和测试集分数差距超过 0.05，可能说明模型泛化不好。
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05

# 云端保存训练结果的 bucket 名字。
# 例子：后面如果把模型上传到 AWS S3/GCP/Azure，可能会用到这个名字。
TRAINING_BUCKET_NAME = "networksecurity-bihao"
