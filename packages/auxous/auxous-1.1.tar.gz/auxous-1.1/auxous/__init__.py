class Auxous:
    def __init__(self):
        print("Welcome To Akash")
    
    def day_name(self, number=None):
        if number == None:
            return None
        days = {1:"monday", 2:"tuesday", 3:"wednessday", 4:"thursday", 5:"friday", 6:"aturday", 7:"sunday"}
        try:    
            print(days[number])
        except KeyError:
            print("Invalid Day Number")

    def month_name(self, number=None):
        if number == None:
            return None
        months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
        try:    
            print(months[number])
        except KeyError:
            print("Invalid Month Number")

    def run(self):
        print("Enter Your Choice\nFind Day Name [1]\nFind Month Name [2]")
        choice = int(input("Enter Choice: "))

        if choice == 1:
            day_num = int(input("Enter Day Number: "))
            self.day_name(day_num)
        elif choice == 2:
            month_num = int(input("Enter Month Name: "))
            self.month_name(month_num) 
        else:
            print("You Entered Wrong Number")     
