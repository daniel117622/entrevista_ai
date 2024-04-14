from mexico import Mexico
from unitedstates import UnitedStates
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datawriter import DataWriter
import time

if __name__ == '__main__':
    chop = Options()
    chop.add_argument("headless=new")

    edop = Options()
    edop.add_argument("headless")



    print("Selecciona un driver. En caso de seleccionar una opción invalida el programa se cerrará:")
    print("1) Chrome")
    print("2) Edge")
    user_input = input("---> ")
    if user_input == "1":
        driver_mx = webdriver.Chrome(options=chop)
        driver_us = webdriver.Chrome(options=chop)
    elif user_input == "2":
        driver_mx= webdriver.Edge(options=edop)
        driver_us= webdriver.Edge(options=edop)
    else:
        exit()
    
    mexico_parser = Mexico(driver_mx)
    united_parser = UnitedStates(driver_us)
    # Precargar los datos
    mexico_parser.get_tables()
    united_parser.get_table()

    while True:
        print("="*20)
        print("Seleccione los datos que desea extraer. ")
        print("1) Entidades federativas, población y densidad de México")
        print("2) Población historica de los censos de México")
        print("3) Proyecciones de población en México")
        print("4) Informacion de los estados de USA")
        print("5) Toponimias de los estados de México")
        print("6) Etimología de los estados de USA")
        user_input = input("---> ")
        if user_input == "1":
            table_data = mexico_parser.first_table_to_data()
            print("Seleccione el nombre del archivo a guardar estos datos sin la extensión: ")
            file_name = input("---> ")
            dw = DataWriter(f"./{file_name}.xlsx")
            dw.write_excel_table1(table_data)
        elif user_input == "2":
            table_data = mexico_parser.second_table_to_data()
            print("Seleccione el nombre del archivo a guardar estos datos sin la extensión: ")
            file_name = input("---> ")
            dw = DataWriter(f"./{file_name}.xlsx")
            dw.write_excel_table2(table_data)
        elif user_input == "3":
            table_data = mexico_parser.third_table_to_data()
            print("Seleccione el nombre del archivo a guardar estos datos sin la extensión: ")
            file_name = input("---> ")
            dw = DataWriter(f"./{file_name}.xlsx")
            dw.write_excel_table3(table_data)
        elif user_input == "4":
            table_data = united_parser.get_state_data()
            print("Seleccione el nombre del archivo a guardar estos datos sin la extensión: ")
            file_name = input("---> ")
            dw = DataWriter(f"./{file_name}.xlsx")
            dw.write_us_table(table_data)
        elif user_input == "5":
            table_data = mexico_parser.extract_toponimias()
            print("Seleccione el nombre del archivo a guardar estos datos sin la extensión: ")
            file_name = input("---> ")
            dw = DataWriter(f"./{file_name}.xlsx")
            dw.write_excel_table3()
        elif user_input == "6":
            table_data = united_parser.get_state_data()
            print("Seleccione el nombre del archivo a guardar estos datos sin la extensión: ")
            file_name = input("---> ")
            dw = DataWriter(f"./{file_name}.xlsx")
            dw.write_us_etimologia(table_data)
        else:
            exit()
            
        print("="*20)
        print("Desea realizar otra operación")
        print("1) Si")
        print("2) No")
        user_input = input("---> ")
        if user_input == "1":
            continue
        else:
            print("Cerrando drivers y saliendo")
            driver_mx.close()
            driver_us.close()
            break