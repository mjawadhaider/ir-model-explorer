from flask import Flask, render_template, request
from scripts.binaryIndependenceModel import search as binaryIndependenceSearch
from scripts.NonOverlappedList import search as nonOverlappedSearch
from scripts.ProximalNodes import search as proximalNodesSearch
from scripts.structureGuidedAndHypertext import browsingStructure, addHyperlinksToContent
from scripts.Fuzzy import search as fuzzySearch
from scripts.ExtendedBoolean import search as booleanExtendedSearch
from scripts.generalizedVector import search as generalizedVectorSearch
from scripts.latentSemantic import search as latentSemanticSearch
from scripts.NeuralNetwork import search as neuralNetworkSearch
from scripts.InferenceModel import search as inferenceModelSearch
from scripts.BeliefModel import search as beliefModelSearch

app = Flask(__name__)

MODELS = [
    # {
    #     "title": "Introduction To Indexes",
    #     "description": "Introduction To Indexes",
    #     "endpoint": "introductionToIndexes",
    #     "url": "introduction-to-indexes"
    # },
    # {
    #     "title": "Ranking System",
    #     "description": "Ranking System",
    #     "endpoint": "rankingSystem",
    #     "url": "ranking-system"
    # },
    {
        "title": "Binary Independence Model",
        "description": "Binary Independence Model",
        "endpoint": "binaryIndependenceModel",
        "url": "binary-independence-model",
        "search": binaryIndependenceSearch,
    },
    {
        "title": "Non Overlapped List",
        "description": "Non-Overlapped List",
        "endpoint": "nonOverlappedList",
        "url": "non-overlapped-list",
        "search": nonOverlappedSearch,
    },
    {
        "title": "Proximal Nodes Models",
        "description": "Proximal Nodes Models",
        "endpoint": "proximalNodesModels",
        "url": "proximal-nodes-models",
        "search": proximalNodesSearch,
    },
    {
        "title": "Structure Guided Browsing and Hypertext Model",
        "description": "Structure Guided Browsing & Hypertext Model",
        "endpoint": "structureGuidedBrowsing",
        "url": "structure-guided-browsing",
        "browsingStructure": browsingStructure,
    },
    {
        "title": "Fuzzy Model",
        "description": "Fuzzy Model",
        "endpoint": "fuzzyModel",
        "url": "fuzzy-model",
        "search": fuzzySearch,
    },
    {
        "title": "Boolean Extended Model",
        "description": "Boolean Extended Model",
        "endpoint": "booleanExtendedModel",
        "url": "boolean-extended-model",
        "search": booleanExtendedSearch,
    },
    {
        "title": "Generalized Vector Model",
        "description": "Generalized Vector Model",
        "endpoint": "generalizedVectorModel",
        "url": "generalized-vector-model",
        "search": generalizedVectorSearch,
    },
    {
        "title": "Latent Semantic Indexing",
        "description": "Latent Semantic Indexing",
        "endpoint": "latentSemanticIndexing",
        "url": "latent-semantic-indexing",
        "search": latentSemanticSearch,
    },
    # {
    #     "title": "Neural Networks",
    #     "description": "Neural Networks",
    #     "endpoint": "neuralNetworks",
    #     "url": "neural-networks",
    #     "search": neuralNetworkSearch,
    # },
    {
        "title": "Interference Model",
        "description": "Interference Model",
        "endpoint": "interferenceModel",
        "url": "interference-model",
        "search": inferenceModelSearch,
    },
    {
        "title": "Belief Network Model",
        "description": "Belief Network Model",
        "endpoint": "beliefNetworkModel",
        "url": "belief-network-model",
        "search": beliefModelSearch,
    },
]


@app.route('/document/<path:doc_path>')
def document(doc_path):
    # Traverse the structure based on the doc_path to find content
    docParts = doc_path.split('/')
    doc = browsingStructure
    for part in docParts:
        doc = doc.get(part, {})

    # Add hyperlinks to the document content
    content = addHyperlinksToContent(doc, '/'.join(docParts), browsingStructure)
    
    # return render_template('document.html', title=docParts[-1], content=content)
    return render_template('document.html', models = MODELS, chapter=docParts[0], title=docParts[-1], content=content)

# Home route
@app.route('/')
def index():
    return render_template('index.html', models = MODELS, activeModel="index")

# Dynamic route generator
def generateModelRoute(model):
    """
    Generate a route handler for a model dynamically.
    """
    def routeHandler():
        results = None                                  # Variable to hold search results
        query = ""                                      # User query input
        endPoint = model["endpoint"]

        # Handle POST requests for querying
        if request.method == "POST" and "search" in model:
            query = request.form.get("query", "")
            if model["search"]:
                results = model["search"](query)

        browsingStructure = None
        if "browsingStructure" in model:
            browsingStructure = model["browsingStructure"]

        return render_template(
            f"{endPoint}.html",
            title=model["title"],
            description=model["description"],
            models=MODELS, 
            activeModel=model["endpoint"],
            results=results,
            query=query,
            browsingStructure=browsingStructure,
        )
    return routeHandler

# Dynamically add routes for models
for model in MODELS:
    app.add_url_rule(
        f'/{model["url"]}',
        endpoint=model["endpoint"],
        view_func=generateModelRoute(model),
        methods=["GET", "POST"]
    )


if __name__ == '__main__':
    app.run(debug=True)
