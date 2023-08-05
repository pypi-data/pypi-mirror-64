from gql import gql
from .nodes import (
    Session,
    Image,
    imageFragment,
    ProgramInvitation,
    ProgramTrackActionResponse,
    programTrackActionResponseFragment,
    ProgramTrackAction,
    programTrackActionFragment,
    ProgramModule,
    programModuleFragment,
    Tag,
    tagFragment,
)
from .context import Context
from typing import Optional, Dict, Any, Callable
import datetime
from typing import Awaitable
import asyncio
import traceback
from ..gql import GqlClient

OnResponseCallback = Callable[[ProgramTrackActionResponse], Awaitable[None]]


class ObschartApiClient(object):
    _gql_client: GqlClient
    _context: Context

    def __init__(
        self, gql_client,
    ):
        super().__init__()

        self._gql_client = gql_client
        self._context = Context(self)

    def set_authentication_token(self, authentication_token: str):
        self._gql_client.transport.headers = self._gql_client.transport.headers or {}
        self._gql_client.transport.headers["Authorization"] = f"Bearer {authentication_token}"

    def _execute(self, query, variables: Optional[Dict[str, Any]] = None):
        return self._gql_client.execute(query, variables)

    def _execute_mutation(self, query, input: Optional[Dict[str, Any]] = None):
        variables = {"input": input}
        return self._execute(query, variables)

    async def create_session(self, email: str, password: str):
        query = gql(
            """
          mutation CreateSessionMutation($input: CreateSessionInput) {
            createSession(input: $input) {
              token
              session {
                id
              }
            }
          }
          """
        )

        input = {"password": password, "email": email}
        result = await self._execute_mutation(query, input)

        authentication_token = result["createSession"]["token"]
        self.set_authentication_token(authentication_token)

        return Session(result["createSession"]["session"], Context(self))

    async def poll_program_track_action_responses(self, filter: dict):
        query = gql(
            """
          query OnResponseQuery($filter: ProgramTrackActionResponseFilterInput) {
            programTrackActionResponses(filter: $filter, first: 9999) {
              edges {
                node {
                  ...ProgramTrackActionResponse
                }
              }
            }
          }
        """
            + programTrackActionResponseFragment
        )

        filter = filter.copy()
        now = datetime.datetime.utcnow()
        filter.update(
            {"createdAt": {"after": now.replace(tzinfo=datetime.timezone.utc).isoformat()}}
        )
        variables = {"filter": filter}

        while True:
            try:
                response = await self._execute(query, variables)
                edges = response["programTrackActionResponses"]["edges"]

                if len(edges) > 0:
                    break
            except Exception as exception:
                traceback.print_exception(None, exception, exception.__traceback__)

            await asyncio.sleep(1)

        responses: list[ProgramTrackActionResponse] = [
            ProgramTrackActionResponse(edge["node"], self._context) for edge in edges
        ]

        return responses

    async def create_program_track_action(self, data: Any, waits_for_feedback: bool):
        query = gql(
            """
          mutation CreateProgramTrackActionMutation($input: CreateProgramTrackActionInput!) {
            createProgramTrackAction(input: $input) {
              programTrackAction  {
                ...ProgramTrackAction
              }
            }
          }
          """
            + programTrackActionFragment
        )

        input = {"data": data, "waitsForFeedback": waits_for_feedback}
        result = await self._execute_mutation(query, input)

        return ProgramTrackAction(
            result["createProgramTrackAction"]["programTrackAction"], self._context
        )

    async def create_image(self, image: Any):
        query = gql(
            """
          mutation CreateImageMutation($input: CreateImageInput!) {
            createImage(input: $input) {
              image  {
                ...Image
              }
            }
          }
          """
            + imageFragment
        )

        input = {"image": image}
        result = await self._execute_mutation(query, input)

        return Image(result["createImage"]["image"], self._context)

    async def create_program_invitation(self, program_id: str):
        query = gql(
            """
          mutation CreateProgramInvitationMutation($input: CreateProgramInvitationInput!) {
            createProgramInvitation(input: $input) {
              programInvitation  {
                id
              }
            }
          }
          """
        )

        input = {"programId": program_id}
        result = await self._execute_mutation(query, input)

        return ProgramInvitation(
            result["createProgramInvitation"]["programInvitation"], self._context
        )

    async def send_program_invitation_sms(self, program_invitation_id: str, phone_number: str):
        query = gql(
            """
          mutation SendProgramInvitationSmsMutation($input: SendProgramInvitationSmsInput) {
            sendProgramInvitationSms(input: $input) {
              programInvitation  {
                id
              }
            }
          }
          """
        )

        input = {"id": program_invitation_id, "phoneNumber": phone_number}
        result = await self._execute(query, input)

        return ProgramInvitation(
            result["sendProgramInvitationSms"]["programInvitation"], self._context
        )

    async def get_current_session(self):
        query = gql(
            """
          query CurrentSessionQuery {
            currentSession {
              id
              user {
                id
                name
                email
              }
            }
          }
          """
        )

        result = await self._execute(query)

        return Session(result["currentSession"], self._context)

    async def get_program_track_action_response(self, id):
        query = gql(
            """
          query ProgramTrackActionResponseQuery($id: ID) {
            programTrackActionResponse(id: $id) {
              ...ProgramTrackActionResponse
            }
          }
          """
            + programTrackActionResponseFragment
        )

        variables = {"id": id}
        result = await self._execute(query, variables)

        return ProgramTrackActionResponse(result["programTrackActionResponse"], self._context)

    async def update_program_track_action_response(
        self, id: str, feedback_program_track_action_id: str
    ):
        query = gql(
            """
            mutation UpdateProgramTrackActionResponseMutation($input: UpdateProgramTrackActionResponseInput!)  {
                updateProgramTrackActionResponse(input: $input) {
                    programTrackActionResponse {
                        ...ProgramTrackActionResponse
                    }
                }
            }
        """
            + programTrackActionResponseFragment
        )

        input = {
            "id": id,
            "feedbackProgramTrackActionId": feedback_program_track_action_id,
        }
        result = await self._context.client._execute_mutation(query, input)

        return ProgramTrackActionResponse(
            result["updateProgramTrackActionResponse"]["programTrackActionResponse"], self._execute,
        )

    async def list_program_modules(self, filter: dict):
        query = gql(
            """
          query ListProgramModules($filter: ProgramModuleFilterInput) {
            programModules(filter: $filter, first: 9999) {
              edges {
                node {
                  ...ProgramModule
                }
              }
            }
          }
        """
            + programModuleFragment
        )

        variables = {"filter": filter}
        response = await self._execute(query, variables)

        nodes: list[ProgramModule] = [
            ProgramModule(edge["node"], self._context)
            for edge in response["programModules"]["edges"]
        ]

        return nodes

    async def list_tags(self, filter: dict):
        query = gql(
            """
          query ListTags($filter: TagFilterInput) {
            tags(filter: $filter, first: 9999) {
              edges {
                node {
                  ...Tag
                }
              }
            }
          }
        """
            + tagFragment
        )

        variables = {"filter": filter}
        response = await self._execute(query, variables)

        nodes: list[Tag] = [Tag(edge["node"], self._context) for edge in response["tags"]["edges"]]

        return nodes

    async def update_program_module(self, id: str, is_public: bool):
        query = gql(
            """
            mutation UpdateProgramModuleMutation($input: UpdateProgramModuleInput!)  {
                updateProgramModule(input: $input) {
                    programModule {
                        ...ProgramModule
                    }
                }
            }
        """
            + programModuleFragment
        )

        input = {
            "id": id,
            "isPublic": is_public,
        }
        result = await self._context.client._execute_mutation(query, input)

        return ProgramModule(result["updateProgramModule"]["programModule"], self._execute,)
