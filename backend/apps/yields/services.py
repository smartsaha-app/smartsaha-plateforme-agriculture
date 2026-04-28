"""
apps/yields/services.py
-----------------------
Services ML pour les rendements.

YieldForecastService  → régression linéaire scikit-learn
YieldAnalyticsService → statistiques + graphiques pandas/matplotlib
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # ← backend non-interactif obligatoire en prod
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ← Imports corrigés : apps.yields au lieu de SmartSaha
from apps.yields.models import YieldRecord, YieldForecast
from apps.groups.models import MemberGroup
from django.db.models import Q


class YieldForecastService:
    """
    Prévision de rendement par régression linéaire.

    Pipeline :
        1. fetch_data()    → charge l'historique YieldRecord en DataFrame
        2. train_model()   → entraîne LinearRegression sur (date_ordinal, yield)
        3. predict_next()  → prédit le rendement J+days_ahead
        4. save_forecast() → persiste dans YieldForecast (idempotent)
    """
    def __init__(self, parcel_crop):
        self.parcel_crop = parcel_crop
        self.model = LinearRegression()

    def fetch_data(self) -> pd.DataFrame | None:
        """Charge l'historique de rendement pour cette ParcelCrop."""
        qs = YieldRecord.objects.filter(
            parcelCrop=self.parcel_crop
        ).order_by('date')
        if not qs.exists():
            return None
        data = pd.DataFrame(list(qs.values('date', 'yield_amount')))
        data['date_ordinal'] = pd.to_datetime(data['date']).map(
            lambda d: d.toordinal()
        )
        return data

    def train_model(self, data: pd.DataFrame) -> None:
        """Entraîne le modèle de régression linéaire."""
        X = data[['date_ordinal']]
        y = data['yield_amount']
        self.model.fit(X, y)

    def predict_next(self, days_ahead: int = 7) -> tuple | None:
        """Prédit le rendement pour J+days_ahead. Retourne (date, yield) ou None."""
        data = self.fetch_data()
        if data is None or data.empty:
            return None
        self.train_model(data)
        last_date = data['date'].max()
        if isinstance(last_date, pd.Timestamp):
            next_date = (last_date + pd.Timedelta(days=days_ahead)).date()
        else:
            next_date = last_date + pd.Timedelta(days=days_ahead)
        X_pred = pd.DataFrame([[next_date.toordinal()]], columns=['date_ordinal'])
        predicted_yield = self.model.predict(X_pred)[0]
        return next_date, predicted_yield

    def save_forecast(self, days_ahead: int = 7) -> YieldForecast | None:
        """
        Calcule et persiste la prévision.
        Idempotent : si une prévision existe déjà pour cette date, la retourne.
        """
        result = self.predict_next(days_ahead)
        if result is None:
            return None
        forecast_date, predicted_yield = result
        existing = YieldForecast.objects.filter(
            parcelCrop=self.parcel_crop,
            forecast_date=forecast_date,
        ).first()
        if existing:
            return existing
        return YieldForecast.objects.create(
            parcelCrop=self.parcel_crop,
            forecast_date=forecast_date,
            predicted_yield=predicted_yield,
        )


