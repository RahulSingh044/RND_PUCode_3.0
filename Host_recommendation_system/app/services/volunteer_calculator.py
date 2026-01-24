from app.schemas.internal import VolunteerPlanInternal


def calculate_volunteer_plan(participant_count: int) -> VolunteerPlanInternal:
    """
    Calculates volunteer requirements and role distribution.

    Philosophy:
    - Volunteers reduce chaos more than infra
    - Entry + seating + food must NEVER share people
    - One clear lead is mandatory
    """

    # --------------------------------------------------
    # Volunteer count calculation
    # --------------------------------------------------
    # Rule of thumb: 1 volunteer per ~40 participants
    if participant_count <= 30:
        total_volunteers = 1
    else:
        total_volunteers = max(2, round(participant_count / 40))

    # --------------------------------------------------
    # Role distribution
    # --------------------------------------------------
    # Baseline split logic
    entry_volunteers = max(1, round(total_volunteers * 0.3))
    seating_volunteers = max(1, round(total_volunteers * 0.4))
    food_volunteers = max(1, total_volunteers - entry_volunteers - seating_volunteers)

    # Ensure we don’t exceed total
    allocated = entry_volunteers + seating_volunteers + food_volunteers
    if allocated > total_volunteers:
        food_volunteers = max(0, food_volunteers - (allocated - total_volunteers))

    # Lead volunteer is ALWAYS 1 (overlaps with seating/crowd)
    role_distribution = {
        "entry_and_checkin": entry_volunteers,
        "seating_and_crowd_flow": seating_volunteers,
        "food_management": food_volunteers,
        "lead_coordinator": 1
    }

    return VolunteerPlanInternal(
        ratio="1 volunteer per 40 participants",
        total_required=total_volunteers,
        role_distribution=role_distribution
    )
