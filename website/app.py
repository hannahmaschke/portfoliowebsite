import os
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, url_for

# Initialize the Flask application
app = Flask(__name__)

# --- SEARCH FUNCTION ---
def perform_search(query):
    results = []
    # Define which pages to search through and their corresponding route names and titles
    pages_to_search = [
        {'file': 'index.html', 'endpoint': 'home', 'title': 'Homepage'},
        {'file': 'about.html', 'endpoint': 'about', 'title': 'About Me'},
        {'file': 'projects.html', 'endpoint': 'projects', 'title': 'Projects'},
        {'file': 'contact.html', 'endpoint': 'contact', 'title': 'Contact Me'}
    ]

    for page in pages_to_search:
        try:
            # Construct the full path to the template file
            filepath = os.path.join(app.root_path, 'templates', page['file'])
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use BeautifulSoup to parse HTML and get only the visible text
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()

            # Perform a case-insensitive search
            if query.lower() in text.lower():
                # Find the first occurrence to create a snippet
                index = text.lower().find(query.lower())
                snippet_start = max(0, index - 50)
                snippet_end = index + len(query) + 50
                snippet = text[snippet_start:snippet_end].strip()

                results.append({
                    'title': page['title'],
                    'url': url_for(page['endpoint']),
                    'snippet': snippet
                })
        except FileNotFoundError:
            # If a file like projects.html doesn't exist yet, just skip it
            continue
            
    return results

# route for the homepage
@app.route('/')
def home():
    """Renders the homepage."""
    return render_template('index.html')


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html')

@app.route('/projects')
def projects():
    """Renders the projects page."""
    return render_template('projects.html')


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html')


# --- SEARCH ROUTE ---
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    results = perform_search(query)
    return render_template('search_results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
