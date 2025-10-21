import pickle  # nosec B403

import importlib_resources


class ThemeUnpickler(pickle.Unpickler):
    """
    Points the unpickler to the Theme class. Allows unpickling for package
    init.
    """

    def find_class(self, module, name):
        if name == "Theme":
            from gptables.core.theme import Theme

            return Theme
        return super().find_class(module, name)


file = importlib_resources.files("gptables") / "theme_pickles/gptheme.pickle"

with importlib_resources.as_file(file) as path:
    gptheme = ThemeUnpickler(open(path, "rb")).load()
