
import glob
import geopandas as gpd
import pandas as pd
from tqdm import tqdm
import shapely
from shapely.wkb import loads
from shapely.geometry import Point, Polygon, LineString, MultiLineString
from shapely.ops import unary_union, polygonize
import PySimpleGUI as sg
import warnings
warnings.filterwarnings("ignore")

class latin_design:
    
    def __init__(self, point:gpd.GeoDataFrame, buffer_length:int = None):
        
        self.point = point
        if self.point.crs is None:
            self.point.crs = {'init': 'epsg:3857'}
        self.point.to_crs({'init': 'epsg:3857'})
        pd.options.mode.chained_assignment = None
        warnings.filterwarnings("ignore")
        self.buffer_length = buffer_length
        xcords = self.point.geometry.x
        ycords = self.point.geometry.y
        if self.buffer_length is None:
            point_data = Point((xcords, ycords)).buffer(71)
        else:
            point_data = Point((xcords, ycords)).buffer(self.buffer_length)
            
        s = point_data.simplify(0.5, preserve_topology=False)
        
        num_tiles = 3
        minx, miny, maxx, maxy = s.bounds
        dx = (maxx - minx) / num_tiles
        dy = (maxy - miny) / num_tiles
        
        lines = []
        for x in tqdm(range(num_tiles + 1)):
            lines.append(LineString([(minx + x * dx, miny), (minx + x * dx, maxy)]))
        for y in range(num_tiles + 1):
            lines.append(LineString([(minx, miny + y * dy), (maxx, miny + y * dy)]))
        self.plot = gpd.GeoDataFrame(geometry=gpd.GeoSeries(polygonize(unary_union(MultiLineString(lines))))).iloc[[1,3,4,5,7]]
        if self.plot.crs == None:
            self.plot.crs = {'init': 'epsg:3857'}

class select_geoms:
    
    def __init__(self, gdf_path, length:int = None):
        
        self.gdf_path = gdf_path
        self.length = length
        pd.options.mode.chained_assignment = None
        warnings.filterwarnings("ignore")
        if isinstance(self.gdf_path, str):
            try:
                data = pd.concat([gpd.read_file(shp).to_crs({'init': 'epsg:3857'}) for shp in [i for i in glob.glob(f"{self.gdf_path}/*.shp")]]).pipe(gpd.GeoDataFrame)
                data = data.explode().reset_index().drop(['level_0', 'level_1'], axis = 1)
                if data.crs == None:
                    data.crs = {'init': 'epsg:3857'}
                check_topology(data)
            except ValueError:
                datad = gpd.read_file([i for i in glob.glob(f"{self.gdf_path}/*.shp")]).to_crs({'init': 'epsg:3857'})
                data = datad.copy().to_crs({'init': 'epsg:3857'})
                if data.crs == None:
                    data.crs = {'init': 'epsg:3857'}
                print(f"\nCRS is {data.crs} for {self.gdf_path}")
                data = data.explode().reset_index().drop(['level_0', 'level_1'], axis = 1)
                check_topology(data)
        else:
            data = gdf_path.copy().to_crs({'init': 'epsg:3857'})
            data = data.explode().reset_index().drop(['level_0', 'level_1'], axis = 1)
            check_topology(data)
        datas = gpd.GeoDataFrame(geometry=gpd.GeoSeries(data.centroid))
        geom_withina =gpd.GeoDataFrame()
        for index, row in tqdm(datas.iterrows(), total = datas.shape[0]):
            if self.length is None:
                uid = latin_design(gpd.GeoDataFrame(geometry=gpd.GeoSeries(Point((row['geometry'].x, row['geometry'].y)))), 71).plot
            else:
                uid = latin_design(gpd.GeoDataFrame(geometry=gpd.GeoSeries(Point((row['geometry'].x, row['geometry'].y)))), self.length).plot
            uid['UID'] = int(index)
            geom_withina = geom_withina.append(uid)
        if geom_withina.crs is None:
            geom_withina.crs = {'init': 'epsg:4326'}
        
        geom_withina.to_crs({'init': 'epsg:4326'})
        crs = {'init': 'epsg:4326'}
        within_buffer = gpd.GeoDataFrame()
        for i in geom_withina['UID']:
            dta = geom_withina.loc[geom_withina.UID == i]
            geom_within = []
            for index, row in tqdm(dta.iterrows(), total = dta.shape[0]):
                df = gpd.GeoDataFrame(geometry=gpd.GeoSeries(row['geometry']))
                for k in data['geometry']:
                    df1 = gpd.GeoDataFrame(geometry=gpd.GeoSeries(k))
                    if any(df['geometry'].within(df1['geometry'])) == True:
                        for p in df['geometry']:
                            geom_within.append(p)
                    else:
                        pass
            if len(geom_within) == 5:
                within_buffer = within_buffer.append(gpd.GeoDataFrame(geometry=gpd.GeoSeries(geom_within)))
            else:
                pass        
        if within_buffer.crs is None:
            within_buffer.crs = crs
        try:
            within_buffer = within_buffer.to_crs(crs)
            within_buffer["geometry"] = within_buffer["geometry"].apply(lambda geom: geom.wkb)
            within_buffer = within_buffer.drop_duplicates(["geometry"])
            within_buffer["geometry"] = within_buffer["geometry"].apply(lambda geom: loads(geom))
            def treatment(row):
                if row['Treatment'] == 0:
                    return 'High'
                elif row['Treatment'] == 1:
                    return 'Mid-High'
                elif row['Treatment'] == 2:
                    return 'Control'
                elif row['Treatment'] == 3:
                    return 'Mid-Low'
                elif row['Treatment'] == 4:
                    return 'Low'
                else:
                    return 'NA'
            within_buffer['Treatment'] = within_buffer.index
            within_buffer = within_buffer.assign(Treatment=within_buffer.apply(treatment, axis=1))
            design_plot = gpd.overlay(data, within_buffer, how = 'union')
            design_plot['Treatment'].fillna("Actual", inplace = True)
            if not isinstance(self.gdf_path, str):
                if design_plot.crs == None:
                    design_plot.crs = {'init': 'epsg:4326'}
                design_plot = design_plot.to_crs({'init': 'epsg:4326'})
                check_topology(design_plot)
                self.geodesign = design_plot
            else:
                check_topology(design_plot).topology
                self.geodesign = design_plot
        except AttributeError:
            sg.Popup("     Side length of the test plot is larger than required, wont have any Test plot for the AOI,\n     because test plot threshold length is bigger,\n\n     Please insert smaller length for the Test Plots")
            self.geodesign = None
            pass

