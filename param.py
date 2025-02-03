import stl2

DashKey = {
    "r":{"desc":'Sinus, r:', "value":'1', "type":"float", "width":'150px'},
    "height":{"desc":'height:', "value":'8', "type":"float", "width":'150px'},
    "rbmax":{"desc":' | Bulge, r:', "value":'0.7', "type":"float", "width":'150px'},
    "hb1":{"desc":'h1:', "value":'2', "type":"float", "width":'150px'},
    "hb2":{"desc":'h2:', "value":'6', "type":"float", "width":'150px'},
    "ntheta":{"desc":' | Grid resolution, ntheta:', "value":'30', "type":"int","width":'150px'},
    "nheight":{"desc":'nheight:', "value":'20', "type":"int", "width":'150px'},
    }

fn="generated_cylinder.stl"
cyl = stl2.Geo2STL({"fn":fn});
cyl.InitDashKeys(DashKey); cyl.mesh_x3d(); cyl.IEN(); cyl.Extractx2D(); cyl.mesh2stl(); stl2.save_d2f(fn, cyl.stl); cyl.Buttons(DashKey)

output = stl2.widgets.Output(); cyl.output = output;
plotly_button = stl2.widgets.Button(description='Plot'); plotly_button.on_click(cyl.on_PlotlyPlot);
download_button = stl2.widgets.Button(description='Download'); download_button.on_click(cyl.on_download)

cyl.PlotlyPlot()

display(stl2.widgets.HBox([plotly_button, download_button]));
display(stl2.widgets.HBox(cyl.DashButtons));
display(stl2.widgets.VBox([output]))

