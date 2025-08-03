import jwt
from tech_professional_coacher.utils.config.settings import settings
from jwt import PyJWKClient,ExpiredSignatureError, InvalidTokenError
from tech_professional_coacher.models.errors import TokenExpiredError, InvalidTokenAuthError

class JWTAuthenticationService:
    def __init__(self):
        print("keyclok jwks url", settings.KEYCLOAK_JWKS_URL)
        self.jwks_client = PyJWKClient(settings.KEYCLOAK_JWKS_URL)


    def validate_token(self, token: str) -> dict:
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token).key
            decoded_token = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                audience="account"  # ajuste conforme necessário
            )
            return decoded_token

        except ExpiredSignatureError:
            raise TokenExpiredError("Token has expired.")

        except InvalidTokenError as e:
            raise InvalidTokenAuthError(f"Invalid token: {str(e)}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(".env")
    jwks_url = "http://keycloak.localhost.nip.io/realms/test-dev/protocol/openid-connect/certs"
    service = JWTAuthenticationService()

    token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJLR0FiQTlUaWs2bFE5bTJUWUVqY19iOHREdWJXMXBZckUtV0JTWGlQa2o4In0.eyJleHAiOjE3NTM4MjUyMjMsImlhdCI6MTc1MzgyNDkyMywianRpIjoib25ydHJvOjFlN2QwODhmLWNjMDMtZmQ4Zi05NWI5LWUwZDlhNjUxM2Q0MiIsImlzcyI6Imh0dHA6Ly9rZXljbG9hay5sb2NhbGhvc3QubmlwLmlvL3JlYWxtcy90ZXN0LWRldiIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJkZjgwMjU3NS1mZDAxLTQ3ZDQtYmRlMi05ZDI3ZTliOTI4NzYiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ0ZXN0LWRldi1jbGllbnQiLCJzaWQiOiJhYTM1MDNjMi01ZWFmLTRkNTAtODM3OC0yNDlhY2ViMzY2ZmQiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vd3d3LmtleWNsb2FrLm9yZyJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtdGVzdC1kZXYiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJ0ZXN0IHRlc3QiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ0ZXN0IiwiZ2l2ZW5fbmFtZSI6InRlc3QiLCJmYW1pbHlfbmFtZSI6InRlc3QiLCJlbWFpbCI6InRlc3RAdGVzdC5jb20ifQ.fK5Fn7wPMWV9cTkX_OTI0MPnV6FX9GKEronxAhR2L055MFvV1uJtWu-33tfionw-fBWouxMJHl0m0De-XzllwY9gbl-ennNiR6h81Xb0RmN9RxBp8XIRgO4kP0EB755d-wA8lSCbPtD6U8B0FVjmht7w6JROexniRexsqm6QIQK0nPGHecUYYbkRrsGG2gx4IFvRiOCjI2mlaVJ0o0xNJSyWyXCFI1Ld-tUlJvXXRJTakEgi-DedIROZ81TlPx1eUIypn5ZnFbqGbOKG3syt3QNgZQdTQg8j0fkb83_QycBYv-BysuoQ_Bb6SEZopSuB4733CubHQPIDWA7t6PAGrA"
    decoded = service.validate_token(token)
    print(decoded)
