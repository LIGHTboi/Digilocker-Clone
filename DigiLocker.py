import tkinter as tk
from tkinter import ttk, filedialog
from tkPDFViewer import tkPDFViewer
import pickle
import os
import shutil
from PIL import ImageTk, Image
import mysql.connector as conn


# current_user_adhaar = 405924156291
LoggedIn = False
Closed = False

#Add your image directory
_emblem = 'D:\\CODING\Python Files\comp project\emblem.png'
_userImage = 'D:\\CODING\Python Files\comp project\%s.png'
_logo = 'D:\\CODING\Python Files\comp project\logo.png'
_qrCode = 'D:\\CODING\Python Files\comp project\QRcode.png'
_icon = "D:\\CODING\Python Files\comp project\icon.png"

# Connecting to the MySQL server
db = conn.connect(host = 'localhost', user = 'root', password = 'minimilitia1')
cur = db.cursor()

# Creating Database
cur.execute('create database if not exists digilocker')

cur.execute('use digilocker')

# Creating Table
cur.execute("create table if not exists login_details(\
    first_name varchar(1000),\
    last_name varchar(1000),\
    email varchar(1000),\
    gender char(1),\
    mobile_number bigint not null,\
    adhaar_number bigint primary key,\
    password varchar(1000),\
    dob date)")

db.commit()

# Function for Error Message pop-up
def error(error_message, parent):

    error_window = tk.Toplevel(parent)
    error_window.geometry('+550+325')
    error_window.grab_set()

    error_label = tk.Label(error_window, text = error_message, font = 'arial 20 bold').pack(padx=10,pady=10)

    def cmd():
        parent.grab_set()
        error_window.destroy()

    okay_button = tk.Button(error_window, 
    text = 'OK', 
    font = 'arial 15 bold', 
    borderwidth=5, 
    command=cmd)
    okay_button.pack(padx = 10, pady = 10)

    error_window.resizable(False, False)
    error_window.protocol("WM_DELETE_WINDOW", cmd)

