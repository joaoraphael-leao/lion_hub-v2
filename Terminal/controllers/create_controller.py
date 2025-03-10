def create_dict(model, questions: dict[str, str]) -> dict[str, str]:
    model_dict = {}
    for key, question in questions.items():
        answer = input(question)
        model_dict[key] = answer
    return model_dict

def creator(model):
    if model == "User":
        user_dict = create_dict("User", user_questions)
        return User(name=user_dict["name"], email=user_dict["email"], password=user_dict["password"])        
    elif model == "Group":
        event_dict = create_dict("Group", group_questions)
    elif model == "Event":
        return create_event()
    elif model == "Post":
        return create_post()
    else:
        throw "Model not found"
