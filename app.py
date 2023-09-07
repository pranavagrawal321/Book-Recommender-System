import pandas as pd
from flask import Flask, render_template, request
import numpy as np

popular_df = pd.read_pickle("popular_books.pkl")
pt = pd.read_pickle("pt.pkl")
books = pd.read_pickle("books.pkl")
similarity_scores = pd.read_pickle("similarity_scores.pkl")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", book_name=popular_df["Book-Title"].to_list(),
                           author_name=popular_df["Book-Author"].to_list(),
                           image=popular_df["Image-URL-M"].to_list(),
                           votes=popular_df["num_ratings"].to_list(),
                           rating=popular_df["avg_ratings"].to_list()
                           )


@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html")


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    print(data)
    
    return render_template('recommend.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
