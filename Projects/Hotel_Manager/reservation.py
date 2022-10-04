# Jean-françois Léon
 
 
import doctest
import random
import datetime
 
from room import Room, MONTHS, DAYS_PER_MONTH
 
class Reservation:
    booking_numbers = []
    
    def __init__(self, name, room_reserved, check_in, check_out, booking_number = None):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> print(my_reservation.check_in)
        2021-05-03
        >>> print(my_reservation.check_out)
        2021-05-10
        >>> my_reservation.booking_number
        1953400675629
        >>> r1.availability[(2021, 5)][9]
        False
        
        """
                
        if not room_reserved.is_available(check_in, check_out):
            raise AssertionError("The room you attempt to reserve is not available at the given dates")
        
        if booking_number == None:
            booking_number = random.randint(10**12, (10**13)-1)
        
        start_date = datetime.date(check_in.year, check_in.month, check_in.day)
        one_day = datetime.timedelta(days=1)
        
        while start_date <= check_out:
            room_reserved.availability[(start_date.year, start_date.month)][start_date.day] = False
            start_date += one_day
 
        self.booking_number = booking_number
        self.name = name
        self.room_reserved = room_reserved
        self.check_in = check_in
        self.check_out = check_out
        
    
    def __str__(self):
        '''
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> print(my_reservation)
        Booking number: 1953400675629
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
    
        '''
        Line_1 = 'Booking number: ' + str(self.booking_number) + '\n'
        Line_2 = 'Name: ' + self.name + '\n'
        Line_3 = 'Room reserved: ' + str(self.room_reserved) + '\n'
        Line_4 = 'Check-in date: ' + str(self.check_in) + '\n'
        Line_5 = 'Check-out date: ' + str(self.check_out)
        
        return Line_1 + Line_2 + Line_3 + Line_4 + Line_5
    
    def to_short_string(self):
        
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> my_reservation.to_short_string()
        '1953400675629--Mrs. Santos'
        
        """
        return str(self.booking_number) + '--' + self.name
    
    
    @classmethod
    def from_short_string(self, short_string, check_in, check_out, my_room):
        """
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 4)
        >>> my_reservation = Reservation.from_short_string('1953400675629--Mrs. Santos', date1, date2, r1)
        >>> print(my_reservation.check_in)
        2021-05-03
        >>> print(my_reservation.check_out)
        2021-05-04
        >>> my_reservation.booking_number
        1953400675629
        >>> r1.availability[(2021, 5)][3]
        False
        """
        Name = short_string[15:]
        Booking_num = int(short_string[:13])
        my_reservation = Reservation(Name, my_room, check_in, check_out, Booking_num)
        return my_reservation
    
    @staticmethod
    def get_reservations_from_row(my_room, tuples_list):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = [] # needs to be reset for the test below to pass
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(MONTHS, 2021)
        >>> rsv_strs = [(2021, 'May', 3, '1953400675629--Jack'), (2021, 'May', 4, '1953400675629--Jack')]
        >>> rsv_dict = Reservation.get_reservations_from_row(r1, rsv_strs)
        >>> print(rsv_dict[1953400675629])
        Booking number: 1953400675629
        Name: Jack
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-05
        
        """
        
        booking_nums = []
        dates = []
        names_list = []
        rerservation_dict = {}
        
        # We separate each elements of the tuples to have more flexibility in their use.
        for elem in tuples_list:
            # We create a date from the first 3 elements of each tuple
            date = datetime.date(elem[0], MONTHS.index(elem[1])+1, elem[2])
            dates.append(date)
            if elem[3] != '':
                booking_nums.append(int(elem[3][:13]))
                names_list.append(elem[3][15:])
        
        check_dates = {}
        # We're creating a dictionary check_dates
        # Each key will be a booking number and each value, a list of its corresponding reservations dates.
        index = 0
        for num in booking_nums:
            # This loop associates each list of dates to its corresponding booking number.
            if num in check_dates:
                check_dates[num] += [dates[index]]
            else:
                check_dates[num] = [dates[index]]
                
            index += 1
        
        # Let's remove the duplicates of the name list to avoid any IndexError or name mismatches.
        sorted_names_list =[]
        for name in names_list:
            if name not in sorted_names_list:
                sorted_names_list.append(name)
                
        index = 0
        # For each booking number, we create a reservation from the name of our list of names,
        # our given room, the min and max dates of our list of dates and that booking number.
        for num in check_dates:
            name = sorted_names_list[index]
            check_in = min(check_dates[num])
            check_out = max(check_dates[num]) + datetime.timedelta(days=1)
            rerservation_dict[num] = Reservation(name, my_room, check_in, check_out, num)
            index += 1
            
        return rerservation_dict