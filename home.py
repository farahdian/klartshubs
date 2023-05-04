from flask import Flask, render_template
import requests
import credentials 


#initialize the app
app = Flask(__name__)


#query api for table
def query_api():
    try:
        data=requests.get(credentials.DB_URL, headers=credentials.HEADER).json()
        
    except Exception as exc:
        data=None
    return data['records']

def query_record(record_id):
    try: 
        data=requests.get(credentials.DB_URL+"/"+record_id, headers=credentials.HEADER).json()
    except Exception as exc:
        data=None
    return data['fields']

#create hub class
class hub():
    def __init__(self, id, name, address, photo_ref,category):
        self.id = id
        self.name = name
        self.address = address 
        self.photo_ref = photo_ref
        self.category= category
    #def infobox(self):
     #   return render_template("card.html", name=self.name, address=self.address, category=self.category)



#start route
@app.route('/')
def get_hubs():
    response=query_api()
    result=[]
    for record in response:
        fields= record['fields']
        record_name=fields['Name']
        record_addr=fields['Address']
        record_photo_ref=fields['Photo_Reference']
        hub_instance= hub(record['id'], record_name, record_addr, record_photo_ref, fields['Category'])
        result.append(hub_instance)
    return render_template('index.html', cards=result, url=credentials.GMAPS_PHOTOS_URL, key=credentials.API_KEY)

@app.route('/hubs/<hub_id>')
def get_a_hub(hub_id):
    res=query_record(hub_id)
    print(res)
    return render_template("hub.html", hub=res,url=credentials.GMAPS_PHOTOS_URL, key=credentials.API_KEY)



#allow debug console
if __name__ == '__main__':
    app.run(debug=True)