# User Screen
def create_user_screen(CurrentUser):
    
    # Making folder to store User Uploaded Files
    if not os.path.exists(f"C:/ProgramData/MySQL/MySQL Server 8.0/Data/digilocker/users/{CurrentUser}"):
        os.makedirs(f"C:/ProgramData/MySQL/MySQL Server 8.0/Data/digilocker/users/{CurrentUser}")
    
    try:
        user_files_paths = open(f"C:/ProgramData/MySQL/MySQL Server 8.0/Data/digilocker/users/{CurrentUser}/file_paths.dat", 'rb')
        pickle.load(user_files_paths)
    except:
        user_files_paths = open(f"C:/ProgramData/MySQL/MySQL Server 8.0/Data/digilocker/users/{CurrentUser}/file_paths.dat", 'wb')
        pickle.dump({}, user_files_paths)

    user_files_paths.close()

    # Function to create Current User's Adhaar Card
    def adhaar_card_creator():
        cur.execute(f'select first_name, last_name, gender, dob, mobile_number, adhaar_number from login_details where adhaar_number = {CurrentUser}')
        CurrentUser_data = cur.fetchone()

        def cmd():
            view_files_screen.grab_set()
            adhaar_card_screen.destroy()    

        # Creating Adhaar Card Screen
        adhaar_card_screen = tk.Toplevel(user_screen)
        adhaar_card_screen.geometry('800x300+400+150')
        adhaar_card_screen.title('Adhaar Card')
        adhaar_card_screen.resizable(False, False)
        adhaar_card_screen.grab_set()

        # Emblem
        resized = Image.open(_emblem).resize((75,75))
        adhaar_card_screen.emblem_photo = ImageTk.PhotoImage(resized)
        logo = tk.Label(adhaar_card_screen, image = adhaar_card_screen.emblem_photo)
        logo.grid(row = 0, column = 0, sticky = 'nw')

        # Government of India Heading
        heading = tk.Label(adhaar_card_screen, 
            text = 'GOVERNMENT OF INDIA', 
            font = 'arial 20 bold').grid(row = 0, column = 1, sticky = 'n', padx = (100, 0))

        # User Full Name
        full_name_label = tk.Label(adhaar_card_screen, 
            text = f'Name: {CurrentUser_data[0]} {CurrentUser_data[1]}', 
            font = 'arial 20 bold').grid(row = 1, column = 1, sticky = 'w')

        # User DOB
        dob_label = tk.Label(adhaar_card_screen, 
            text = f'DOB: {CurrentUser_data[3]}', 
            font = 'arial 20 bold').grid(row = 2, column = 1, sticky = 'w')

        # User Gender
        gender_label = tk.Label(adhaar_card_screen, 
            text = f"Gender: {'Male' if CurrentUser_data[2] == 'M' else 'Female'}", 
            font = 'arial 20 bold').grid(row = 3, column = 1, sticky = 'w')

        # User Mobile No.
        mobile_no_label = tk.Label(adhaar_card_screen, 
            text = f'Mobile No.: {CurrentUser_data[4]}', 
            font = 'arial 20 bold').grid(row = 4, column = 1, sticky = 'w')

        # User Adhaar Number
        adhaar_number_label = tk.Label(adhaar_card_screen, 
            text = f'{str(CurrentUser)[0:4]} {str(CurrentUser)[4:8]} {str(CurrentUser)[8:13]}', 
            font = 'arial 20 bold').grid(row = 5, column = 1, sticky = 'w', pady = (30, 0))

        # User Image
        resized = Image.open(_userImage %(CurrentUser_data[2])).resize((150,180))
        global user_image
        user_image = ImageTk.PhotoImage(resized)
        user_image_label = tk.Label(adhaar_card_screen, 
            image = user_image,
            borderwidth = 2,
            relief = 'solid')
        user_image_label.grid(row = 1, column = 0, padx = 10, rowspan = 5, sticky = 'n')

        # User QR Code
        resized = Image.open(_qrCode).resize((150,140))
        global qr_code
        qr_code = ImageTk.PhotoImage(resized)
        qr_code_logo = tk.Label(adhaar_card_screen, 
            image = qr_code,
            borderwidth = 2)
        qr_code_logo.grid(row = 3, column = 2, padx = 10, rowspan = 3)

        adhaar_card_screen.protocol("WM_DELETE_WINDOW", cmd)

    # Function to create a window for viewing Uploaded Files
    def view_files():
        # Creating Screen to show uploaded files
        global view_files_screen
        view_files_screen = tk.Toplevel(user_screen)
        view_files_screen.geometry('750x200+400+275')
        view_files_screen.grab_set()
        view_files_screen.resizable(False, False)

        select_file_label = tk.Label(view_files_screen,text="Select File: ", font = 'arial 30 bold').grid(row=0,column=0, padx = 18, pady = 10)

        # Extracting file paths of all user uploaded documents
        user_files_paths = open(f"C:/ProgramData/MySQL/MySQL Server 8.0/Data/digilocker/users/{CurrentUser}/file_paths.dat", 'rb')
        file_path = pickle.load(user_files_paths)
        user_files_paths.close()
        file_names = ['Adhaar Card', *file_path.keys()]

        # Combobox to show files uploaded by Current User
        files_combo = ttk.Combobox(view_files_screen, value = file_names, font = 'arial 30 bold', state = 'readonly')
        files_combo.current(0)
        files_combo.grid(row=0,column=1)

        def open_file():
            
            document_choice = files_combo.get()

            if document_choice == 'Adhaar Card':
                adhaar_card_creator()
            else:

                file_format = file_path[document_choice].split('.')[-1]
                if file_format == 'pdf':
                    # Creating screen to display documnet PDF content
                    pdf_screen = tk.Toplevel(view_files_screen)
                    pdf_screen.geometry('800x800+400+10')
                    pdf_screen.resizable(False, False)
                    pdf_screen.grab_set()

                    # Creating ShowPdf object
                    pdf_obj = tkPDFViewer.ShowPdf()

                    # Adding PDF file path
                    pdf_content = pdf_obj.pdf_view(pdf_screen, 
                        pdf_location = file_path[document_choice], 
                        width = 800, 
                        height = 800)
                    pdf_content.pack()

                    def cmd():
                        view_files_screen.grab_set()
                        pdf_screen.destroy()

                    pdf_screen.protocol('WM_DELETE_WINDOW', cmd)

                else:
                    # Creating screen to display the document Image
                    image_screen = tk.Toplevel(view_files_screen)
                    image_screen.geometry('1280x720+160+90')
                    image_screen.resizable(False, False)
                    image_screen.grab_set()
                    
                    # Resizing the document image
                    resized_image = Image.open(file_path[document_choice]).resize((1280,720))

                    # Creating Label to store document image
                    image_screen.document_image = ImageTk.PhotoImage(resized_image)
                    image_screen.document_image_label = tk.Label(image_screen, image = image_screen.document_image)
                    image_screen.document_image_label.pack()

                    def cmd():
                        view_files_screen.grab_set()
                        image_screen.destroy()

                    image_screen.protocol('WM_DELETE_WINDOW', cmd)


        # Open file button
        open_file_button = tk.Button(view_files_screen,
        text="Open",
        command=open_file,
        font = 'arial 30 bold', 
        borderwidth = 5)
        open_file_button.grid(row = 2, column = 0, columnspan=2, pady = (20, 20))

    # Function to create a window for Uploading Files
    def upload_file():
        
        # Creating the Upload File Screen
        filename = ''
        upload_file_screen = tk.Toplevel(user_screen)
        upload_file_screen.geometry('950x400+400+250')
        upload_file_screen.grab_set()
        upload_file_screen.resizable(False, False)

        # Function for File Select Dialog Pop-Up
        def select_file_dialog():

            nonlocal filename
            # Asking User for file path
            filename = filedialog.askopenfilename(title = 'Open a Document or an Image File',
                filetypes = (("PDF File", "*.pdf"), 
                            ("JPG File", "*.jpg"), 
                            ("JPEG File", "*.jpeg"), 
                            ("PNG File", "*.png")))

        def confirmed_upload_file():
            # Loading all previous documents' file paths 
            user_files_paths = open(f"C:/ProgramData/MySQL/MySQL Server 8.0/Data/digilocker/users/{CurrentUser}/file_paths.dat", 'rb')
            file_paths = pickle.load(user_files_paths)

            document_name = document_name_entry.get()

            # Checking if any file is selected
            if filename:
                if document_name not in file_paths.keys():
                    # Copying file from user-given path to user database directory
                    shutil.copy(filename, f"C:/ProgramData/MySQL/MySQL Server 8.0/Data/digilocker/users/{CurrentUser}")

                    # Opening the file again in write mode to delete previous data
                    user_files_paths.close()
                    user_files_paths = open(f"C:/ProgramData/MySQL/MySQL Server 8.0/Data/digilocker/users/{CurrentUser}/file_paths.dat", 'wb')

                    original_file_name = f"C:/ProgramData/MySQL/MySQL Server 8.0/Data/digilocker/users/{CurrentUser}/{filename.split('/')[-1]}"
                    new_file_name = f"C:/ProgramData/MySQL/MySQL Server 8.0/Data/digilocker/users/{CurrentUser}/{document_name}.{filename.split('.')[-1]}"

                    # Adding Document Name with File Path in User File Paths data file
                    file_paths[document_name] = new_file_name
                    pickle.dump(file_paths, user_files_paths)

                    # Renaming file to the same as Document Name
                    os.rename(original_file_name, new_file_name)
                else:
                    error('There already exists a document with the same name!', upload_file_screen)

            user_files_paths.close()

        # Confirm Upload File Button
        confirmed_upload_file = tk.Button(upload_file_screen, 
            text = 'Upload File',
            font = 'arial 30 bold',
            borderwidth = 10,  
            command = confirmed_upload_file)
        confirmed_upload_file.grid(row = 2, column = 0, columnspan = 2)


        # Document Name Label
        document_name_label = tk.Label(upload_file_screen, text = 'Enter Document Name: ',font = 'arial 30 bold')
        document_name_label.grid(row = 0, column = 0, padx = 15, pady = (20, 40))

        # Entry Box to take document name input from user
        document_name_entry = tk.Entry(upload_file_screen, font = 'arial 30 bold', borderwidth = 5)
        document_name_entry.grid(row = 0, column = 1, pady = (20, 40))

        # Button to Select File for uploading
        select_file_button = tk.Button(upload_file_screen, 
            text = 'Select File', 
            font = 'arial 30 bold',
            borderwidth = 10, 
            command = select_file_dialog)
        select_file_button.grid(row = 1, column = 0, columnspan = 2, pady=(0, 40))

    def logout():
        global LoggedIn
        LoggedIn = False
        user_screen.destroy()

    def exit():
        global Closed
        Closed = True
        user_screen.destroy()

    # Function to Create User Screen Widgets
    def user_screen_widgets():
        # View Files Button
        View_Files_button=tk.Button(user_screen,
            text="View Files",
            command=view_files, 
            font = 'arial 40 bold', 
            borderwidth = 8)
        View_Files_button.grid(row=0,column=0, padx = 150, pady=(100, 100))
        
        # Upload Files Button
        Upload_Files_button=tk.Button(user_screen,
            text = "Upload Files",
            command = upload_file, 
            font = 'arial 40 bold', 
            borderwidth = 8)
        Upload_Files_button.grid(row=0,column=1, padx = 150, pady=(10, 10))

        # LogOut Button
        LogOut_button=tk.Button(user_screen,
            text = "Logout",
            command = logout,
            font = 'arial 40 bold', 
            borderwidth = 8)
        LogOut_button.grid(row=1,column=0, padx = 150, pady=(10, 10))

        # Exit Button
        Exit_button=tk.Button(user_screen,
            text = "Exit",
            command = exit,
            font = 'arial 40 bold', 
            borderwidth = 8)
        Exit_button.grid(row=1,column=1, padx = 150)

        # Creating Logo
        resized = Image.open(_logo).resize((400,200))
        global logo_photo
        logo_photo = ImageTk.PhotoImage(resized)
        logo = tk.Label(user_screen, image = logo_photo)
        logo.grid(row = 2, column = 0, columnspan = 2, pady = (50, 0))

        # Creating Emblem
        resized = Image.open(_emblem).resize((150,150))
        user_screen.emblem_photo = ImageTk.PhotoImage(resized)
        logo = tk.Label(user_screen, image = user_screen.emblem_photo)
        logo.grid(row = 0, column = 0, columnspan = 2, pady = (0, 0))
    
    # Creating Main User Screen if logged in
    user_screen = tk.Tk()
    user_screen.geometry('1280x720+160+50')
    user_screen.iconphoto(True, ImageTk.PhotoImage(Image.open(_icon)))
    user_screen.title("DigiLocker")

    user_screen_widgets()
    user_screen.resizable(False, False)
    user_screen.protocol('WM_DELETE_WINDOW', exit)
    user_screen.mainloop()

