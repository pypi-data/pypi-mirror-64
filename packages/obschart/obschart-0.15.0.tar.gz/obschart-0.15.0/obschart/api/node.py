from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .context import Context


class Node(object):
    _data: Any
    _context: "Context"

    def __init__(self, data: Any, context: "Context"):
        super().__init__()

        self._data = data
        self._context = context

    def _execute(self, query, variables):
        if not self._context:
            raise Exception("Expected context")

        return self._context.client._execute(query, variables)

    def __repr__(self):
        return f"{self.__class__.__name__} (ID: {self.id}) {self._data}"

    @property
    def id(self):
        return self._data["id"]
