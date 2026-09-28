import geopandas as gpd
import shapely
from shapely.geometry import LineString, Point, box

plss_33_36 = gpd.read_file(r"data\plss\Public_Land_Survey_Sections\plss_33-36.gpkg")
plss_33_mask = plss_33_36["PLS_TWP__1"] == 33
plss_33 = plss_33_36[plss_33_mask]
plss_36_mask = plss_33_36["PLS_TWP__1"] == 36
plss_36 = plss_33_36[plss_36_mask]

hw_542 = gpd.read_file(r"C:\Users\rifra\HW\old_growth_tops\data\state_routs\baker_hw.gpkg").to_crs(
    plss_33_36.crs
)
welcome_creek = gpd.read_file(
    r"C:\Users\rifra\HW\old_growth_tops\data\creeks\full_welcome_creek.gpkg",
)
welcome_creek = gpd.GeoSeries([welcome_creek.union_all()], crs=welcome_creek.crs).to_crs(
    plss_33_36.crs
)

plss_33_bounds = plss_33.union_all().bounds

half_e_w_plss_33 = (plss_33_bounds[0] + plss_33_bounds[2]) / 2

half_e_w_plss_33_geo = gpd.GeoSeries(
    LineString(
        [Point(half_e_w_plss_33, plss_33_bounds[3]), Point(half_e_w_plss_33, plss_33_bounds[1])]
    ),
    crs=plss_33_36.crs,
)
plss_36_bounds = plss_36.union_all().bounds
top_36 = LineString(
    [Point(plss_36_bounds[0], plss_36_bounds[3]), Point(plss_36_bounds[2], plss_36_bounds[3])]
)

hw_geom = hw_542.union_all()
creek_geom = welcome_creek.union_all()
half_e_w_geom = half_e_w_plss_33_geo.union_all()
hw_geom_series = gpd.GeoSeries(hw_geom)

south_west_bound = half_e_w_geom.intersection(hw_geom)
south_east_bound = creek_geom.intersection(hw_geom)
north_east_bound = creek_geom.intersection(top_36)
north_east_bound = shapely.transform(north_east_bound, lambda x: x)
north_west_bound = Point(half_e_w_plss_33, plss_33_bounds[3])

welcome_creek_clip_box = box(-20000000, south_east_bound.y, 0, north_east_bound.y)
half_e_w_geom_clip_box = box(-20000000, south_west_bound.y, 0, north_west_bound.y)
hw_542_clip_box = box(south_east_bound.x, 7000000, south_west_bound.x, 5000000)
east_bound = welcome_creek.clip(welcome_creek_clip_box).union_all()
north_bound = LineString([north_east_bound, north_west_bound])
west_bound = half_e_w_plss_33_geo.clip(half_e_w_geom_clip_box).union_all()
south_bound = hw_geom_series.clip(hw_542_clip_box).union_all()

s = gpd.GeoSeries([east_bound, north_bound, west_bound, south_bound], crs=plss_33_36.crs)
polygon = s.polygonize()
polygon.to_file(r"C:\Users\rifra\HW\old_growth_tops\data\mask\research_area.gpkg", driver="GPKG")
print("nothing")
