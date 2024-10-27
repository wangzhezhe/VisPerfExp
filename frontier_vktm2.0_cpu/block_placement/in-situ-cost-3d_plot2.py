import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Tuple, Iterable
import matplotlib.pyplot as plt

def plotPlane(fig: go.Figure,
              d: float,
              colorScaleName: str) -> None:
    """
        :param fig: figure to plot on
        :param colorScaleName: choose from <https://plotly.com/javascript/colorscales/>
    """
    # x, y, z

    x = np.arange(0, 3, 0.1)
    y = np.arange(0, 3, 0.1)
    x,y = np.meshgrid(x,y)

    #z = d*(1+x)/(1+y)
    z = (1+y)/(d*(1+x))

    # draw plane
    surface = go.Surface(x=x, y=y, z=z, colorscale=colorScaleName, showscale=False)
    fig.add_trace(surface, row=1, col=1)


def plotPlaneFix(fig: go.Figure) -> None:
    """
        :param fig: figure to plot on
        :param colorScaleName: choose from <https://plotly.com/javascript/colorscales/>
    """
    # x, y, z

    x = np.arange(0, 3, 0.1)
    y = np.arange(0, 3, 0.1)
    x,y = np.meshgrid(x,y)

    z = np.ones_like(x)

    # draw plane
    surface = go.Surface(x=x, y=y, z=z, colorscale="Greys", showscale=False,opacity=0.5)
    fig.add_trace(surface, row=1, col=1)


# create figure
fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'surface'}]])

# plot two intersectioned surfaces

plotPlane(fig, 1.1, "Blues")
plotPlane(fig, 1.25, "Oranges")
plotPlane(fig, 1.5, "Greens")
plotPlaneFix(fig)

#doc https://plotly.com/python/reference/layout/xaxis/#layout-xaxis-tickfont
fig.update_xaxes(tickfont_size=50)
fig.update_yaxes(tickfont_size=50)

fig.update_scenes(xaxis_title_text='Op',  
                  yaxis_title_text='Vp',  
                  zaxis_title_text='VCEF')

fig.show()