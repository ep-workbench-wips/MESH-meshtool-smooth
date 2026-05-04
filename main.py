import subprocess
import openep
import os



try:
    case = cases[case_1]
    MESHTOOL = meshtool
    debug = False

except:
    temp_dir = "/Users/vinush-vigneswaran/Documents/03_CODE/wips/meshtool_smooth/temp_dir"
    MESHTOOL = "/usr/local/bin/meshtool"
    debug = True

output_mesh = os.path.join(temp_dir, "smooth_mesh")
input_mesh = os.path.join(temp_dir, "in")

if not debug:
    openep.export_openep_mat(case, filename=f"{input_mesh}")

def run(cmd):
    subprocess.run([MESHTOOL] + cmd, check=True)

# SMOOTH
run([
    "smooth", "mesh",
    f"-msh={input_mesh}",
    f"-outmsh={output_mesh}",
    "-smth=0.7",
    "-tags=0",
    "-ifmt=carp_txt",
    "-ofmt=vtk"
])

# CLEAN TOPOLOGY
run([
    "clean", "topology",
    f"-msh={output_mesh}",
    f"-outmsh={output_mesh}",
    "-ifmt=vtk",
    "-ofmt=carp_txt"
])

# CLEAN QUALITY
run([
    "clean", "quality",
    f"-msh={output_mesh}",
    "-thr=0.5",
    f"-outmsh={output_mesh}"
])


output_case = openep.load_opencarp(
    f"{output_mesh}.pts",
    f"{output_mesh}.elem",
    f"{output_mesh}.lon",
)

if not debug:
    out_cases[f'{case_1}_smooth'] = output_case