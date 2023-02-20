import os
import requests

from exif import Image
from typing import Dict, Any, Union

JSONDict = Dict[str, Any]


class ImageData:
    def __init__(self, imgpath: str) -> None:
        self._imgpath = os.path.abspath(imgpath)
        self.has_data = False

    def read_image(self) -> None:
        """Read image from file"""
        try:
            with open(self._imgpath, "rb") as rb_img:
                self.img_file = Image(rb_img)
                if self.img_file.has_exif:
                    self.has_data = True
        except Exception as e:
            print("Image file is invalid: {}".format(e))

    def dms_coordinates_to_dd_coordinates(self, geo_dir: str):
        # https://auth0.com/blog/read-edit-exif-metadata-in-photos-with-python/

        if geo_dir == "lat":
            coordinates = self.img_file.get("gps_latitude")
            coordinates_ref = self.img_file.get("gps_latitude_ref")
        else:
            coordinates = self.img_file.get("gps_longitude")
            coordinates_ref = self.img_file.get("gps_longitude_ref")

        decimal_degrees = coordinates[0] + coordinates[1] / 60 + coordinates[2] / 3600

        if coordinates_ref == "S" or coordinates_ref == "W":
            decimal_degrees = -decimal_degrees

        return decimal_degrees

    def get_geo(self) -> Union[JSONDict, None]:

        if not self.img_file.get("gps_latitude", None):
            return None

        lat_dd = self.dms_coordinates_to_dd_coordinates("lat")
        lon_dd = self.dms_coordinates_to_dd_coordinates("lon")

        query = {"lat": lat_dd, "lon": lon_dd, "format": "json"}
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse?", params=query
        )
        return response.json()

    def get_datetime(self) -> str:
        dt = self.img_file.datetime_original
        return dt

    def prepare(self) -> None:
        self.read_image()
        if self.has_data:
            t = self.get_datetime()
            print("Time:", t)
            g = self.get_geo()
            print("Geo:", g)
        else:
            print("No data")


if __name__ == "__main__":

    x_jpeg = "data/1_dix.jpeg"
    proc = ImageData(x_jpeg)
    print(proc.prepare())
