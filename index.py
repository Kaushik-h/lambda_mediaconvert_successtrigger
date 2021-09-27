import os
import psycopg2
import json

def lambda_handler(event, context):
	
	statusCode = 200
	body={}
	table_name="Media_media"
	bucket_name='s3://'+ os.environ['BucketName']

	try:
		path=event["detail"]["outputGroupDetails"][0]["outputDetails"][0]["outputFilePaths"][0]
		transcoded_path=path.replace(bucket_name,"")
		output_filename=transcoded_path.split("/")[-1]
		media_id=output_filename.split(".")[0]

		conn = psycopg2.connect(
		database="litap_DB", user='litap', password='q73ZmWuhtv6JaTJ', host='litap-db-alpha.copddvrpnnv0.us-east-2.rds.amazonaws.com', port= '5432')
		cursor = conn.cursor()
		cursor.execute("UPDATE \"" + table_name + "\" SET \"transcodedValue\" =\'" + transcoded_path + "\' WHERE \"mediaId\"=\'"+media_id+ "\';")

		cursor.execute("SELECT * FROM \"" + table_name + "\" WHERE \"mediaId\"=\'"+media_id+ "\';")
		print(cursor.fetchall())

		conn.commit()
		conn.close()

	except Exception as e:
		print ('Exception: %s' % e)
		statusCode = 500
		raise	

	finally:
		return {
			'statusCode': statusCode,
			'body': json.dumps(body),
			'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
		}


