import subprocess
import openep
import os
import tempfile

case = cases[case_1]
MESHTOOL = meshtool_executable
debug = False

def run(cmd):
    os.system(MESHTOOL + " " + " ".join(cmd))

with tempfile.TemporaryDirectory() as temp_dir:
    output_mesh = os.path.join(temp_dir, "smooth_mesh")
    input_mesh = os.path.join(temp_dir, "rough_mesh")
    openep.export_openCARP(case, prefix=f"{input_mesh}")

    # SMOOTH
    run([
        "smooth", "mesh",
        f"-msh={input_mesh}",
        f"-outmsh={output_mesh}",
        "-iter=500",
        "-smth=0.7",
        "-tags=0",
        "-ifmt=carp_txt",
        "-ofmt=carp_txt"
    ])
    print("Smooth completed")
    # CLEAN TOPOLOGY
    run([
        "clean", "topology",
        f"-msh={output_mesh}",
        f"-outmsh={output_mesh}",
        "-ifmt=carp_txt",
        "-ofmt=carp_txt"
    ])
    print("Clean completed")
    # CLEAN QUALITY
    run([
        "clean", "quality",
        f"-msh={output_mesh}",
        "-thr=0.5",
        f"-outmsh={output_mesh}_final",
        "-ifmt=carp_txt",
        "-ofmt=carp_txt"
    ])
    print("Quality completed")
    output_case = openep.load_opencarp(
        f"{output_mesh}.pts",
        f"{output_mesh}.elem",
        f"{output_mesh}.lon",
    )

out_cases[f'{case_1}_smooth'] = output_case