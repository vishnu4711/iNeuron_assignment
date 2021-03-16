from flask import Flask,request,render_template
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import requests


app = Flask(__name__)
@app.route("/",methods=["POST","GET"])
def homepage():
    return render_template("index.html")

@app.route("/scrap",methods = ["POST"])
def index():
    if request.method == "POST":
        searchstring = request.form["content"].replace(" ","")
        try:
            fk_url = "https://www.flipkart.com/search?q=" + searchstring
            fk_req = uReq(fk_url)
            fk_page = fk_req.read()
            fk_req.close()
            fk_html = bs(fk_page, "html.parser")
            prod_lst = fk_html.find_all("div", {"class": "_1AtVbE col-12-12"})
            del prod_lst[0:2]
            pro = prod_lst[0]
            pro_link = "https://www.flipkart.com" + pro.div.div.div.a["href"]
            pro_page_get = requests.get(pro_link)
            pro_html = bs(pro_page_get.text, "html.parser")
            comments = pro_html.find_all("div", {"class": "_16PBlm"})
            del comments[-1]

            # collection = db[searchstring]

            reviews = []

            # commented before for loop

            for c in comments:
                try:
                    name = c.find("p", {"class": "_2sc7ZR _2V5EHH"}).text
                except:
                    name = "no name"

                try:
                    rating = c.find("div", {"class": "_3LWZlK _1BLPMq"}).text
                except:
                    rating = "no rating"

                try:
                    comment_heading = c.find("p", {"class": "_2-N8zT"}).text
                except:
                    comment_heading = "No Comment"

                try:
                    comment_tag = c.find("div", {"class": ""}).text
                except:
                    comment_tag = "Empty!!!"

                dict = {"Product": searchstring, "Name": name, "Rating": rating, "CommentHead": comment_heading,
                        "Comment": comment_tag}
                # collection.insert_one(dict)
                reviews.append(dict)
            return render_template("results.html", reviews=reviews)


        except:
            return "something wrong"
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)