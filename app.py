from flask import Flask,render_template,request,redirect,url_for

import FeatureExtraction
import pickle
from urllib.parse import urlparse,urlencode
import re
from bs4 import BeautifulSoup
import requests
import whois
import urllib.request
from datetime import datetime
import time
import socket
from urllib.error import HTTPError
from cython.parallel import prange

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", title='Phishing')

@app.route('/about')
def about():
    return render_template("about.html", title='Phishing')


@app.route('/getURL',methods=['GET','POST'])
def getURL():
    if request.method == 'POST':
        global url
        url = request.form['url']
        print("Given URL: ",url)
        import pandas as pd



# In[16]:


        cd = None
        class FeatureExtraction:
            def __init__(self):
                pass
            
            def getProtocol(self,url):
                return urlparse(url).scheme
            
            def getDomain(self,url):
                return urlparse(url).netloc
            
            def getPath(self,url):
                return urlparse(url).path
            
            def havingIP(self,url):
                """If the domain part has IP then it is phishing otherwise legitimate"""
                match=re.search('(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  #IPv4
                            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  #IPv4 in hexadecimal
                            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}',url)     #Ipv6
                if match:
                    #print match.group()
                    return 1            # phishing
                else:
                    #print 'No matching pattern found'
                    return 0            # legitimate
            
            def long_url(self,url):
                """This function is defined in order to differntiate website based on the length of the URL"""
                if len(url) < 54:
                    return 0            # legitimate
                elif len(url) >= 54 and len(url) <= 75:
                    return 2            # suspicious
                else:
                    return 1            # phishing
            
            def have_at_symbol(self,url):
                """This function is used to check whether the URL contains @ symbol or not"""
                if "@" in url:
                    return 1            # phishing
                else:
                    return 0            # legitimate
            
            def redirection(self,url):
                """If the url has symbol(//) after protocol then such URL is to be classified as phishing """
                if "//" in urlparse(url).path:
                    return 1            # phishing
                else:
                    return 0            # legitimate
                
            def prefix_suffix_separation(self,url):
                """If the domain has '-' symbol then it is considered as phishing site"""
                if "-" in urlparse(url).netloc:
                    return 1            # phishing
                else:
                    return 0            # legitimate
                
            def sub_domains(self,url):
                """If the url has more than 3 dots then it is a phishing"""
                if url.count(".") < 3:
                    return 0            # legitimate
                elif url.count(".") == 3:
                    return 2            # suspicious
                else:
                    return 1            # phishing
                
            def shortening_service(self,url):
                """Tiny URL -> phishing otherwise legitimate"""
                match=re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                            'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                            'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                            'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                            'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                            'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                            'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',url)
                if match:
                    return 1               # phishing
                else:
                    return 0               # legitimate
                
            """
            def google_index(self,url):
                user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
                headers = { 'User-Agent' : user_agent}
                query = {'q': 'info:' + url}
                google = "https://www.google.com/search?" + urlencode(query)
                #data = requests.get(google, headers=headers,proxies=proxies)
                data = requests.get(google,headers=headers)
                data.encoding = 'ISO-8859-1'
                soup = BeautifulSoup(str(data.content), "html.parser")
                try:
                    check = soup.find(id="rso").find("div").find("div").find("h3").find("a")
                    if soup.find(id="rso").find("div").find("div").find("h3").find("a").find("href" != None):
                        href = check['href']
                        return 0 # indexed
                    else:
                        return 1
                except AttributeError:
                    return 1 # indexed
                #print("Waiting " + str(seconds) + " seconds until checking next URL.\n")
                #time.sleep(float(seconds))
            """
            """
            def abnormal_url(self,url):
                dns = 0
                #domain_name = ""
                try:
                    #domain = urlparse(url).netloc
                    #print(domain)
                    domain_name = whois.whois(urlparse(url).netloc)
                    #print(domain_name)
                except:
                    dns = 1
                
                if dns == 1:
                    return 1 # phishing
                else:
                    hostname=domain_name.domain_name
                    #match=re.search(hostname,url)
                    if hostname in url:
                        return 0 # legitimate
                    else:
                        return 1 # phishing
            """
            
            def web_traffic(self,url):
                try:
                    rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
                except TypeError:
                    return 1
                except HTTPError:
                    return 2
                rank= int(rank)
                if (rank<100000):
                    return 0
                else:
                    return 2
                
            def domain_registration_length(self,url):
                dns = 0
                try:
                    domain_name = whois.whois(urlparse(url).netloc)
                except:
                    dns = 1
                
                if dns == 1:
                    return 1      #phishing
                else:
                    expiration_date = domain_name.expiration_date
                    today = time.strftime('%Y-%m-%d')
                    today = datetime.strptime(today, '%Y-%m-%d')
                    if expiration_date is None:
                        return 1
                    elif type(expiration_date) is list or type(today) is list :
                        return 2     #If it is a type of list then we can't select a single value from list. So,it is regarded as suspected website  
                    else:
                        creation_date = domain_name.creation_date
                        expiration_date = domain_name.expiration_date
                        if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
                            try:
                                creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
                                expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
                            except:
                                return 2
                        registration_length = abs((expiration_date - today).days)
                        if registration_length / 365 <= 1:
                            return 1 #phishing
                        else:
                            return 0 # legitimate
                    
            def age_domain(self,url):
                dns = 0
                try:
                    domain_name = whois.whois(urlparse(url).netloc)
                except:
                    dns = 1
                
                if dns == 1:
                    return 1
                else:
                    creation_date = domain_name.creation_date
                    expiration_date = domain_name.expiration_date
                    if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
                        try:
                            creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
                            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
                        except:
                            return 2
                    if ((expiration_date is None) or (creation_date is None)):
                        return 1
                    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
                        return 2
                    else:
                        ageofdomain = abs((expiration_date - creation_date).days)
                        if ((ageofdomain/30) < 6):
                            return 1
                        else:
                            return 0
             
            
            def dns_record(self,url):
                dns = 0
                try:
                    domain_name = whois.whois(urlparse(url).netloc)
                    #rint(domain_name)
                except:
                    dns = 1
                
                if dns == 1:
                    return 1
                else:
                    return 0
                
           
            def statistical_report(self,url):
                hostname = url
                h = [(x.start(0), x.end(0)) for x in re.finditer('https://|http://|www.|https://www.|http://www.', hostname)]
                z = int(len(h))
                if z != 0:
                    y = h[0][1]
                    hostname = hostname[y:]
                    h = [(x.start(0), x.end(0)) for x in re.finditer('/', hostname)]
                    z = int(len(h))
                    if z != 0:
                        hostname = hostname[:h[0][0]]
                url_match=re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
                try:
                    ip_address = socket.gethostbyname(hostname)
                    ip_match=re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip_address)  
                except:
                    return 1
        
                if url_match:
                    return 1
                else:
                    return 0
                
            def https_token(self,url):
                match=re.search('https://|http://',url)
                try:
                    if match.start(0)==0 and match.start(0) is not None:
                        url=url   [match.end(0):]
                        match=re.search('http|https',url)
                        if match:
                            return 1
                        else:
                            return 0
                except:
                    return 1
        fe = FeatureExtraction()
        feat=[]
        protocol = []
        domain = []   
        path = []
        
