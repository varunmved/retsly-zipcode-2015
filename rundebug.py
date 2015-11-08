import os
from tejava import app

os.environ["DEBUG"] = "debug"
app.run(debug=True)

