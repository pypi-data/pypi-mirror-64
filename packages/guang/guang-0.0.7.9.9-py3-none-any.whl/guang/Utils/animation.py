import plotly.graph_objects as go
import numpy as np
from guang.interesting import Lorenz
from guang.Utils.plotly import Scatter3d
from guang.Utils.toolsfunc import ExtremeValue

def get_Traces():
    global k
    t = np.linspace(0, 10, 900)
    Traces=[]
    k = 3
    for i in range(k):
        Traces.append(Lorenz.Trace(t = t, xyz=[10*np.random.rand(),10*np.random.rand(),10*np.random.rand()+10]))
    return Traces

def getRange(x, dx=1.5):
    return np.min(x) - dx, np.max(x) + dx


def get_extrem():
    Value = ExtremeValue()
    Traces = get_Traces()
    for trace in Traces:
        x,y,z = trace[:,0], trace[:,1], trace[:,2]
        xm, xM = getRange(x)
        ym, yM = getRange(y)
        zm, zM = getRange(z)
        xm, ym, zm = Value.get_min(x=xm, y=ym, z=zm)
        xM, yM, zM = Value.get_max(x=xM, y=yM, z=zM)
    return xm, xM, ym, yM, zm, zM

def get_frames(all_steps = 100, period=100):
    Traces = get_Traces()
    N = len(Traces[0][:,0])
    step = N // all_steps
    i_start, i_end = 0, 0

    frames = []
    for i in range(all_steps):
        i_end += step
        i_start = i_end - period if i_end > period else 0
        data = []

        for trace in Traces:
            x, y, z = trace[:, 0], trace[:, 1], trace[:, 2]

            data_x = x[i_start:i_end]
            data_y = y[i_start:i_end]
            data_z = z[i_start:i_end]
            data.append(go.Scatter3d(x=data_x, y=data_y, z=data_z,
                                     mode="lines+markers",
                                     line=dict(
                                         color=None,
                                         width=1.5),
                                     marker=dict(
                                         size=1.5,
                                         color=z,
                                         colorscale='Viridis')))

        frames.append(go.Frame(data=data,
                               traces=[i for i in range(len(data))]  ####THIS IS THE LINE THAT MUST BE INSERTED
                               ) )
        return frames


def get_layout():
    layout = go.Layout(width=780, height=780,

                       scene={
                           'xaxis': {'range': [xm, xM], "nticks": 10, 'autorange': False, "zeroline": False},
                           # , 'rangemode': 'tozero', 'tickmode': "linear", 'tick0': -5, 'dtick': 1},
                           'yaxis': {'range': [ym, yM], "nticks": 10, 'autorange': False, "zeroline": False},
                           # , 'rangemode': 'tozero', 'tickmode': "linear", 'tick0': -5, 'dtick': 1},
                           'zaxis': {'range': [zm, zM], "nticks": 10, 'autorange': False, "zeroline": False},
                           # , 'rangemode': 'tozero', 'tickmode': "linear", 'tick0': -5, 'dtick': 1},
                           'aspectmode': 'cube',
                       },
                       title="Lorenz Curve",
                       hovermode="closest",
                       updatemenus=[dict(type="buttons",
                                         buttons=[dict(label="Play",
                                                       method="animate",
                                                       args=[None, dict(frame=dict(duration=10, redraw=True),
                                                                        transition=dict(duration=0),
                                                                        fromcurrent=True,
                                                                        mode='immediate'
                                                                        )])])])
    return layout


if __name__ == "__main__":

    frames = get_frames()
    xm, xM, ym, yM, zm, zM = get_extrem()
    initial_data = [go.Scatter3d(x=[xm], y=[ym], z=[zm]),
                    go.Scatter3d(x=[xM], y=[yM], z=[zM]),
                    go.Scatter3d(x=[xm], y=[yM], z=[zm]), ]

    fig = go.Figure(
        data=initial_data,

        layout=layout,

        frames=frames
    )
    fig.show()

