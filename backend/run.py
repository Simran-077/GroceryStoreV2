from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from extensions import db
from flask_cors import CORS


def create_app():
    # initialization
    app = Flask(__name__)
    app.secret_key = "21f1000649"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///groceryStoreV2.db'
    db.init_app(app=app)

    # initializing api
    api = Api(app=app)
    jwt = JWTManager(app=app)
    app.config['JWT_SECRET_KEY'] = '21f1000649'
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # importing all api resources
    from lib.api.user import UserAPI
    from lib.api.sections import SectionAPI, GetAllSections, SectionRequestsAPI
    from lib.api.approve_managers import ApproveManagerAPI
    from lib.api.approve_sectionRequests import ApproveSectionRequests
    from lib.api.products import ProductsAPI
    from lib.api.products import ProductImage
    from lib.api.cart import CartAPI
    from lib.api.buy import BuyAPI
    from lib.api.search_products import SearchProductsAPI
    # registering all the api resources
    api.add_resource(UserAPI, '/user')
    api.add_resource(SectionAPI, '/section')
    api.add_resource(GetAllSections, '/sections')
    api.add_resource(ApproveManagerAPI, '/unapproved')
    api.add_resource(SectionRequestsAPI, '/section/request')
    api.add_resource(ApproveSectionRequests, '/section/approve')
    api.add_resource(ProductsAPI, '/product')
    api.add_resource(ProductImage, '/product/img')
    api.add_resource(CartAPI, '/cart')
    api.add_resource(BuyAPI, '/buy')
    api.add_resource(SearchProductsAPI, '/product/search')
    # api docs init code
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/docs/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test application"
        }
    )
    return app


def init_admin():
    # creating a defualt admin
    from models.user import User
    # check if admin exists
    if (User.query.filter_by(username='admin').first()):
        return 0
    admin = User(name='admin', username='admin',
                 password='admin', role='admin')
    db.session.add(admin)
    db.session.commit()
    print(admin, flush=True)


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        print("create all func ran", flush=True)
        init_admin()
    app.run(debug=True, threaded=True)
