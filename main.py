import streamlit as st
import pandas as pd
from PIL import Image
# from drug_db import *
import random
import re
import mysql.connector as sql_db

conn = sql_db.connect(host='localhost', database='test101', user='root', password='root')
c = conn.cursor()

#use this code in cmd to run this "streamlit run main.py"


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://color.adobe.com/media/theme/92471.png");
background-size: 100%;
background-position: fixed;
background-repeat: no-repeat;
background-attachment: scroll;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


#  Validation
# Password validation in Python
# using naive method

# Function to validate the password
def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(passwd) < 4:
        st.info('Password length should be at least 4')
        val = False

    if not any(char.islower() for char in passwd):
        st.info('Password should have at least one lowercase letter')
        val = False

    if val:
        return val


# Define a function for validating an Email
def email_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if (re.fullmatch(regex, email)):
        return True
    else:
        st.info("Email is not valid")
        return False


# Phone Number validation
def phone_check(phone):
    # 1) Begins with 0 or 91
    # 2) Then contains 6,7 or 8 or 9.
    # 3) Then contains 9 digits
    Pattern = re.compile("[6-9][0-9]{9}")
    if Pattern.match(phone):
        return True
    else:
        st.info("Phone Number Must is not valid use")
        return False

#sql part

##this part for signup
def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_State VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL 
                    )''')
    print('Customer Table create Successfully')


def customer_add_data(Cname, Cpass, Cemail, Cstate, Cnumber):
    c.execute('''INSERT INTO Customers (C_Name,C_Password,C_Email, C_State, C_Number) VALUES(%s,%s,%s,%s,%s)''',
              (Cname, Cpass, Cemail, Cstate, Cnumber))
    conn.commit()


def customer_view_all_data(email=None):
    if email is None:
        c.execute('SELECT * FROM Customers')
        customer_data = c.fetchall()
        return customer_data
    else:
        c.execute('SELECT * FROM Customers WHERE C_Email= %s', (email,))
        customer_data = c.fetchall()
        return customer_data


def customer_update(Cemail, Cnumber):
    c.execute(''' UPDATE Customers SET C_Number = %s WHERE C_Email = %s''', (Cnumber, Cemail,))
    conn.commit()
    print("Updating")


def customer_delete(Cemail):
    c.execute(''' DELETE FROM Customers WHERE C_Email = %s''', (Cemail,))
    conn.commit()


def drug_update(Duse, Did):
    c.execute(''' UPDATE Drugs SET D_Use = %s WHERE D_id = %s''', (Duse, Did))
    conn.commit()


def drug_delete(Did):
    c.execute(''' DELETE FROM Drugs WHERE D_id = %s''', (Did,))
    conn.commit()


def drug_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                D_Name VARCHAR(50) NOT NULL,
                D_ExpDate DATE NOT NULL, 
                D_Use VARCHAR(50) NOT NULL,
                D_Qty INT NOT NULL, 
                D_id INT PRIMARY KEY NOT NULL)
                ''')
    print('DRUG Table create Successfully')

#add drugs
def drug_add_data(Dname, Dexpdate, Duse, Dqty, Did):
    c.execute('''INSERT INTO Drugs (D_Name, D_ExpDate, D_Use, D_Qty, D_id) VALUES(%s,%s,%s,%s,%s)''',
              (Dname, Dexpdate, Duse, Dqty, Did))
    conn.commit()


def drug_view_all_data():
    c.execute('SELECT * FROM Drugs')
    drug_data = c.fetchall()
    return drug_data


