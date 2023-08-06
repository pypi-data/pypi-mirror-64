
import collections

from cycler import cycler

from .basic_rng import RandomGenerator

class StyleRandomizer:
    """
    Gets random matplotlib styles
    """
    brights = 'purple', '#cccccc', "white", "magenta", 'yellow', 'lime', "cyan", "orange", "red", "xkcd:lightblue"
    backgrounds = "#ffdddd", '#ddffdd', '#ddddff'
    darks = 'black', '#800000', '#008000', '#000080'
    grid_axis = 'x', 'y'
    markers = '*', ' '
    dashes = '-.', '-', '--'
    padding_range = -8, 8
    figsize_range = 4, 6
    font_size = 'large', 'small'

    def __init__(self, seed=0, **kwargs):
        self._rng = RandomGenerator(seed)
        self._usages = collections.defaultdict(int)

        for k, v in kwargs.items():
            assert hasattr(self, k)
            setattr(self, k, v)

    def pick(self, items):
        """
        Pick a random item from the given list, prioritizing ones that have been used less recently
        """
        min_usage = min(self._usages[item] for item in items)
        min_used_items = [item for item in items if self._usages[item] == min_usage]
        item = self._rng.choose(min_used_items)
        self._usages[item] += 1
        return item

    def pick_range(self, bottom, top, divisions=1000):
        return self._rng.rand(divisions + 1) / divisions * (top - bottom) + bottom

    def get_random_style(self):
        """
        Get a random style pack
        """
        colors = cycler('color', list({self.pick(self.brights) for _ in range(10)}))
        updated_rc_params = {
            'axes.edgecolor' : self.pick(self.brights),
            'axes.facecolor' : self.pick(self.backgrounds),
            'axes.grid' : True,
            'axes.grid.axis' : self.pick(self.grid_axis),
            'axes.grid.which' : 'both',
            'axes.labelcolor' : self.pick(self.darks),
            'axes.labelsize' : self.pick(self.font_size),
            'axes.labelpad' : self.pick_range(*self.padding_range),
            'axes.linewidth' : 4,
            'axes.labelweight' : 'bold',
            'axes.spines.bottom': True,
            'axes.spines.left': True,
            'axes.spines.right': False,
            'axes.spines.top': True,
            'axes.titlepad' : self.pick_range(*self.padding_range),
            'axes.titlesize' : self.pick(self.font_size),
            'axes.xmargin' : 0.2,
            'axes.ymargin' : 0.2,
            'axes.prop_cycle' : colors,
            'axes.unicode_minus' : False,
            'figure.figsize' : [self.pick_range(*self.figsize_range) for _ in range(2)],
            'font.size' : 8,
            'font.stretch' : 'ultra-expanded',
            'grid.color' : self.pick(self.darks),
            'grid.linestyle' : self.pick(self.dashes),
            'grid.linewidth' : 2,
            'legend.edgecolor' : self.pick(self.darks),
            'legend.facecolor' : self.pick(self.backgrounds),
            'legend.handleheight' : self.pick_range(*self.padding_range),
            'legend.shadow' : True,
            'legend.markerscale' : 2,
            'lines.marker' : self.pick(self.markers),

            'xtick.color' : self.pick(self.brights),
            'ytick.color' : self.pick(self.brights),

            'patch.facecolor' : self.pick(self.backgrounds),
        }
        return updated_rc_params
