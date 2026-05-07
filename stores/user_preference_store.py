from models import UserPreference
from stores.base_store import BaseStore

class UserPreferenceStore(BaseStore):
    def create_user_preference(self, user_pref: UserPreference) -> None:
        self.add(user_pref)
    
    def get_user_preference(self, user_id: int) -> UserPreference | None:
        return UserPreference.query.filter_by(user_id=user_id).first()
    
    def update_user_preference(self, user_prefs: UserPreference, display_name: str, email: str, country: str) -> None:
        user_prefs.display_name = display_name
        user_prefs.email = email
        user_prefs.country = country
        self.commit()

auth_store_instance = UserPreferenceStore()