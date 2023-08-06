
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings

from .get_random_style import StyleRandomizer

class RandomizerContext:

    def __init__(self):
        self.randomizer = StyleRandomizer()
        self.in_randomization_context = False
        self.original_params = None

    def reset(self):
        self.randomizer = StyleRandomizer()
        if self.original_params is not None:
            mpl.rcParams.update(self.original_params)

    def randomize_style(self):
        style = self.randomizer.get_random_style()
        if self.original_params is None:
            self.original_params = {k : mpl.rcParams[k] for k in style}
        mpl.rcParams.update(style)

    def wrap(self, func):
        def new_func(*args, **kwargs):
            val = func(*args, **kwargs)
            if self.in_randomization_context:
                self.randomize_style()
            return val
        new_func.__name__ = func.__name__
        new_func.__doc__ = func.__doc__
        return new_func

    def sarcastic(self):
        self.in_randomization_context = True
        self.randomize_style()

    def normal(self):
        self.reset()
        self.in_randomization_context = False

    def __enter__(self):
        self.sarcastic()

    def __exit__(self, *_, **__):
        self.normal()

context = RandomizerContext()

plt.show = context.wrap(plt.show)
plt.savefig = context.wrap(plt.savefig)
