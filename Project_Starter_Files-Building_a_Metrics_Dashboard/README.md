**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

All the screenshot images are stored in the directory `answer-img`.

## Verify the monitoring installation

*TODO:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation

See screenshot Verify_the_monitoring_installation.JPG

## Setup the Jaeger and Prometheus source
*TODO:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.

See screenshot Setup_the_Jaeger_and_Prometheus_source.JPG

## Create a Basic Dashboard
*TODO:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.

See screenshot Create_a_Basic_Dashboard.JPG

## Describe SLO/SLI
*TODO:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.

The SLIs are the decription of concrete implemented metric how to messure the SLOs.

*Example SLOs*
*monthly uptime:* The availability of the application should be 99,5% of the month.
*request response time:* In 99,5% the application reponse time should be in 100 ms or less per month.

*Corresponding SLIs*
*monthly uptime:* 
Availability SLI = (ammount of HTTP 2xx requests / all HTTP requests) per month

*request response time:* 
Response time SLI = (ammount of HTTP requests with response time <= 100 ms / all HTTP requests) per month

## Creating SLI metrics.
*TODO:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs. 

Availability SLI = (ammount of HTTP 2xx requests / all HTTP requests) per month

Response time SLI = (ammount of HTTP requests with response time <= 100 ms / all HTTP requests) per month

Response time SLI = (ammount of HTTP requests with response time >= 100 ms and <= 2s/ all HTTP requests) per month

Error rate SLI = (HTTP 5xx requests / all HTTP requets) per month

CPU usgae < 85% in avarage per day


## Create a Dashboard to measure our SLIs
*TODO:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.

For uptime of the services I use the following metric:
Availability SLI = (ammount of HTTP 2xx requests / all HTTP requests)
sum(increase(flask_http_request_total{status=~"2.."}[1d]))/sum(increase(flask_http_request_total[1d]))

Measure 40x and 50x errors:
sum(increase(flask_http_request_total{status=~"4.."}[1d]))
sum(increase(flask_http_request_total{status=~"5.."}[1d]))

See screenshot Create_a_Dashboard_to_measure_our_SLIs.JPG

## Tracing our Flask App
*TODO:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here. Also provide a (screenshot) sample Python file containing a trace and span code used to perform Jaeger traces on the backend service.

I have extended the app.py file in the directory reference-app/backend which contains all the test endpoints I have used to create Grafana and Jaeger metric data.

Code screenshot see Tracing_our_Flask_App_Code.JPG

Jaeger screeshot see Tracing_our_Flask_App_Jaeger.JPG

## Jaeger in Dashboards
*TODO:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.

See screenshot Jaeger_in_Dashboards.JPG

## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue also include a screenshot of the tracer span to demonstrate how we can user a tracer to locate errors easily.

See screenshot Report_Error.JPG

TROUBLE TICKET

Name: Service endpoint get_slow is to slow

Date: 2025-04-10 14:53

Subject: The service endpoint get_slow takes 4.58 sec to answer.

Affected Area: endpoint get_slow

Severity: high

Description: From the Jaeger screenshot you can see that most of the time is consumed in the sub module "get_slow slow sub task". Please do futher investigation why we need such a lot of time in this module and how can we fix it.


## Creating SLIs and SLOs
*TODO:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name four SLIs that you would use to measure the success of this SLO.

Availability SLI = (ammount of HTTP 2xx requests / all HTTP requests) per month

Response time SLI = (ammount of HTTP requests with response time <= 100 ms / all HTTP requests) per month

Response time SLI = (ammount of HTTP requests with response time >= 100 ms and <= 2s/ all HTTP requests) per month

Error rate SLI = (HTTP 5xx requests / all HTTP requets) per month

## Building KPIs for our plan
*TODO*: Now that we have our SLIs and SLOs, create a list of 2-3 KPIs to accurately measure these metrics as well as a description of why those KPIs were chosen. We will make a dashboard for this, but first write them down here.

Availability SLI = (ammount of HTTP 2xx requests / all HTTP requests) >= 99,95%
sum(increase(flask_http_request_total{status=~"2.."}[30d]))/sum(increase(flask_http_request_total[30d]))

Error rate SLI = (HTTP 5xx requests / all HTTP requets) per month <= 0,05%
sum(increase(flask_http_request_total{status=~"5.."}[30d]))/sum(increase(flask_http_request_total[30d]))

## Final Dashboard
*TODO*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  

See screenshot Final_Dashboard.JPG