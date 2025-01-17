# NBA Game Day Notifications Website

## **Project Overview**
This project is an alert system that sends real-time NBA game day score notifications to a webpage and subscribed users via HTTP requests and SMS/Email. It leverages **Amazon SNS**, **AWS Lambda and Python**, **Amazon EvenBridge**, **NBA APIs**, **Amazon Dynamodb**, and **Web UI (HTML, CSS, and Javascript)** to provide sports fans with up-to-date game information. The project demonstrates cloud computing principles and efficient notification mechanisms.


## **Technical Architecture**
![nba_API](https://github.com/PreciousDipe/game-day-notifications/blob/main/assets/game-day-notifications.drawio.svg)

---
link to the NBA Notification Webpage ![link](https://preciousdipe.github.io/game-day-notifications/nba.html)
---
## **Features**
- Fetches live NBA game scores using an external API.
- Sends formatted score updates to subscribers via SMS/Email using Amazon SNS.
- Scheduled automation for regular updates using Amazon EventBridge.
- Designed with security in mind, following the principle of least privilege for IAM roles.

## **Prerequisites**
- Free account with subscription and API Key at [sportsdata.io](https://sportsdata.io/)
- Personal AWS account with basic understanding of AWS and Python

---


## **Technologies**
- **Cloud Provider**: AWS
- **Core Services**: SNS, Lambda, EventBridge
- **External API**: NBA Game API (SportsData.io)
- **Programming Language**: Python 3.x, HTML, CSS, JavaScript
- **IAM Security**:
  - Least privilege policies for Lambda, SNS, and EventBridge, Dynamodb

---

## **Project Structure**
```bash
game-day-notifications/
├── lambda/
│   ├── gd_notifications.py       # Main lambda function code
├── src/
│   ├── nba.css         # Main css code
├── ├── nba.js          # Main javascript code
├── policies/
│   ├── gb_sns_policy.json           # SNS publishing permissions
├── .gitignore
├── nba.html            # Main html code
└── README.md                        # Project documentation
```

## **Setup Instructions**

### **Clone the Repository**
```bash
git clone https://github.com/PreciousDipe/game-day-notifications.git
cd game-day-notifications
```

### **What I Learned**
1. Designing a notification system with AWS SNS and Lambda.
2. Securing AWS services with least privilege IAM policies.
3. Automating workflows using EventBridge.
4. Integrating external APIs into cloud-based workflows.
5. Storing extracted data in DynamoDB to enable personalized notifications and improve user engagement.
6. Building and deploying an intuitive web interface to view live updates seamlessly.
