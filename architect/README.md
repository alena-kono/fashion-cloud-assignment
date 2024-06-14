# Fashion Cloud Assignment: architect

[Architecture diagram](architecture-diagram.png)

## Description

Main goals of this architecture:
- [x] To create scalable and fault-tolerant data processing pipeline.
- [x] To provide high-performance via async processing.
- [x] To provide cost-efficiency.
- [x] To meet all business requirements.

### High-level design

To address main goals, I chose serverless architecture built upon AWS solutions landscape. 

#### Entrypoints

- Data producers send requests to API.
- API Load Balancer routes requests to auto-scaling group.
- Auto-scaling group scales automatically to provide high-availability. 
- An API gateway is a front door for API, routing requests and handling security.

Optionally:
- Connect API gateway with monitoring tools to enable performance and other monitoring.
- Add more regions to distribute our services worldwide.

#### Files cleaning

- Send json files to isolated AWS S3 Bucket.
- Trigger S3 upload event and send it to AWS SQS (queue service). This allows to queue scanning of multiple files. 
- Scan the files with antivirus software, move infected and cleaned files to different AWS S3 buckets.

Optionally:
- As we utilise AWS SQS, we are able to scan multiple files in parallel by creating an auto-scaling group.
 
#### Data validation and further processing

- Data processing block is triggered by AWS Lambda.
- Text files are distributed to AWS Glue Workflow, media files are distributed to another workflow where their different resolutions are created.
- AWS Glue handles crawling, data validation and normalisation.

AWS Glue has been chosen over AWS Data Pipeline solution because:
- It allows designing complex ETL pipelines.
- It automatically generates Scala or Python code for the ETL jobs that can be further customized. 
- Amazon keeps on enhancing Glue, while AWS Data Pipeline is stalled.

#### Data storage and catalogisation

- Processed text data is stored at AWS DynamoDB NoSQL database.
- AWS DynamoDB streams data to AWS OpenSearch to provide high-performance searching.
- Processed media files are stored at AWS S3 bucket.

AWS Dynamo has been chosen over AWS Redshift database because:
- It provides fast access to individual product details (e.g., retrieving a specific product by ID for product page display).
- It allows to update product information frequently (e.g., stock levels, pricing).

However, AWS Redshift could be added in the following cases:
- To perform complex analysis on product data (e.g., identifying top-selling products, analyzing sales trends by category).
- To run complex queries on historical data (e.g., analyzing sales performance over time).

#### Events processing and notifications
- All events emitted in cases of failures are streamlined to AWS EventBridge where are proccessing using configurable rules.
- AWS SNS (Simple Notification Service) notifies producers of failure events, e.g. sends them emails. 
 

#### Additions

They are not included into diagram, however should be considered:

- Performing backups.
- Logging.
- Monitoring.
- Network management (virtual private clouds, public and private subnets, etc.).
