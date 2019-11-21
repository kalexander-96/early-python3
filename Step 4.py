import json
import datetime
import os
import pickle
import sys # importing modules to be used throughout the code


class Batch:#creating the blueprints for the batch class
    def __init__(self, batch_number, num_of_components, date_of_creation,
                 component_type, size_or_model, location, status):
        self.batch_number = batch_number
        self.num_of_components = num_of_components
        self.date_of_creation = date_of_creation
        self.type = component_type
        self.size_or_model = size_or_model
        self.components = []
        self.location = location
        self.status = status

    def display_batch(self):#creating a method within the batch class that allows it to print itself
        print('Batch Number: ', self.batch_number)
        print('Date of creation: ', self.date_of_creation)
        print('Component type: ', self.type)
        print('Size/model of component(s): ', self.size_or_model)
        print('Number of components: ', self.num_of_components)
        print('Location: ', self.location)
        print('Status: ', self.status)


class Component:#creating the blueprint for the component class
    def __init__(self, serial_number, batch_number, component_type, size_or_model, status, finish):
        self.serial_number = serial_number
        self.serial_numbers = []
        self.batch_number = batch_number
        self.component_type = component_type
        self.size_or_model = size_or_model
        self.status = status
        self.finish = finish

    def display_component(self):#method allows the component to pront the details of all other components contained within the same batch
        print('Serial number(s): ', self.serial_numbers)

    def display_full_component_details(self):#component prints details of itself
        print('')
        print('Serial number: ', self.serial_number)
        print('Batch Number: ', self.batch_number)
        print('Component Type: ', self.component_type)
        print('Size or Model: ', self.size_or_model)
        print('Status: ', self.status)
        print('Finish: ', self.finish)


def create_batch_file(batch_id):  # creating the function used to create a batch file reads in variable called batch_id
    filename = str(batch_id.batch_number) + '.pck'  # creates file name to look for based on batch_id read in above
    f1 = open(filename, 'wb')  # opens file with same name as pythcreated above, creates new file if one doesn't exist
    pickle.dump(batch_id, f1)  # dumps the data into the file
    f1.close()  # closes file


def view_batch_file(batch_id):  # creating function used to view batch files
    filename = batch_id + '.pck'  # creates file name to look for based on batch_id read in above
    if os.path.exists(filename):  # if the file exists it will load the contents and return them
        f2 = open(filename, 'rb')
        file_contents = pickle.load(f2)
        f2.close()
        return file_contents
    else:
        return 0  # if they do not exist it will return zero


def view_full_batch():# this function will load and return the full batch list
    if os.path.exists("BatchIndex.json"):# if the file exists it will load the contents and return them
        f5 = open('BatchIndex.json', 'rb')
        indata = json.load(f5)
        file_contents = indata.get('batch_list')
        f5.close()
        return file_contents
    else:
        return 0  # if they do not exist it will return zero


def create_component_file(component_id):  # this function creates a component file
    filename = str(component_id.serial_number) + '.pck'  #works in the same way as the above create_batch_file
    f3 = open(filename, 'wb')
    pickle.dump(component_id, f3)
    f3.close()


def view_component_file(component_id):  # function allowas user to view a component file
    filename = component_id + '.pck'  # this function works same way as its view batch counterpart
    if os.path.exists(filename):
        f4 = open(filename, 'rb')
        file_contents = pickle.load(f4)
        f4.close()
        return file_contents
    else:
        return 0


def allocate_new_location():  # this function allows the user to allocate a location to batches
    batch_number = str(input('Please enter Batch Number you would like to transfer: '))  # takes in batch number
    batch_transfer = view_batch_file(batch_number)  # calls function to get batch details
    if batch_transfer.location == 'Factory Floor - Warehouse Not Allocated':  # if the batch hasn't been allocated
        print('1: Paisley \n2: Dubai')  # display two options
        new_location = str(input('Please select new location from numbered options above: '))  # user chooses from above
        if new_location == '1':
            batch_transfer.location = 'Paisley Factory'  # if the user chose 1 the location is paisley
        elif new_location == '2':
            batch_transfer.location = 'Dubai Factory'  # if the user chose 2 the location is dubai
        print('Batch transferred to', batch_transfer.location)  # displays where the batch is now located
    else:
        print('Batch already allocated location.')  # if the batch is already allocated display message
    create_batch_file(batch_transfer)  # calls function to overwrite the previous batch details


def allocate_finish_type(component_number):   # this function allows the user to allocate a finish to components
    component = view_component_file(component_number)  # calls function to get component details
    if component.finish == 'None':  # if the finish hasn't been set
        print('1: Polished Metal Finish \n2: Custom Painted Finish')  # display options
        new_finish = str(input('Please select new finish from numbered options above: '))  # user inputs
        if new_finish == '1':  # if the user chooses 1 then apply polished finish
            component.finish = 'Polished Metal Finish'
            component.status = 'Manufactured - Finished'
        elif new_finish == '2':  # if the user chooses 2 then user is prompted to enter their company name
            company_livery = str(input('Please enter Company Name: '))
            component.finish = 'Custom Painted Finish - ' + company_livery  # finish is custom with company name
            component.status = 'Manufactured - Finished'
        print('Finish Applied: ', component.finish)
    else:
        print('Component already finished with:', component.finish)  # component already finished message is displayed
    create_component_file(component)  # calls function to create the component file


