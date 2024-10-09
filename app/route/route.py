class RouteApp:
    def init_app(self, app):
        from app.resources import product
        app.register_blueprint(product, url_prefix='/api/v1')
