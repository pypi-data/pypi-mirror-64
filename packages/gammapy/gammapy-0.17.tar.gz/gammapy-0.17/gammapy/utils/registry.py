# Licensed under a 3-clause BSD style license - see LICENSE.rst

__all__ = ["Registry"]


class Registry(list):
    """Registry class."""

    def get_cls(self, tag):
        for cls in self:
            if hasattr(cls, "tag") and cls.tag == tag:
                return cls
        raise KeyError(f"No model found with tag: {tag!r}")

    def __str__(self):
        info = "Registry\n"
        info += "--------\n\n"

        len_max = max([len(_.tag) for _ in self])

        for item in self:
            info += f"\t{item.tag:{len_max}s}: {item.__name__}\n"

        return info.expandtabs(tabsize=2)
