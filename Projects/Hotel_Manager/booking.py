# Jean-François Léon
 
import doctest
import random
import matplotlib
import os
import hotel
from hotel import Hotel
 
 
class Booking:
    def __init__(self, hotels):
        self.hotels = hotels
        
    @classmethod
    def load_system(self):
        hotels_folder = os.listdir("hotels")
        hotels_list = []
        for my_hotel in hotels_folder:
            a_hotel = Hotel.load_hotel(my_hotel)