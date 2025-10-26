from pydantic import BaseModel, SecretStr

from ...utils import hash_password


class PasswordDTO(BaseModel):
    password: SecretStr


class HashedPasswordDTO(BaseModel):
    password: str


def handle(dto: PasswordDTO) -> HashedPasswordDTO:
    return HashedPasswordDTO(
        password=hash_password(dto.password.get_secret_value())
    )
