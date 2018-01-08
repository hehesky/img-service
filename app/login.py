import mysalt
import db_util



###tested 2017-10-03
def verify_password(conn,username,password):
    """returns True if username-password matches in database"""    
 
    user_info=db_util.query_user(conn,username)
    
    if len(user_info)==0:        
        return False
    salt=stored_password=str(user_info[0][1])
    stored_password=str(user_info[0][2])
    salted_password=mysalt.salted_password(salt,password)
    return salted_password==stored_password


def retrieve_pic(conn,username):

    user_pic=db_util.query_image(conn,username)
    pic_names = [str(user_pic[i][0]) for i in range(0, len(user_pic))]
    
    return pic_names
    
    
def register(conn,username,password):

    salt=mysalt.generate_salt()
    salted_password=mysalt.salted_password(salt,password)
    
    user_info=db_util.query_user(conn,username)
    if user_info:#meaning there is a user with this name
        return "Username exists"

    state=db_util.add_new_user(conn,username,salt,salted_password)

    return state
    