class rotate_plot:
    
    def __init__(self, aux_data, plot:gpd.GeoDataFrame, attribute:str):
        
        self.aux_data = aux_data
        self.plot = plot
        self.attribute = attribute
        warnings.filterwarnings("ignore")
        pd.options.mode.chained_assignment = None
        xmax, ymin, xmin, ymax= self.plot.total_bounds
        if isinstance(self.aux_data, gpd.GeoDataFrame):
            
            data = self.aux_data[[f"{self.attribute}", 'geometry']].copy()
            ploy = Polygon([[xmax, ymin], [xmax, ymax], [xmin, ymax], [xmin, ymin]])
            plot_data = gpd.GeoDataFrame(geometry=gpd.GeoSeries(ploy))
            geom_within = []
            for index, row in tqdm(data.iterrows(), total = data.shape[0]):
                df = gpd.GeoDataFrame(geometry=gpd.GeoSeries(row['geometry']))
                if any(df['geometry'].within(plot_data['geometry'])) == True:
                    for p in df['geometry']:
                        geom_within.append(p)
                else:
                    pass
            point_data = gpd.GeoDataFrame(geometry=gpd.GeoSeries(geom_within))
            df_data = data[data.index.isin(point_data.index)]
            mean_val = df_data[f"{self.attribute}"].mean()
            if mean_val is not None:
                self.plot['rotate'] = self.plot.apply(lambda x: shapely.affinity.rotate(x['geometry'], mean_val), axis = 1)
                del self.plot['geometry']
                self.plot.rename(columns={"rotate": "geometry"}, inplace = True)
                self.plot.set_geometry(col = 'geometry', inplace = True)
                self.geodesign = self.plot
            else:
                pass
        else:
            pass


class composite_union:
    
    def __init__(self, data, buffer = None):
        
        self.data = data
        self.buffer = buffer
        
        pd.options.mode.chained_assignment = None
        warnings.filterwarnings("ignore")
        if data.crs == {'init': 'epsg: 4326'} and buffer == None:
            unary_data = gpd.GeoDataFrame(
                geometry=gpd.GeoSeries(unary_union(data.geometry).intersection(
                    unary_union(data.geometry).buffer(0.0005)))).explode().reset_index().drop(['level_0', 'level_1'],
                                                                                              axis = 1)
            self.geosolution = unary_data
            if self.geosolution.crs == None:
                self.geosolution.crs = data.crs
            self.centroid = self.geosolution.centroid
            
        elif data.crs == {'init': 'epsg: 3857'} and buffer == None:
            unary_data = gpd.GeoDataFrame(
                geometry=gpd.GeoSeries(unary_union(data.geometry).intersection(
                    unary_union(data.geometry).buffer(50)))).explode().reset_index().drop(['level_0', 'level_1'],
                                                                                              axis = 1)
            self.geosolution = unary_data
            if self.geosolution.crs == None:
                self.geosolution.crs = data.crs
            self.centroid = self.geosolution.centroid
            
        elif buffer is not None and data.crs != None:
            unary_data = gpd.GeoDataFrame(
                geometry=gpd.GeoSeries(unary_union(data.geometry).intersection(
                    unary_union(data.geometry).buffer(self.buffer)))).explode().reset_index().drop(['level_0', 'level_1'],
                                                                                              axis = 1)
            self.geosolution = unary_data
            if self.geosolution.crs == None:
                self.geosolution.crs = data.crs
            self.centroid = self.geosolution.centroid
            
        elif buffer is not None and data.crs == None:
            data.crs = {'init': 'epsg:4326'}
            unary_data = gpd.GeoDataFrame(
                geometry=gpd.GeoSeries(unary_union(data.geometry).intersection(
                    unary_union(data.geometry).buffer(0.005)))).explode().reset_index().drop(['level_0', 'level_1'],
                                                                                              axis = 1)
            self.geosolution = unary_data
            if self.geosolution.crs == None:
                self.geosolution.crs = data.crs
            self.centroid = self.geosolution.centroid
            
        else:
            self.geosolution = gpd.GeoDataFrame(geometry=gpd.GeoSeries(Polygon(unary_union(data.geometry).exterior.coords[:])))
            self.centroid = gpd.GeoDataFrame(geometry=gpd.GeoSeries(Polygon(unary_union(data.geometry).exterior.coords[:])).centroid)

class check_topology:
    
    def __init__(self, data):
        
        self.data = data
        pd.options.mode.chained_assignment = None
        warnings.filterwarnings("ignore")
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
                    mid = gpd.GeoDataFrame(geometry=gpd.GeoSeries(pol))
                    val_data = val_data.append(mid)
                else:
                    break
            else:
                val = gpd.GeoDataFrame(geometry=gpd.GeoSeries(row['geometry']))
                val_data = val_data.append(val)
        if val_data.crs == None:
            val_data.crs = {'init': 'epsg:4326'}
        self.geodesign = val_data