from collections import defaultdict
from typing import List , DefaultDict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dataformat import ITableRow_1 , ITableRow_2, ITableRow_3
import threading
import re


class Mexico():
    
    def __init__(self, driver) -> None:
        self.driver = driver
        self._ENTIDADES_URL = "https://es.wikipedia.org/wiki/Anexo:Entidades_federativas_de_M%C3%A9xico_por_superficie,_poblaci%C3%B3n_y_densidad"
        self.tables = []
        self.driver.get(self._ENTIDADES_URL)



    def get_tables(self) -> None:
        """Refreshes or loads the table DOM elements in memory."""
        # Removes last element to avoid the footer
        # Places the driver back in root
        self.driver.get(self._ENTIDADES_URL)
        self.tables = self.driver.find_elements(By.CSS_SELECTOR,"table")[0:3]

    
    def first_table_to_data(self) -> DefaultDict[str, ITableRow_1]:
        """Builds a dictionary that can be consumed by DataWriter"""
        
        # Internal helper function
        def _get_numbers(string_item):
            return re.sub("[^\d\.]", "" ,string_item)
        def _default_dict() -> ITableRow_1:
            return {"superficie": None , "poblacion": None, "densidad": None}
        data = defaultdict(_default_dict)

        rows = self.tables[0].find_elements(By.CSS_SELECTOR , "tr")[3:]
        for row in rows:
            estado = row.find_element(By.CSS_SELECTOR,"td>a").get_attribute("innerHTML")
            #Rest of the items
            cells      = row.find_elements(By.CSS_SELECTOR, "td")
            superficie = _get_numbers(cells[4].get_attribute("innerHTML"))
            poblacion  = _get_numbers(cells[6].get_attribute("innerHTML"))
            densidad   = _get_numbers(cells[7].get_attribute("innerHTML"))

            data[estado]["superficie"] = int(superficie)
            data[estado]["densidad"]   = int(densidad)
            data[estado]["poblacion"]  = int(poblacion)

        return data      

    def second_table_to_data(self) -> DefaultDict[str, ITableRow_2]:
        """Builds a dictionary that can be consumed by DataWriter"""
        
        # Internal helper function
        def _get_numbers(string_item):
            return re.sub("[^\d\.]", "" ,string_item)
        # Useful to be more specific about the dates
        def _default_dict() -> ITableRow_2:
            return {
                "year_2020": None, "year_2010": None, "year_2000": None, "year_1990": None,
                "year_1980": None, "year_1970": None, "year_1960": None, "year_1950": None,
                "year_1940": None, "year_1930": None, "year_1921": None, "year_1910": None
        }

        data = defaultdict(_default_dict)
        # Helpful to assign the correct position
        idx_to_year = {
            0: "year_2020", 1: "year_2010", 2 : "year_2000", 3 : "year_1990",
            4: "year_1980", 5: "year_1970", 6 : "year_1960", 7 : "year_1950",
            8: "year_1940", 9: "year_1930", 10: "year_1921", 11: "year_1910"
        }

        rows = self.tables[1].find_elements(By.CSS_SELECTOR , "tr")[2:]
        for row in rows:
            estado = row.find_element(By.CSS_SELECTOR,"td>a").get_attribute("innerHTML")
            current_idx = 0
            for cell in row.find_elements(By.CSS_SELECTOR , "td")[2:]:
                s = _get_numbers(cell.get_attribute("innerHTML"))
                poblacion_value = int(s) if s.isdecimal() else None
                current_year = idx_to_year[current_idx]
                data[estado][current_year] = poblacion_value
                current_idx += 1 
               
        return data      

    def third_table_to_data(self) -> DefaultDict[str, ITableRow_3]:
        """Builds a dictionary that can be consumed by DataWriter"""
        
        def _get_numbers(string_item):
                return re.sub("[^\d\.]", "" ,string_item)
        # Custom default dict for each table
        def _default_dict() -> ITableRow_3:
            return {"year_2010": None , "year_2015" : None , "year_2020" : None , "year_2025" : None , "year_2030" : None }
        # YEAR 2020 is cell 2 and above
        dtable3 = defaultdict(_default_dict)
        idx_to_year = {
            0: "year_2020", 1: "year_2015", 2: "year_2010", 3: "year_2025", 4: "year_2030"
        }       
        # Assume the population list is from 2020 - 10 * iteration
        rows = self.tables[2].find_elements(By.CSS_SELECTOR , "tr")[2:-1]
        
        for row in rows:
            estado = row.find_element(By.CSS_SELECTOR, "td>a").get_attribute("innerHTML")    
            current_year = "2010"
            # Only find cells with numeric values    
            curr_idx = 0
            for cell in row.find_elements(By.CSS_SELECTOR, "td")[2:]:
                s = _get_numbers(cell.get_attribute("innerHTML"))
                poblacion_value = int(s) if s.isdecimal() else None
                current_year = idx_to_year[curr_idx]
                dtable3[estado][current_year] = poblacion_value
                curr_idx += 1
                

        return dtable3         
    
    def extract_toponimias_threaded(self) -> DefaultDict:
        """Uses a default headless webdriver. The driver selected on the class creation is discarded
        because it could cause many windows to open if it is not headless. Not recommended to use this, thought
        the time constraints were on the driver.get operation, but it was mostly on the search algorithm. Could potentially be
        faster on very slow internet connections """
        rows = self.tables[2].find_elements(By.CSS_SELECTOR , "tr")[2:-1]
        href_to_visit = []
        for row in rows:
            estado = row.find_element(By.CSS_SELECTOR, "td>a")
            href_to_visit.append( estado.get_attribute("href") )

        dtoponimias = defaultdict(str)
        lock = threading.Lock()
        threads = []

        for link in href_to_visit:
            thread = threading.Thread(target=self._visit_link_and_extract_toponimia, args=(link, dtoponimias, lock))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()     

        return dtoponimias
    
    def extract_toponimias(self) -> DefaultDict:
        """Recommended method to build the data. Single threaded version."""
        rows = self.tables[2].find_elements(By.CSS_SELECTOR , "tr")[2:-1]
        href_to_visit = []
        for row in rows:
            estado = row.find_element(By.CSS_SELECTOR, "td>a")
            href_to_visit.append( estado.get_attribute("href") )

        dtoponimias = defaultdict()

        for link in href_to_visit:
            self.driver.get(link)

            text_area = self.driver.find_element(By.CSS_SELECTOR, "#mw-content-text>div")
            paragraphs = text_area.find_elements(By.XPATH, "./*")

            is_toponimia_next = False

            for paragraph in paragraphs:
                if paragraph.tag_name == "h2":
                    try:
                        titulo = paragraph.find_element(By.ID, "Toponimia").get_attribute("innerHTML")
                        is_toponimia_next = True
                        continue
                    except:
                        pass
                if is_toponimia_next:
                    # Avoid figures or spans embedded between title and text
                    if paragraph.tag_name != "p":
                        continue
                    dtoponimias[link] = paragraph.text
                    break
        return dtoponimias


    def _visit_link_and_extract_toponimia(self , link , dtoponimias, lock):
        options = Options()
        # Example configuration applied to the original driver
        options.add_argument('--headless')  
        options.add_argument('--no-sandbox') 
        options.add_argument('--disable-dev-shm-usage')  
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=3')


        tmp_driver = webdriver.Chrome(options=options)  # Or use your specific driver configuration
        
        tmp_driver.get(link)
        text_area = tmp_driver.find_element(By.CSS_SELECTOR, "#mw-content-text>div")
        paragraphs = text_area.find_elements(By.XPATH, "./*")

        is_toponimia_next = False
        for paragraph in paragraphs:
            if paragraph.tag_name == "h2":
                try:
                    titulo = paragraph.find_element(By.ID, "Toponimia").get_attribute("innerHTML")
                    is_toponimia_next = True
                    continue
                except:
                    pass
            if is_toponimia_next:
                if paragraph.tag_name != "p":
                    continue
                with lock:
                    dtoponimias[link] = paragraph.text
                break

        tmp_driver.quit()