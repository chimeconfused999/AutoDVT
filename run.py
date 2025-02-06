import stl2


fn="generated_cylinder.stl"
cyl = stl2.Geo2STL({"fn":fn});
cyl.readParam("parameters.json")
cyl.InitDashKeys(cyl.DashKey); cyl.mesh_x3d(); cyl.IEN(); cyl.Extractx2D(); cyl.mesh2stl(); stl2.save_d2f(fn, cyl.stl); cyl.Buttons(cyl.DashKey)

output = stl2.widgets.Output(); cyl.output = output;
plotly_button = stl2.widgets.Button(description='Plot'); plotly_button.on_click(cyl.on_PlotlyPlot);
download_button = stl2.widgets.Button(description='Download'); download_button.on_click(cyl.on_download)

cyl.PlotlyPlot()

stl2.display(stl2.widgets.HBox([plotly_button, download_button]));
stl2.display(stl2.widgets.HBox(cyl.DashButtons));
stl2.display(stl2.widgets.VBox([output]))

