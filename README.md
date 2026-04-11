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
    A secure OAuth2 authorization server built with FastAPI, implementing the Authorization Code Flow with PKCE for internal and SaaS applications. 
    It provides user authentication, OTP verification, and a consent-based authorization system with strong security and clean architecture.
</p>
</div>

### Features

- [x] OAuth2 Authorization Code Flow with PKCE
- [x] Secure access and refresh token management (JWT)
- [x] Public user registration with OTP verification (email/SMS)
- [x] User authentication and consent-based authorization
- [x] OAuth client (application) registration and management
- [x] Scope-based access control
- [x] Token expiration and revocation
- [x] Protection against user enumeration and brute-force attacks
- [x] Admin panel for managing users and OAuth clients
- [x] Built with FastAPI and clean, modular architecture

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
