# lion_hub-v2

## Lion Hub is a social network project using Object Oriented Programming

## Main Classes:

### User
In a social network, we will have user accounts.
Users will have these attributes:
<ul>
    <li>id: to a better management of Users </li>
    <li>Username: an unique string username for the account</li>
    <li>associated email: an unique string email for the account</li>
    <li>password: A string that is used to acess the account</li>
    <li>Notifications: A list of Notifications objects of notifications.</li>
    <li>Privacity: A boolean attribute that defines if the profile is private</li>
    <li>Following List: A list/dict with Users that the User follows</li>
    <li>Followers List: A list/dict with Users that follows the User</li>
</ul>
And this methods:
<ul>
    <li>Constructor: __init__ to inicialize the class User</li>
    <li>__str__: to define what happens when someone print a User object</li>
    <li>Getters to these attributes: username, email</li>
    <li>Setters to these attributes: usernamme</li>
    <li>General edit: Menu to manage and set these three attributes</li>
    <li>Create post: To create a new post that the User is the owner</li>
    <li>Edit Post: To edit data of a post that the User is the owner</li>
    <li>Delete Post: To delete a post that the User is the owner</li>
    <li>See my posts: Filter function to see Posts that the user is owner</li>
    <li>Delete account: Delete you</li>
</ul>


### Post
In a social network, users create, edit, delete posts, its a main thing for the interaction

Post will have these attributes:
<ul>
    <li>Title: the main name for a post</li>
    <li>content: the description / content of the post</li>
    <li>image: Optional url for an image for the post</li>
    <li>video: Optional url for a video in the post</li>
    <li>Author: the owner of the post</li>
    <li>id: The id of the post to interact easily with posts</li>
</ul>

And these methods:
<ul>
    <li>Constructor: __init__ to inicialize the class</li>
    <li>__str__: to define what happens when someone print a Post object</li>
    <li>Getters for these attritutes: author, title, content, url video, url image</li>
    We don´t have setters because we manage our posts in the Class User.
</ul>

## 