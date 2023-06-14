import abc
from typing import Any, Union
from jose import jwt
from jose.exceptions import ExpiredSignatureError


JWT_SECRET_KEY = "MYSECRET"
JWT_ALGORITHM = "HS256"


class AbstractTokenProcessor(abc.ABC):

    @abc.abstractmethod
    def encode_token(self, data_to_encode: dict[str, Any]) -> str:  # pragma: no cover
        pass

    @abc.abstractmethod
    def decode_token(self, data_to_encode: dict[str, Any]) -> Union[dict[str, Any], None]:  # pragma: no cover
        pass


class JoseJWTTokenProcessor(AbstractTokenProcessor):

    def encode_token(self, data_to_encode: dict) -> str:
        return jwt.encode(data_to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    def decode_token(self, data_to_decode: str) -> Union[dict[str, Any], None]:
        try:
            return jwt.decode(data_to_decode, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except ExpiredSignatureError:
            return None
