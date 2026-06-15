from app.models.user import User


def has_availability_overlap(
    current_user: User,
    other_user: User
):
    for current_slot in current_user.availability_slots:

        for other_slot in other_user.availability_slots:

            if current_slot.day != other_slot.day:
                continue

            if (
                current_slot.start_time < other_slot.end_time
                and
                other_slot.start_time < current_slot.end_time
            ):
                return True

    return False


def get_match_reasons(
    current_user: User,
    other_user: User
):

    reasons = []

    # Shared Interests
    current_interests = {
        interest.id: interest.name
        for interest in current_user.interests
    }

    for interest in other_user.interests:

        if interest.id in current_interests:

            reasons.append(
                f"Shared interest: {interest.name}"
            )

    # Preference Matching
    if (
        current_user.preference
        and
        other_user.preference
    ):

        # Language Match
        if (
            current_user.preference.language
            ==
            other_user.preference.language
        ):
            reasons.append(
                f"Same language: {current_user.preference.language}"
            )

        # City Match
        if (
            current_user.preference.city
            ==
            other_user.preference.city
        ):
            reasons.append(
                f"Same city: {current_user.preference.city}"
            )

    # Availability Match
    if has_availability_overlap(
        current_user,
        other_user
    ):
        reasons.append(
            "Availability overlap found"
        )

    return reasons


def calculate_match_score(
    current_user: User,
    other_user: User
):

    score = 0

    # Interest Matching
    current_interest_ids = {
        interest.id
        for interest in current_user.interests
    }

    other_interest_ids = {
        interest.id
        for interest in other_user.interests
    }

    common_interests = (
        current_interest_ids &
        other_interest_ids
    )

    score += len(common_interests) * 10

    # Preference Matching
    if (
        current_user.preference
        and
        other_user.preference
    ):

        # Language Match
        if (
            current_user.preference.language
            ==
            other_user.preference.language
        ):
            score += 20

        # City Match
        if (
            current_user.preference.city
            ==
            other_user.preference.city
        ):
            score += 20

    # Availability Match
    if has_availability_overlap(
        current_user,
        other_user
    ):
        score += 30

    return score


def passes_preference_filter(
    current_user: User,
    other_user: User
):

    if not current_user.preference:
        return True

    # Gender Check
    if (
        current_user.preference.preferred_gender
        and
        other_user.gender
        !=
        current_user.preference.preferred_gender
    ):
        return False

    # Age Check
    if (
        other_user.age
        <
        current_user.preference.age_min
        or
        other_user.age
        >
        current_user.preference.age_max
    ):
        return False

    return True


def passes_mutual_preference_filter(
    current_user: User,
    other_user: User
):

    return (
        passes_preference_filter(
            current_user,
            other_user
        )
        and
        passes_preference_filter(
            other_user,
            current_user
        )
    )