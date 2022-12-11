def memory(catagory, type_):
    if(catagory == "greetings"):
        if(type_ == "hello"):
            return "Yes, I am listening"
    elif(catagory == "statement"):
        if(type_ == "exit"):
            return "Roger that."
    else:
        return "I am not sure what to say!"