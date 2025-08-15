"""Модуль для определения типов данных, используемых в приложении."""

from typing import List

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения, включая параметры Elasticsearch."""

    es_hosts: str
    es_login: str = Field(default="", env="ES_LOGIN")  # Логин для доступа к Elasticsearch
    es_password: str = Field(default="", env="ES_PASSWORD")  # Пароль для доступа к Elasticsearch
    # PROXY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Parameters(BaseModel):
    """Параметры приложения, включая параметры Elasticsearch и модели."""

    es_request_timeout: int = 100
    es_max_retries: int = 50
    es_retry_on_timeout: bool = True
    es_chunk_size: int = 300
    es_max_hits: int = 100  # 200
    es_index: str = "ch_documents*"  # "ch_documents"  # "publicator_paragraphs*"
    es_first_field: str = "pub_aliases"  # "pub_aliases" "sys_ids"
    es_mod_id_name: str = "mod_id"  # наименование поля модуля в индексе
    es_doc_id_name: str = "doc_id"  # наименование поля документа в индексе
    es_second_field: str = "text_lem"  # "lemmatized_text"
    es_third_field: str = "title_lem"  # "lemmatized_text"
    stopwords_files: List[str] = []
    ds_candidates_quantity_total: int = 500  # количество кандидатов, передающихся для переранжирования всего
    ds_model_name: str = "BAAI/bge-reranker-large"  # '/home/an/.cache/huggingface/hub/models--BAAI--bge-reranker-large'
    ds_rank_score: float = -10.0
    project_host: str = "0.0.0.0"
    # project_port: int = 8080
    max_sentences: int = 10  # количество предложений после которой текст разбивается на части
    sentences_chunk_size: int = 10  # количество предложений в куске текста
    sentences_overlap: int = 3  # количество перекрывающихся слов между чанками
    dence_max_pairs: int = 50  # количество пар для переранжирования "gbe" т. к. есть ограничение на память видеокарты
    alias_to_site: dict = {"bss.vip": "https://vip.1gl.ru", "bss": "https://1gl.ru", "uss": "https://1jur.ru"}


# Модель для входных данных (запроса)
class QueryRequest(BaseModel):
    query: str
    alias: str


# Модель для выходных данных (ответа)
class AnswerResponse(BaseModel):
    ranking_dicts: list
