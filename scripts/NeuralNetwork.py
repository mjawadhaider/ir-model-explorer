import os
import pandas as pd
import numpy as np

# 1️⃣ **Data Preparation**
def load_txt_files(folder_path):
    """Load all .txt files from the given folder into a Pandas DataFrame."""
    data = {'filename': [], 'text': []}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                text = file.read().lower()  # Convert to lowercase
                text = ''.join(char if char.isalnum() else ' ' for char in text)  # Remove non-alphanumeric chars
                data['filename'].append(filename)
                data['text'].append(text)
    return pd.DataFrame(data)

def tokenize(text):
    """Split the text into words."""
    return text.split()

def build_vocabulary(documents):
    """Create a vocabulary from all the words in the documents."""
    vocab = set()
    for doc in documents:
        tokens = tokenize(doc)
        vocab.update(tokens)
    return list(vocab)

def create_bow_vector(document, vocabulary):
    """Create a Bag-of-Words (BoW) vector for a document."""
    tokens = tokenize(document)
    vector = np.zeros(len(vocabulary), dtype=int)
    for token in tokens:
        if token in vocabulary:
            index = vocabulary.index(token)
            vector[index] += 1
    return vector

def prepare_bow_vectors(documents, vocabulary):
    """Convert all documents into BoW vectors."""
    return np.array([create_bow_vector(doc, vocabulary) for doc in documents])

# 2️⃣ **Neural Network Design**
class NeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim):
        """Initialize weights and biases for the hidden and output layers."""
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.01  # Weights for input to hidden
        self.B1 = np.zeros((1, hidden_dim))  # Bias for hidden layer
        self.W2 = np.random.randn(hidden_dim, output_dim) * 0.01  # Weights for hidden to output
        self.B2 = np.zeros((1, output_dim))  # Bias for output layer

    def relu(self, x):
        """ReLU activation function."""
        return np.maximum(0, x)

    def relu_derivative(self, x):
        """Derivative of ReLU (used for backpropagation)."""
        return np.where(x > 0, 1, 0)

    def forward(self, x):
        """Forward pass through the network."""
        self.Z1 = np.dot(x, self.W1) + self.B1  # Linear transformation
        self.A1 = self.relu(self.Z1)  # Apply ReLU
        self.Z2 = np.dot(self.A1, self.W2) + self.B2  # Linear transformation for output
        return self.Z2

    def backward(self, x, y_true, y_pred, learning_rate):
        """Backward pass for weight updates."""
        m = x.shape[0]  # Number of examples

        # Compute gradients for output layer
        dZ2 = y_pred - y_true  # Gradient of loss wrt output
        dW2 = np.dot(self.A1.T, dZ2) / m
        dB2 = np.sum(dZ2, axis=0, keepdims=True) / m

        # Compute gradients for hidden layer
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.relu_derivative(self.Z1)
        dW1 = np.dot(x.T, dZ1) / m
        dB1 = np.sum(dZ1, axis=0, keepdims=True) / m

        # Update weights and biases
        self.W1 -= learning_rate * dW1
        self.B1 -= learning_rate * dB1
        self.W2 -= learning_rate * dW2
        self.B2 -= learning_rate * dB2

# 3️⃣ **Training**
def train_model(model, X_train, y_train, epochs=100, learning_rate=0.01):
    """Train the model on the training set."""
    for epoch in range(epochs):
        y_pred = model.forward(X_train)  # Forward pass
        loss = np.mean((y_pred - y_train) ** 2)  # Mean squared error loss
        model.backward(X_train, y_train, y_pred, learning_rate)  # Backward pass
        
        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss:.4f}')

# 4️⃣ **Inference**
def test_model(model, X_test):
    """Test the trained model on new document vectors."""
    y_pred = model.forward(X_test)
    return y_pred

# 5️⃣ **Query from Model**
def query_model(model, query, vocabulary, df):
    """Query the model and rank the documents based on their relevance scores."""
    # Convert query to BoW vector
    query_vector = create_bow_vector(query, vocabulary)  # BoW vector for the query
    query_vector = query_vector.reshape(1, -1)  # Reshape to (1, input_dim)
    
    # Compute relevance scores for each document using document BoW vectors
    X_documents = prepare_bow_vectors(df['text'], vocabulary)  # All document BoW vectors
    relevance_scores = model.forward(X_documents)  # Forward pass for all documents
    
    # Assign the relevance scores back to the DataFrame
    df['relevance'] = relevance_scores.flatten()  # Add relevance score as a new column
    ranked_docs = df.sort_values(by='relevance', ascending=False)  # Rank documents
    return ranked_docs[['filename', 'relevance']]

def search(query):
    folder_path = 'data/documents'
    df = load_txt_files(folder_path)

    vocabulary = build_vocabulary(df['text'])
    X = prepare_bow_vectors(df['text'], vocabulary)
    
    y = np.random.rand(len(X), 1)  # Random relevance scores (replace with real scores)
    split_index = int(0.8 * len(X))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    input_dim = X.shape[1]
    model = NeuralNetwork(input_dim=input_dim, hidden_dim=10, output_dim=1)
    train_model(model, X_train, y_train, epochs=50, learning_rate=0.01)

    return query_model(model, query, vocabulary, df)

# 6️⃣ **Main Workflow**
def main():
    folder_path = 'data/documents'
    df = load_txt_files(folder_path)
    print(f"Loaded {len(df)} documents.")

    vocabulary = build_vocabulary(df['text'])
    X = prepare_bow_vectors(df['text'], vocabulary)
    
    y = np.random.rand(len(X), 1)  # Random relevance scores (replace with real scores)
    split_index = int(0.8 * len(X))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    input_dim = X.shape[1]
    model = NeuralNetwork(input_dim=input_dim, hidden_dim=10, output_dim=1)
    train_model(model, X_train, y_train, epochs=50, learning_rate=0.01)

    while True:
        query = input("\nEnter your query (or 'exit' to stop): ")
        if query.lower() == 'exit':
            break
        ranked_docs = query_model(model, query, vocabulary, df)
        print("\nTop Matching Documents:")
        print(ranked_docs.head(5))  # Show top 5 relevant documents

if __name__ == "__main__":
    main()
