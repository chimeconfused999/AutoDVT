import numpy as np, base64, matplotlib.pyplot as plt, json, plotly.graph_objects as go
import json, plotly
from IPython.display import HTML, display
from ipywidgets import Button, HBox, VBox, widgets
from mpl_toolkits.mplot3d import art3d
from stl import mesh
from plotly.subplots import make_subplots

class Geo2STL:
    def __init__(self, O={}):
        defValue = {"nsd":3, "nen":3, "fn":"generated_cylinder.stl"}
        if isinstance(O, dict):
          for k,v in O.items(): defValue[k]=v
          self.P = defValue
    def readParam(self, f="parameters.json", debug = False):
      try:
        with open(f, "r") as file:
          self.DashKey = json.load(file)
          if debug: print(self.DashKey)
      except FileNotFoundError:
          if debug:print("File not found!")
      except json.JSONDecodeError:
          if debug:print("Error decoding JSON!")

    def Init(self,O={}):
      for k,v in O.items(): self.P[k]=v
      ntheta = self.P["ntheta"]; nheight = self.P["nheight"]; nsd = self.P["nsd"]; nen = self.P["nen"];
      nn=ntheta*nheight; ne=2*ntheta*(nheight-1);
      self.P["nn"]=nn; self.P["ne"]=ne;
      self.x3d = np.zeros([nn,nsd]);
      self.ij2nn=np.zeros([ntheta, nheight], dtype=int)
      self.ien=np.zeros([ne, nen], dtype=int)

    def InitDashKeys(self,O={}):
      self.DashKey = O;
      for k,v in O.items(): self.P[k]=int(v["value"]) if v["type"] == "int" else float(v["value"])
      ntheta = self.P["ntheta"]; nheight = self.P["nheight"]; nsd = self.P["nsd"]; nen = self.P["nen"];

      nn=ntheta*nheight; ne=2*ntheta*(nheight-1);
      self.P["nn"]=nn; self.P["ne"]=ne;
      self.x3d = np.zeros([nn,nsd]);
      self.ij2nn=np.zeros([ntheta, nheight], dtype=int)
      self.ien=np.zeros([ne, nen], dtype=int)

    def mesh_x3d(self,O={}):
      import numpy as np
      ii=0; nheight = self.P["nheight"]; height = self.P["height"]; ntheta = self.P["ntheta"];
      hb1 = self.P["hb1"]; hb2 = self.P["hb2"]; rbmax = self.P["rbmax"]; r = self.P["r"];
      x3d = self.x3d; ij2nn = self.ij2nn; pi=np.pi;
      theta=np.linspace(0,2*np.pi,ntheta+1); h=np.linspace(0,height,nheight)
      for i in range(nheight):
        for j in range(ntheta):
          rr=r; a=r; b=r+rbmax;
          if (h[i]>=hb1 and h[i]<=hb2):
            thetab = -pi + 2*pi/(hb2-hb1)*(h[i]-hb1) # [-pi:pi]
            rr = (a+b)/2 + (b-a)/2 * np.cos(thetab)

          x3d[ii,:] = [rr*np.cos(theta[j]), rr*np.sin(theta[j]), h[i]]
          ij2nn[j,i] = ii
          ii = ii+1
      self.x3d = x3d; self.ij2nn = ij2nn;
    def IEN(self,O={}):
      ie=0; nheight = self.P["nheight"]; ntheta = self.P["ntheta"];
      ien=self.ien
      for i in range(nheight-1):
        for j in range(ntheta):
          n1 = i*ntheta + j; n2= n1+1 if j+1<ntheta else i*ntheta;
          n4=(i+1)*ntheta + j; n3=n4+1 if j+1<ntheta else (i+1)*ntheta;
          ien[ie,:] = [n1,n2,n4]; ien[ie+1,:] = [n2,n3,n4]
          ie = ie+2
      self.ien = ien

    def mesh2stl(self,O={}):
      ne = self.P["ne"]; ien=self.ien; x3d=self.x3d;
      side_facets = ""
      for ie in range(ne):
        n1=ien[ie,0]; n2=ien[ie,1]; n3=ien[ie,2];
        v1 = [x3d[n1,0], x3d[n1,1], x3d[n1,2]]
        v2 = [x3d[n2,0], x3d[n2,1], x3d[n2,2]]
        v3 = [x3d[n3,0], x3d[n3,1], x3d[n3,2]]
        side_facets += "facet normal {} {} 0\nouter loop\n".format(x3d[n1,0], x3d[n1,1])
        side_facets += "vertex {} {} {}\n".format(*v1)
        side_facets += "vertex {} {} {}\n".format(*v2)
        side_facets += "vertex {} {} {}\n".format(*v3)
        side_facets += "endloop\nendfacet\n"
      stl_file = "solid generated_cylinder\n" + side_facets + "endsolid generated_cylinder"
      self.stl = stl_file

    def Buttons(self,O={}):
      DashButtons=[]; DashKey = self.DashKey;
      for k, v in DashKey.items():
        button=widgets.Text(description=f'{v["desc"]}:', value=v["value"]); button.layout.width = v["width"]
        DashButtons.append(button);
      self.DashButtons = DashButtons
    def Extractx2D(self,O={}):
      ij2nn=self.ij2nn; x3d=self.x3d; ien=self.ien;  P=self.P;
      n2d=ij2nn[0,:]; n2d=np.append(n2d,np.flip(ij2nn[round(P["ntheta"]/2),:])); n2d=np.append(n2d,0)
      xx=x3d[n2d,0]; yy=x3d[n2d,2]
      self.x2d = [xx, yy]
    def Extractx2D(self, O={}):
      ij2nn=self.ij2nn; x3d=self.x3d; ien=self.ien;  P=self.P;
      n2d=ij2nn[0,:]; 
      n2d=np.append(n2d, np.flip(ij2nn[round(P["ntheta"]/2),:]))
      n2d=np.append(n2d, 0)
      xx=x3d[n2d,0]; yy=x3d[n2d,2]
      self.x2d = [xx, yy]  # ✅ This line initializes self.x2d
    def PlotlyPlot(self):
      """Generate a Plotly figure and return it as JSON for Flask rendering."""

      # Ensure mesh data exists before plotting
      if not hasattr(self, "x2d") or not hasattr(self, "x3d") or not hasattr(self, "ien"):
          print("Error: Mesh data is missing!")
          return json.dumps({"error": "Mesh data not initialized"})  # Return empty JSON if data is missing

      [xx, yy] = self.x2d
      [x, y, z] = self.x3d.transpose()
      [i, j, k] = self.ien.transpose()
      data = {"x2d":self.x2d, "x3d":self.x3d.transpose(), "ien":self.ien}

      return data
      # Create the Plotly figure
      #fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'scatter'}, {'type': 'mesh3d'}]])

      #fig.add_trace(go.Scatter(x=xx, y=yy, mode="lines"), row=1, col=1)
      #fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, color='skyblue', opacity=0.50), row=1, col=2)

      #fig.update_yaxes(scaleanchor="x", scaleratio=1)
      #fig.update_layout(height=600, width=800)

      #return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)  # ✅ Ensure valid JSON format

    def PlotFromFile(self,fn):
      [xx,yy] = self.x2d;

      cube_mesh = mesh.Mesh.from_file(fn)
      fig = plt.figure()
      ax1 = fig.add_subplot(121, projection='3d');   ax2 = fig.add_subplot(122)

      ax1.add_collection3d(art3d.Poly3DCollection(cube_mesh.vectors))
      scale = cube_mesh.points.flatten()
      ax1.auto_scale_xyz(scale, scale, scale)

      ax2.plot(xx, yy);   ax2.set_aspect('equal')

      plt.show()
    def on_download(self,b):
      with self.output: download(self.stl,self.P["fn"])

    def on_PlotlyPlot(self,b):
      i=0; self.output.clear_output(wait=True)
      for k, v in self.DashKey.items():
        self.DashKey[k]["value"]=self.DashButtons[i].value; i=i+1;
      self.InitDashKeys(DashKey); self.mesh_x3d(); self.IEN(); self.Extractx2D(); self.mesh2stl(); save_d2f(self.P["fn"], self.stl)
      #self.PlotlyPlot()
      [xx,yy] = self.x2d; [x,y,z] = self.x3d.transpose(); [i,j,k] = self.ien.transpose()

      with self.output:
        #print(self.DashKey)
        self.PlotlyPlot()
        #self.PlotFromFile(fn)

    def on_Plot(self,b):
      i=0; self.output.clear_output()
      for k, v in self.DashKey.items():
        self.DashKey[k]["value"]=self.DashButtons[i].value; i=i+1;
      self.InitDashKeys(DashKey); self.mesh_x3d(); self.IEN(); self.Extractx2D(); self.mesh2stl(); save_d2f(self.P["fn"], self.stl)
      with self.output:
        self.PlotFromFile(self.P["fn"])
def save_d2f(fn,d):
  with open(fn, "w") as f: f.write(d)
def download(stl_file,fn):
  b64_encoded_stl = base64.b64encode(stl_file.encode()).decode()
  download_link = f"data:application/octet-stream;base64,{b64_encoded_stl}"
  download_button = f'<a href="{download_link}" download="{fn}">Download STL File</a>'
  display(HTML(download_button))
