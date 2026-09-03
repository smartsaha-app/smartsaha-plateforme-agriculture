"""
apps/crops/views.py

-------------------

ViewSets pour Crop, Variety, StatusCrop, ParcelCrop.
"""

from django.db import models
from django.utils.decorators import method_decorator

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiTypes,
)

from apps.core.mixins import CacheInvalidationMixin, BaseModelViewSet
from apps.crops.models import Crop, StatusCrop, Variety, ParcelCrop
from apps.groups.models import MemberGroup

from apps.crops.serializers import (
    CropSerializer,
    StatusCropSerializer,
    VarietySerializer,
    ParcelCropSerializer,
    FAO56Serializer,
)

from services.flask_fao56 import (
    fao56_tree,
    fao56_other,
    FlaskFAO56Error,
)


# ============================================================
# CONFIGURATION FAO-56
# ============================================================

# Correspondance :
# nom utilisé dans Django -> nom attendu par le service FAO-56
FAO56_CROP_MAPPING = {

    # --------------------------------------------------------
    # Cultures en anglais / noms FAO-56
    # --------------------------------------------------------

    "almond": "almond",
    "apple": "apple",
    "avocado": "avocado",
    "cacao": "cacao",
    "citrus": "citrus",
    "coffee": "coffee",
    "grapewine": "grapewine",
    "mango": "mango",
    "peach": "peach",
    "strawberry": "strawberry",
    "sugarcane": "sugarcane",
    "vanilla": "vanilla",
    "walnut": "walnut",

    "onion": "onion",
    "potato": "potato",
    "carrots": "carrots",
    "maize": "maize",
    "celery": "celery",
    "lettuce": "lettuce",
    "spinach": "spinach",
    "radish": "radish",
    "eggplant": "eggplant",
    "tomato": "tomato",
    "sweet potato": "sweet potato",
    "cassava": "cassava",
    "beans green": "beans green",
    "beans": "beans",
    "peas": "peas",
    "soybeans": "soybeans",
    "cotton": "cotton",
    "sesame": "sesame",
    "sunflower": "sunflower",
    "millet": "millet",
    "sorghum": "sorghum",
    "rice": "rice",
    "pineapple": "pineapple",
    "grapes": "grapes",
    "pistachios": "pistachios",

    # --------------------------------------------------------
    # Français -> FAO-56
    # --------------------------------------------------------

    "riz": "rice",

    "maïs": "maize",
    "mais": "maize",

    "manioc": "cassava",

    "tomate": "tomato",

    "oignon": "onion",

    "pomme de terre": "potato",

    "carotte": "carrots",

    "céleri": "celery",
    "celeri": "celery",

    "laitue": "lettuce",

    "épinard": "spinach",
    "epinard": "spinach",

    "radis": "radish",

    "aubergine": "eggplant",

    "patate douce": "sweet potato",

    "haricot vert": "beans green",
    "haricots verts": "beans green",

    "haricot": "beans",
    "haricots": "beans",

    "pois": "peas",

    "soja": "soybeans",

    "coton": "cotton",

    "sésame": "sesame",
    "sesame": "sesame",

    "tournesol": "sunflower",

    "mil": "millet",

    "sorgho": "sorghum",

    "ananas": "pineapple",

    "raisin": "grapes",
    "raisins": "grapes",

    "pistache": "pistachios",
    "pistaches": "pistachios",
}


# ============================================================
# CULTURES UTILISANT FAO56_TREE
# ============================================================

TREE_CROPS = {
    "almond",
    "apple",
    "avocado",
    "cacao",
    "citrus",
    "coffee",
    "grapewine",
    "mango",
    "peach",
    "strawberry",
    "sugarcane",
    "vanilla",
    "walnut",
}


# ============================================================
# VARIETY VIEWSET
# ============================================================

