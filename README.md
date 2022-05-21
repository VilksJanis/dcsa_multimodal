# Submission project for "Multimodal Hackathon Amsterdam: DCSA Maritime"

## ! PLEASE REFER TO THE OFFICIAL DCSA JIT DOCUMENTATION AT https://dcsa.org/standards/jit-port-call/

## Prerequisites/Dependencies

1. Installed docker and docker-compose;
2. Google Maps API key
3. Access DCSA API (TERMINAL and CARRIER):
    - API base url for events;
    - TOKEN URL;
    - Client id;
    - Client secret.

## Running process:

1. update environment variables for `docker-compose.yaml`
    ```
    version: '3.8'
    services:
    api:
        environment:
        - GOOGLE_MAPS_API_KEY=
        - API_BASE_URL_TERMINAL=
        - API_CLIENT_ID_TERMINAL=
        - API_CLIENT_SECRET_TERMINAL=
        - API_BASE_URL_CARRIER=
        - API_CLIENT_ID_CARRIER=
        - API_CLIENT_SECRET_CARRIER=
        - TOKEN_URL=
    ```

2. run `docker-compose up`
3. access dashboard via `http://127.0.0.1:5000/dashboard`

