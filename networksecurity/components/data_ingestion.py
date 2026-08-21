from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# MongoDB database/collection 名字、feature_store 路径、train/test 路径、切分比例等。
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from pymongo.server_api import ServerApi
import certifi
import os
import sys
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # =========================
    # 功能模块 1：从 MongoDB 读取数据
    # =========================
    # 作用：
    # 从配置里指定的 MongoDB database 和 collection 读取所有 document，
    # 然后转成 pandas DataFrame。

    def export_collection_as_dataframe(self):
        """从 MongoDB collection 读取数据，并转换成 pandas DataFrame。"""
        try:

            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                server_api=ServerApi("1"),
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=30000,
                connectTimeoutMS=30000,
                socketTimeoutMS=60000,
            )
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find().limit(50)))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # =========================
    # 功能模块 2：保存原始数据到 Feature Store， 返回同一个 dataframe，方便后续继续切分 train/test。
    # =========================
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # =========================
    # 功能模块 3：切分训练集和测试集
    # =========================
    # 作用：
    # 把完整数据按照配置比例切成 train_set 和 test_set，
    # 再分别保存为 train.csv 和 test.csv。
    
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            # train_test_split 会随机把数据切分成训练集和测试集。
            # test_size=0.2 表示 20% 数据作为测试集，80% 作为训练集。
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )

            # 获取 train.csv 的父目录。
            # 注意：training_file_path 和 testing_file_path 通常在同一个 ingested 目录里。
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            # 如果 ingested 目录不存在，就创建它。
            # 例子：Artifacts/时间戳/data_ingestion/ingested
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            # 保存训练集。
            # 例子：Artifacts/.../data_ingestion/ingested/train.csv
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            # 保存测试集。
            # 例子：Artifacts/.../data_ingestion/ingested/test.csv
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # =========================
    # 功能模块 4：Data Ingestion 主流程
    # =========================
    # 作用：
    # 串联上面的 3 个步骤：
    # 1. 从 MongoDB 读取数据。
    # 2. 保存原始数据到 feature_store。
    # 3. 切分并保存 train.csv / test.csv。
    # 4. 返回 DataIngestionArtifact，告诉后续阶段 train/test 文件在哪里。
    # DataIngestionArtifact(
    #     trained_file_path=".../train.csv",
    #     test_file_path=".../test.csv"
    # )
    def initiate_data_ingestion(self):
        try:
            # 第一步：从 MongoDB 导出数据为 DataFrame。
            dataframe = self.export_collection_as_dataframe()

            # 第二步：把原始 DataFrame 保存到 feature_store CSV。
            dataframe = self.export_data_into_feature_store(dataframe)

            # 第三步：把数据切分成训练集和测试集，并保存到 ingested 目录。
            self.split_data_as_train_test(dataframe)

            # 第四步：创建 artifact 对象。
            # artifact 不保存真实数据，只保存关键文件路径，方便下一个阶段使用。
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            # 返回本阶段结果对象。
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
