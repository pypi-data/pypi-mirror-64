import numpy as np
import matplotlib as mpl


def _linear3color(start_color,center_color,end_color, n=10):
    input_colors = [mpl.colors.to_rgb(start_color), mpl.colors.to_rgb(center_color), mpl.colors.to_rgb(end_color)]
    position = [0,0.33, 1]
    colormap = _make_cmap(input_colors, position=position)
    output_colors = []
    for i in range(n+1):
        color = colormap(i/n)
        html = mpl.colors.to_hex(color, keep_alpha=False)
        output_colors.append(html)
    return output_colors


def _make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''

    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            raise ValueError("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            raise ValueError("position must start with 0 and end with 1")

    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap