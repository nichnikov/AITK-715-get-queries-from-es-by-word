import functools
import multiprocessing.pool
from functools import wraps
from itertools import groupby


def grouped_tuples_list(data: list[tuple]):
    # Sort the data by the grouping key (e.g., the first element of the tuple)
    data.sort(key=lambda x: x[0])

    grouped_data = []
    for key, group in groupby(data, key=lambda x: x[0]):
        # Extract the second elements from the grouped tuples
        values = [item[1:] for item in group]
        grouped_data.append((key, list(values)))

    return grouped_data


def sliding_window_words(words_list, window_size, overlap=0):
    """
    Разбивает список слов на части с помощью плавающего окна.

    :param words_list: список слов для обработки
    :param window_size: размер окна (количество слов в чанке)
    :param overlap: количество перекрывающихся слов между чанками
    :return: список чанков (каждый чанк - это список слов)
    """
    if overlap >= window_size:
        raise ValueError("Перекрытие должно быть меньше размера окна")
    if window_size <= 0:
        raise ValueError("Размер окна должен быть положительным числом")

    chunks = []
    step = window_size - overlap
    for i in range(0, len(words_list), step):
        chunk = words_list[i : i + window_size]
        chunks.append(chunk)

    return chunks


def build_document_link(alias: str, module_id: str, document_id: str, doc_source: dict, alias_to_site: dict) -> str:
    """
    Возвращает ссылку формата site_address + ?#/document/{mod_id}/{doc_id}/
    """
    site_address = alias_to_site.get(alias, "")
    mod_id = doc_source.get(module_id, "")
    doc_id = doc_source.get(document_id, "")

    # mod_id = doc_source.get("mod_id", "")
    # doc_id = doc_source.get("doc_id", "")

    link = f"{site_address}?#/document/{mod_id}/{doc_id}/"
    return link


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def text2text_entry(text1: str, text2: str) -> float:
    """
    :param text1: текст, вхождение которого оценивается
    :param text2: текст, вхождение в который оценивается
    """
    tx1_len = len(set(text1.split()))
    if tx1_len != 0:
        intersection = set(text1.split()) & set(text2.split())
        return float(len(intersection) / tx1_len)
    else:
        return 0.0


def jaccard_similarity(text1: str, text2: str) -> float:
    """"""
    intersection = set(text1.split()) & set(text2.split())
    union = set(text1.split()).union(set(text2.split()))
    if len(union) != 0:
        return float(len(intersection) / len(union))
    else:
        return 0.0


def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""

    def timeout_decorator(item):
        """Wrap the original function."""

        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)

        return func_wrapper

    return timeout_decorator


# Пример использования
if __name__ == "__main__":
    words = [
        "Python",
        "—",
        "это",
        "высокоуровневый",
        "язык",
        "программирования",
        "общего",
        "назначения",
        "который",
        "ориентирован",
        "на",
        "повышение",
        "производительности",
        "разработчика",
        "и",
        "читаемости",
        "кода.",
    ]

    # Разбиваем на чанки по 5 слов с перекрытием в 2 слова
    word_chunks = sliding_window_words(words, window_size=5, overlap=2)
    print(word_chunks)

    for i, chunk in enumerate(word_chunks, 1):
        print(f"Чанк {i}: {chunk}")
