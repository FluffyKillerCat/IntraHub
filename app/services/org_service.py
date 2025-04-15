from sqlalchemy.orm import Session
from app.models.organizations import Organizations
from app.services.token_service import get_current_token
from app.models.admins import Admins
from app.models.user_orgs import UserOrgs
from app.models.user import User
from app.models.user_orgs import UserOrgs
from app.utilities.jwt import decode_access_token
def create_org(token, db: Session, admin, org_in):
    payload = decode_access_token(token)


    if payload["sub"] == admin.username:

        new_org = Organizations(

            created_id= admin.username,
            org_name= org_in.org_name
        )




        db.add(new_org)
        db.commit()
        db.refresh(new_org)
        new_org_user = UserOrgs(

            user_id=admin.username,
            part_of=new_org.org_name,
            is_admin=True
        )
        db.add(new_org_user)
        db.commit()
        db.refresh(new_org_user)

        new_admin = Admins(
            user_id  = admin.id,
            org_id = new_org.org_name,
            accepted_by= admin.username,
            status = 'approved'
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_org

def add_user_to(token: str, db: Session, user_org_data, admin):

    payload = decode_access_token(token)





    try:
        if  payload['orgs'][str(user_org_data.part_of)] is True:

            is_org_admin = db.query(Admins).filter(Admins.org_id == user_org_data.org, Admins.user_id == admin.id).first()
            is_old_user = db.query(UserOrgs).filter(UserOrgs.part_of == user_org_data.part_of, UserOrgs.user_id ==  user_org_data.username)
            if is_old_user:

                raise ValueError(f"User already part of {user_org_data.org}")
            if is_org_admin:

                return None




            user  = user_org_data.username

            org = user_org_data.part_of

            new_org_user = UserOrgs(

                user_id=user,
                part_of=org
            )


            db.add(new_org_user)
            db.commit()
            db.refresh(new_org_user)

            return new_org_user


        else:

            return None
    except Exception:
        return None