def order_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_id VARCHAR(100) PRIMARY KEY NOT NULL)
    ''')


def order_delete(Oid):
    c.execute(''' DELETE FROM Orders WHERE O_id = %s''', (Oid,))


def order_add_data(O_Name, O_Items, O_Qty, O_id):
    c.execute('''INSERT INTO Orders (O_Name, O_Items, O_Qty, O_id) VALUES(%s,%s,%s,%s,%s)''',
              (O_Name, O_Items, O_Qty, O_id))
    conn.commit()


# def(username):


# __________________________________________________________________________________


def admin() -> object:
    pagpage_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://color.adobe.com/media/theme/92471.png");
    background-size: 100%;
    background-position: fixed;
    background-repeat: no-repeat;
    background-attachment: scroll;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}
    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)
    menu = ["Drugs", "Customers", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    ## DRUGS
    if choice == "Drugs":

        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":

            st.subheader("Add Drugs")

            col1, col2 = st.columns(2)

            with col1:
                drug_name = st.text_area("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_area("When to Use")
            with col2:
                drug_quantity = st.text_area("Enter the quantity")
                drug_id = st.text_area("Enter the Drug id (example:#D1)")

            if st.button("Add Drug"):
                drug_add_data(drug_name, drug_expiry, drug_mainuse, drug_quantity, drug_id)
                st.success("Successfully Added Data")
        if choice == "View":
            st.subheader("Drug Details")
            drug_result = drug_view_all_data()
            # st.write(drug_result)
            with st.expander("View All Drug Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity", "ID"])
                st.dataframe(drug_clean_df)
            with st.expander("View Drug Quantity"):
                drug_name_quantity_df = drug_clean_df[['Name', 'Quantity']]
                # drug_name_quantity_df = drug_name_quantity_df.reset_index()
                st.dataframe(drug_name_quantity_df)
        if choice == 'Update':
            st.subheader("Update Drug Details")
            d_id = st.text_area("Drug ID")
            d_use = st.text_area("Drug Use")
            if st.button(label='Update'):
                drug_update(d_use, d_id)

        if choice == 'Delete':
            st.subheader("Delete Drugs")
            did = st.text_area("Drug ID")
            if st.button(label="Delete"):
                drug_delete(did)



    ## CUSTOMERS
    elif choice == "Customers":

        menu = ["View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            # st.write(cust_result)
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password", "Email-ID", "Area", "Number"])
                st.dataframe(cust_clean_df)

        if choice == 'Update':
            st.subheader("Update Customer Details")
            cust_email = st.text_area("Email")
            cust_number = st.text_area("Phone Number")
            if st.button(label='Update'):
                customer_update(cust_email, cust_number)

        if choice == 'Delete':
            st.subheader("Delete Customer")
            cust_email = st.text_area("Email")
            if st.button(label="Delete"):
                customer_delete(cust_email)


#this part is for orders


    elif choice == "About":
        st.subheader("DBMS Mini Project")
        st.subheader("By Ankit Singh(60), Sahil Jhodge(26) & Prathmeshn Shinde(56)")



#login part
def getauthenicate(username, password):
    # print("Auth")
    if (len(username) > 0) and (len(password) > 0):
        try:
            c.execute('SELECT C_Password FROM Customers WHERE C_Name = %s', (username,))
            cust_password = c.fetchall()
            # print(cust_password[0][0], "Outside password")
            # print(password, "Parameter password")
            if cust_password[0][0] == password:
                return True
            else:
                st.info("Password is incorrect, please try again !")
                return False
        except:
            st.info("Error, User does not exist in Database !")
    else:
        st.info("Username and Password cannot be blank !")
        return False


###################################################################


def customer(username, password):
    if getauthenicate(username, password):
#css
        page_bg_img = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://color.adobe.com/media/theme/92471.png");
        background-size: 100%;
        background-position: fixed;
        background-repeat: no-repeat;
        background-attachment: scroll;
        }}
        
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}
        [data-testid="stToolbar"] {{
        right: 2rem;
        }}
        </style>
        """


        drug_result = drug_view_all_data()
        print(drug_result)

        st.subheader("Drug: " + drug_result[0][0])
        img = Image.open('images/dolo650.png')
        st.image(img, width=100, caption="Rs. 15/-")
        dolo650 = st.slider(label="Quantity", min_value=0, max_value=10, key=1)
        st.info("When to USE: " + str(drug_result[0][2]))

        st.subheader("Drug: " + drug_result[1][0])
        img = Image.open('images/ciplox-500.jpg')
        st.image(img, width=100, caption="Rs. 10/-")
        Ciplox500 = st.slider(label="Quantity", min_value=0, max_value=10, key=2)
        st.info("When to USE: " + str(drug_result[1][2]))

        st.subheader("Drug: " + drug_result[2][0])
        img = Image.open('images/4987176019271_1__40383.webp')
        st.image(img, width=100, caption="Rs. 66/-")
        vicks = st.slider(label="Quantity", min_value=0, max_value=10, key=3)
        st.info("When to USE: " + str(drug_result[2][2]))

        if st.button(label="Buy now"):
            O_items = ""

            if int(dolo650) > 0:
                O_items += "Dolo-650,"
            if int(Ciplox500) > 0:
                O_items += "Ciplox500,"
            if int(vicks) > 0:
                O_items += "Vicks"
            O_Qty = str(dolo650) + str(',') + str(Ciplox500) + str(",") + str(vicks)

            O_id = username + "#O" + str(random.randint(0, 1000000))
            # order_add_data(O_Name, O_Items,O_Qty, O_id):
            order_add_data(username, O_items, O_Qty, O_id)


if __name__ == '__main__':
    drug_create_table()
    cust_create_table()
    order_create_table()

    menu = ["Login", "SignUp", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.checkbox(label="Login"):
            customer(username, password)


    elif choice == "SignUp":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")

        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        col1, col2, col3 = st.columns(3)

        with col1:
            cust_email = st.text_area("Email ID")
        with col2:
            cust_area = st.text_area("State")
        with col3:
            cust_number = st.text_area("Phone Number")

        if st.button("Signup"):
            if password_check(cust_password) and password_check(cust_password1):
                if (cust_password == cust_password1):
                    if (email_check(cust_email)) and (phone_check(cust_number)):
                        customer_add_data(cust_name, cust_password, cust_email, cust_area, cust_number, )
                        st.success("Account Created!")
                        st.info("Go to Login Menu to login")
                else:
                    st.warning('Password dont match')
#Admin
    elif choice == "Admin":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        # if st.sidebar.button("Login"):
        if username == 'admin' and password == 'admin':
            admin()
        elif username == 'Admin' and password == 'Admin':
            admin()
        elif username == 'root' and password == 'root':
            admin()
        else:
            st.info("Username or Password for the ADMIN is incorrect !!!")
