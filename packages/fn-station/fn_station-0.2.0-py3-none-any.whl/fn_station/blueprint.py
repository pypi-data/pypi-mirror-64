from flask import Blueprint, render_template, request


def make_blueprint(station, url_prefix):
    blueprint = Blueprint(
        "fn_station", __name__,
        template_folder="templates",
        static_folder="static",
        url_prefix=url_prefix,
    )
    tabs = {}

    def register_tab(title, *, url=None, provide_search=False):
        slug = title.lower()
        if url is None:
            url = f"/{slug}/"
        tabs[slug] = tab = dict(url=url_prefix + url, title=title, slug=slug)

        def decorator(func=None):
            if func is None:
                def func():
                    return render_template(slug + ".html", current_tab=tab, provide_search=provide_search)
                func.__name__ = slug

            return blueprint.route(url)(func)

        return decorator

    register_tab("Composers", url="/", provide_search=True)()
    register_tab("Dashboards", provide_search=True)()
    register_tab("Queries")()
    register_tab("API")()

    @blueprint.context_processor
    def context():
        query = request.args.get("search", "").split()

        def search(*strings):
            if not query:
                return True
            return any(
                keyword.casefold() in string.casefold()
                for keyword in query
                for string in strings
            )

        return dict(
            station=station,
            tabs=tabs,
            search=search,
        )

    return blueprint
