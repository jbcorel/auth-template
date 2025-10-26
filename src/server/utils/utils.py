import traceback
from pathlib import Path
import orjson
from collections.abc import Iterable
from fastapi.encoders import jsonable_encoder


def get_unique_dicts(data: Iterable[dict]) -> list[dict]:
    unique = set()
    for elem in data:
        unique.add(orjson.dumps(jsonable_encoder(elem), sort_keys=True))
    return [orjson.loads(elem) for elem in unique]


def get_path(path: str | Path) -> Path:
    """
    :param path: Полный или относительный путь до директории/файла
    :return: Полный путь до директории/файла

    Вы так же можете прочитать содержимое файла
    >>> query = get_path('sql/extract.sql').read_text(encoding='utf-8')
    """
    stack = traceback.extract_stack()
    call_from_file = stack[-2].filename
    parent_dir = Path(call_from_file).parent
    return parent_dir.joinpath(path).resolve()
