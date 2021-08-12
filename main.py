import models
from database import init

from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from werkzeug.utils import redirect
from flask_security import SQLAlchemyUserDatastore, Security, login_required, current_user
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogue.db'
app.config['SECRET_KEY'] = 'secret'
app.config['SECURITY_PASSWORD_SALT'] = 'sequre'

init(app)
migrate = Migrate(app, models.db)
models.db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(models.db, models.User, models.Role)
security = Security(app, user_datastore)


class MyAdminIndexView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class ProductAdmin(MyAdminIndexView):
    column_filters = ('params', 'address')


admin = Admin(app, name="Admin")

admin.add_view(ProductAdmin(models.Product, models.db.session))
admin.add_view(MyAdminIndexView(models.ProductParams, models.db.session))
admin.add_view(MyAdminIndexView(models.DeliveryAddress, models.db.session))


@app.route('/')
@login_required
def login():
    return redirect('/admin')


if __name__ == '__main__':
    app.run()
