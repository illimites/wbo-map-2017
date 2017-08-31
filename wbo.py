from bs4 import BeautifulSoup

class Projekt2017(object):
    """docstring for Projekt2017"""
    def __init__(self):
        super(Projekt2017, self).__init__()

    def fit_transform(self, pid, project):
        self.data = {'id': pid}
        self.data['url']='https://www.wroclaw.pl/budzet-obywatelski-wroclaw/wbo2016/projekty-2017/projekt,id,{}'.format(pid)
        self.make_soup(project)
        self.get_title()
        self.get_category()
        self.get_budget()
        self.get_threshold()
        self.get_districts()
        self.get_region()
        self.get_localization()
        self.get_description()

    def make_soup(self, project):
        self.soup = BeautifulSoup(project, 'html.parser')

    def get_title(self):
        title_element = self.soup.select("body > div.container > div:nth-of-type(2) > div > article > div.row.boxProjectHeader > div.col-sm-10 > div > h1")
        self.data['title']=list(title_element[0].children)[0].strip()

    def get_category(self):
        the_element = self.soup.select("#projekt > div.row.rowProjectParams > div:nth-of-type(1) > p")
        self.data['category'] = list(the_element[0].children)[1].strip()

    def get_budget(self):
        the_element = self.soup.select("#projekt > div.row.rowProjectParams > div:nth-of-type(2) > p")
        self.data['budget'] = list(the_element[0].children)[1].strip()
        self.data['budget_integer'] = int(self.data['budget'].replace('zł','').strip().replace(' ',''))

    def get_threshold(self):
        the_element = self.soup.select("#projekt > div.txtBudget > p > span")
        self.data['threshold'] = the_element[0].text.strip()

    def get_districts(self):
        the_element = self.soup.select("#projekt > div.boxProjectDesc.withMap.withIcon > div.row > div:nth-of-type(4) p")
        if len(the_element)>0:
            the_children = list(the_element[0].children)
            self.data['osiedla_list'] = [x.strip() for x in the_children[1].strip().split(',')]
            self.data['osiedla'] = ", ".join(self.data['osiedla_list'])
        else:
            self.data['osiedla_list'] = []
            self.data['osiedla'] = ""

    def get_region(self):
        the_element = self.soup.select("#projekt > div.boxProjectDesc.withMap.withIcon > div.row > div.col-sm-4 > p")
        self.data['region'] = list(the_element[0].children)[2].strip()
        self.data['region_no'] = list(the_element[0].children)[2].strip().split(':')[0].split(' ')[1].strip()


    def get_localization(self):
        title_element = self.soup.select("#projekt > div.boxProjectDesc.withMap.withIcon > div.row > div:nth-of-type(3) > p")
        self.data['detailed_location'] = list(title_element[0].children)[1].strip()

        the_positions_list = [x.replace('}','').replace('{', '').replace(',','').replace(']','').replace('[','').strip().split(':')[1].strip() 
            for x in self.soup.text.split('\n') if 'latitude' in x or 'longitude' in x]

        the_positions = []
        for i,x in enumerate(the_positions_list):
            if i % 2:
                the_positions.append([the_positions_list[i], the_positions_list[i-1]])

        self.data['positions'] = the_positions

        self.data['the_geom'] = "MULTIPOINT({})".format(", ".join(["{} {}".format(x[0], x[1]) for x in the_positions]))

    def get_description(self):
        the_element = self.soup.select("#projekt > div:nth-of-type(4) p")
        self.data['description'] = str(the_element[0]).replace('<br/>', '').replace('<br />', '').replace('<br>', '').replace('</br>', '').replace('\r','').replace('<p>','').replace('</p>','')

        the_element = self.soup.select("#projekt > div:nth-of-type(5) p")
        self.data['description'] += str(the_element[0]).replace('<br/>', '').replace('<br />', '').replace('<br>', '').replace('</br>', '').replace('\r','').replace('<p>','').replace('</p>','')
