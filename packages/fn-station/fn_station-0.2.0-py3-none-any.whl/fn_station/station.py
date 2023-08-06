import inspect
import pickle
from base64 import b64encode
from dataclasses import dataclass, field
from datetime import datetime
from importlib import import_module
from typing import List, Dict, Any

from dash import dash
from flasgger import Swagger, SwaggerView
from flask import request
from fn_graph import Composer
from fn_graph_studio import ExternalStudio
from networkx import to_dict_of_lists

from fn_station.api import respond, dataclass_schemas, HandledError
from fn_station.blueprint import make_blueprint
from fn_station.utils import slugify, rows_to_dicts


@dataclass
class StationComposer:
    slug: str
    url: str
    title: str
    composer: Composer
    description: str

    def serialise(self):
        sources = {
            name: inspect.getsource(f)
            for name, f in self.composer._functions.items()
            if not getattr(f, "_is_fn_graph_link", False)
        }

        dag = to_dict_of_lists(self.composer.dag())

        return SerialisedComposer(
            title=self.title,
            slug=self.slug,
            sources=sources,
            dag=dag,
            git_commit="TODO",
        )

    def calculate(self, client_id, user, parameters, result_nodes, save_history=False):
        results = (
            self.composer.update_parameters(**parameters)
                .calculate(result_nodes, intermediates=True)
        )

        if not save_history:
            return results, -1

        from fn_station.history import ComposerQuery, session_scope

        with session_scope() as session:
            query = ComposerQuery(
                client_id=client_id,
                user=user,
                results=pickle.dumps(results),
                parameters=parameters,
                composer=self.serialise().__dict__,
                timestamp=datetime.now(),
            )
            session.add(query)
            return results, query.id


@dataclass
class SerialisedComposer:
    title: str
    slug: str
    sources: Dict[str, str]
    dag: Dict[str, List[str]]
    git_commit: str


@dataclass
class ComposerCalculationRequest:
    name: str
    nodes: List[str]
    parameters: Dict[str, Any] = field(default_factory=dict)
    client_id: str = None


@dataclass
class ComposerCalculationResponse:
    id: int
    client_id: str
    nodes: Dict[str, Any]


@dataclass
class HistoricalQueryRequest:
    query_id: int


@dataclass
class HistoricalQueryResponse:
    query_id: int
    client_id: str
    user: str
    results: str
    parameters: Dict[str, Any]
    composer: SerialisedComposer
    timestamp: datetime


@dataclass
class Dashboard:
    slug: str
    url: str
    title: str
    description: str


class ComposerStation:
    def __init__(self, app, url_prefix="", save_history=False):
        self.app = app
        if url_prefix:
            url_prefix = "/" + url_prefix.strip("/")
        self.url_prefix = url_prefix
        self.composers: Dict[str, StationComposer] = {}
        self.dashboards = []
        self.endpoints = []
        self.blueprint = make_blueprint(self, url_prefix)
        self.save_history = save_history
        app.register_blueprint(self.blueprint)
        Swagger(app)

        @self.register_endpoint
        def composer_calculate(req: ComposerCalculationRequest) -> ComposerCalculationResponse:
            slug = req.name
            if slug not in self.composers:
                raise HandledError(404, f"Composer {slug} not found")
            composer = self.composers[slug]
            results, query_id = composer.calculate(
                client_id=req.client_id,
                user="TODO@businessoptics.biz",
                parameters=req.parameters,
                result_nodes=req.nodes,
                save_history=self.save_history,
            )
            return ComposerCalculationResponse(
                id=query_id,
                client_id=req.client_id,
                nodes=results,
            )

        @self.register_endpoint
        def get_historical_query(req: HistoricalQueryRequest) -> HistoricalQueryResponse:
            from fn_station.history import ComposerQuery, session_scope

            with session_scope() as session:
                query: ComposerQuery = session.query(ComposerQuery).filter_by(id=req.query_id).one_or_none()
                if not query:
                    raise HandledError(404, f"Query {req.query_id} not found")
                return HistoricalQueryResponse(
                    query_id=query.id,
                    client_id=query.client_id,
                    user=query.user,
                    results=b64encode(query.results),
                    parameters=query.parameters,
                    composer=query.composer,
                    timestamp=query.timestamp,
                )

    @property
    def history(self):
        from fn_station.history import ComposerQuery, session_scope

        with session_scope() as session:
            return rows_to_dicts(session.query(ComposerQuery).all())

    def register_composer(self, slug, title, composer: Composer, **kwargs):
        url = f"{self.url_prefix}/composer_studio/{slug}/"
        if slug in self.composers:
            raise ValueError(f"{slug} is already a registered composer")
        self.composers[slug] = StationComposer(slug, url, title, composer, **kwargs)
        dash_app = dash.Dash(
            server=self.app,
            url_base_pathname=url,
        )
        ExternalStudio(dash_app, composer)
        return self

    def register_dash(
            self,
            module_name,
            title,
            description,
            slug=None,
            # icon=None,
            # ignore_default_stylesheets=False,
    ):
        slug = slug or slugify(title)
        url = f"{self.url_prefix}/dash/{slug}/"

        def factory(name, **kwargs):
            external_stylesheets = kwargs.pop("external_stylesheets", [])
            # if not ignore_default_stylesheets:
            #     external_stylesheets = (
            #         external_stylesheets + self.default_dash_stylesheets
            #     )
            return dash.Dash(
                name,
                server=self.app,
                url_base_pathname=url,
                external_stylesheets=external_stylesheets,
                **kwargs,
            )

        import_module(module_name).create_app(factory)

        self.dashboards.append(
            Dashboard(
                slug=slug,
                title=title,
                description=description,
                # icon=icon,
                url=url,
            )
        )

        return self

    def register_endpoint(self, func):
        schemas = dict(dataclass_schemas(func))
        return_schema = schemas.pop("return")
        error_response_schema = {
            "schema": {
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["error"],
                    },
                    "message": {
                        "type": "string",
                    },
                },
            },
        }

        class MyView(SwaggerView):
            parameters = [
                {
                    "name": "body",
                    "in": "body",
                    "schema": {
                        "properties": schemas,
                    },
                    "required": True,
                }
            ]
            responses = {
                200: {
                    "schema": {
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["ok"],
                            },
                            "result": return_schema,
                        },
                    },
                },
                "4XX": error_response_schema,
                "5XX": error_response_schema,
            }

            def post(self):
                try:
                    payload = request.json
                except ValueError:
                    return {
                               "status": "error",
                               "message": f"Failed to parse JSON",
                           }, 400
                return respond(func, payload, schemas, return_schema)

        self.app.add_url_rule(
            f"{self.url_prefix}/api/{func.__name__}/",
            view_func=MyView.as_view(func.__name__),
            methods=["POST"]
        )

    def register_permissions(self):
        def decorator(func):
            return func  # TODO

        return decorator

    def register_authentication(self):
        def decorator(func):
            return func  # TODO

        return decorator
