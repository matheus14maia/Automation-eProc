import os
import datetime
import re
import shutil
import io
import pandas as pd

from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException


class Eproc:
    pasta_lista = r'D:\\Ficus\\Dados eProc\\Oab eProc.csv'
    pasta = r'D:\\Ficus\\Dados eProc\\'
    documento = ''
    url = 'https://eproc1.tjto.jus.br/eprocV2_prod_1grau/externo_controlador.php?acao=principal&sigla_orgao_sistema=TJTO&sigla_sistema=Eproc'
    dados = {}
    pasta_path = "C:\\Users\\FicusMaheus\\Downloads"

    cliente1 = ''

    lista = pd.read_csv(pasta_lista, header=None, dtype=str)
    lista_oab = lista.values

    options = uc.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": "C:\\Users\\FicusMaheus\\Downloads",  # Change default directory for downloads
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
    })
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-popup-blocking')

    driver = uc.Chrome(options=options)
    driver.get(url)

    wait = ui.WebDriverWait(driver, 15)

    elem = wait.until(lambda driver: driver.find_element(By.ID, 'dropdownMenuButton'))
    elem.click()

    elem = wait.until(lambda driver: driver.find_elements(By.CLASS_NAME, 'dropdown-item'))
    elem[0].click()

    sleep(8)

    elem = wait.until(lambda driver: driver.find_element(By.XPATH, '/html/body/div/div[3]/div[1]/div[1]/ul/li[3]/a'))
    elem.click()

    sleep(3)

    elem = wait.until(
        lambda driver: driver.find_element(By.XPATH, '/html/body/div/div[3]/div[1]/div[1]/ul/li[3]/ul/li/a'))
    elem.click()

    sleep(3)

    elem = wait.until(lambda driver: driver.find_element(By.ID, 'selTipoPesquisa'))
    select = Select(elem)
    select.select_by_value('OA')

    sleep(3)

    for cliente1 in lista_oab:
        cliente1 = str(cliente1)
        cliente1 = cliente1.replace('\"', '')
        cliente1 = cliente1.replace('\'', '')
        cliente1 = cliente1.replace('[', '')
        cliente1 = cliente1.replace(']', '')
        pasta_final = pasta + cliente1
        if not os.path.exists(pasta_final):
            os.mkdir(pasta_final)

            elem = wait.until(lambda driver: driver.find_element(By.ID, 'numNumOab'))
            elem.send_keys(cliente1)

            sleep(3)

            elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                 '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[4]/fieldset/div[9]/dl/dd/div'))
            elem.click()

            sleep(3)

            elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                 '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[4]/fieldset/div[9]/dl/dd/div/div/ul/li[214]/label/input'))
            elem.click()
            sleep(1)
            elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                 '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[4]/fieldset/div[9]/dl/dd/div/div/ul/li[215]/label/input'))
            elem.click()
            sleep(1)
            elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                 '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[4]/fieldset/div[9]/dl/dd/div/div/ul/li[216]/label/input'))
            elem.click()

            sleep(3)

            elem = wait.until(lambda driver: driver.find_element(By.CLASS_NAME, 'infraLabelOpcional'))
            elem.click()

            sleep(3)

            elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                 '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[4]/fieldset/div[14]/dl/dd/input'))
            elem.click()

            sleep(3)

            elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                 '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[5]/button[1]'))
            elem.click()

            sleep(3)

            try:
                tbody = wait.until(lambda driver: driver.find_elements(By.TAG_NAME, 'tbody'))

                tr = tbody[7].find_elements(By.TAG_NAME, 'tr')
                pg_source = driver.page_source
                tabls = pd.read_html(pg_source)
                tab = tabls[0]
                tab.to_csv(pasta_final + "\\processos.csv", sep=';', encoding='iso-8859-1', index=False, header=False)
                for i in tr:
                    if not os.path.exists(pasta_final + "\\dados_processos"):
                        os.mkdir(pasta_final + "\\dados_processos")

                    sintetico = pasta_final + "\\dados_processos\\"
                    elem = i.find_element(By.TAG_NAME, 'a')
                    processo = elem.text
                    processo = processo.replace('.', '')
                    ActionChains(driver).key_down(Keys.CONTROL).click(elem).key_up(Keys.CONTROL).perform()
                    sleep(2)
                    driver.switch_to.window(driver.window_handles[1])
                    sleep(1)

                    page_source = driver.page_source
                    tables = pd.read_html(page_source)
                    table = pd.concat([tables[3], tables[4]], ignore_index=True)
                    table.to_csv(sintetico + f'{processo}.csv', sep=';', encoding='iso-8859-1', index=False,
                                 header=False)

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    sleep(3)


            except:
                driver.refresh()
                continue

            driver.refresh()
        else:
            if os.path.exists(pasta_final + "\\dados_processos"):
                sintetico_teste = pasta_final + "\\dados_processos\\"

                processos_path = rf'{pasta_final}\\processos.csv'
                df_verificar = pd.read_csv(processos_path, header=None, dtype=str, encoding='iso-8859-1')
                lista_proc = []
                if len(df_verificar.values) > 15:
                    for i in range(len(df_verificar.values[14:])):
                        lista_proc.append(
                            str(df_verificar.values[i]).split(';')[0].replace('.', '').replace('\'', '').replace('[', ''))
                else:
                    lista_proc.append(
                        str(df_verificar.values[14]).split(';')[0].replace('.', '').replace('\'', '').replace('[', ''))

                i = 0
                for proc in lista_proc:
                    if not os.path.exists(sintetico_teste + f'{proc}.csv'):
                        i += 1

                if i >= 1:
                    elem = wait.until(lambda driver: driver.find_element(By.ID, 'numNumOab'))
                    elem.send_keys(cliente1)

                    sleep(3)

                    elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                         '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[4]/fieldset/div[9]/dl/dd/div'))
                    elem.click()

                    sleep(3)

                    elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                         '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[4]/fieldset/div[9]/dl/dd/div/div/ul/li[214]/label/input'))
                    elem.click()
                    sleep(1)
                    elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                         '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[4]/fieldset/div[9]/dl/dd/div/div/ul/li[215]/label/input'))
                    elem.click()
                    sleep(1)
                    elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                         '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[4]/fieldset/div[9]/dl/dd/div/div/ul/li[216]/label/input'))
                    elem.click()

                    sleep(3)

                    elem = wait.until(lambda driver: driver.find_element(By.CLASS_NAME, 'infraLabelOpcional'))
                    elem.click()

                    sleep(3)

                    elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                         '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[4]/fieldset/div[14]/dl/dd/input'))
                    elem.click()

                    sleep(3)

                    elem = wait.until(lambda driver: driver.find_element(By.XPATH,
                                                                         '/html/body/div[1]/div[3]/div[2]/div/div[1]/form/div[5]/button[1]'))
                    elem.click()

                    sleep(3)

                    try:
                        tbody = wait.until(lambda driver: driver.find_elements(By.TAG_NAME, 'tbody'))

                        tr = tbody[7].find_elements(By.TAG_NAME, 'tr')
                        pg_source = driver.page_source
                        tabls = pd.read_html(pg_source)
                        tab = tabls[0]
                        tab.to_csv(pasta_final + "\\processos.csv", sep=';', encoding='iso-8859-1', index=False,
                                   header=False)
                        for i in tr:
                            if not os.path.exists(pasta_final + "\\dados_processos"):
                                os.mkdir(pasta_final + "\\dados_processos")

                            sintetico = pasta_final + "\\dados_processos\\"
                            elem = i.find_element(By.TAG_NAME, 'a')
                            processo = elem.text
                            processo = processo.replace('.', '')
                            if not os.path.exists(sintetico+f'{processo}.csv'):
                                ActionChains(driver).key_down(Keys.CONTROL).click(elem).key_up(Keys.CONTROL).perform()
                                sleep(2)
                                driver.switch_to.window(driver.window_handles[1])
                                sleep(1)

                                page_source = driver.page_source
                                tables = pd.read_html(page_source)
                                table = pd.concat([tables[3], tables[4]], ignore_index=True)
                                table.to_csv(sintetico + f'{processo}.csv', sep=';', encoding='iso-8859-1', index=False,
                                             header=False)

                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                                sleep(3)

                    except:
                        driver.refresh()
                        continue

                    driver.refresh()

            else:
                continue
