from fastmcp import FastMCP
from fastmcp.server.auth import MultiAuth, OAuthProxy
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.providers import FileSystemProvider, SkillsDirectoryProvider
from mcp_types import (
    CompletionArgument,
    CompletionContext,
    PromptReference,
    ResourceTemplateReference,
)

from utils import BASE_DIR

upstream_verifier = JWTVerifier(
    jwks_uri="https://login.example.com/.well-known/jwks.json",
    issuer="https://login.example.com",
    audience="my-app",
)

auth = MultiAuth(
    server=OAuthProxy(
        upstream_authorization_endpoint="http://127.0.0.1:8000/o/authorize/",
        upstream_token_endpoint="https://login.example.com/oauth/token",
        upstream_client_id="mcprouter",
        upstream_client_secret="secret",
        token_verifier=upstream_verifier,
        base_url="http://127.0.0.1:8000",
    ),
    verifiers=[
        JWTVerifier(
            jwks_uri="https://internal-issuer.example.com/.well-known/jwks.json",
            issuer="https://internal-issuer.example.com",
            audience="my-mcp-server",
        ),
    ],
)

mcp = FastMCP(
    name='Global MCP server',
    auth=auth,
    on_duplicate='ignore',
    strict_input_validation=False,
    providers=[
        FileSystemProvider(BASE_DIR.joinpath('components')),
        SkillsDirectoryProvider(roots=[BASE_DIR.joinpath('.claude', 'skills')])
    ]
)


@mcp.completion
async def completion(ref: PromptReference | ResourceTemplateReference, argument: CompletionArgument, context: CompletionContext | None = None):
    pass
