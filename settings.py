from datetime import datetime
from pydantic import Field
from pydantic_settings import BaseSettings
import pandas as pd
import os
import subprocess
from pathlib import Path


class Settings(BaseSettings):
    """Configuration settings with support for environment variables."""

    api_key: str = Field(default="sk-67f25953525e848c7da998a9a7d57b4c", env="API_KEY")
    base_url: str = Field(
        default="https://apis.iflow.cn/v1",
        env="BASE_URL",
    )
    model: str = Field(default="qwen3-coder-plus", env="MODEL")

    # api_key: str = Field(
    #     default="sk-BK8CPpt4jIbO3naJ76GUhoaxJhu88Y43n08PnI7wCI8019SG", env="API_KEY"
    # )
    # base_url: str = Field(
    #     default="https://api.holdai.top/v1",
    #     env="BASE_URL",
    # )
    # model: str = Field(default="claude-sonnet-4-5-20250929", env="MODEL")

    # TEST_BED: str = Field(default="/Users/hanyu/projects", env="TEST_BED")
    # PROJECT_NAME: str = Field(default="astropy", env="PROJECT_NAME")
    TEST_BED: str = Field(default="/root/temp_container", env="TEST_BED")
    PROJECT_NAME: str = Field(default="astropy__astropy-13033", env="PROJECT_NAME")
    INSTANCE_ID: str = Field(default="astropy__astropy-13033", env="INSTANCE_ID")
    DATASET: str = Field(default="verified", env="DATASET")
    PROBLEM_STATEMENT: str = Field(default="", env="PROBLEM_STATEMENT")
    timestamp: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    )
    LOG_DIR: str = Field(default="results/logs", env="LOG_DIR")
    DOCKER_IMAGE:str = Field(default="",env="DOCKER_IMAGE")
    def load_problem_statement(self) -> None:
        try:
            dataset_file = f"dataset/{self.DATASET}.parquet"
            if not os.path.exists(dataset_file):
                return
            df = pd.read_parquet(dataset_file)
            filtered_df = df[df["instance_id"] == self.INSTANCE_ID]
            problem_dict = filtered_df.iloc[0].to_dict()
            self.PROBLEM_STATEMENT = problem_dict.get(
                "problem_statement", str(problem_dict)
            )

            # Set the docker image based on INSTANCE_ID
            self.DOCKER_IMAGE = f"sweb.eval.x86_64.{self.INSTANCE_ID}:latest"

            # Get the base commit and switch to it
            # base_commit = problem_dict.get("base_commit")
            # if base_commit:
            #     project_path = Path(self.TEST_BED) / self.PROJECT_NAME
            #     if project_path.exists():
            #         print(
            #             f"Switching to base commit {base_commit} for project {project_path}"
            #         )
            #         try:
            #             # Run git checkout to switch to the base commit
            #             result = subprocess.run(
            #                 ["git", "checkout", base_commit],
            #                 cwd=project_path,
            #                 capture_output=True,
            #                 text=True,
            #                 timeout=30,
            #             )
            #             if result.returncode != 0:
            #                 print(f"Error checking out base commit: {result.stderr}")
            #             else:
            #                 print(f"Successfully switched to base commit {base_commit}")
            #         except subprocess.TimeoutExpired:
            #             print("Git checkout command timed out")
            #         except Exception as e:
            #             print(f"Error during git checkout: {e}")
            #     else:
            #         print(f"Project path does not exist: {project_path}")
            # else:
            #     print("No base_commit found in dataset")

            return

        except Exception as e:
            print(f"{e=}")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
if not settings.PROBLEM_STATEMENT:
    settings.load_problem_statement()
