# Exercice 3 :

src/api/dependencies.py

### Ce module fournit des dépendances FastAPI pour l'authentification et l'autorisation des utilisateurs via JWT.

## Utilisation :

À utiliser comme dépendances dans les routes FastAPI pour sécuriser l'accès selon le statut et le rôle de l'utilisateur.

## Dépendances externes :

- FastAPI (Depends, HTTPException, status)
- fastapi.security (OAuth2PasswordBearer)
- jose (jwt, JWTError)
- pydantic (ValidationError)
- sqlalchemy.orm (Session)

Modules internes pour la gestion des utilisateurs, des schémas de token, et la configuration.

from fastapi import Depends, HTTPException, status<br>
from fastapi.security import OAuth2PasswordBearer (Système d'authentification avec mot de passe)<br>
from jose import jwt, JWTError (Système des jetons)<br>
from pydantic import ValidationError<br>
from sqlalchemy.orm import Session<br>

from ..db.session import get_db<br>
from ..models.users import User<br>
from ..repositories.users import UserRepository<br>
from ..api.schemas.token import TokenPayload<br>
from ..utils.security import ALGORITHM<br>
from ..config import settings<br>

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

Cette ligne crée une instance de `OAuth2PasswordBearer`, utilisée pour récupérer et valider les tokens OAuth2 des requêtes entrantes.Le paramètre `tokenUrl` spécifie l'URL à laquelle les clients peuvent obtenir un token, généralement le point de terminaison de connexion de l'API. `settings.API_V1_STR` permet de construire dynamiquement l'URL du token en fonction de la version de l'API définie dans la configuration.

- `get_current_user` : Récupère l'utilisateur courant à partir du token JWT fourni. Lève une exception si le token est invalide ou si l'utilisateur n'existe pas.

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dépendance pour obtenir l'utilisateur actuel à partir du token JWT.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Impossible de valider les informations d'identification",
        )

    repository = UserRepository(User, db)
    user = repository.get(id=token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé",
        )
    return user

- `get_current_active_user` : Vérifie que l'utilisateur courant est actif. Lève une exception si l'utilisateur est inactif.

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dépendance pour obtenir l'utilisateur actif actuel.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilisateur inactif",
        )
    return current_user

- `get_current_admin_user` : Vérifie que l'utilisateur courant possède les droits administrateur. Lève une exception si l'utilisateur n'a pas les privilèges requis.

def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Dépendance pour obtenir l'utilisateur administrateur actuel.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Privilèges insuffisants",
        )
    return current_user

# Exercice 4 :

Ce module fournit des fonctions utilitaires pour le hachage de mots de passe, leur vérification et la création de jetons d'accès JWT.

Fonctions :

**create_access_token(subject, expires_delta=None) :** Génère un jeton d'accès JWT pour le sujet donné (identifiant utilisateur), avec une durée d'expiration optionnelle. Utilise la clé secrète et l'algorithme définis dans la configuration de l'application.<br>
**verify_password(plain_password, hashed_password) :** Vérifie un mot de passe en clair par rapport à sa version hachée en utilisant bcrypt.<br>
**get_password_hash(password) :** Hache un mot de passe en clair avec bcrypt.

# Dépendances :

**jose.jwt :** Pour l'encodage des jetons JWT.,<br>
**passlib.context.CryptContext :** Pour le hachage et la vérification des mots de passe.,<br>
**settings :** Configuration de l'application contenant SECRET_KEY et ACCESS_TOKEN_EXPIRE_MINUTES.