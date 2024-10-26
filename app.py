# Importação
from flask import Flask

app = Flask(__name__)

# Definir uma rota raiz (pagina inicial)
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)