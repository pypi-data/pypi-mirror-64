
import math
import time
import glob
import shapely
import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import PySimpleGUI as sg
from shapely.geometry import Polygon
from shapely.ops import cascaded_union

class check_topology:
    
    def __init__(self, data):
        
        self.data = data
        pd.options.mode.chained_assignment = None
        if isinstance(data, str):
            gdf = gpd.read_file(self.data)
        elif isinstance(data, gpd.GeoDataFrame):
            gdf = self.data
        else:
            pass
        val_data = gpd.GeoDataFrame()
        for index, row in tqdm(gdf.iterrows(), total = gdf.shape[0]):
            if row['geometry'].is_valid == False | row['geometry'].is_simple == False:
                deci = sg.PopupYesNo("Do you want to fix the geometry?")
                if deci == 'Yes':
                    pol = row['geometry'].buffer(0)
                    time.sleep(1)
                    mid = gpd.GeoDataFrame(geometry=gpd.GeoSeries(pol))
                    val_data = val_data.append(mid)
                else:
                    break
            else:
                val = gpd.GeoDataFrame(geometry=gpd.GeoSeries(row['geometry']))
                val_data = val_data.append(val)
        if val_data.crs == None:
            val_data.crs = {'init': 'epsg:4326'}
        self.geosolution = val_data

class dissolve_polygon:
    
    def __init__(self,
                 data: gpd.GeoDataFrame, threshold: float
                 )-> gpd.GeoDataFrame:
        self.threshold = threshold
        pd.options.mode.chained_assignment = None
        if not isinstance(data, gpd.GeoDataFrame):
            return gpd.GeoDataFrame()
        data = data.copy()
        while True:
            src = src_idx = None
            for i in range(len(data.index)):
                row = data.iloc[i]
                row_geom = row["geometry"]
                if row_geom.area <= threshold/1.0e10:
                    src_idx = i
                    src = row
                    break
            if src is None:
                break
            src_geom = src["geometry"]
            # if not isinstance(src_geom, (shapely.geometry.polygon.Polygon)):
            #     print(f"src {src.name} is not a polygon")
            # Find adjacent poly with largest shared border to merge
            dst = dst_len = None
            intersection = data.intersection(src_geom)
            for i in tqdm(range(len(data.index))):
                if src_idx == i:
                    continue
                shape = intersection.iloc[i]
                intersection_length = 0
                if isinstance(shape, shapely.geometry.LineString):
                    intersection_length = shape.length
                elif isinstance(shape, shapely.geometry.MultiLineString):
                    intersection_length = max([line.length for line in shape.geoms])
                else:
                    continue
                if dst is None or intersection_length > dst_len:
                    dst = data.iloc[i]
                    dst_len = intersection_length
                    continue
            if dst is None:
                # print(f"Couldn't find candidate for merge with {src_idx}")
                break
            dst_geom = dst["geometry"]
            #print(f"Merging {src.name} into {dst.name}")
            try:
                data.loc[dst.name, "geometry"] = cascaded_union([src_geom, dst_geom])
            except ValueError:
                pass
            if src_geom.area > dst_geom.area:
                #print(f"Copying attributes from src {src.name} to dst {dst.name}")
                for column in data.columns:
                    if column == "geometry":
                        continue
                    data.loc[dst.name, column] = src[column]
            data.drop([src.name], inplace=True)
        self.geosolution = data