#        url="https://fffffffffffffffffffffffffffffffffffffffffffffffffstaticmail.000webhostapp.com/"
        
        protocol.append(fe.getProtocol(url))
        path.append(fe.getPath(url))
        domain.append(fe.getDomain(url))
        
        feat.append(fe.have_at_symbol(url))
        feat.append(fe.havingIP(url))
        feat.append(fe.prefix_suffix_separation(url))
        feat.append(fe.redirection(url))
        feat.append(fe.sub_domains(url))
        feat.append(fe.long_url(url))
        # feat.append(fe.age_domain(url))            
        #feat.append(fe.dns_record(url))
        #feat.append(fe.domain_registration_length(url))
        feat.append(fe.https_token(url))
        feat.append(fe.statistical_report(url))         
        feat.append(fe.shortening_service(url))
        #feat.append(fe.web_traffic(url))
                    
        print(feat)
#        data = FeatureExtraction.getAttributess(url)
#        print(data)
        RFmodel = pickle.load(open('RFModel1.sav', 'rb'))
        predicted_value = RFmodel.predict([feat])
        print("predicted value: ",predicted_value)
        if predicted_value == 0:    
            value = "Legitimate"
            return render_template("index.html",error=value)
        else:
            value = "Phishing"
            return render_template("index.html",error=value)
            
        
#def view(ur):
#    import webbrowser
#    return webbrowser.open(ur)
#
@app.route('/goto',methods=['GET','POST'])
def goto():
    a = url
    return redirect(a)

if __name__ == "__main__":
    app.run(debug=True)