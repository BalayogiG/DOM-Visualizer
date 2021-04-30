#Packages
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from PIL import Image
import streamlit.components.v1 as components
import warnings
warnings.filterwarnings('ignore')

# DOM visualizer with functions
# 1. Cleaning html
# 2. Get html source
# 3. Cleaning Soup
# 4. Dataframe Creation
# 5. Data cleaning
# 6. Visualize

class DOM_visualizer:
    def cleanMe(self, html):
        soup = bs(html, "html5lib")
        [x.extract() for x in soup.find_all('script')]
        [x.extract() for x in soup.find_all('style')]
        [x.extract() for x in soup.find_all('meta')]
        [x.extract() for x in soup.find_all('noscript')]
        [x.extract() for x in soup.find_all('link')]
        [x.extract() for x in soup.find_all('br')]
        [x.extract() for x in soup.find_all(text=lambda text:isinstance(text, Comment))]
        return soup

    def get_html_source(self, url):
        source_code = requests.get(url)
        soup = bs(source_code.content, 'html.parser')
        soup = source_code.content
        return soup

    def clean_html_soup(self, soup):
        cleaned_html = self.cleanMe(str(soup))
        return cleaned_html

    def dataframe_creation(self, html):
        data = pd.DataFrame()
        source = []
        target = []
        for tag in html.find_all(True):
            child = tag.children
            for i in child:
                source.append(tag.name)
                target.append(i.name)
        data['source'] = source
        data['target'] = target
        return data

    def data_clean(self,df):
        df = df.dropna()
        return df

    def visualize(self, df):
        plt.figure(figsize=(20, 10))
        G = nx.from_pandas_edgelist(df, source='source', target='target', create_using=nx.DiGraph())
        node_limit = len(G.nodes)
        pos = graphviz_layout(G, prog='dot')
        nx.draw(G,pos, with_labels=True, node_size=5000,font_size=20, font_color='black', node_color=range(node_limit), cmap=plt.cm.spring)
        plt.title('DOM Tree Visualization')
        plt.savefig("DOM_Tree_viz.png", dpi=300)
        st.pyplot()

dom = DOM_visualizer()

image = Image.open('images/DOM_Tree_viz.png')
st.image(image, caption='Document Object Model Tree Visualization', width=150)
st.title("DOM Tree Visualization")

url = st.text_input("Enter Url:")
visualize = st.button("Visualize DOM")

if visualize:
    if url != '':
        html_source = dom.get_html_source(url)
        clean_html = dom.clean_html_soup(html_source)
        html_dataframe = dom.dataframe_creation(clean_html)
        clean_html_dataframe = dom.data_clean(html_dataframe)
        dom.visualize(clean_html_dataframe)

Topics = pd.DataFrame()
Topics['topics'] = ['Select topic','What is DOM', 'Types of DOM','HTML DOM']


option = st.sidebar.selectbox(
    'Select the Topic',
     Topics['topics'])

if option == 'Select topic':
	option = ''

if option == 'What is DOM':
    st.write(option)
    components.html("<ul><li>The DOM is a W3C (World Wide Web Consortium) standard.</li><li>The DOM defines a standard for accessing documents</li><li>The W3C Document Object Model (DOM) is a platform and language-neutral interface that allows programs and scripts to dynamically access and update the content, structure, and style of a document.</li></ul>", width=700, height=500)

if option == 'Types of DOM':
    st.write(option)
    components.html("<ul><li>Core DOM - standard model for all document types</li><li>XML DOM - standard model for XML documents</li><li>HTML DOM - standard model for HTML documents</li></ul>", width=700, height=500)

if option == 'HTML DOM':
    st.write(option)
    components.html("<p>The HTML DOM is a standard <strong>object</strong> model and <strong>programming interface</strong> for HTML. It defines:</p><ul><li>The HTML elements as <b>objects</b></li><li>The <b>properties</b> of all HTML elements</li><li>The <b>methods</b> to access all HTML elements</li><li>The <b>events</b> for all HTML elements</li></ul><p>In other words: The HTML DOM is a standard for <b>how to get, change, add, or delete HTML elements.</b></p>", width=700, height=500)
