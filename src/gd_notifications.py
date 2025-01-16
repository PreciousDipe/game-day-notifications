import os
import json
import urllib.request
from datetime import datetime, timedelta, timezone
import boto3

def format_game_data(game):
    status = game.get("Status", "Unknown")
    away_team = game.get("AwayTeam", "Unknown")
    home_team = game.get("HomeTeam", "Unknown")
    final_score = f"{game.get('AwayTeamScore', 'N/A')}-{game.get('HomeTeamScore', 'N/A')}"
    start_time = game.get("DateTime", "Unknown")
    channel = game.get("Channel", "Unknown")
    
    quarters = game.get("Quarters", [])
    quarter_scores = ', '.join([f"Q{q['Number']}: {q.get('AwayScore', 'N/A')}-{q.get('HomeScore', 'N/A')}" for q in quarters])
    
    if status == "Final":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Final Score: {final_score}\n"
            f"Start Time: {start_time}\n"
            f"Channel: {channel}\n"
            f"Quarter Scores: {quarter_scores}\n"
        )
    elif status == "InProgress":
        last_play = game.get("LastPlay", "N/A")
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Current Score: {final_score}\n"
            f"Last Play: {last_play}\n"
            f"Channel: {channel}\n"
        )
    elif status == "Scheduled":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Start Time: {start_time}\n"
            f"Channel: {channel}\n"
        )
    else:
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Details are unavailable at the moment.\n"
        )

def lambda_handler(event, context):
    api_key = os.getenv("NBA_API_KEY")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")
    dynamodb = boto3.resource('dynamodb')
    table_name = os.getenv("DYNAMODB_TABLE").strip()
    table = dynamodb.Table(table_name)

    utc_now = datetime.now(timezone.utc)
    central_time = utc_now - timedelta(hours=6)
    today_date = central_time.strftime("%Y-%m-%d")
    
    api_url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{today_date}?key={api_key}"
    
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            if not data:
                return {"statusCode": 404, "body": "No games available"}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error fetching data: {e}"}
    
    messages = [format_game_data(game) for game in data]
    final_message = "\n---\n".join(messages) if messages else "No games available for today."
    
    game_items = []
    for game in data:
        try:
            item = {
                'GameID': str(game.get('GameID', 'Unknown')),
                'DateTime': game.get('DateTime'),
                'Status': game.get('Status', 'Unknown'),
                'AwayTeam': game.get('AwayTeam', 'Unknown'),
                'HomeTeam': game.get('HomeTeam', 'Unknown'),
                'StartTime': game.get('DateTime', 'Unknown'),
                'Channel': game.get('Channel', 'Unknown'),
                'LastUpdated': datetime.now().isoformat()
            }
            table.put_item(Item=item)
            game_items.append(item)
        except Exception as e:
            return {"statusCode": 500, "body": f"Error pushing data to DynamoDB: {e}"}
    
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=final_message,
            Subject="NBA Game Updates"
        )
    except Exception as e:
        return {"statusCode": 500, "body": f"Error publishing to SNS: {e}"}
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "data": game_items
        })
    }

# Additional handler for fetching games from DynamoDB
async def fetch_games_handler(event):
    try:
        dynamodb = boto3.client('dynamodb')
        params = {
            "TableName": "NBARESULTS",  # Replace with your table name
        }

        result = await dynamodb.scan(params).promise()  # Fetch all records from the table
        games = result.get('Items', [])

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",  # Enable CORS for your frontend
            },
            "body": json.dumps(games),  # Return games as an array of objects
        }
    except Exception as error:
        print("Error fetching data from DynamoDB:", error)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to fetch data"}),
        }