sudo kill -9 $(lsof -t -i:5000 -sTCP:LISTEN)
