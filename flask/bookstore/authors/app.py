import connexion

if __name__ == "__main__":
    PORT = 9002
    # Create the application instance
    app = connexion.FlaskApp(__name__, specification_dir="./openapi/")
    # Read the swagger.yml file to configure the endpoints
    app.add_api("openapi.yaml")
    application = app.app # wisi application?
    print("APP",app.server)
    print(app.__str__())
    app.run(PORT,debug=True)
    