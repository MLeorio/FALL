from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models import (
    Annonce,
    Annonce_Pydantic,
    AnnonceIn_Pydantic,
    Device,
    DeviceIn_Pydantic,
)
from config import Settings
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise


class Status(BaseModel):
    message: str


app = FastAPI(
    title="TOR API",
    debug=True,
    version="V1",
    description="API pour l'application des objets perdus ou retrouvés",
    docs_url="/",
)


@app.on_event("startup")
async def startup_event():
    settings = Settings()
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


@app.get("/annonces", response_model=List[Annonce_Pydantic])
async def get_annonces():
    """Recuperer toutes les annonces publiees sur la plateforme

    Returns:
        List[AnnonceIn_Pydantic]: La liste des annonces preformatees
    """
    return await Annonce_Pydantic.from_queryset(Annonce.all())


@app.get("/annonces/public", response_model=List[Annonce_Pydantic])
async def get_actives_annonces():
    """Retourne la liste des annonces actives; censees etre deja publiees sur la plateforme publique

    Returns:
        List[AnnonceIn_Pydantic]: La liste des annonces preformatees
    """
    return await Annonce.filter(actif=1, statut="fall").all()


@app.get("/annonces/private", response_model=List[Annonce_Pydantic])
async def get_inactive_annonce():
    """Retourne la liste des annonces inactives. Cette liste sera consultee par les admins pour valider les annonces

    Returns:
       List[AnnonceIn_Pydantic]: La liste des annonces preformatees
    """
    return await Annonce.filter(actif=0, statut="fall").all()


@app.post("/annonce/", response_model=Annonce_Pydantic)
async def create_annonce(annonce: AnnonceIn_Pydantic):
    """Methode pour la creation d'une annonce et la publiee sur la plateforme

    Args:
        annonce (AnnonceIn_Pydantic): Objet Annonce pour l'enregistrement

    Returns:
       Annonce_Pydantic : objet Annonce tout juste publiee
    """
    obj = await Annonce.create(**annonce.model_dump(exclude_unset=True))
    return await Annonce_Pydantic.from_tortoise_orm(obj)


@app.get(
    "/annonce/{id}",
    response_model=Annonce_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_annonce(annonce_id: int):
    """Recuperer une annonce publier selon son Id

    Args:
        annonce_id (int): id de l'annonce a recuperer

    Returns:
        AnnonceIn_Pydantic: Informations relatives a une annonce sans toutes les informations
    """
    return await Annonce_Pydantic.from_queryset_single(Annonce.get(id=annonce_id))


@app.put("/annonce/{id}", response_model=Annonce_Pydantic)
async def update_annonce(annonce_id: int, annonce: AnnonceIn_Pydantic):
    """Mettre a jour les informations d'une annonce

    Args:
        annonce_id (int): Id de l'annonce a modifier
        annonce (AnnonceIn_Pydantic): Objet avec les nouvelles valeurs a sauvergarder

    Returns:
        Annonce_Pydantic : Retour de l'objet mise a jour
    """
    await Annonce.filter(id=annonce_id).update(**annonce.model_dump(exclude_unset=True))
    return await Annonce_Pydantic.from_queryset_single(Annonce.get(id=annonce_id))


@app.get("/annonce/publier/{id}", response_model=Status)
async def publish_annonce(annonce_id: int):
    await Annonce.filter(id=annonce_id).update(actif=1, updated_at=datetime.now())
    return Status(message="L'annonce à bien été publiée")


@app.get("/annonce/done/{id}", response_model=Status)
async def acchieve_annonce(annonce_id: int):
    await Annonce.filter(id=annonce_id).update(
        statut="pupa", actif=0, updated_at=datetime.now()
    )
    return Status(message="Felicitation, objet bien rendu au proprietaire !")


@app.delete("/annonce/{id}", response_model=Status)
async def delete_annonce(annonce_id: int):
    """Suppression de l'annonce selectionner

    Args:
        annonce_id (int): Id de l'annonce a supprimer

    Raises:
        HTTPException: L'objet choisi n'est pas retrouver dans la base (Soumettre un nouvel Id)

    Returns:
        Status : Message de confirmation de la suppression de l'annonce
    """
    deleted_count = await Annonce.filter(id=annonce_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"L'annonce {annonce_id} n'a pas été trouvée"
        )
    return Status(message=f"L'annonce {annonce_id} a été supprimée")


@app.post("/installation/", response_model=Status)
async def get_device_info(device: DeviceIn_Pydantic):
    """Recuperation et sauvegarde des infos de l'appareil qui fait une installation

    Args:
        device (DevicesIn_Pydantic): Infos relatives a l'appareil

    Returns:
        Status: Message de confirmation de bonne installation
    """
    obj = await Device.create(**device.model_dump(exclude_unset=True))
    return Status(
        message=f"Nous sommes heureux de vous compter parmis nous, utilisateur {obj.device_id}"
    )