@method_decorator(
    name="list",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="retrieve",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="create",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="update",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="partial_update",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="destroy",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
class VarietyViewSet(
    CacheInvalidationMixin,
    viewsets.ModelViewSet
):
    """
    Variétés de cultures — lecture publique.
    """

    queryset = Variety.objects.all()

    serializer_class = VarietySerializer

    permission_classes = [
        permissions.AllowAny
    ]

    cache_prefix = "variety"


# ============================================================
# STATUS CROP VIEWSET
# ============================================================

@method_decorator(
    name="list",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="retrieve",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="create",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="update",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="partial_update",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="destroy",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
class StatusCropViewSet(
    CacheInvalidationMixin,
    viewsets.ModelViewSet
):
    """
    Statuts de culture — lecture publique.
    """

    queryset = StatusCrop.objects.all()

    serializer_class = StatusCropSerializer

    permission_classes = [
        permissions.AllowAny
    ]

    cache_prefix = "status_crop"


# ============================================================
# CROP VIEWSET
# ============================================================

@method_decorator(
    name="list",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="retrieve",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="create",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="update",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="partial_update",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="destroy",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
class CropViewSet(
    CacheInvalidationMixin,
    viewsets.ModelViewSet
):
    """
    Cultures — filtrées par l'agriculteur connecté.
    """

    serializer_class = CropSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    cache_prefix = "crop"

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return Crop.objects.none()

        return (
            Crop.objects
            .filter(owner=self.request.user)
            .select_related("variety")
        )

    def perform_create(
        self,
        serializer
    ):
        serializer.save(
            owner=self.request.user
        )


# ============================================================
# PARCEL CROP VIEWSET
# ============================================================

@method_decorator(
    name="list",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="retrieve",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="create",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="update",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="partial_update",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
@method_decorator(
    name="destroy",
    decorator=extend_schema(tags=["Cultures & Variétés"])
)
class ParcelCropViewSet(
    CacheInvalidationMixin,
    viewsets.ModelViewSet
):
    """
    Cultures d'une parcelle.
    """

    serializer_class = ParcelCropSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    cache_prefix = "parcel_crop"

    # ========================================================
    # QUERYSET
    # ========================================================

    def get_queryset(self):

        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return ParcelCrop.objects.none()

        user = self.request.user

        # ----------------------------------------------------
        # Cultures possédées directement par l'utilisateur
        # ----------------------------------------------------

        queryset = ParcelCrop.objects.filter(
            parcel__owner=user
        )

        # ----------------------------------------------------
        # Groupes dont l'utilisateur est leader
        # ----------------------------------------------------

        led_groups = (
            MemberGroup.objects
            .filter(
                user=user,
                role__role_type="LEADER",
                status="ACTIVE"
            )
            .values_list(
                "group_id",
                flat=True
            )
        )

        if led_groups.exists():

            member_ids = (
                MemberGroup.objects
                .filter(
                    group_id__in=led_groups,
                    status="ACTIVE"
                )
                .values_list(
                    "user_id",
                    flat=True
                )
            )

            queryset = (
                ParcelCrop.objects
                .filter(
                    models.Q(
                        parcel__owner=user
                    )
                    |
                    models.Q(
                        parcel__owner_id__in=member_ids
                    )
                )
                .distinct()
            )

        return (
            queryset
            .select_related(
                "parcel",
                "crop",
                "crop__variety",
                "status"
            )
        )

    # ========================================================
    # CREATE
    # ========================================================

    def perform_create(
        self,
        serializer
    ):

        parcel = serializer.validated_data["parcel"]

        if parcel.owner != self.request.user:
            raise PermissionDenied(
                "Vous ne pouvez pas ajouter de culture "
                "à cette parcelle."
            )

        serializer.save()

    # ========================================================
    # UPDATE
    # ========================================================

    def perform_update(
        self,
        serializer
    ):

        parcel = serializer.validated_data.get(
            "parcel",
            serializer.instance.parcel
        )

        if parcel.owner != self.request.user:
            raise PermissionDenied(
                "Vous ne pouvez pas modifier cette culture."
            )

        serializer.save()

    # ========================================================
    # FAO-56
    # ========================================================

    @extend_schema(
        request=FAO56Serializer,
        responses=OpenApiTypes.OBJECT,
        tags=["FAO-56"],
        description=(
            "Lance le calcul FAO-56 pour une culture "
            "associée à une parcelle."
        ),
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="fao56",
    )
    def fao56(
        self,
        request,
        pk=None
    ):
        """
        Lance le calcul FAO-56.

        Le paramètre {id} correspond au ParcelCrop.

        Django récupère automatiquement :

            - la culture
            - la parcelle
            - les coordonnées GPS
            - le centre de la parcelle
            - la date de plantation

        Le frontend fournit :

            - irrigation
            - irrigation_count (optionnel)
        """

        # ====================================================
        # 1. VALIDATION DES DONNÉES FAO-56
        # ====================================================

        serializer = FAO56Serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        irrigation = serializer.validated_data.get(
            "irrigation",
            False
        )

        irrigation_count = serializer.validated_data.get(
            "irrigation_count"
        )

        try:

            # =================================================
            # 2. RÉCUPÉRER LE PARCEL CROP
            # =================================================

            parcel_crop = self.get_object()

            crop = parcel_crop.crop

            parcel = parcel_crop.parcel

            # =================================================
            # 3. CENTRE DE LA PARCELLE
            # =================================================

            center = parcel.get_center()

            if not center:

                return Response(
                    {
                        "success": False,
                        "message": (
                            "Impossible de déterminer le centre "
                            "de la parcelle."
                        ),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            lat = float(center["lat"])

            lng = float(center["lng"])

            # =================================================
            # 4. NOM DE LA CULTURE
            # =================================================

            crop_name = (
                crop.name
                .strip()
                .lower()
            )

            fao56_crop = FAO56_CROP_MAPPING.get(
                crop_name
            )

            if not fao56_crop:

                return Response(
                    {
                        "success": False,
                        "message": (
                            f"La culture '{crop.name}' "
                            "n'est pas configurée pour FAO-56."
                        ),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # =================================================
            # 5. DATE DE PLANTATION
            # =================================================

            start_date = None

            if parcel_crop.planting_date:

                start_date = (
                    parcel_crop
                    .planting_date
                    .isoformat()
                )

            # =================================================
            # 6. LOG
            # =================================================

            print(
                "\n"
                "=============================================="
            )

            print("🌱 CALCUL FAO-56")

            print(
                "=============================================="
            )

            print(
                f"ParcelCrop ID : {parcel_crop.id}"
            )

            print(
                f"Culture       : {crop.name}"
            )

            print(
                f"FAO-56 crop   : {fao56_crop}"
            )

            print(
                f"Latitude      : {lat}"
            )

            print(
                f"Longitude     : {lng}"
            )

            print(
                f"Start date    : {start_date}"
            )

            print(
                f"Irrigation    : {irrigation}"
            )

            print(
                f"Irrigations   : {irrigation_count}"
            )

            print(
                "==============================================\n"
            )

            # =================================================
            # 7. APPEL FLASK
            # =================================================

            if fao56_crop in TREE_CROPS:

                print(
                    "🌳 Utilisation de FAO56 TREE"
                )

                result = fao56_tree(
                    crop=fao56_crop,
                    lat=lat,
                    long=lng,
                    irrigation=irrigation,
                )

            else:

                print(
                    "🌾 Utilisation de FAO56 OTHER"
                )

                if not start_date:

                    return Response(
                        {
                            "success": False,
                            "message": (
                                "La date de plantation "
                                "est obligatoire pour cette "
                                "culture."
                            ),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                result = fao56_other(
                    crop=fao56_crop,
                    lat=lat,
                    long=lng,
                    start_date=start_date,
                    irrigation=irrigation,
                )

            # =================================================
            # 8. RÉPONSE
            # =================================================

            return Response(
                {
                    "success": True,

                    "parcel_crop_id": (
                        parcel_crop.id
                    ),

                    "parcel": {
                        "uuid": str(
                            parcel.uuid
                        ),
                        "name": (
                            parcel.parcel_name
                        ),
                    },

                    "crop": {
                        "id": crop.id,
                        "name": crop.name,
                        "fao56_name": fao56_crop,
                    },

                    "location": {
                        "lat": lat,
                        "long": lng,
                    },

                    "start_date": start_date,

                    "irrigation": irrigation,

                    "irrigation_count": (
                        irrigation_count
                    ),

                    "data": result.get(
                        "data",
                        []
                    ),
                },
                status=status.HTTP_200_OK,
            )

        # ====================================================
        # 9. ERREUR FLASK
        # ====================================================

        except FlaskFAO56Error as exc:

            print(
                "\n"
                "=============================================="
            )

            print(
                "❌ ERREUR SERVICE FLASK FAO-56"
            )

            print(
                f"Erreur : {exc}"
            )

            print(
                "==============================================\n"
            )

            return Response(
                {
                    "success": False,
                    "message": str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # ====================================================
        # 10. AUTRE ERREUR
        # ====================================================

        except Exception as exc:

            print(
                "\n"
                "=============================================="
            )

            print(
                "❌ ERREUR FAO-56 DJANGO"
            )

            print(
                f"Erreur : {exc}"
            )

            print(
                "==============================================\n"
            )

            return Response(
                {
                    "success": False,
                    "message": (
                        "Une erreur est survenue "
                        "lors du calcul FAO-56."
                    ),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )