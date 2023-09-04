class HashableByIdMixin:
    def __hash__(self) -> int:
        return hash(self.id)
