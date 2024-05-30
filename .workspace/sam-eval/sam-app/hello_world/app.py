import json
import os

from pyathena import connect
import pandas as pd


def calculate_success_rates():
    """Calculate the success rates for each spot on the basketball court.
    """
    stage_bucket_name = "shooting-insights-athena-results"
    stage_bucket_region = "us-east-1"
    source_bucket_name = "shooting-insights-data"
    source_bucket_region = "us-east-1"
    source_json_paths = [
        "/collection/midrange/",
        "/collection/threepoint/",
    ]

    for path in source_json_paths:
        path_name = os.path.basename(os.path.normpath(path))

        # Connect to Athena
        conn = connect(s3_staging_dir=f's3://{stage_bucket_name}/sam-eval-athena-results/{path_name}/',
                       region_name=stage_bucket_region)

        # Define the Athena queries
        create_table_query = f"""
        CREATE EXTERNAL TABLE IF NOT EXISTS basketball_shots_{path_name} (
        `spot_1` int,
        `spot_2` int,
        `spot_3` int,
        `spot_4` int,
        `spot_5` int,
        `spot_6` int,
        `spot_7` int,
        `spot_8` int,
        `spot_9` int,
        `spot_10` int,
        `spot_11` int,
        `temp` int,
        `date` string,
        `time` string
        )
        ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
        WITH LOCATION 's3://{source_bucket_name}{path}'
        TBLPROPERTIES ('has_encrypted_data'='false');
        """

        calculate_success_rate_query = """
        SELECT
        (SUM(spot_1) + SUM(spot_2) + SUM(spot_3) + SUM(spot_4)) / (4 * COUNT(*)) AS left_success_rate,
        (SUM(spot_5) + SUM(spot_6) + SUM(spot_7)) / (3 * COUNT(*)) AS center_success_rate,
        (SUM(spot_8) + SUM(spot_9) + SUM(spot_10) + SUM(spot_11)) / (4 * COUNT(*)) AS right_success_rate
        FROM basketball_shots;
        """

        # Execute the queries
        pd.read_sql(create_table_query, conn)
        success_rates = pd.read_sql(calculate_success_rate_query, conn)

        # Print the success rates
        print(success_rates)


def lambda_handler(event, context):
    """The entrypoint of the lambda invocation.
    """
    try:
        # Connect to Athena and execute the queries
        calculate_success_rates()
    except Exception as e:
        # Log the exception
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred')
        }