def search_product():  # this function allows user to search for specific component
    component_list = []  # creates a list for later use
    print("Component type: Please Choose From numbers; \n1 - Winglet Attachment Strut"
          "\n2 - Door Seal Clamp Handle \n3 - Rudder Pivot Fins")  # Display options for user to choose from
    type_selection = int(input("Please enter the component type you would like to find: "))
    if type_selection == 1:
        component_type = 'Winglet Strut'
    elif type_selection == 2:
        component_type = 'Door Seal Clamp Handle'
    elif type_selection == 3:
        component_type = 'Rudder Pivot Fins'
    print("Size or Model selection: Please Choose From numbers; \n1 - 10mm diameter x 75mm length "
          "\n2 - 12mm diameter x 100mm length"
          " \n3 - 16mm diameter x 150mm length")  # Display options for user to choose from
    size_or_model_selection = int(input("Please enter the size or model: "))
    if size_or_model_selection == 1:
        size_or_model = '10mm diameter x 75mm length'
    elif size_or_model_selection == 2:
        size_or_model = '12mm diameter x 100mm length'
    elif size_or_model_selection == 3:
        size_or_model = '16mm diameter x 150mm length'
    print("Finish selection: Choose from numbers; \n1 - Polished Metal \n2 -Unfinished")
    print("Custom finishes are only available by special order.") # Display options for user to choose from
    finish = input("Please enter a finish type: ")
    if finish == '1':
        component_finish = 'Polished Metal Finish'
    elif finish == '2':
        component_finish = 'None'
    for filename in os.listdir(os.getcwd()):  # begins a loop which is executed on every file in current directory
        if len(filename) == 19 and filename.endswith('.pck'):  # this line ensures only component files are opened
            f = open(filename, 'rb')
            component = pickle.load(f)
            f.close()  # this block opens the component files
            if component.component_type == component_type and component.size_or_model == size_or_model\
                    and component.finish == component_finish:  # if component meets all criteria set by user
                component_list.append(component.serial_number)  # adds relevant serial numbers to established list
            else:
                pass  # if it doesn't meet criteria passes to next file
    if len(component_list) == 0:  # if the lenght of the component list is zero
        print("ITEM NOT IN STOCK")  # display error message if above criteria
        pass
    else:
        print("Quantity Available: ", len(component_list), "\n"
              "Serial Numbers: ", component_list)  # display the quantity available and serial numbers list
        choice = input("Would you like to fetch the details of these Components? Y/N: ")  # get details for user if Y
        if choice == 'Y' or choice == 'y':
            for components in component_list:
                comp = view_component_file(components)  # calls function to view component file
                comp.display_full_component_details()  # calls method of class to display full details of itself
        else:
            pass


def return_to_menu():  # this function gives the user the option to return to the main menu
    menu = str(input("Return to Menu? 'Y' or 'N' "))  # user input Y or N
    if menu == 'Y':
        main() # run function main which takes user back to menu
    else:
        print('Goodbye')  # exit message
        sys.exit()  # exit system


