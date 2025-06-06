from dataclasses import dataclass

from Template.application.common.interactor import Interactor
from Template.application.common.uow import UnitOfWork
from Template.application.common.repositories import UserRepository

from Template.domain.entities.user import User
from Template.domain.value_objects.user import UserId
from Template.domain.services.user import UserService


@dataclass(frozen=True)
class UserInputDTO:
    user_id: UserId


@dataclass(frozen=True)
class UserOutputDTO:
    user_id: UserId


class CreateUser(Interactor[UserInputDTO, UserOutputDTO]):
    def __init__(
        self,
        repository: UserRepository,
        user_service: UserService,
        uow: UnitOfWork,
    ):
        self.repository = repository
        self.user_service = user_service
        self.uow = uow

    async def __call__(self, data: UserInputDTO) -> UserOutputDTO:
        user: User = self.user_service.create(data.user_id)

        user_exists: bool = await self.repository.exists(data.user_id)

        if not user_exists:
            await self.repository.create(user)
            await self.uow.commit()

        return UserOutputDTO(user_id=user.user_id)
