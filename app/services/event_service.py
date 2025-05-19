from app.models.event import Event
from sqlalchemy.orm import Session
from app.models.organizations import Organizations
from app.models.event_attendee import EventAttendee
from app.models.user_orgs import UserOrgs
from app.services.token_service import get_current_token

from app.utilities.jwt import decode_access_token
def create_event(db: Session, creator_id, event_data, token):




    orgs = db.query(UserOrgs.part_of, UserOrgs.is_admin).filter(UserOrgs.user_id == creator_id.username).all()
    orgs = {org[0]: org[1] for org in orgs}


    if not any(org == event_data.org_id for org in orgs):
        raise ValueError(f"User is not an admin in {event_data.org_id}")

    try:

        if orgs[event_data.org_id] is True :
            new_event = Event(
                creator_id=creator_id.id,
                title=event_data.title,
                description=event_data.description,
                location=event_data.location,
                event_type=event_data.event_type,
                event_date=event_data.event_date,
                start_time=event_data.start_time,
                end_time=event_data.end_time,
                max_attendees=event_data.max_attendees,
                org_id = event_data.org_id,
                invitation_type=event_data.invitation_type,

            )



            db.add(new_event)
            db.commit()
            db.refresh(new_event)
            return new_event
        else:
            raise ValueError("Only Admins can make events")
    except Exception as e:
        raise ValueError(f"{e}")





def get_all_events(db: Session, current_user, token):
    #payload = decode_access_token(token)
    #orgs = list(payload['orgs'].keys())
    orgs = db.query(UserOrgs.part_of).filter(UserOrgs.user_id == current_user.username).distinct().all()
    orgs = [i[0] for i in orgs]
    

    # Query events associated with the organizations
    org_events = db.query(Event).filter(Event.org_id.in_(orgs)).all()

    # Query events where the current user is registered as an attendee
    user_event_ids = db.query(EventAttendee.event_id).filter(EventAttendee.user_id == current_user.id).distinct().all()
    user_event_ids = [event_id[0] for event_id in user_event_ids]  # Extracting event IDs from tuples

    user_events = db.query(Event).filter(Event.id.in_(user_event_ids)).all()

    # Combine both sets of events and remove duplicates
    all_events = {event.id: event for event in org_events + user_events}.values()
    all_events = set(all_events)  # Ensures distinct values

    return list(all_events)


def get_event_by_id(db: Session, event_id: str, current_user, token):
    orgs = db.query(UserOrgs.part_of).filter(UserOrgs.user_id == current_user.username).distinct().all()
    orgs = [i[0] for i in orgs]

    event = db.query(Event).filter(Event.title == event_id, Event.org_id.in_(orgs)).first()

    return event


def delete_event_title(db: Session, event_title: str, current_user):
    # Get organizations the user belongs to
    orgs = db.query(UserOrgs.part_of).filter(UserOrgs.user_id == current_user.username).distinct().all()
    orgs = [i[0] for i in orgs]

    # Fetch the event properly as an ORM instance
    event = db.query(Event).filter(Event.title == event_title, Event.org_id.in_(orgs)).first()

    if not event:
        return {"error": "Event not found"}

    # Delete related attendees first
    db.query(EventAttendee).filter(EventAttendee.event_id == event.id).delete(synchronize_session=False)

    # Delete the event instance
    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}