class hexagon_grid:
    
    def __init__(self,
                 data, 
                 spacing
                 ):
        self.data = data
        self.spacing = spacing
        pd.options.mode.chained_assignment = None
        if isinstance(data, str):
            gdf = gpd.read_file(self.data)
        elif isinstance(data, gpd.GeoDataFrame):
            gdf = self.data
        else:
            pass
        
        hSpacing = spacing/100000
        vSpacing = spacing/100000
        hOverlay = 0.0
        vOverlay = 0.0
    
        # To preserve symmetry, hspacing is fixed relative to vspacing
        xVertexLo = 0.288675134594813 * vSpacing
        xVertexHi = 0.577350269189626 * vSpacing
        hSpacing = xVertexLo + xVertexHi
    
        hOverlay = hSpacing
        
        halfVSpacing = vSpacing / 2.0
    
        xmin, ymin = [i.min() for i in gdf.bounds.T.values[:2]]
        xmax, ymax = [i.max() for i in gdf.bounds.T.values[2:]]
        cols = int(math.ceil((xmax - xmin) / hOverlay))
        rows = int(math.ceil((ymax - ymin) / (vSpacing - vOverlay)))
        
        geoms = []
        for col in tqdm(range(cols)):
            # (column + 1) and (row + 1) calculation is used to maintain
            # topology between adjacent shapes and avoid overlaps/holes
            # due to rounding errors
            x1 = xmin + (col * hOverlay)    # far left
            x2 = x1 + (xVertexHi - xVertexLo)  # left
            x3 = xmin + (col * hOverlay) + hSpacing  # right
            x4 = x3 + (xVertexHi - xVertexLo)  # far right
    
            for row in range(rows):
                if (col % 2) == 0:
                    y1 = ymax + (row * vOverlay) - (((row * 2) + 0) * halfVSpacing)  # hi
                    y2 = ymax + (row * vOverlay) - (((row * 2) + 1) * halfVSpacing)  # mid
                    y3 = ymax + (row * vOverlay) - (((row * 2) + 2) * halfVSpacing)  # lo
                else:
                    y1 = ymax + (row * vOverlay) - (((row * 2) + 1) * halfVSpacing)  # hi
                    y2 = ymax + (row * vOverlay) - (((row * 2) + 2) * halfVSpacing)  # mid
                    y3 = ymax + (row * vOverlay) - (((row * 2) + 3) * halfVSpacing)  # lo
    
                geoms.append((
                    (x1, y2),
                    (x2, y1), (x3, y1), (x4, y2), (x3, y3), (x2, y3),
                    (x1, y2)
                ))
                
        hexa_data =  gpd.GeoDataFrame(
            index=[i for i in range(len(geoms))],
            geometry=pd.Series(geoms).apply(lambda x: Polygon(x)),
            crs=gdf.crs
            )
        
        datax = gpd.GeoDataFrame(crs = {'init': 'epsg:4326'})
        for index, row in tqdm(hexa_data.iterrows(), total = hexa_data.shape[0]):
            if row['geometry'] != None and row['geometry'].geom_type == 'Polygon':
                df = gpd.GeoDataFrame(geometry=gpd.GeoSeries(row['geometry']))
                datax = datax.append(df, sort = False)
            else:
                pass
        if datax.crs ==None:
            datax.crs ={'init': 'epsg:4326'}
        final_hexa =gpd.overlay(gdf.explode().reset_index().drop(['level_0', 'level_1'], axis = 1),
                                gpd.overlay(gdf.explode().reset_index().drop(['level_0', 'level_1'], axis = 1),
                                            datax, how='intersection'),
                                how = 'union')[['geometry']].copy()
        area_threshold = (spacing*spacing)*0.33
        disolve_hexa = dissolve_polygon(final_hexa, area_threshold).geosolution
        check_topology(disolve_hexa)
        self.geosolution = disolve_hexa

class merge_shapefile:
    
    def __init__(self, shape_path):
        
        self.shape_path = shape_path
        pd.options.mode.chained_assignment = None
        if not isinstance(self.shape_path, gpd.GeoDataFrame):
            try:
                gdf = pd.concat([gpd.read_file(shp)for shp in [i for i in glob.glob(f"{shape_path}/*.shp")]]).pipe(gpd.GeoDataFrame)
                self.geosolution = gdf
            except ValueError:
                self.geosolution = gpd.read_file(self.shape_path)
        elif isinstance(self.shape_path, gpd.GeoDataFrame):
            self.geosolution = self.shape_path
        else:
            pass

class check_crs:
    
    def __init__(self,
                 gdf
                 ):
        
        self.gdf = gdf
        pd.options.mode.chained_assignment = None
        if isinstance(gdf, gpd.GeoDataFrame):
            if gdf.crs == None:
                gdf.crs = {'init': 'epsg: 4326'}
            self.geosolution = gdf
        elif isinstance(gdf, str):
            data = gpd.read_file(gdf)
            if data.crs == None:
                data.crs = {'init': 'epsg: 4326'}
            self.geosolution = data
        else:
            pass