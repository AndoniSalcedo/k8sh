import re

def highlight_output(text):
    if not text:
        return text

    # Verbs / Actions
    text = re.sub(r'\b(Running|Ready|Completed|Active)\b', '\033[92m\\1\033[0m', text)
    # Errors / Warnings
    text = re.sub(r'\b(Error|CrashLoopBackOff|OOMKilled|Terminating|ImagePullBackOff|ErrImagePull)\b', '\033[91m\\1\033[0m', text)
    # Intermediate states
    text = re.sub(r'\b(Pending|ContainerCreating|Init)\b', '\033[93m\\1\033[0m', text)
    
    return text
