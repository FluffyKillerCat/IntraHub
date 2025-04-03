from sqlalchemy.orm import Session
from app.models.admins import Admins



def add_admin_to_org(db: Session, userdata, curr_admin):

    is_curr_admin_allowed = db.query(Admins).filter(Admins.user_id == curr_admin, Admins.org_id == userdata.org_id, Admins.status == 'accepted').first()
    if is_curr_admin_allowed:
        new_admins = Admins(

            user_id= userdata.user_id,
            org_id= userdata.org_id,
            accepted_by=  curr_admin,

        )
        db.add(new_admins)
        db.commit()
        db.refresh(new_admins)
        return new_admins
    else:
        return None






