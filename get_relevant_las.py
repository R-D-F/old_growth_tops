import shutil
from pathlib import Path

import geopandas as gpd
import laspy
from shapely import box

base_path = Path(__file__).parent

las_folder = base_path / "data"
research_area = base_path / r"data\mask\research_area.gpkg"
research_area_gdf = gpd.read_file(research_area)
research_geo = research_area_gdf.geometry

las_files = [p for p in las_folder.iterdir() if p.suffix.lower() == ".laz"]
print(f"Found {len(las_files)} LAS/LAZ files")

output_crs = "EPSG:2285"
area_in_output_crs = research_area_gdf.to_crs(output_crs)

research_las = []
polys = []
overlap_polys = []
dst = r"data\matched_las"

for las in las_files:
    las_ob = laspy.read(las)
    min_xyz, max_xyz = las_ob.header.mins, las_ob.header.maxs
    poly = box(min_xyz[0], min_xyz[1], max_xyz[0], max_xyz[1])
    polys.append(poly)

    if area_in_output_crs.intersects(poly).any():
        research_las.append(las)
        overlap_polys.append(poly)
        print("MATCH:", las.name)
print("somethign")
for las in research_las:
    shutil.copy2(las, dst)
