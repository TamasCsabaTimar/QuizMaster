import main
print("Successfully imported main.py")
print(f"FastAPI app: {main.app}")
print(f"Available endpoints: {[route.path for route in main.app.routes]}")