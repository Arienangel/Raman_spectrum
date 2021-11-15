from datetime import datetime
import os, sys
import pandas as pd


# read file
def asc_parser(path):
    with open(path, "r") as f:
        filename = os.path.split(path)[-1][:-4]
        return {filename: dict(map(lambda x: x.split(), list(f)))}


argv = sys.argv[1:]
if len(argv) == 0: argv = ["."]
data = dict()
for path in argv:
    if os.path.isfile(path):
        if path[-4:] == ".asc":
            data.update(asc_parser(path))
    if os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                if file[-4:] == ".asc":
                    data.update(asc_parser(os.path.join(dirpath, file)))

# create dataframe
data = pd.DataFrame(data)
data = data.astype(float)
data.index = data.index.astype(float)
data = data.sort_index()
data = (data - data[data.index > 50].min()) / (data[data.index > 50].max() - data[data.index > 50].min())

# xlsx output
filename = f"Raman shift {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.xlsx"
with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
    data.to_excel(writer, "Data")
    wb = writer.book
    chart = wb.add_chart({"type": "scatter"})
    max_row = len(data)
    #yapf: disable
    for i in range(len(data.columns)):
        col = i + 1
        chart.add_series({
            "name": ["Data", 0, col],
            "categories": ["Data", 1, 0, max_row, 0],
            "values": ["Data", 1, col, max_row, col],
            "line": {"width": 0.5},
            "marker": {"type": "none"},
        })
    chart.set_size({"height": 720, "width": 1280})
    chart.set_x_axis({
        "name": "Raman shift",
        "min": 0,
        "max": data.index[-1],
        "name_font": {"size": 12},
        "num_font": {"size": 10},
        "major_gridlines": {"visible": True,"line": {"width": 0.5}},
    })
    chart.set_y_axis({
        "min": 0,
        "max": 1,
        "name_font": {"size": 12},
        "num_font": {"size": 10},
        "major_gridlines": {"visible": True,"line": {"width": 0.5}},
    })
    chart.set_legend({
        "position": "overlay_right",
        "fill": {"color": "#f2f2f2"},"border": {"width": 1,"color": "#868686"},
        'font': {'size': 8}
    })
    #yapf: enable
    chart.show_blanks_as('span')
    chartsheet = wb.add_chartsheet("Figure")
    chartsheet.set_chart(chart)
    chartsheet.activate()
os.startfile(filename)