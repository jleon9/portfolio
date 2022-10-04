# Jean-François Léon

import doctest
import datetime
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
 
 
 
class Room:
    
    def __init__(self, room_type, room_num, price):
        TYPES_OF_ROOMS_AVAILABLE = ['twin', 'double', 'queen', 'king']
        
        if type(room_type) != str or type(room_num) != int or type(price) != float:
            raise AssertionError("Your input must follow the format: string, integer, float")
        
        if room_type.lower() not in TYPES_OF_ROOMS_AVAILABLE:
            raise AssertionError("Please enter one of the available room types we offer.")
        
        if room_num <= 0:
            raise AssertionError("Enter a positive number of rooms to reserve.")
        
        if price < 0:
            raise AssertionError("Enter a positive price")
        
        
        self.room_type = room_type
        self.room_num = room_num
        self.price = price
        self.availability = {}
       
    def __str__(self):
        """
        >>> my_room = Room('Double', 237, 99.99)
        >>> str(my_room)
        'Room 237,Double,99.99'
        
        """
        return 'Room ' + str(self.room_num) + ','+ self.room_type +','+ str(self.price)
    
    
    def set_up_room_availability(self, month_list, year):
        
        '''
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> len(r.availability)
        2
        >>> len(r.availability[(2021, 6)])
        31
        >>> r.availability[(2021, 5)][5]
        True
        >>> print(r.availability[(2021, 5)][0])
        None
        
        >>> r2 = Room("Twin", 102, 70.0)
        >>> r2.set_up_room_availability(['Feb', 'Mar'], 2016)
        >>> len(r2.availability[(2016, 2)])
        29
        '''
        COPY_DAYS_PER_MONTH = list(DAYS_PER_MONTH)
        if year % 4 == 0:
            if year % 100 != 0:
                COPY_DAYS_PER_MONTH[1] = 29
            
            elif year % 400 == 0:
                COPY_DAYS_PER_MONTH[1] = 29
                
        
        num_months_list = []
        nums_of_months = {}
        days_in_month = {}
        num = 1
        index = 0
        for month in MONTHS:
            num_months_list.append(num)
            nums_of_months[month] = num_months_list[index]
            days_in_month[month] = DAYS_PER_MONTH[index]
            index += 1
            num += 1
                
        
        start_date = nums_of_months[month_list[0]]
        end_date = nums_of_months[month_list[len(month_list)-1]]
        
        for month in MONTHS[start_date-1:end_date]:
            list_of_availabilities = [None]
            for i in range(0, days_in_month[month]):
                list_of_availabilities.append(True)
            
            self.availability[(year, nums_of_months[month])] = list_of_availabilities
            
    def reserve_room(self, date):
        '''
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 20)
        >>> r.reserve_room(date1)
        >>> r.availability[(2021, 6)][20]
        False
        '''
        if self.availability[(date.year, date.month)][date.day] == False:
            raise AssertionError("This room has already been reserved at this time.")
        
        str_month = MONTHS[date.month-1]
        self.set_up_room_availability([str_month], date.year)
        month_availabilities = self.availability
        month_availabilities[(date.year, date.month)][date.day] = False
        
    def make_available(self, date):
        '''
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 20)
        >>> r.make_available(date1)
        >>> r.availability[(2021, 6)][20]
        True
        >>> r.availability[(2021, 5)][3] = False
        >>> date2 = datetime.date(2021, 5, 3)
        >>> r.make_available(date2)
        >>> r.availability[(2021, 5)][3]
        True
        '''
        str_month = MONTHS[date.month]
        self.set_up_room_availability([str_month], date.year)
        month_availabilities = self.availability
        month_availabilities[(date.year, date.month)][date.day] = True
        
    def is_available(self, check_in, check_out):
        
        '''
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 5, 25)
        >>> date2 = datetime.date(2021, 6, 10)
        >>> r1.is_available(date1, date2)
        True
        >>> r1.availability[(2021, 5)][28] = False
        >>> r1.is_available(date1, date2)
        False
        '''
        time_difference = check_out - check_in
        if time_difference.days <= 0:
            raise AssertionError("Please enter a positive amount of days.")
        
        start_date = datetime.date(check_in.year, check_in.month, check_in.day)
        one_day = datetime.timedelta(days=1)
        
        list_of_availabilities = []
        list_of_availabilities.append(self.availability[(start_date.year, start_date.month)])
        while start_date <= check_out:
            if start_date.day == 1 and (start_date.month != check_in.month):
                if (start_date.year, start_date.month) in self.availability:
                    list_of_availabilities.append(self.availability[(start_date.year, start_date.month)])
                else:
                    new_month = self.set_up_room_availability([MONTHS[start_date.month]], start_date.year)
                    self.availability[(start_date.year, start_date.month)] = new_month     
            start_date += one_day
            
        availabilities_by_days = []
        for elem in list_of_availabilities:
            for boolean in elem:
                if boolean != None:
                    availabilities_by_days.append(boolean)
        availabilities_by_days = [None] + availabilities_by_days
        
        num_of_days = (check_out - check_in).days
        check_out_index = DAYS_PER_MONTH[check_in.month - 1] + num_of_days
        our_date_range = availabilities_by_days[check_in.day:check_out_index + 1]
        return False not in our_date_range
    
    @staticmethod
    
    def find_available_room(list_of_rooms, room_type, date1, date2):
        """
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> r2.set_up_room_availability(['May'], 2021)
        >>> r3.set_up_room_availability(['May'], 2021)
        >>> r1.availability[(2021, 5)][8] = False
        >>> r = [r1, r2, r3]
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
        >>> my_room == r3
        True
        >>> r3.availability[(2021, 5)][3] = False
        >>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
        >>> print(my_room)
        None
        
        >>> r = Room("King", 110, 120.0)
        >>> r.set_up_room_availability(['Dec'], 2021)
        >>> r.set_up_room_availability(['Jan'], 2022)
        >>> date1 = datetime.date(2021, 12, 20)
        >>> date2 = datetime.date(2022, 1, 8)
        >>> my_room = Room.find_available_room([r], 'Queen', date1, date2)
        >>> print(my_room)
        None
        >>> my_room = Room.find_available_room([r], 'King', date1, date2)
        >>> my_room == r
        True
        """
        
        time_diff = date2 - date1
        if time_diff.days <= 0:
            raise AssertionError("Please enter a positive amount of days")
        
        for room in list_of_rooms:
            if room.is_available(date1, date2) and room.room_type == room_type:
                return room
        
        return None