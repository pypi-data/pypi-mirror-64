
# Sarcastic Color Scheme

Color scheme for when you want to present some data visualization, but sarcastically.

This is useful for

 - presenting bad data where you aren't confident in the results,
 - turning in assignments you'd rather not do
 - annoying people who care about good dataviz


# Features

The code for all the demos can be found [here](https://github.com/kavigupta/sarcastic-color-theme/blob/master/demo/demo.py).


## Afwul background

<img src="https://github.com/kavigupta/sarcastic-color-theme/raw/master/demo/sarcastic_0.png">

Yes, you saw that correctly, there are two different awful background colors for the plot background and the legend background.

## Terrible plot colors

Yes, the colors on display here are cyan, grey, light blue, purple and orange. Yes, that looks terrible.

## Bad spacing

You may have noticed the abysmal spacing of the title. Yes, that is deliberate.

## Weird inexplicable borders / grid

Yes, you are right that the borders aren't all correctly there.

## Colored axes

Yep, the axes are colored, different colors.

# Inconsistent Style

This wouldn't be maximally awful if it was consistent, which is why running exactly the same code two more times yields these:

<img src="https://github.com/kavigupta/sarcastic-color-theme/raw/master/demo/sarcastic_1.png">
<img src="https://github.com/kavigupta/sarcastic-color-theme/raw/master/demo/sarcastic_2.png">

This way, not only is every graph terrible looking, but you can't get used to the style!

# How to install and use

You can install this package using the following command

```sh
pip install sarcastic-color-scheme
```

To use it you can run

```python
from sarcastic_color_scheme import sarcastic
```

and then either run

```python
sarcastic.sarcastic()
```

to make all subsequent graphs sarcastic (`sarcastic.normal()` undoes the change), or to make a single graph sarcastic run

```python
with sarcastic:
    # your graph code here
```

# Configurable

If you look at [the code](https://github.com/kavigupta/sarcastic-color-theme/blob/master/demo/demo.py) you'll notice that you use a context manager to make sure that the sarcasm mode is enabled:

```python
with sarcastic:
    test_graph()
```

You can also run

```python
sarcastic.sarcastic()
test_graph()
sarcastic.normal()
```

to get the same effect, without the context manager. After the context manager is complete, the styles are reset to where they were before it ran as can be seen in the plot


<img src="https://github.com/kavigupta/sarcastic-color-theme/raw/master/demo/back_to_normal.png">
