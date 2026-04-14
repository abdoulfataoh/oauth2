<div align="center">
  <p>
    <img src="docs/icon.png" style="width:80px;height:80px;">
  </p>
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=E9205E&width=170&lines=Oauth2+service" alt="Typing SVG" />
  </a>
</div>

<div align="center">
  <p>
    <a href="https://github.com/abdoulfataoh/fastapi-oauth2-service/actions/workflows/test.yaml"><img src="https://github.com/abdoulfataoh/fastapi-oauth2-service/actions/workflows/test.yaml/badge.svg"></a>
  </p>
  <p>
    A FastAPI-based authentication server implementing OAuth2 Authorization Code Flow with PKCE, user authentication, OTP verification, and consent-based authorization.
</p>
</div>

### Features

- [x] OAuth2 Authorization Code Flow with PKCE
- [x] Secure access token (JWT)
- [x] Public user registration with OTP verification (email/SMS)
- [x] User authentication and consent-based authorization
- [x] OAuth client (application) registration and management
- [x] Scope-based access control
- [x] Protection against user enumeration and brute-force attacks
- [x] Admin panel for managing users and OAuth clients



### Requirements

- Python 3.10+
- PostgreSQL / MySQL / SQLite
- Make (optional)
- poetry (optional)

### Oauth2 code Flow with PKCE Diagram

```mermaid

sequenceDiagram
    participant User
    participant ClientApp
    participant AuthServerFront
    participant AuthServerBackend

    %% Step 0: Entry point
    User->>ClientApp: Request application access

    %% Step 1: Start OAuth
    User->>ClientApp: Click "Login with OAuth"
    ClientApp-->>User: Redirect /authorize
    User->>AuthServerBackend: GET /authorize

    %% Step 2: Auth check
    alt User not authenticated
        AuthServerBackend-->>User: Redirect /login?request_id=xxx
        User->>AuthServerFront: Load /login
        User->>AuthServerFront: Submit credentials
        AuthServerFront->>AuthServerBackend: POST /login
        AuthServerBackend-->>User: Set cookie + redirect /consent
    else User already authenticated
        AuthServerBackend-->>User: Redirect /consent?request_id=xxx
    end

    %% Step 3: Consent
    User->>AuthServerFront: Load /consent
    AuthServerFront->>AuthServerBackend: GET /consent-data

    alt User approves
        User->>AuthServerFront: Click "Approve"
        AuthServerFront->>AuthServerBackend: POST /consent

        AuthServerBackend-->>User: Redirect client/callback?code=xxx&state=xxx
        User->>ClientApp: GET /callback

        %% Step 4: Token exchange
        ClientApp->>AuthServerBackend: POST /token (code + code_verifier)

        alt Code valid
            AuthServerBackend-->>ClientApp: access_token
        else Invalid code
            AuthServerBackend-->>ClientApp: error
        end

    else User denies
        User->>AuthServerFront: Click "Deny"
        AuthServerFront->>AuthServerBackend: POST /consent (deny)
        AuthServerBackend-->>User: Redirect with error=access_denied
    end

```

### Development

###### Install dependencies

```bash
poetry install
poetry shell
````

###### Available commands

```bash
  make help
```

```bash
Available commands:
--------------------------------
make help            - Display this help message
make dev             - Run development server
make prod            - Run production server
make test            - Run tests
make lint            - Run linter
make docker-build    - Build docker image
make test-all        - Run lint + tests

Database commands:
--------------------------------
make db-migrate m='msg' - Create migration
make db-upgrade        - Apply migrations
make db-downgrade      - Rollback last migration
make db-current        - Show current revision
make db-history        - Show migration history
make db-reset          - Reset DB (dev only)

Cleanup:
--------------------------------
make reset            - Reset DB + clean cache
```

### Run local server

###### Setup database

```bash
make db-migrate
make db-upgrade
```

###### Start server

```bash
make dev
````


### Project Configuration

This document lists all environment variables used to configure the application.



###### General Variables
| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| TEST | bool | Enable test mode | false |
| DEBUG | bool | Debug mode (linked to TEST) | false |


###### Database
| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| DATABASE_TYPE | str | Database type (sqlite3, mysql, postgresql) | sqlite3 |
| DATABASE_SERVER | str | Database host | - |
| DATABASE_USER | str | Database username | - |
| DATABASE_PASSWORD | str | Database password | - |
| DATABASE_NAME | str | Database name | - |


###### OAuth UI (Frontend)
| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| OAUTH_UI_URI | str | Frontend base URL | http://localhost:5173 |
| OAUTH_UI_LOGIN_URL | derived | Login URL | {OAUTH_UI_URI}/login |
| OAUTH_UI_CONSENT_URL | derived | Consent URL | {OAUTH_UI_URI}/consent |
| OAUTH_USER_ACCOUNT_URL | derived | User account URL | {OAUTH_UI_URI}/account |

###### Cookies and Sessions
| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| UI_COOKIES_EXPIRE_NAME | str | Session cookie name | UI_COOKIES |
| UI_COOKIES_EXPIRE_SECONDS | int | Expiration duration (seconds) | 10800 |
| UI_COOKIES_ONLY_ON_HTTPS | bool | Restrict cookies to HTTPS | false |


###### Security (JWT and OTP)
| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| JWT_SECRET_KEY | str | Secret key for JWT signing | 1234 |
| JWT_ALGORITHM | str | JWT algorithm | HS256 |
| OTP_MAX_ATTEMPTS | int | Maximum OTP retries | 5 |
| OTP_EXPIRE_SECOND | int | OTP expiration (seconds) | 180 |


###### OAuth API (Backend)
| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| OAUTH_API_PREFIX | str | API route prefix | /oauth2 |
| OAUTH_API_URI | str | Backend base URI | localhost:8000 |



###### Token Expiration
| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| REQUEST_AUTHORIZATION_EXPIRE_SECONDS | int | Auth request lifetime | 180 |
| AUTHORIZATION_CODE_EXPIRE_SECONDS | int | Auth code lifetime | 60 |
| ACCESS_TOKEN_EXPIRE_SECONDS | int | Access token lifetime | 600 |
