from flask import Flask, render_template, request, jsonify, send_file
import os, json
import plotly
from stl2 import Geo2STL

app = Flask(__name__)

# Initialize Geo2STL
fn = "generated_cylinder.stl"
cyl = Geo2STL({"fn": fn})

# Load JSON parameters
with open("parameters.json", "r") as f:
    DashKey = json.load(f)


d1 = [{"x":['2030-10-04', '2025-11-04', '2023-12-04'], "y": [90, 40, 60], "type": "scatter"}];
print(d1)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        for key in request.form:
            if key in DashKey:
                DashKey[key]["value"] = request.form[key]

        # ✅ Ensure all required methods are called before plotting
        cyl.InitDashKeys(DashKey)
        cyl.mesh_x3d()
        cyl.IEN()
        cyl.Extractx2D()  # ✅ This ensures `self.x2d` is created before plotting
        cyl.mesh2stl()
        test = ["a", 1]
        #return jsonify(test)  # ✅ Now `self.x2d` exists
        return jsonify(d1)

    return render_template("index.html", params=DashKey)

@app.route("/download")
def download():
    """Serve the generated STL file for download."""
    return send_file(fn, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
