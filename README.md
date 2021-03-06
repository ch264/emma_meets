# emma_meets

https://emmameets.herokuapp.com/

Emma Meets was created to provide a social media platform, for dog owners to find and leave reviews for dog related products. Users can sign up, reset their password by email, create a profile for their dog, browse existing products in the database, leave reviews and favorite products to their profile page. In addition they can remove these as well as their reviews. Each review has a rating that is dispayed as an average rating on the product page itself and in the product cards on the profile. If a user does not find a dog-related product on the page, they can create a category, which populates in a dropdown menu in the create product page. here they can upload an appropriate picture and information about the product they would like to review. After they are done, they can logout again.  

![](static/EmmaMeets.gif)

## Note on Image Uploader

Heroku does not support file uploads for free. Therefore I have taken out the option to upload a profile image or to attach an image to product when it is created. I had to remove the image uploader for now because Heroku would throw an error when trying to sign up and upload an image.

Please login with the credentials red@mail.com and password: red to see a sample profile with a profile picture. 


## List of technologies used 

- Bulma
- HTML5
- CSS3
- Jinja2
- jQuery
- Flask
- Flask-login
- Peewee ORM
- Python3
- SQLite Database
- Postgresql

## installation steps

1. clone down the repository
2. in your terminal run:
	 - pip3 install -r 
	 - python3 app.py
3. then go to localhost:8000/ to start the app

## User stories

Emma Meets is a community platform for dog owners who only want the best for their pooches. When encountering a product that has helped the owner or the dog, they can share their experience on Emma Meets and help other dogs/owners decide on which products to go for. 
Our users love their dogs and love talking about them. Each dog has their own profile displaying the most important characteristics of the dog. This will help with the future implementation of elastic search where dogs will be able to search for other dogs in their location, by breed or favorite toy etc.
Our users are looking for a community of other user that love their dogs as much as they do.


## Link to wireframes

https://trello.com/c/pJTTsD6G/14-wireframes

## Link to ERD

https://trello.com/c/nuxyuQmI/15-erd

![EmmaMeets_ERD](https://github.com/ch264/emma_meets/blob/master/static/EmmaMeets_ERD.jpg)


## unsolved problems
- Heroku does not support free image upload, therefore images are hardcoded at this moment. User should be able to upload a profile image and an image for a newly created dog related product
- Average ratings do not always round up 
- reviews should show the product their are written for
- reviews should show the authers name
- the footer is not sticking to the bottom - removal for the moment
- a new product category should be created at a different stage - improve user flow and UX

## future features
- when user logs in, they should go to a page with all recent reviews displayed (meaty content)
- implement pagination on profile page
- implement Elastic Search 
- use instagram API to display pictures of profile
- add birthdate and calculate automatic age change on profile
- users should be added to product table in database
- users should be able to follow each other
- users should be able to see live updates and notifications of new products and reviews added