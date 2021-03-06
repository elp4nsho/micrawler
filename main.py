from selenium import webdriver
from lxml import html
import requests
import time
from multiprocessing import Process, Lock, Manager, Value

manager = Manager()

index = manager.list()
index.append(0)

workers = manager.list()
numeroDeWorkers = 2

driverss = []

for i in range(numeroDeWorkers):
    dri = webdriver.Chrome()
    driverss.append(dri)
    workers.append(i)

listaDeLinks = manager.list()


def subExplorar(url, driver,inde):
    try:
        print(url)
        #driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(2)
        links = list(map(lambda x: x.get_attribute("href"), driver.find_elements_by_xpath("//a")))
        listaDeLinks.extend(links)
        file = open("./info/"+driver.title + str(time.time()) + ".txt", "w+")
        file.write(url + "\n" + driver.page_source)
        print("termine: " + url)
        #driver.quit()
    except Exception as e:
        fil = open("./errores/linksnoaccedidos.txt", "w+")
        print(e)
        fil.close()
    workers.append(inde)


def explorar(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    links = list(map(lambda x: x.get_attribute("href"), driver.find_elements_by_xpath("//a")))
    file = open("./info/"+driver.title + str(time.time()) + ".txt", "w+")
    file.write(url + "\n" + driver.page_source)
    driver.quit()
    return links


def demorar():
    time.sleep(3)
    index[0] += 1
    print("ok")
    workers.append("uno")


# for i in range(5):
#    p = Process(target=demorar)
#    p.start()
#    workers.append(p)

def workerDisponible():
    return True if len(workers) > 0 else False


linksPrimerNivel = explorar("https://simple.ripley.cl/")
print(linksPrimerNivel[0])


def cavar(array):
    index[0] = 0
    while index[0] < len(array):
        # print(index)
        #print(array[index[0]])
        link = array[index[0]]
        if workerDisponible():
            driv = workers.pop()
            elDri = driverss[driv]
            w = Process(target=subExplorar, args=(link, elDri,driv))
            index[0] += 1
            w.start()



try:
    cavar(linksPrimerNivel)
    print("fin cabar 1")
    print(listaDeLinks)
    cavar(linksPrimerNivel)
    


except Exception as e:
    print(e)
    pass

print("fin Crawl")

# print()
