from app import create_app

app = create_app()

def print_url_map():
  print(app.url_map)

if __name__ == "__main__":
  print_url_map()
