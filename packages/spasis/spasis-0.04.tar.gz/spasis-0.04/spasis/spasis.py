
import numpy as np
import geopandas as gpd
import pandas as pd
import glob
from scipy.spatial import Voronoi, voronoi_plot_2d
import shapely
from shapely.ops import unary_union, nearest_points
        
class create_voronoi:
    
    def __init__(self,
                    boundary,
                    point_shape,
                    attribute:str = None
                    ):
        
        self.boundary = boundary
        self.point_shape = point_shape
        self.attribute = attribute
        
        if isinstance(boundary, str):
            bounds = gpd.read_file(boundary)
            if bounds.crs == None:
                bounds.crs = {'init': 'epsg:4326'}
        elif isinstance(boundary, gpd.GeoDataFrame):
            bounds = self.boundary
            if bounds.crs == None:
                bounds.crs = {'init': 'epsg:4326'}
        else:
            raise TypeError("Expecting a string like object of gpd.Geodataframe like object for point shapefile")
        
        if isinstance(point_shape, str):
            centr = gpd.read_file(point_shape)
            if centr.crs == None:
                centr.crs = {'init': 'epsg:4326'}
        elif isinstance(point_shape, gpd.GeoDataFrame):
            centr = self.point_shape
            if centr.crs == None:
                centr.crs = {'init': 'epsg:4326'}
        else:
            raise TypeError("Expecting a string like object of gpd.Geodataframe like object for point shapefile")
        
        listarray = []
        for pp in centr.geometry:
            listarray.append([pp.x, pp.y])
        nparray = np.array(listarray)
        vor = Voronoi(nparray)
        voronoi_plot_2d(vor)
        lines = [
            shapely.geometry.LineString(vor.vertices[line])
            for line in vor.ridge_vertices
            if -1 not in line
        ]
        
        polygon = gpd.GeoDataFrame()
        for poly in shapely.ops.polygonize(lines):
            polygooons = gpd.GeoDataFrame(geometry=gpd.GeoSeries(poly))
            polygon = polygon.append(polygooons)
        if polygon.crs == None:
            polygon.crs = {'init': 'epsg:4326'}
        if self.attribute is not None:
            clipped_data = gpd.overlay(bounds, polygon, how='identity')
            if 'OBJECTID' not in clipped_data.columns.unique():
                clipped_data['OBJECTID']=range(0, len(clipped_data))
            daat = gpd.sjoin(clipped_data, centr, how = 'left', op= 'intersects')
            if daat.crs == None:
                daat.crs = {'init': 'epsg:4326'}
            df = daat[['OBJECTID',f"{self.attribute}", 'geometry']].copy()
            final_da=df.dissolve(by='OBJECTID')
            final_da[f"{self.attribute}"].interpolate(method ='nearest', inplace = True)
            voronoi_data = gpd.overlay(final_da, bounds, how = 'union')
            self.spasis = voronoi_data
            if self.spasis.crs == None:
                self.spasis.crs = {'init': 'epsg:4326'}
        else:
            voronoi_pod = gpd.overlay(bounds, polygon, how='identity')
            voronoi_data = gpd.overlay(voronoi_pod, bounds, how = 'union')
            voronoi_data = voronoi_data[['geometry']].copy()
            daat_fala = gpd.sjoin(voronoi_data, bounds, how = 'left', op= 'intersects')
            daat_fala.drop('index_right', axis = 1, inplace = True)
            self.spasis = daat_fala
            if self.spasis.crs == None:
                self.spasis.crs = {'init': 'epsg:4326'}

class transfer_val:
    
    def __init__(self,
                     datas,
                     area_threshld:float,
                     attribute:str,
                     naval = None):
        
        self.datas = datas
        self.area_threshld = area_threshld
        self.attribute = attribute
        self.naval = naval
        if isinstance(self.datas, str):
            data = gpd.read_file(self.datas)
        elif isinstance(self.datas, gpd.GeoDataFrame):
            data = self.datas
        else:
            raise TypeError(f"{self.datas} is not supported type of data location,\neither use shapefile location or geodataframe")
        if 'UID' not in data.columns.unique():
            data['UID']=range(0, len(data))
        
        if self.naval is not None:
            print(f"Considered values {self.naval} in the {self.attribute} for replacing the NAN value")
            if len(data[data[f"{self.attribute}"].isnull()]) != 0:
                data[f"{self.attribute}"].fillna(self.naval, inplace = True)
            else:
                pass
        else:
            print(f"Considered values 3 in the {self.attribute} for replacing the NAN value")
            if len(data[data[f"{self.attribute}"].isnull()]) != 0:
                data[f"{self.attribute}"].fillna(3, inplace = True)
            else:
                pass
        data['area_ac'] = data.geometry.area*(100000**2)/4046.86
        df_null = data[data[f"{self.attribute}"].isnull()]
        area_silv = data[data['area_ac']<=self.area_threshld]
        silv = pd.concat([area_silv , df_null], sort = False)
        del silv[f"{self.attribute}"]
        ohex = data[data['area_ac']>=self.area_threshld]
        
        def conv_point(gdf):
            centx = gpd.GeoDataFrame(geometry=gpd.GeoSeries(gdf.representative_point()))
            if centx.crs == None:
                centx.crs = {'init': 'epsg:4326'}
            faul = gpd.sjoin(centx, gdf, op="intersects")
            del faul['index_right']
            return faul
        
        def calculate_nearest(row, destination, val, col="geometry"):
            # 1 - create unary union    
            dest_unary = destination["geometry"].unary_union
            # 2 - find closest point
            nearest_geom = nearest_points(row[col], dest_unary)
            # 3 - Find the corresponding geom
            match_geom = destination.loc[destination.geometry 
                        == nearest_geom[1]]
            # 4 - get the corresponding value
            match_value = match_geom[val].to_numpy()[0]
            return match_value
        
        silv_p = conv_point(silv)
        ohex_p =conv_point(ohex)
        silv_p["near_geom"] = silv_p.apply(calculate_nearest, destination=ohex_p, val="geometry", axis=1)
        silv_p["near_GZ"] = silv_p.apply(calculate_nearest, destination=ohex_p, val=f"{self.attribute}", axis=1)
        del silv_p["geometry"]
        silv_p.rename(columns={"near_geom": "geometry", "near_GZ": f"{self.attribute}"}, inplace = True)
        silve = gpd.GeoDataFrame(silv_p, geometry='geometry', crs={"init":"epsg:4326"})
        
        fg = silve[[f"{self.attribute}", "UID"]].copy()
        data_dvm=silv.merge(fg, on=["UID"])
        point_df = pd.concat([ohex, data_dvm], sort = False)
        point_df.drop(['UID', 'area_ac'], inplace = True, axis= 1)
        self.spasis = point_df

class binaryClassifier:
    
    def __init__(self, row, source_col, output_col, threshold):
        
        self.row = row
        self.source_col = source_col
        self.output_col = output_col
        self.threshold = threshold
        #uses: bogs = bogs.apply(binaryClassifier, source_col='area_km2', output_col='small_big', threshold=l_mean_size, axis=1)
        # If area of input geometry is lower that the threshold value
        if self.row[self.source_col] < self.threshold:
            # Update the output column with value 0
            self.row[self.output_col] = 0
        # If area of input geometry is higher than the threshold value update with value 1
        else:
            self.row[self.output_col] = 1
        # Return the updated row
        self.spasis = self.row