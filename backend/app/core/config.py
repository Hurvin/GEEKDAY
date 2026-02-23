from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sophnet_api_key: str = ""
    sophnet_base_url: str = "https://www.sophnet.com/api/open-apis/v1"
    sophnet_model: str = "Qwen2.5-72B-Instruct"
    use_mock_data: bool = True
    app_name: str = "Chaoyun Yunnao API"
    api_prefix: str = "/api/v1"
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        # 兼容两种启动方式：
        # 1) 在 backend 目录运行（读取 backend/.env）
        # 2) 在项目根目录运行（读取 ../.env）
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
