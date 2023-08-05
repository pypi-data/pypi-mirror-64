__version__ = '0.1.2'


def remove_practice_queues(chats_this_day):
    """remove the Practice queue from this list of chats 
    
    Arguments:
        chats_this_day {[list]} -- [list of dict of Chats]
    
    Returns:
        [list] -- [list of dict of Chats]
    """
    res = [chat for chat in chats_this_day if not "practice" in chat.get("queue")]
    return res

def get_chats_answered(chats_this_day):
    """get all the Chat answered
    
    Arguments:
        chats_this_day {[list]} -- [list of dicts of Chats]
    
    Returns:
        [list] -- [list of dict of Chats]
    """
    chats_answered = [chat for chat in chats_this_day if chat.get("accepted") != None]
    return chats_answered