def create_login_register_screen():

    # To create Login Screen
    def login():
        # Creating Login Window
        login_window=tk.Toplevel(root)
        login_window.geometry('800x250+400+275')
        login_window.title("Login")
        login_window.grab_set()
        login_window.resizable(False, False)
        
        # Adhaar Number and Password Label
        adhaar_number_label=tk.Label(login_window,text="Enter Aadhaar Number:", font = 'arial 30 bold').grid(row=0,column=0)
        password_label=tk.Label(login_window,text="Enter Password:", font = 'arial 30 bold').grid(row=1,column=0)

        # Adhaar Number and Password Entry Box
        adhaar_number_entry=tk.Entry(login_window, font = 'arial 20 bold', borderwidth = 4)
        adhaar_number_entry.grid(row=0,column=1, padx = 10)

        password_entry=tk.Entry(login_window, font = 'arial 20 bold', borderwidth = 4)
        password_entry.grid(row = 1,column = 1, padx = 10)

        def login_cmd():

            password = password_entry.get()

            userExists = False
            try:
                adhaar_number = int(adhaar_number_entry.get())
                cur.execute(f'select adhaar_number from login_details where adhaar_number = {adhaar_number}')
                if cur.fetchone():
                    userExists = True
                else:
                    error("Account does not exist!", login_window)
            except:
                error("Invalid details!", login_window)
            
            if userExists:
                cur.execute(f'select password from login_details where adhaar_number = {adhaar_number}')
                current_user_password = cur.fetchone()[0]
                if password == current_user_password:
                    root.destroy()
                    global LoggedIn, current_user_adhaar
                    LoggedIn = True
                    current_user_adhaar = adhaar_number
                else:
                    error('Incorrect password!', login_window)

        # Login Button for confirming login
        login_button_ls=tk.Button(login_window,
        text="Login",
        command=login_cmd, 
        font = 'arial 30 bold', 
        borderwidth = 5)
        login_button_ls.grid(row = 2, column = 0, columnspan=2, pady = 20)

    # To create Register Screen
    def register():
        # Creating Register Window
        register_window=tk.Toplevel(root)
        register_window.geometry('890x600+400+130')
        register_window.title("Register")
        register_window.grab_set()
        register_window.resizable(False, False)

        # Creating User Info Labels for registration
        first_name_label=tk.Label(register_window,text="First Name:", font = 'arial 30 bold').grid(row=0,column=0)
        last_name_label=tk.Label(register_window,text="Last Name:", font = 'arial 30 bold').grid(row=1,column=0)
        email_label=tk.Label(register_window,text="Email:", font = 'arial 30 bold').grid(row=2,column=0)
        gender_label=tk.Label(register_window,text="Gender (M or F):", font = 'arial 30 bold').grid(row=3,column=0)
        mobile_label=tk.Label(register_window,text="Mobile Number:", font = 'arial 30 bold').grid(row=4,column=0)
        aadhaar_number_label=tk.Label(register_window,text="Aadhaar Number:", font = 'arial 30 bold').grid(row=5,column=0)
        dob_label = tk.Label(register_window,text="Date of Birth (YYYY-MM-DD):", font = 'arial 30 bold').grid(row=6,column=0)
        Password_label=tk.Label(register_window,text="Password:", font = 'arial 30 bold').grid(row=7,column=0)
        CPassword_label=tk.Label(register_window,text="Confirm Password:", font = 'arial 30 bold').grid(row=8,column=0)
        
        # Creating Entry boxes for user to type info
        first_name_entry=tk.Entry(register_window, font = 'arial 20 bold', borderwidth = 4)
        first_name_entry.grid(row=0,column=1, padx = (10, 10))

        last_name_entry=tk.Entry(register_window, font = 'arial 20 bold', borderwidth = 4)
        last_name_entry.grid(row=1,column=1, padx = (10, 10))

        email_entry=tk.Entry(register_window, font = 'arial 20 bold', borderwidth = 4)
        email_entry.grid(row=2,column=1, padx = (10, 10))

        gender_entry=tk.Entry(register_window, font = 'arial 20 bold', borderwidth = 4)
        gender_entry.grid(row=3,column=1, padx = (10, 10))

        mobile_entry=tk.Entry(register_window, font = 'arial 20 bold', borderwidth = 4)
        mobile_entry.grid(row=4,column=1, padx = (10, 10))

        aadhaar_number_entry=tk.Entry(register_window, font = 'arial 20 bold', borderwidth = 4)
        aadhaar_number_entry.grid(row=5,column=1, padx = (10, 10))

        dob_entry = tk.Entry(register_window, font = 'arial 20 bold', borderwidth = 4)
        dob_entry.grid(row=6,column=1, padx = (10, 10))

        password_entry=tk.Entry(register_window, font = 'arial 20 bold', borderwidth = 4)
        password_entry.grid(row=7,column=1, padx = (10, 10))

        cpassword_entry=tk.Entry(register_window, font = 'arial 20 bold', borderwidth = 4)
        cpassword_entry.grid(row=8,column=1, padx = (10, 10))
        
        # Function to register the user details in the database
        def reg_cmd():

            # User Registration Data
            reg_data = {
            "first_name":first_name_entry.get(),
            "last_name":last_name_entry.get(),
            "email":email_entry.get(),
            "gender":gender_entry.get(),
            "mobile_number":mobile_entry.get(),
            "adhaar_number":aadhaar_number_entry.get(),
            "password":password_entry.get(),
            "dob": dob_entry.get()
            }

            cpassword=cpassword_entry.get()

            reg_data_values = reg_data.values()

            # Checking for empty fields
            check = True
            for value in reg_data_values:
                if value != '':
                    pass
                else:
                    error('The fields cannot be empty!', register_window)
                    check = False
                    break
            
            # Confirming Data Validity
            if check:
                if str(reg_data["adhaar_number"]).isdigit() and len(str(reg_data["adhaar_number"])) == 12:

                    if cpassword==reg_data["password"]:

                        if reg_data['mobile_number'].isdigit() and len(reg_data['mobile_number']) == 10:

                            if reg_data['gender'] in ('M', 'F'):

                                if '@' in reg_data['email']:
                                
                                    if all(map(lambda val: val.isdigit() , reg_data['dob'].split('-'))):

                                        dump_query = 'insert into login_details values(%s, %s, %s, %s, %s, %s, %s, %s)'
                                        try:
                                            cur.execute(dump_query, tuple(reg_data_values))
                                            db.commit()
                                            error("You have been registered successfully!", register_window)
                                        except:
                                            error('An account with this Adhaar Number is already registered!', register_window)
                                    else:
                                        error('Invalid Date of Birth!', register_window)
                                else:
                                    error('Invalid email!', register_window)
                            else:
                                error('Invalid gender!', register_window)
                        else:
                            error("Invalid mobile number!", register_window)
                    else:
                        error("The passwords do not match!", register_window)
                else:
                    error("Invalid Adhaar Number!", register_window)


        # Creating Register Button for Registration Window
        register_button_rs=tk.Button(register_window,
        text="Register",
        command=reg_cmd, 
        font = 'arial 30 bold', 
        borderwidth = 5)
        register_button_rs.grid(row = 9, column = 0, columnspan=2, pady = (20, 20))

    # To create Welcome Screen Widgets
    def welcome_screen_widgets():
        # Creating Title
        title=tk.Label(root,
            text="WELCOME TO DIGILOCKER",
            fg="blue", 
            font = 'arial 60 bold')
        title.grid(row=0,column=0,columnspan=3, padx = (100, 0))

        # Creating Login Button
        Login_button=tk.Button(root,
            text="Login",
            command=login, 
            font = 'arial 40 bold', 
            borderwidth = 8)
        Login_button.grid(row=2,column=0, padx = 150)

        # Creating Register Button
        register_button=tk.Button(root,
            text="Register",
            command=register, 
            font = 'arial 40 bold', 
            borderwidth = 8)
        register_button.grid(row=2,column=1,padx=1,pady=50)

        # Creating Exit Button
        exit_button=tk.Button(root,
            text="Exit",
            command=on_closing, 
            font = 'arial 40 bold', 
            borderwidth = 8)
        exit_button.grid(row=2,column=2, padx = 150, pady=50)

        # Creating Slogan
        slogan=tk.Label(root,
            text="DOCUMENT WALLET \nTO EMPOWER CITIZENS",
            fg="blue",
            font="arial 50 bold")
        slogan.grid(row = 3, column = 0, columnspan = 3,padx = (100,0))

        # Creating Logo
        resized = Image.open(_logo).resize((400,200))
        global photo
        photo = ImageTk.PhotoImage(resized)
        logo = tk.Label(root, image = photo)
        logo.grid(row = 4, column = 0, columnspan = 3)

    def on_closing():
        global Closed
        Closed = True
        root.destroy()

    # Createing Welcome Screen
    root=tk.Tk()
    root.geometry('1280x720+160+50')
    root.iconphoto(True, ImageTk.PhotoImage(file=_icon))
    root.title("DigiLocker")

    welcome_screen_widgets()
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

while not Closed:
    if not LoggedIn:
        create_login_register_screen()
    else:
        create_user_screen(current_user_adhaar)




