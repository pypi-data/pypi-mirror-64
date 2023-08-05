from .gql_client_transport import GqlClientTransport
from .api.nodes import ProgramTrackActionResponse
from typing import Optional, Any, Callable
from .blocks_action_builder import BlocksActionBuilder
from typing import Awaitable
import asyncio
import traceback
from .gql import GqlClient
from .api import ObschartApiClient


OnResponseCallback = Callable[[ProgramTrackActionResponse], Awaitable[None]]


class ObschartClient(ObschartApiClient):
    def __init__(
        self,
        authentication_token: Optional[str] = None,
        api_url: Optional[str] = "https://api.obschart.com/",
    ):

        transport = GqlClientTransport(api_url)
        gql_client = GqlClient(transport=transport)
        super().__init__(gql_client=gql_client)

        if authentication_token:
            self.set_authentication_token(authentication_token)

    def on_response(self, on_response_callback: OnResponseCallback):
        async def main() -> Any:
            while True:
                responses = await self.poll_program_track_action_responses(
                    {"applicationId": {"eq": "me"}}
                )

                results = await asyncio.gather(
                    *[on_response_callback(response) for response in responses],
                    return_exceptions=True,
                )

                for result in results:
                    if isinstance(result, Exception):
                        exception = result
                        traceback.print_exception(None, exception, exception.__traceback__)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    def build_feedback_data(self):
        return BlocksActionBuilder()
