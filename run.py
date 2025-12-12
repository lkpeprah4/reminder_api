
from app import create_app
import app.scheduler 

app=create_app()

if __name__ == "__main__":
    app.run(debug=True)
