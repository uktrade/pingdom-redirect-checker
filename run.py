import os
from app import app
from app import check_redirects

execute_checks = check_redirects.run_check() 


port = int(os.environ.get("PORT", 5000))
app.run( 
        host="0.0.0.0",
        port=port
)
