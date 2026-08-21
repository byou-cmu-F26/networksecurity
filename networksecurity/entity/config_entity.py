from datetime import datetime
import os
from networksecurity.constant import training_pipeline as training_pipeline

# 它负责生成本次运行最外层的目录，比如：
# Artifacts/08_21_2026_10_30_00/
class TrainingPipelineConfig:

    def __init__(self, timestamp=None):
        # 如果外面没有传 timestamp，就取当前时间。
        if timestamp is None:
            timestamp = datetime.now()

        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")

        # 训练流水线名字，例子：NetworkSecurity
        self.pipeline_name = training_pipeline.PIPELINE_NAME

        # 产物总目录名Artifacts，来自常量文件里的 ARTIFACT_DIR。
        self.artifact_name = training_pipeline.ARTIFACT_DIR

        # 本次运行的产物目录，例子：Artifacts/08_21_2026_10_30_00
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)

        # 最终模型目录。
        # 例子：训练完成后，最终可部署模型可能会放到 final_model/。
        self.model_dir = os.path.join("final_model")

        # 保存本次运行的时间戳字符串，后面其他配置也可以复用。
        self.timestamp: str = timestamp



# DataIngestionConfig 是数据摄取阶段的配置。
# 它负责告诉程序：从哪个 MongoDB database/collection 读数据，
# 原始数据、训练集、测试集分别保存到哪里。
class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Data Ingestion 阶段的总目录。
        # 例子：Artifacts/08_21_2026_10_30_00/data_ingestion
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME,
        )

        # Feature Store 文件路径，用来保存从 MongoDB 导出的原始 CSV。
        # 例子：Artifacts/.../data_ingestion/feature_store/phisingData.csv
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME,
        )

        # 训练集文件路径。
        # 例子：Artifacts/.../data_ingestion/ingested/train.csv
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME,
        )

        # 测试集文件路径。
        # 例子：Artifacts/.../data_ingestion/ingested/test.csv
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME,
        )

        # 训练集/测试集切分比例。
        # 例子：0.2 表示 20% 数据作为测试集，80% 作为训练集。
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION

        # MongoDB collection 名字。
        # 例子：BIHAO database 下面的 NetworkData collection。
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME

        # MongoDB database 名字。
        # 例子：BIHAO
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME


# DataValidationConfig 是数据验证阶段的配置。
# 它负责告诉程序：验证通过/不通过的数据保存到哪里，漂移报告保存到哪里。
class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Data Validation 阶段的总目录。
        # 例子：Artifacts/08_21_2026_10_30_00/data_validation
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME,
        )

        # 验证通过的数据目录。
        # 例子：Artifacts/.../data_validation/validated/
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)

        # 验证失败的数据目录。
        # 例子：Artifacts/.../data_validation/invalid/
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)

        # 验证通过的训练集路径。
        # 例子：Artifacts/.../data_validation/validated/train.csv
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)

        # 验证通过的测试集路径。
        # 例子：Artifacts/.../data_validation/validated/test.csv
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)

        # 验证失败的训练集路径。
        # 例子：Artifacts/.../data_validation/invalid/train.csv
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)

        # 验证失败的测试集路径。
        # 例子：Artifacts/.../data_validation/invalid/test.csv
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)

        # 数据漂移报告路径。
        # 例子：Artifacts/.../data_validation/drift_report/report.yaml
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )


# DataTransformationConfig 是数据转换阶段的配置。
# 它负责告诉程序：转换后的 numpy 数据保存到哪里，预处理对象保存到哪里。
class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Data Transformation 阶段的总目录。
        # 例子：Artifacts/08_21_2026_10_30_00/data_transformation
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_TRANSFORMATION_DIR_NAME,
        )

        # 转换后的训练数据路径。
        # replace("csv", "npy") 会把 train.csv 变成 train.npy。
        # 例子：Artifacts/.../data_transformation/transformed/train.npy
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),
        )

        # 转换后的测试数据路径。
        # 例子：Artifacts/.../data_transformation/transformed/test.npy
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"),
        )

        # 预处理对象保存路径。
        # 例子：KNNImputer/Scaler 等对象会保存成 preprocessing.pkl。
        self.transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir,
            training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,
        )


# ModelTrainerConfig 是模型训练阶段的配置。
# 它负责告诉程序：模型保存到哪里，以及最低期望分数是多少。
class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Model Trainer 阶段的总目录。
        # 例子：Artifacts/08_21_2026_10_30_00/model_trainer
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.MODEL_TRAINER_DIR_NAME,
        )

        # 训练好的模型文件路径。
        # 例子：Artifacts/.../model_trainer/trained_model/model.pkl
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir,
            training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
            training_pipeline.MODEL_FILE_NAME,
        )

        # 模型最低期望分数。
        # 例子：0.6 表示模型评分低于 60% 时，可能认为模型不合格。
        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE

        # 过拟合/欠拟合判断阈值。
        # 例子：训练分数和测试分数差距超过 0.05 时，需要警惕模型泛化不好。
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD
