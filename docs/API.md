# API Documentation

## Authentication

### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Campaigns

### List Campaigns

```http
GET /api/campaigns
Authorization: Bearer TOKEN
```

### Create Campaign

```http
POST /api/campaigns
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "name": "Test Campaign",
  "template": "google",
  "redirect_url": "https://www.google.com"
}
```

### Get Campaign

```http
GET /api/campaigns/{id}
Authorization: Bearer TOKEN
```

### Update Campaign

```http
PUT /api/campaigns/{id}
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "status": "active"
}
```

### Delete Campaign

```http
DELETE /api/campaigns/{id}
Authorization: Bearer TOKEN
```

## Victims

### List Victims

```http
GET /api/victims
Authorization: Bearer TOKEN
```

### Get Campaign Victims

```http
GET /api/victims?campaign_id={id}
Authorization: Bearer TOKEN
```

## Analytics

### Get Statistics

```http
GET /api/analytics
Authorization: Bearer TOKEN
```

## AI Engine

### Generate Template

```http
POST /api/ai/generate
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "url": "https://example.com/login",
  "platform": "custom"
}
```

## Evasion

### Check Evasion

```http
POST /api/evasion/check
Content-Type: application/json

{
  "user_agent": "Mozilla/5.0...",
  "ip": "192.168.1.1"
}
```

## Blockchain

### Verify Credentials

```http
POST /api/blockchain/verify
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

## Quantum Crypto

### Encrypt Data

```http
POST /api/quantum/encrypt
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "data": "sensitive information"
}
```

## Infrastructure

### Deploy Infrastructure

```http
POST /api/infrastructure/spin
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "provider": "docker",
  "port": 8080
}
```

### Destroy Infrastructure

```http
POST /api/infrastructure/destroy
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "id": "deployment_id"
}
```

## MFA Bypass

### Attempt Bypass

```http
POST /api/mfa/bypass
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "target": "user@example.com",
  "method": "relay"
}
```

## Payload Delivery

### Deliver Payload

```http
POST /api/payload/deliver
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "method": "email",
  "target": "user@example.com",
  "payload_id": "payload_id"
}
```

## Reconnaissance

### Scan Target

```http
POST /api/recon/target
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "target": "example.com"
}
```

## Social Engineering

### Engage Target

```http
POST /api/social/engage
Authorization: Bearer TOKEN
Content-Type: application/json

{
  "channel": "email",
  "to": "user@example.com",
  "subject": "Important Notification",
  "body": "..."
}
```
