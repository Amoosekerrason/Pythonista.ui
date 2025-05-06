from typing import Generic, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E")


class Ok(Generic[T, E]):
    def __init__(self, val: T):
        self.val = val

    def is_ok(self):
        return True

    def is_err(self):
        return False


class Err(Generic[T, E]):
    def __init__(self, err: E):
        self.err = err

    def is_ok(self):
        return False

    def is_err(self):
        return True


Result = Union[Ok[T, E], Err[T, E]]
