from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dataformat import ITableRow_US , IEtimilogia_US
from typing import List
import re

def _get_numbers(string_item): 
    return re.sub("[^\d\.]", "" ,string_item)

ROOT_URL = "https://es.wikipedia.org/wiki/Estado_de_los_Estados_Unidos"

class UnitedStates():
    def __init__(self , driver) -> None:
        self.driver = driver

    def get_table(self) -> None:
        " Load the target table into the class instance "
        self.driver.get(ROOT_URL)
        # The index of the current table
        self.table = self.driver.find_elements(By.CSS_SELECTOR,"table")[1]

    def get_state_data(self) -> List[ITableRow_US]:
        """Returns a list of table entries. Can be used later along a datawriter instance
        to save this in a Excel file """
        rows  = self.table.find_elements(By.CSS_SELECTOR, "tbody>tr")

        all_rows = []


        for row in rows:
            cells         = row.find_elements(By.CSS_SELECTOR,"td")
            name          = cells[1].text
            official_name = cells[2].text
            abbreviation  = cells[3].text
            density       = float(_get_numbers(cells[-1].text))
            surface       = float(_get_numbers(cells[-2].text))
            population    = int(_get_numbers(cells[-3].text))

            table_row = ITableRow_US(name=name,
                                    official_name=official_name,
                                    abbreviation=abbreviation,
                                    density=density,
                                    surface=surface,
                                    population=population)
            all_rows.append(table_row)
        
        return all_rows
    
    
    def get_etimologias(self) -> List[IEtimilogia_US]:
        """The list of dataclasses can be used with datawriter to generate an excel file"""
        
        rows  = self.table.find_elements(By.CSS_SELECTOR, "tbody>tr")
        all_hrefs = []
        for row in rows:
            # Get the second entry of the row
            cell = row.find_elements(By.CSS_SELECTOR, "td")[1]
            # Get the href link for that element
            href = cell.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            all_hrefs.append(href)

        etimologias = []
        for link in all_hrefs:
            self.driver.get(link)

            text_area = self.driver.find_element(By.CSS_SELECTOR, "#mw-content-text>div")
            paragraphs = text_area.find_elements(By.XPATH, "./*")

            is_toponimia_next = False

            for paragraph in paragraphs:
                if paragraph.tag_name == "h2":
                    try:
                        titulo = paragraph.find_element(By.ID, "Etimología").get_attribute("innerHTML")
                        is_toponimia_next = True
                        continue
                    except:
                        pass
                if is_toponimia_next:
                    # Avoid figures or spans embedded between title and text
                    if paragraph.tag_name != "p":
                        continue
                    etimologias.append(IEtimilogia_US(link = link , text = paragraph.text))
                    break        
        
        return etimologias