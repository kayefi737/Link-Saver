

'''@app.get("/posts/latest")
def get_latest_post():
    length = len(userData)
    recent = length-1 
    return{"detail": userData[recent]}


@app.get("/posts/random")
def get_random_post():
    length = len(userData)
    randomLink = randrange(0, length-1)
    return userData[randomLink]


@app.get("/posts/{UserID}")
def get_specific_post(UserID: int, response: Response):
    data = {}
    message = "Link Not Found"
    response.status_code = status.HTTP_404_NOT_FOUND
    #raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    length = len(userData)
    for i in range(length):
        if userData[i]["UserID"] == UserID:
            data = userData[i]
            message = "Link Found"
            response.status_code = status.HTTP_200_OK
            break 
    return{"Info": data, "message": message}

   

@app.post("/posts/save")
def save_links(post: Links, response: Response):
    length = len(userData)
    post_dict = post.dict()
    post_dict["UserID"] = length +1
    if post_dict["rated_18"] == None:
        post_dict["rated_18"] = False
    userData.append(post_dict)
    response.status_code=status.HTTP_201_CREATED
    return{"data": post_dict, "message":"Link Saved Successfully"} 
   


@app.put("/posts/{UserID}")
def update_links(UserID: int,post: UpdateLinks, response: Response):
    for i in range(len(userData)):
        if userData[i]["UserID"] == UserID:
            if post.title != None:
                userData[i]["title"]= post.title
            if post.Content != None:
                userData[i]["content"] = post.Content
            if post.rated_18 != None:
                userData[i]["rated_18"] = post.rated_18
            response.status_code=status.HTTP_200_OK
            return {"data":userData[i], "message": "Link Updated Successfully"}

    response.status_code=status.HTTP_404_NOT_FOUND
    return{"data":[], "message": "Link Not Found"}


@app.delete("/posts/delete{UserID}")
def delete_posts(UserID: int, response: Response):
    lengthOfUserData = len(userData)
    for i in range(lengthOfUserData):
        if userData[i]["UserID"] == UserID:
            index = userData[i]
            userData.remove(index)
            break
        response.status_code=status.HTTP_200_OK
        return{"data: Link Deleted"}'''

'''@app.post("/auth/login")
def login(req: LoginRequest, response: Response):
    result = {}
    if pass_input.verify(req.password, userDetail["password"]):
        result["msg"] = "success"
        result["access_token"] = create_token({"username": req.username}, 3)
        result["token_type"] = "bearer"
        response.status_code = status.HTTP_200_OK
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )    
    return result''' 





#pass_input = CryptContext(schemes=["bcrypt"], deprecated="auto")
