<div align="center">
  <p>
    <a href="https://pypi.org/project/fastapi_oauth2_service/"><img src="https://github.com/abdoulfataoh/fastapi-oauth2-service/blob/master/docs/icon.png" style="width:80px;height:80px;"></a>
  </p>
  <h3>fastapi oauth2 service</h3>
</div>

<div align="center">
  <p>
    <a href="https://github.com/abdoulfataoh/fastapi-oauth2-service/actions/workflows/test.yaml"><img src="https://github.com/abdoulfataoh/fastapi-oauth2-service/actions/workflows/test.yaml/badge.svg"></a>
  </p>
  <p>A FastAPI-based OAuth2 service that enables secure user authentication and authorization, providing token management and API access control for seamless integration with applications.</p>
</div>

### Features
- [x] CRUD Users
- [x] Reset User Password via email or sms
- [x] Admin UI panel

### Oauth2 code Flow

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': 'transparent', 'secondaryColor': 'transparent', 'tertiaryColor': 'transparent', 'actorTextColor': '#000000', 'lineColor': '#00FF00', 'primaryBorderColor': '#9c1ca3'}}}%%

sequenceDiagram
    participant User
    participant Client as ClientApplication
    participant Auth as AuthenticationBackend

    User->>Client: 1. Request App access.
    Client-->>User: 2. 302 Redirect User to Auth.
    User->>Auth: 3. Connect to Auth and grant access to the app using the user's username, password and 2FA.
    Auth-->>User: 4. 302 Redirect to App, Return authorization code.
    User->>Client: 5. Connect to App and provide authorization code.
    Client->>Auth: 6. Request Exchange authorization using an access code.
    Auth-->>Client: 7. Return access token.
```