class YieldAnalyticsService:
    """
    Analyse statistique des rendements via pandas.
    Génère graphiques (histogramme, boxplot, tendance, rendement/ha).
    """
    def __init__(self, user=None):
        self.user = user

    def load_data(self) -> pd.DataFrame | None:
        """Charge les relevés de l'utilisateur (et ses membres s'il est leader) en DataFrame."""
        qs = YieldRecord.objects.select_related('parcelCrop__parcel')
        if self.user:
            # Même logique d'isolation que Task/Parcel
            led_groups = MemberGroup.objects.filter(
                user=self.user, role__role_type='LEADER', status='ACTIVE'
            ).values_list('group_id', flat=True)
            
            if led_groups.exists():
                member_ids = MemberGroup.objects.filter(
                    group_id__in=led_groups, status='ACTIVE'
                ).values_list('user_id', flat=True)
                qs = qs.filter(Q(parcelCrop__parcel__owner=self.user) | Q(parcelCrop__parcel__owner_id__in=member_ids))
            else:
                qs = qs.filter(parcelCrop__parcel__owner=self.user)

        df = pd.DataFrame(list(qs.values(
            'date', 'yield_amount', 'area', 'parcelCrop_id'
        )))
        if df.empty:
            return None
        df['year'] = pd.to_datetime(df['date']).dt.year
        df['yield_per_area'] = df['yield_amount'] / df['area']
        return df

    def generate_histogram(self, df: pd.DataFrame, path: str = 'histogram_yield.png') -> str:
        plt.figure()
        df['yield_amount'].plot.hist(bins=20, alpha=0.7)
        plt.title('Distribution des rendements')
        plt.xlabel('Rendement'); plt.ylabel('Fréquence')
        plt.savefig(path); plt.close()
        return path

    def generate_boxplot(self, df: pd.DataFrame, path: str = 'boxplot_yield_by_year.png') -> str:
        plt.figure()
        df.boxplot(column='yield_amount', by='year')
        plt.title('Variation annuelle des rendements')
        plt.suptitle(''); plt.xlabel('Année'); plt.ylabel('Rendement')
        plt.savefig(path); plt.close()
        return path

    def generate_trend(self, df: pd.DataFrame, path: str = 'trend_yield_by_year.png') -> str:
        plt.figure()
        df.groupby('year')['yield_amount'].mean().plot(marker='o')
        plt.title('Tendance des rendements moyens par an')
        plt.xlabel('Année'); plt.ylabel('Rendement moyen'); plt.grid(True)
        plt.savefig(path); plt.close()
        return path

    def generate_yield_per_area(self, df: pd.DataFrame, path: str = 'yield_per_area.png') -> str:
        plt.figure()
        for pid, group in df.groupby('parcelCrop_id'):
            group.groupby('year')['yield_per_area'].mean().plot(
                marker='x', label=f'Parcelle {pid}'
            )
        plt.title('Rendement par surface (t/ha) par parcelle')
        plt.xlabel('Année'); plt.ylabel('Rendement/ha')
        plt.legend(); plt.grid(True)
        plt.savefig(path); plt.close()
        return path

    def get_user_stats(self) -> dict:
        """
        Retourne les statistiques de rendement par parcelle.
        """
        records = YieldRecord.objects.select_related('parcelCrop__parcel')
        if self.user:
            led_groups = MemberGroup.objects.filter(
                user=self.user, role__role_type='LEADER', status='ACTIVE'
            ).values_list('group_id', flat=True)
            
            if led_groups.exists():
                member_ids = MemberGroup.objects.filter(
                    group_id__in=led_groups, status='ACTIVE'
                ).values_list('user_id', flat=True)
                records = records.filter(Q(parcelCrop__parcel__owner=self.user) | Q(parcelCrop__parcel__owner_id__in=member_ids))
            else:
                records = records.filter(parcelCrop__parcel__owner=self.user)

        if not records.exists():
            return {}
        df = pd.DataFrame(list(records.values(
            'parcelCrop_id', 'parcelCrop__parcel__parcel_name',
            'date', 'yield_amount', 'area',
        )))
        df['year'] = pd.to_datetime(df['date']).dt.year
        df['yield_per_area'] = df['yield_amount'] / df['area']
        stats = {}
        for pid, group in df.groupby('parcelCrop_id'):
            stats[pid] = {
                'parcel_name':          group['parcelCrop__parcel__parcel_name'].iloc[0],
                'years':                group['year'].tolist(),
                'dates':                group['date'].astype(str).tolist(),
                'yield_amount':         group['yield_amount'].tolist(),
                'yield_per_area':       group['yield_per_area'].tolist(),
                'mean_yield':           group['yield_amount'].mean(),
                'mean_yield_per_area':  group['yield_per_area'].mean(),
            }
        return stats