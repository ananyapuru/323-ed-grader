import csv
from collections import defaultdict

################################################## CONSTANTS ##################################################

# For answers that aren't verified or endorsed, but are > 100 characters long, we count it towards the verified/unendorsed count.
MIN_UNENDORSED_ANSWER_CHARACTER_THRESHOLD = 100      # Change the threshold as you see fit :)
QUESTION_MARK_CHARACTER = "?"


################################################## CONSTANTS ##################################################


def get_text_length(text):
    """
    Safely return the length of a string,
    accounting for None or empty input.
    """
    if not text:
        return 0
    return len(text)


def does_text_contain_questions(text):
    """
    Return True if text empty or contains "?", False otherwise.
    """
    if not text:
        return True
    return QUESTION_MARK_CHARACTER in text


def is_verified_or_endorsed(text, endorsed_flag):
    """
    Returns True if:
      - endorsed_flag is True, OR
      - text is > 100 characters (special rule for unendorsed items) AND text does not contain any question marks.
    """
    # If it’s endorsed or verified, we count it automatically.
    if endorsed_flag:
        return True

    # Otherwise, check if text is > 100 chars and that text does not contain questions
    if get_text_length(text) > MIN_UNENDORSED_ANSWER_CHARACTER_THRESHOLD and not does_text_contain_questions(text):
        return True
    return False


def get_user_name(user_dict):
    """
    Returns contributor's name.
    """
    return user_dict.get("name", "unknown name")


def parse_comments(comments_list, user_counts):
    """
    Recursively parse a list of comments/answers. Each comment can have:
       - comment["endorsed"]
       - comment["text"]
       - comment["user"] -> { name, email, ... }
       - nested comment["comments"]
    """
    for comment in comments_list:
        text = comment.get("text", "")
        endorsed_flag = comment.get("endorsed", False)
        user_dict = comment.get("user", {})

        # If comment is verified/endorsed by the rules, increment.
        if is_verified_or_endorsed(text, endorsed_flag):
            user_id = get_user_name(user_dict)
            user_counts[user_id] += 1

        # Recurse on sub-comments
        sub_comments = comment.get("comments", [])
        if sub_comments:
            parse_comments(sub_comments, user_counts)


def parse_post_or_announcement(obj, user_counts):
    """
    Parse a top-level post/question/announcement JSON object.
    We check the main object itself, then parse its nested comments (answers).
    """
    text = obj.get("text", "")
    endorsed_flag = obj.get("endorsed", False)  # Since some posts have "endorsed": true
    user_dict = obj.get("user", {})

    # Checking the top-level post/announcement itself
    if is_verified_or_endorsed(text, endorsed_flag):
        user_id = get_user_name(user_dict)
        user_counts[user_id] += 1

    # Parsing all nested comments.
    comments = obj.get("comments", [])
    parse_comments(comments, user_counts)

    # Parsing all nested answers.
    answers = obj.get("answers", [])
    parse_comments(answers, user_counts)


def group_by_count(user_counts):
    """
    Invert user_counts (user -> count)
    into a dictionary of count -> list_of_users
    so that we can group them by the number of verified/endorsed items.
    """
    count_to_users = defaultdict(list)
    for user, count in user_counts.items():
        count_to_users[count].append(user)
    return dict(count_to_users)


def write_csv_output(user_counts, csv_filename="verified_endorsed_counts.csv"):
    """
    Write user_counts to a CSV file with two columns:
      Contributor, Verified/Endorsed Count
    """
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Contributor", "Verified/Endorsed Count"])
        for user, count in sorted(user_counts.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([user, count])
