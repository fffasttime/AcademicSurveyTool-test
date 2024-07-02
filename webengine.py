from flask import Flask, jsonify
import reference
from paper_data import PaperData

app = Flask(__name__)

# Sample books data
books = [
    {"title": "Title 1", "author": "Author 1"},
    {"title": "Book 2", "author": "Author 2"},
]

refs = reference.loadDetailReference('reliAI_ref.json')
#refs = reference.loadDetailReference('rtl_ref.json')

@app.route("/books", methods=["GET"])
def get_books():
    # refs = reference.loadDetailReference('reliAI_ref.json')
    result = []
    for k, v in refs.items():

        result.append({
            'key': k,
            'title': v.base.title,
            'author': ' and '.join(v.base.authors),
            'suggestion': v.suggestion.suggestion,
            'relation': v.suggestion.relation,
            'rating': v.suggestion.rating,
        })

    return jsonify(result)

paper_data_file = 'paperdata_final4.json'
paper = PaperData.load(paper_data_file)

@app.route("/sections", methods=["GET"])
def get_sections():
    result = []
    for section in paper.main_sections:

        result.append({
            'title': section.title, 
            'beginning': section.beginning,
            'reference': [{'key': k, 
                           'title': refs[k].base.title} for k in section.ref_entries ]
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
