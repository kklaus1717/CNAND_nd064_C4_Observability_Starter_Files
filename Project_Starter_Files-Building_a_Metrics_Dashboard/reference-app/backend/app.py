import logging
from flask import Flask, render_template, request, jsonify
from flask import abort

import pymongo
from flask_pymongo import PyMongo

from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_flask_exporter import PrometheusMetrics
from flask_opentracing import FlaskTracing
import time
import random

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

metrics = PrometheusMetrics(app)
# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")

logging.getLogger("").handlers = []
logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_tracer(service):

    config = Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "logging": True,
            "reporter_batch_size": 1,
        },
        service_name=service,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(service_name_label=service),
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


tracer = init_tracer("Backend")
flask_tracer = FlaskTracing(tracer, True, app)


@app.route("/")
def homepage():
    with tracer.start_span("homepage") as span:
        span.set_tag("in_main", "Print homepage")
        return "Hello World Version 2"


@app.route("/api")
def my_api():
    with tracer.start_span("get_api") as span:
        span.log_kv({"event": "Do some job"})
        span.set_tag("in_api", "Respond with API")
        time.sleep(random.uniform(0, 1))
        with tracer.start_span("get_api sub task", child_of=span) as sub_span:
            sub_span.log_kv({"event": "Do some sub job"})
            time.sleep(random.uniform(0, 2))
        answer = "something api"
        return jsonify(repsonse=answer)

@app.route("/slow")
def get_slow():
    with tracer.start_span("get_slow") as span:
        span.log_kv({"event": "Do some slow job"})
        time.sleep(random.uniform(0, 1))
        with tracer.start_span("get_slow slow sub task", child_of=span) as sub_span:
            sub_span.log_kv({"event": "Do some slow sub job"})
            time.sleep(random.uniform(3, 4))
        answer = "something slow"
        return jsonify(repsonse=answer)

@app.route("/error400")
def get400():
    with tracer.start_span("get_error400") as span:
        span.log_kv({"event": "400 error"})
        answer = "something error 400"
        abort(400)
        return jsonify(repsonse=answer)

@app.route("/error500")
def get500():
    with tracer.start_span("get_error500") as span:
        span.log_kv({"event": "500 error"})
        answer = "something error 500"
        abort(500)
        return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
def add_star():
    with tracer.start_span("star") as span:
        try:
            span.set_tag("request_name", request.json["name"])
            star = mongo.db.stars
            name = request.json["name"]
            distance = request.json["distance"]
            star_id = star.insert({"name": name, "distance": distance})
            new_star = star.find_one({"_id": star_id})
            output = {"name": new_star["name"], "distance": new_star["distance"]}
        except Exception:
            logger.error("An error has occured: ", exc_info=True)
    return jsonify({"result": output})

@app.route("/star/<star_id>", methods=["GET"])
def get_star(star_id):
    with tracer.start_span("get_star") as span:
        output = {}
        try:
            output = {"name" : "Hans Schuster",
                      "age" : 34/0}
        except Exception:
            logger.error("An error has occured: ", exc_info=True)
            abort(500)
    return jsonify(output)


if __name__ == "__main__":
    app.run()
