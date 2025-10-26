from datetime import datetime, timezone
from ipaddress import IPv4Address

from pydantic import BaseModel
from server.config.settings import Settings
from server.core.deps import Mailer
from ..entities import User, AuthTokenInfo
from ..repositories import AuthTokenRepository
from ...utils import generate_auth_token

class DTO(BaseModel):
    access_token: str
    token_type: str
    

async def handle(
    user: User,
    repository: AuthTokenRepository,
    mailer: Mailer,
    settings: Settings,
    client_ip: IPv4Address,
    user_agent: str
) -> DTO:
    active_sessions = list(await repository.get_by_user_id(user.id))
    
    token = generate_auth_token()
    token_info = AuthTokenInfo.create(
        token=token,
        client_ip=client_ip,
        user_agent=user_agent,
        user_id=user.id,
        expires=datetime.now(timezone.utc) + settings.token_lifetime
    )

    repository.add(token_info)
    await repository.flush()
    await repository.refresh(token_info)

    if (
        active_sessions
        and (token_info.client_ip, token_info.user_agent) not in { 
            (session.client_ip, session.user_agent) 
            for session in active_sessions
        }
    ):
        await mailer.send_mail(
            subject="Обнаружен вход c нового устройства",
            recipients=[user.email],
            body=f"""
                Был замечен параллельный вход с вашей учетной записи.\n
                IP-адрес: {client_ip}\n
                User-agent: {user_agent}\n
                Если это были не вы, пожалуйста, завершите все сессии и запросите смену пароля.
            """
        )

    return DTO(access_token=token, token_type="bearer")