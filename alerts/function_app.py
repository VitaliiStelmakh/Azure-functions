import azure.functions as func
import logging
import http.client
import json
import os

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="blob/{name}.json", connection="fileblob123_STORAGE") 
def blob_trigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob\nName: {myblob.name}")
    
    # Notification message
    message = f"New file uploaded: {myblob.name}"
    
    discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    # Send notification to Discord
    send_notification(discord_webhook_url, {"content": message})
    # Send notification to Slack
    send_notification(slack_webhook_url, {"text": message})

def send_notification(webhook_url, payload):
    try:
        # Parse the URL to extract the host and path
        parsed_url = http.client.urlsplit(webhook_url)
        host = parsed_url.hostname
        path = parsed_url.path
        
        # Create an HTTP connection
        connection = http.client.HTTPSConnection(host)
        
        # Send the POST request
        connection.request("POST", path, body=json.dumps(payload), headers={"Content-Type": "application/json"})
        response = connection.getresponse()
        
        # Log the response status and data
        logging.info(f"Response from {webhook_url} status: {response.status}")
        logging.info(f"Response body: {response.read().decode()}")

        # Close the connection
        connection.close()
    except Exception as e:
        logging.error(f"Failed to send notification via {webhook_url}: {str(e)}")

