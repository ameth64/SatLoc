import numpy as np
import rasterio
from rasterio.transform import from_bounds
from pyproj import Proj, Transformer
from PIL import Image
import cv2
import torch
from torchvision import transforms as T

# The following helper methods demonstrate how to recover accurate geographic coordinates
# from matched satellite tiles and their indices recorded in CSV files.

def compute_transform_matrix(image_path):
    """
    Compute the affine transforms that convert local pixel coordinates (top-left and bottom-right,
    see the CSV Loc1*/Loc2* fields) from a satellite GeoTIFF into geographic (lon/lat) and UTM
    coordinates.
    
    Args:
        image_path (str): path to the GeoTIFF image.
    
    Returns:
        dict: dictionary with
            - "pixel_to_lonlat" (np.ndarray): 3x3 affine matrix (pixels → lon/lat)
            - "pixel_to_utm" (np.ndarray): 3x3 affine matrix (pixels → UTM)
            - "utm_to_pixel" (np.ndarray): inverse transform (UTM → pixels)
            - "utm_proj" (Proj): configured UTM projection for the image
    """
    with rasterio.open(image_path) as dataset:
        # Image width and height
        W, H = dataset.width, dataset.height
        
        # GeoTIFF bounds (top-left and bottom-right lon/lat)
        lon_min, lat_max = dataset.bounds.left, dataset.bounds.top   # top-left
        lon_max, lat_min = dataset.bounds.right, dataset.bounds.bottom  # bottom-right
        
        # Affine transform from pixels to lon/lat
        pixel_to_lonlat = from_bounds(lon_min, lat_min, lon_max, lat_max, W, H)
        
        # Configure the UTM projection (auto-detect zone and hemisphere via image center)
        wgs84 = Proj("epsg:4326")  # WGS84 lon/lat

        lon_center = (lon_min + lon_max) / 2
        lat_center = (lat_min + lat_max) / 2
        zone = int((lon_center + 180) / 6) + 1
        zone = max(1, min(zone, 60))  # UTM zones are numbered 1–60
        is_southern = lat_center < 0

        utm_proj = Proj(
            proj="utm",
            zone=zone,
            south=is_southern,
            ellps="WGS84",
            datum="WGS84"
        )

        # Converter between lon/lat and UTM
        transformer = Transformer.from_proj(wgs84, utm_proj, always_xy=True)
        
        # Convert bounding lon/lat into the UTM projection
        x_min, y_max = transformer.transform(lon_min, lat_max)
        x_max, y_min = transformer.transform(lon_max, lat_min)

        # Derive the affine transform parameters in the UTM domain
        a_utm = (x_max - x_min) / W
        b_utm = 0
        c_utm = x_min

        d_utm = 0
        e_utm = (y_min - y_max) / H  # compensate for flipped image y-axis
        f_utm = y_max  # anchor UTM Y so northings increase upwards

        # Assemble the pixel → UTM affine matrix
        pixel_to_utm = np.array([
            [a_utm, b_utm, c_utm],
            [d_utm, e_utm, f_utm],
            [0, 0, 1]
        ])

        # Pre-compute the inverse transform (UTM → pixels)
        utm_to_pixel = np.linalg.inv(pixel_to_utm)

        return {
            "pixel_to_lonlat": pixel_to_lonlat,
            "pixel_to_utm": pixel_to_utm,
            "utm_to_pixel": utm_to_pixel,
            "utm_proj": utm_proj
        }


def cal_real_geo(lon1,lat1,lon2,lat2,transform_matrices,sat_image):
    """
    Convert the two local pixel corners (provided by the CSV entry of the matched tile)
    into accurate geographic coordinates using the transforms from compute_transform_matrix.
    
    Args:
        lon1, lat1: local pixel coordinates of the tile's top-left corner (CSV Loc1*)
        lon2, lat2: local pixel coordinates of the tile's bottom-right corner (CSV Loc2*)
        transform_matrices: dictionary of affine transforms returned by compute_transform_matrix
        sat_image: satellite tile image (used for shape)
    
    Returns:
        [lon1, lat1, lon2, lat2]: corrected lon/lat bounds
    """
    location2_LU = [lat1,lon1]
    location2_RD = [lat2,lon2]

    X1 = (0/sat_image.shape[0])*(location2_RD[0]-location2_LU[0])+location2_LU[0]
    Y1 = (0/sat_image.shape[1])*(location2_RD[1]-location2_LU[1])+location2_LU[1]
    X2 = (1)*(location2_RD[0]-location2_LU[0])+location2_LU[0]
    Y2 = (1)*(location2_RD[1]-location2_LU[1])+location2_LU[1]

    lon1, lat1 = rasterio.transform.xy(transform_matrices["pixel_to_lonlat"], X1, Y1, offset='center')
    lon2, lat2 = rasterio.transform.xy(transform_matrices["pixel_to_lonlat"], X2, Y2, offset='center')

    return [lon1, lat1,lon2, lat2] 