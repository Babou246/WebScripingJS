from ast import Bytes
from curses import wrapper
from encodings import utf_8
from io import BytesIO
import json
from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from matplotlib.figure import Figure
from sqlalchemy import MetaData
from tables import Description
from index import Alibaba, Auchan, Jumia, conn,cursor,app,DB_URL,db
from matplotlib.backends.backend_agg import FigureCanvasAgg as VirtualCanvas



###########################################################
################ SHOW ALL PRODUCTS IN TEMPLATES ###########
###########################################################

CORS(app)



@app.route('/chart')
@app.route("/",methods=['GET','POST'])
def index():
    
    results= Jumia.query.all()
    # print(results)
    if request.method == 'POST':
        form = request.form
        search_value = form['recherche']
        # print(search_value)
        search = "%{}%".format(search_value)
        l = Jumia.query.filter(Jumia.description.like(search)).order_by(Jumia.prix_fcfa).all()
        alibaba = Alibaba.query.filter(Alibaba.description.like(search)).order_by(Alibaba.prix_fcfa).all()
        a = Auchan.query.filter(Auchan.description.like(search)).order_by(Auchan.prix_fcfa).all()
        # print(len(a))
        # #########################################
        return render_template('afficheProduit.html',
            name = results, 
            elements = l,
            count = len(search),
            Countl = len(l),
            CountAuchan = len(a),
            CountAlibaba = len(alibaba),
            search = search,
            auchans = a,
            alibaba = alibaba
        )
        
    else:
        l = Jumia.query.all()
        a = Auchan.query.all()
        alibaba = Alibaba.query.all()
        
        return render_template('afficheProduit.html',elements = l,auchans=a,alibaba = alibaba)

##############################################################
################ FONCTION POUR AFFICHER LE DIAG ##############
##############################################################

@app.route('/chart')
def diag():
    param = json.loads(request.args.get("param"))
    # print(param)
    labels = []
    values = []

    for key in param['datas']:
        labels.append(key)
        values.append(param["datas"][key])
    # print(labels)
    # print(values)
    fig = Figure()
    ax1 = fig.subplots(1,1)
    ax1.bar(labels,values)
    fig.savefig("un.png",format="png")
    output = BytesIO()
    VirtualCanvas(fig).print_png(output)
    response = Response(output.getvalue(),mimetype="image/png")  
    return response

#####################################################
################# GET EACH PRODUIT ##################
#####################################################
@app.route('/api/jumia/<id>', methods=['GET'])
def get_descrip(id):
    result = Jumia.query.filter_by(id=id).first()

    if result:
        return jsonify(status="True", 
                    result={
                                "id":result.id,
                                "image":result.image,
                                "description":result.description,
                                "prix_fcfa":result.prix_fcfa
                            }
                        )
    return jsonify(status="False")

@app.route('/api/auchan/<id>', methods=['GET'])
def get_prix(id):
    result = Jumia.query.filter_by(id=id).first()

    if result:
        return jsonify(status="True", 
                    result={
                                "id":result.id,
                                "image":result.image,
                                "description":result.description,
                                "prix_fcfa":result.prix_fcfa
                            }
                        )
    return jsonify(status="False")

####################################################
############ API ALL PRODUITS ######################
####################################################
@app.route('/api/jumia', methods=['GET'])
def get_all():
    result = Jumia.query.all()
    # print(result)
    liste =[]
    for i in result:
        d ={}
        d["id"] = i.id
        print(i.id)
        d["image"] = i.image
        d["description"]  = i.description
        d["prix_fcfa"] = i.prix_fcfa
        liste.append(d)
    return jsonify(liste)

@app.route('/api/auchan', methods=['GET'])
def get_all_produitAuchan():
    result = Auchan.query.all()
    # print(result)
    liste =[]
    for i in result:
        d ={}
        d["id"] = i.id
        d["image"] = i.image
        d["description"]  = i.description
        d["prix_fcfa"] = i.prix_fcfa
        liste.append(d)
    return jsonify(liste)

@app.route('/api/alibaba', methods=['GET'])
def get_produits_alibaba():
    result = Alibaba.query.all()
    # print(result)
    liste =[]
    for i in result:
        d ={}
        d["id"] = i.id
        # d["image"] = i.image
        d["description"]  = i.description
        d["prix_fcfa"] = i.prix_fcfa
        liste.append(d)
    return jsonify(liste)



##########################################################
################# LANCEMENT DU SERVEUR ###################

if __name__ == "__main__":
     app.run(host="0.0.0.0",debug=True)