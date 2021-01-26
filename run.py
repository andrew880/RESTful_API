from flask import Flask

def create_api(config_filename):
    api = Flask(__name__)
    api.config.from_object(config_filename)
    
    from api import api_bp
    api.register_blueprint(api_bp, url_prefix='/api')

    from Model import db
    db.init_app(api)

    return api


if __name__ == "__main__":
    api = create_api("config")
    api.run(debug=True)