def create_batch():
    manufacture_date = (datetime.date.today().strftime('%d%m%y'))  # gets manufacture date which is todays date
    batch_number_date = str(manufacture_date)  # converts above to string
    f6 = open("BatchIndex.json", "r")
    indata = json.load(f6)
    f6.close()  # this block opens and loads the data on the batch index file
    batch_list = indata.get("batch_list")  # get the full batch list
    if len(batch_list) == 0: # if the batch list is empty
        new_batchnum = (batch_number_date + str(1).zfill(4))   # create standard batch number date + number
    else:
        last_batchnum = batch_list[-1]  # fetches the last used batch number
        if last_batchnum[0:6] == batch_number_date:  # if the first section of that number is batch_number_date
            entry_number = int((last_batchnum[6:10])) + 1  # add one to last section of last batch number
            new_batchnum = (batch_number_date + str(entry_number).zfill(4))  # create new batch number
        else:
            new_batchnum = (batch_number_date + str(1).zfill(4))  # creates standard batch number if not todays date
    batch_list.append(new_batchnum)  # appends new number to batch list
    correct = 'N'  # set parameter to N for while loop
    while correct == 'N':
        num_of_components = input("Please enter the number of Components: ")  # enter number of components
        date_of_creation = datetime.date.today()  # sets date of creation to todays date
        location = 'Factory Floor - Warehouse Not Allocated'  # sets location to factory floor as default
        status = 'Manufactured - Unfinished'  # sets status as unfinished
        finish = 'None'  # finish type is set as none
        print("Component type: Please Choose From numbers; \n1 - Winglet Attachment Strut "
              "\n2 - Door Seal Clamp Handle \n3 - Rudder Pivot Fins")
        type_selection = int(input("Please enter the component type: "))  # user input
        if type_selection == 1:
            component_type = 'Winglet Strut'
        elif type_selection == 2:
            component_type = 'Door Seal Clamp Handle'
        elif type_selection == 3:
            component_type = 'Rudder Pivot Fins'
        outdata1 = {'batch_list': batch_list}  # export batch list to dictionary
        f7 = open("BatchIndex.json", "w")
        json.dump(outdata1, f7)
        f7.close()  # block writes in data to batch index fiile
        print("Size or Model selection: Please Choose From numbers; \n1 - 10mm diameter x 75mm length "
              "\n2 - 12mm diameter x 100mm length \n3 - 16mm diameter x 150mm length")
        size_or_model_selection = int(input("Please enter the size or model: "))
        if size_or_model_selection == 1:
            size_or_model = '10mm diameter x 75mm length'
        elif size_or_model_selection == 2:
            size_or_model = '12mm diameter x 100mm length'
        elif size_or_model_selection == 3:
            size_or_model = '16mm diameter x 150mm length'
        print('This batch contains', str(num_of_components), str(component_type) + 's. Is this correct?')
        #  summary of what batch contains
        correct = str(input("Please answer 'Y' or 'N': "))  # user prompted to confirm
    print("")
    new_batch = Batch(new_batchnum, num_of_components, date_of_creation,
                      component_type, size_or_model, location, status)
    # create new instance of batch class
    create_batch_file(new_batch)  # calls function to create batch file
    serial_numbers = []  # creates list for use later
    for n in range(int(num_of_components)):  # loops and creates classes for each component class
        serial_number = str(new_batchnum) + "-" + str(n).zfill(4)  # creates unique component serial number
        serial_numbers.append(serial_number)  # appends to serial numbers list
        current_comp = Component(serial_number, new_batchnum, component_type, size_or_model, status, finish)
        # create new instance of component class
        current_comp.serial_numbers = serial_numbers  # adds serial numbers list to component class
        new_batch.components.append(current_comp)  # appends current component to batch class list
        create_component_file(current_comp)  # calls function to create new component file
    display = input("Would you like to print the batch details? Y/N: ")  # ask user if they want to display details
    if display == 'Y':
        new_batch.display_batch()
        current_comp.display_component() # if yeas display details
    elif display == 'N':
        pass  # pass to next executable code


def main():
    print('WELCOME TO YOUR INVENTORY SYSTEM')
    done = ""
    while done != "8":
        print('\n1: CREATE A NEW BATCH \n2: VIEW FULL BATCH LIST \n'
              '3: VIEW BATCH DETAILS \n4: VIEW COMPONENT DETAILS \n'
              '5: TRANSFER BATCH \n6: APPLY FINISH TO COMPONENT \n7: SEARCH FOR COMPONENT \n8: QUIT\n')
        done = str(input("Please select a numbered option from above: "))
        # main menu from here user chooses, and depending on choice a specific function is launched
        if done == '1': # if choice is 1 then user creates a batch
            create_batch()
            return_to_menu()
        elif done == '2': # user can view the full batch list
            full_batch_list = view_full_batch()
            print(full_batch_list)
            return_to_menu()
        elif done == '3':  # user can launch process to view a batch file
            batch_number = str(input("Which Batch would you like to call: "))
            this_batch = view_batch_file(batch_number)
            if this_batch == 0:
                print('ERROR - File missing or Corrupt')
            else:
                this_batch.display_batch()
            return_to_menu()
        elif done == '4':  # user can launch process to view specific component file
            current_component = str(input("Which Component would you like to call: "))
            this_component = view_component_file(current_component)
            if this_component == 0:
                print('ERROR - File missing or Corrupt')
            else:
                this_component.display_full_component_details()
            return_to_menu()
        elif done == '5':  # user can allocate a new location to a batch file from here
            allocate_new_location()
            return_to_menu()
        elif done == '6':  # user can allocate a finish type to a component file from here
            component_number = str(input('Please enter Component Number you would like to apply a finish to: '))
            allocate_finish_type(component_number)
            return_to_menu()
        elif done == '7':  # user can search by product type they want from here
            search_product()
            return_to_menu()
        elif done == '8':  # choosing this option exits the program
            print('Goodbye')
            sys.exit()


if __name__ == '__main__':
    id_list = []  # set initial id list for later use
    out_data = {'batch_list': id_list}  # create dictionary containing data to be exported
    if not os.path.exists("BatchIndex.json"):  # if json file doesn't exist then this creates it
        f = open("BatchIndex.json", 'w')  # opens new json file
        json.dump(out_data, f)  # dump data for later use
        f.close()  # close file
    main()  # execute main function, this function is where all other functions branch from user input
