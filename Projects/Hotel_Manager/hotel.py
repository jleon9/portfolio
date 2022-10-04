# Jean-François Léon
 
import doctest
import random
import datetime
from room import Room, MONTHS, DAYS_PER_MONTH
from reservation import Reservation
import copy
import os
 
class Hotel:
    
    def __init__(self, name, rooms = [], reservations = {}):
        
        self.name = name
        self.rooms = copy.deepcopy(rooms)
        self.reservations = copy.deepcopy(reservations)
        
    def make_reservation(self, name, room_type, check_in, check_out):
        
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        1953400675629
        >>> print(h.reservations[1953400675629])
        Booking number: 1953400675629
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        
        """
        for room in self.rooms:
            if room.room_type.lower() == room_type.lower() and room.is_available(check_in, check_out):    
                my_reservation = Reservation(name, room, check_in, check_out)
                self.reservations[my_reservation.booking_number] = my_reservation
                return my_reservation.booking_number
        
        raise AssertionError("No room of the given type are available at these dates.")
    
    def get_receipt(self, booking_numbers):
        
        """
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r2.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r3.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> h.get_receipt([num1])
        560.0
        
        >>> date3 = datetime.date(2021, 6, 5)
        >>> num2 = h.make_reservation("Mrs. Santos", "Twin", date1, date3)
        >>> h.get_receipt([num1, num2])
        2375.0
        >>> h.get_receipt([123])
        0.0
        """
            
        reservations_prices = []
        for booking_num in booking_numbers:
            # We avoid the KeyError with this statement
            if booking_num not in self.reservations:
                price_a_night = 0.0
                
            # Otherwise, the key is in our reservation dictionary so we perform the desired operations
            else:
                price_a_night = self.reservations[booking_num].room_reserved.price
                rsv_check_in = self.reservations[booking_num].check_in
                rsv_check_out = self.reservations[booking_num].check_out
                stay = (rsv_check_out - rsv_check_in).days
                reservations_prices.append(price_a_night*stay)
        
        return float(sum(reservations_prices))
    
    def get_reservation_for_booking_number(self, booking_num):
        """
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> rsv = h.get_reservation_for_booking_number(num1)
        >>> print(rsv)
        Booking number: 4191471513010
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 6, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> rsv = h.get_reservation_for_booking_number(num1)       
        >>> print(rsv)
        Booking number: 4191471513010
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-06-10
        
        """
        
        if booking_num in self.reservations:
            return self.reservations[booking_num]
        
        return None
    
    def cancel_reservation(self, booking_num):
        """
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> h.rooms[0].availability[(2021, 5)][4]
        False
        >>> h.cancel_reservation(num1)
        >>> num1 in h.reservations
        False
        >>> h.rooms[0].availability[(2021, 5)][4]
        True
        
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> h.cancel_reservation(num1)
        >>> num1 in h.reservations
        False
        >>> r1.availability[(2021, 5)][4]
        True
        """
        
        if booking_num in self.reservations:
            cancel_room = self.reservations[booking_num].room_reserved
            check_in = self.reservations[booking_num].check_in
            check_out = self.reservations[booking_num].check_out
            start_date = copy.copy(check_in)
            one_day = datetime.timedelta(days=1)
 
            while start_date <= check_out:
                cancel_room.make_available(start_date)
                start_date += one_day
            
            self.reservations.pop(booking_num)
        
        return
        
    def get_available_room_types(self):
        """
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r2.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r3.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
        >>> types = h.get_available_room_types()
        >>> types.sort()
        >>> types
        ['Queen', 'Twin']
        
        """
        
        room_types = []
        for room in self.rooms:
            if room.room_type not in room_types:
                room_types.append(room.room_type)
        
        return room_types
    
    @staticmethod
    def load_hotel_info_file(file_path):
        """
        >>> hotel_name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
        >>> hotel_name
        'Overlook Hotel'
        >>> print(len(rooms))
        500
        >>> print(rooms[236])
        Room 237,Twin,99.99
        """
        
        fobj = open(file_path, 'r')
        file_content = fobj.read()
        list_of_info = file_content.split('\n')
        hotel_name = list_of_info[0]
        list_of_rooms_str = list_of_info[1:-1]
        list_of_rooms = []
        for room in list_of_rooms_str:
            room_info_list = room.split(',')
            room = Room(room_info_list[1], int(room_info_list[0][5:]), float(room_info_list[2]))
            list_of_rooms.append(room)
        fobj.close()
        
        return (hotel_name, list_of_rooms)
    
    def save_hotel_info_file(self):
        """
        >>> r1 = Room("Double", 101, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> h.save_hotel_info_file()
        >>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
        >>> fobj.read()
        'Queen Elizabeth Hotel\\nRoom 101,Double,99.99\\n'
        >>> fobj.close()
        """
        lower_filename = self.name.lower()
        filename = lower_filename.replace(' ', '_')
        fobj = open('hotels/'+ str(filename) + '/hotel_info.txt', 'w', encoding='utf-8')
        fobj.write(self.name + '\n')
        
        for i in range(0, len(self.rooms)):
            fobj.write(str(self.rooms[i])+'\n')
            
        fobj.close()
    
    
    @staticmethod
    def load_reservation_strings_for_month(hotel_folder, month, year):
        
        '''
        >>> name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
        >>> h = Hotel(name, rooms, {})
        >>> rsvs = h.load_reservation_strings_for_month('overlook_hotel', 'Oct', 1975)
        >>> print(rsvs[237][28:32])
        [(1975, 'Oct', 29, ''), (1975, 'Oct', 30, '9998701091820--Jack'), (1975, 'Oct', 31, '9998701091820--Jack')]
        
        '''
        
        filename = str(year)+'_'+month
        fobj = open('hotels/'+str(hotel_folder) +'/'+filename+'.csv', 'r', encoding='utf-8')
        file_content = fobj.read()
        hotel_info = Hotel.load_hotel_info_file('hotels/' + hotel_folder + '/hotel_info.txt')
        hotel_name = hotel_info[0]
        hotel_rooms = hotel_info[1]
        
        for room in hotel_rooms:
            room.set_up_room_availability([month], year)
        
        room_info = file_content.split('\n')
        room_monthly_info = []
        for elem in room_info:
            room_monthly_info.append(elem.split(','))
        
        room_rsv_list = []
        days_in_month = DAYS_PER_MONTH[MONTHS.index(month)]
        
        for elem in room_info[:days_in_month]:
            room_rsv_list.append(elem)
 
        room_nums = []
        for room in hotel_rooms:
            room_nums.append(room.room_num)
            
        day = 1
        reservations_in_month = []
        for string in room_info:
            rsv_in_month = string.split(',')
            reservations_in_month.append(rsv_in_month)
        
        months_list = []
        days_list = []
        for month_rsv in reservations_in_month:
            index = 1
            day = 1
            months_list.append(days_list)
            days_list = []
            for day_rsv in month_rsv[1:]:
                days_list.append((year, month, day, month_rsv[index]))
                day += 1
                index += 1
 
        months_list = months_list[1:]
        rsv_dict = {}
        index = 0
        for room_num in room_nums:
            rsv_dict[room_num] = months_list[index]
            index += 1
        
        fobj.close()
        return rsv_dict
        
    def save_reservations_for_month(self, month, year):
        
        """
        Takes as input a string corresponding to a month (from the MONTHS list) and a year (integer).
        The function should create a new CSV file named after the given month and inside a
        folder named after the hotel (all in lowercase, with spaces replaced by underscores),
        with that folder being in a folder called hotels. The CSV file
        should contain one row per room. The first column of each row will be the room number. There
        will be as many subsequent columns for days in the given month. In every row, after the room
        number, will be the reservation string as given by the Reservation to_short_string method, if a
        reservation occurs in that room on the given day. Or, if no reservation occurs in that room on that
        day, then the column should contain an empty string.
        
        >>> random.seed(987)
        >>> r1 = Room("Double", 237, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> Reservation.booking_numbers = []
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> date1 = datetime.date(2021, 10, 30)
        >>> date2 = datetime.date(2021, 12, 23)
        >>> num = h.make_reservation("Jack", "Double", date1, date2)
        >>> h.save_reservations_for_month('Oct', 2021)
        >>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
        >>> fobj.read()
        '237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
        >>> fobj.close()
 
        """
        fobj = open('hotels/'+self.name.lower().replace(' ', '_')+'/'+str(year)+'_'+month+'.csv', 'w', encoding='utf-8')
        
        days_in_month = DAYS_PER_MONTH[MONTHS.index(month)]
        int_month = MONTHS.index(month)+1
        month_reservation = {}
        for room in self.rooms:
            fobj.write(str(room.room_num))
            for booking_num in self.reservations:
                month_avail = copy.copy(room.availability[year, int_month])
                rsv_short_str = self.reservations[booking_num].to_short_string()
            
            for boolean in month_avail[1:]:
                fobj.write(',')
                if boolean == True:
                    fobj.write('')
                else:
                    fobj.write(rsv_short_str)
            fobj.write('\n')
        fobj.close()
    
    
    def save_hotel(self):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Double", 237, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> date1 = datetime.date(2021, 10, 30)
        >>> date2 = datetime.date(2021, 12, 23)
        >>> h.make_reservation("Jack", "Double", date1, date2)
        1953400675629
        >>> h.save_hotel()
        >>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
        >>> fobj.read()
        'Queen Elizabeth Hotel\\nRoom 237,Double,99.99\\n'
        >>> fobj.close()
        >>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
        >>> fobj.read()
        '237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
        >>> fobj.close()
        """
        
        path_str = "hotels/" + str(self.name.lower().replace(' ', '_'))
        
        if os.path.exists(path_str):
            fobj = open(path_str + '/hotel_info.txt', 'w', encoding='utf-8')
            
        else:
            os.makedirs(path_str) 
            fobj = open(path_str+'/hotel.info.txt', 'w', encoding='utf-8')
        
        fobj.write(self.name+'\n')
        for room in self.rooms:
            fobj.write(str(room)+'\n')
        
        self.save_reservations_for_month
 
        fobj.close()
    
    @classmethod    
    def load_hotel(self, folder):
        
        """
        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> hotel = Hotel.load_hotel('overlook_hotel')
        >>> hotel.name
        'Overlook Hotel'
        >>> str(hotel.rooms[236])
        'Room 237,Twin,99.99'
        >>> print(hotel.reservations[9998701091820])
        Booking number: 9998701091820
        Name: Jack
        Room reserved: Room 237,Twin,99.99
        Check-in date: 1975-10-30
        Check-out date: 1975-12-24
        
        """
        path = "hotels/"+folder
        fobj = open(path+"/"+os.listdir(path)[-1], 'r', encoding='utf-8')
        file_content = fobj.read()
        hotel_info = file_content.split('\n')
        hotel_name = hotel_info[0]
        year = int(os.listdir(path)[0][:-8])
        
        rsv_for_year = []
        list_of_rsv = []
        
        for file in os.listdir(path)[:-1]:
            fobj = open(path+'/'+file, 'r', encoding='utf-8')
            file_content = fobj.read()
            hotel_info = Hotel.load_hotel_info_file("hotels/"+folder+"/hotel_info.txt")
            fobj.close()
            
        for month in range(0, 12):
            month_rsv = Hotel.load_reservation_strings_for_month(folder, MONTHS[month-1], year)
            rsv_for_year.append(month_rsv)
        
        list_of_rooms = hotel_info[1]
        
        list_of_rsv = []
        for room in list_of_rooms:
            room.set_up_room_availability(['Jan', 'Dec'], year)
        
        Hotel_reservations = {}
        for month in rsv_for_year:
            for room_num in month:
                for day in month[room_num]:
                    if day[3] != '':
                        rsv_month = MONTHS.index(day[1])
                        a_rsv = Reservation.get_reservations_from_row(list_of_rooms[room_num-1], rsv_for_year[rsv_month][room_num])
                        Hotel_reservations.update(a_rsv)
                    break
        
        my_hotel = Hotel(hotel_name, list_of_rooms, Hotel_reservations)
        return my_hotel
 