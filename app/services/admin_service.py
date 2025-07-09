from sqlalchemy.orm import Session
from app.models.admins import Admins
from app.models.user_orgs import UserOrgs
from app.models.user import User


def add_admin_to_org(db: Session, userdata, curr_admin):

    is_curr_admin_allowed = db.query(Admins).filter(Admins.user_id == curr_admin.id, Admins.org_id == userdata.org_id).first()
    uid = db.query(User.id).filter(User.username == userdata.user_id).scalar()


    if is_curr_admin_allowed:
        new_admins = Admins(

            user_id= uid,
            org_id= userdata.org_id,
            accepted_by=  curr_admin.username,
            status = "approved"

        )
        db.add(new_admins)
        db.commit()
        db.refresh(new_admins)

        new_org_user = UserOrgs(
            user_id=userdata.user_id,
            part_of= userdata.org_id,
            is_admin=True

        )
        db.add(new_org_user)
        db.commit()
        db.refresh(new_org_user)
        return new_admins
    else:
        print("*" * 100)
        return None
