# Art Of Chocolate
Art Of Chocolate is an E-commerce Website that allows people to buy chocolate with unusual tastes.
It is loved by many pastry chefs around the world.

Also, our clients are people who like to try new tastes who are not afraid to risk and who are adventurous. People from all over the World can order our Chocolate as Website gives shipping option worldwide.

Users can browse the shop and view each product, check chocolate categories and use searchbar. They can also add products to basket and purchase them by using payment with Stripe ( you can find more details [below](#art-of-chocolate) ).

This project is made for Code Institute Full-stack development program - Portfolio 5.

You can access live page to Art Of Chocolate by clicking [here](https://art-of-chocolate.herokuapp.com/).

![Am I reponsive](media/images/am_i_responsive.png)


# Table of content:
- [Art Of Chocolate Shop](#art-of-chocolate)
- [Business Model](#business-model)
- [Marketing Strategy](#marketing-strategy)
- [User Experience](#user-experience)
  - [User Stories](#user-stories)
  - [Features](#features)
  - [Goals](#goals)
   - [Visitor goals](#visitor-goals)
   - [User goals](#user-goals)
- [Design Choices](#design-choices)
  - [Color scheme and styling](#colors-style)
- [Wireframes](#wireframes)
- [ERD Diagram](#erd-diagram)
- [SEO](#seo)
  - [Keyword Research](#keyword-research)
- [Testing](#testing)
- [Local Deployment](#local-deployment)
- [Languages and technologies used](#languages-technologies)
- [Credits and Acknowledgements](#credits)
- [Content](#content)


# Business Model

Art Of Chocolate is a B2C business supporting the end consumer. The site gives User option to interact with central dataset, choose and purchase products and process payment with Stripe. Users can sign-up to Art Of Chocolate Newsletter. Full CRUD functionality is available to the user.


# User Experience
## User Stories

- User Stories were made with an Agile approach, Kanban board. User stories were documented within the Github Project option by using Github issues.

- User stories are divided to:
  - Site Users - Anonymous and Registered Users
  - Superuser

![User Stories, Kanban board](media/images/agile.png)


## Security Features

### User Access

Anonymous and Registered Users do not have access to add, edit or delete products. 

- If Anonymous User tries to access add, edit or delete page, user will be transfered to Sign In page.

![anonymous user](media/images/sign_in_anonymous.png)

- If Registered User tries to access add, edit or delete page, HttpResponse message generates.

![registered user add](media/images/registered_user_add.png)

![registered user edit](media/images/registered_user_edit.png)

![registered user delete](media/images/registered_user_delete.png)


### Form Validation

- Shipping form, Newsletter Mailchimp form and Contact Us form require all input data, they restrict Users to proceed if any of the fields are empty.

### Env.py file

- All Secret Keys, API's, Database Url and E-mail were stored within env.py file to secure unwanted access.

### 404 page

- Custom 404 error for the page that does not exist or is unavailable.

![404 custom page error](media/images/404_error.png)


## Features

### Navigation

![Header ](media/images/header.png)

- Shop name and categories are positioned on the left side of the header.

![Shop name and categories ](media/images/shop_name_and_categories.png)

- Login and sign up buttons, basket icon and search bar are on the right side of the header.

![Logins, signup, search bar](media/images/login_signup_search.png)

- When User logs in greeting message will appear.

![Greeting message singed in](media/images/signed_in_alert.png)

- When User logs out message will appear advising user sign out was successful.

![Greeting message signed out](media/images/signed_out_alert.png)

### Footer

![Footer](media/images/footer.png)

- Newsletter signup offered with mailchimp.

![Mailchimp](media/images/mailchimp.png)

- Social Media Icons for Facebookm Instagram and Pinterest pages.

![Social Media Icons](media/images/social_media_icons.png)

### Landing page and features

- Lnading page is showing chocolate products available in the shop.

![Landing page](media/images/landing_page.png)


- Chocolate page with Information about the chocolate product.

![Chocolate page](media/images/chocolate_page.png)


- Basket page with product added to basket and shipping form.

![Basket page](media/images/basket_page.png)


- If all products are removed from the basket, User can still access the page but shipping Information is removed.

![Empty basket](media/images/empty_basket.png)


- On the checkout page User can confirm that it is ok to proceed to payment with the total amount noted on the page.

![Chocolate page](media/images/checkout_page.png)


### Sign in, Sign Up, Logout, Password reset

![Sign in page](media/images/sign_in_anonymous.png)

E-mail verification

![Email verification](media/images/email_verification.png)

![Email message](media/images/email_message.png)

![Sign up page](media/images/sign_up.png)

![Sign out](media/images/sign_out.png)

![Password reset](media/images/password_reset.png)


### Landing page and features

Superuser has access to add, edit and delete chocolate products.

![Superuser landing page](media/images/super_user_landing_page.png)

![Superuser buttons](media/images/super_user_buttons.png)

- Add

![Add chocolate product](media/images/add_form.png)

- Edit

![Edit chocolate product](media/images/edit_form.png)


- Delete

![Delete chocolate product](media/images/delete_chocolate.png)


Superuser does not have access to basket and checkout pages.

![Superuser access](media/images/super_user_access.png)


### Forms

Shipping form - can only be submitted if all the fields are filled out correctly.

![Shipping form](media/images/shipping_form.png)

Contact form - all fields must be filled out for the form to be sent.

![Contact form](media/images/contact_us.png)

## Goals

### Visitor goals

Target Audience are all the people who love chocolate. Business has a great potential to grow into B2B, where businesses where chocolate is neccesity and main ingreadient like bakeries and coffee shops will be able to purchase high quality products.

- To have easy navigation and clear message.
- To see the insight of the Company and understand quality of the product.
- For the page to be relevant to what the visitor searched online.
- For the product to be of a good quality, as presented.
- To be able to make purchase easy and quickly.
- To be able to see Social Media links for further Information and stories about the Company.

### User Goals

User Goals can be found within the Kanban board as part of User Stories where users goals are mentioned.

## Design Choices

### Font choices

I have decided to use [Google Fonts](https://fonts.google.com/). 
 - Font Style used: Manrope 300
 - This font complements Art Of Chocolate WebShop reallz well.
 - I have included example of the style below: 
  
![main page](media/images/google_font.png)


### Icons

- Social Media Icons [Facebook](https://www.facebook.com/), [Instagram](https://www.instagram.com/) and [Pinterest](https://www.pinterest.ie/) 
- [Fontawesome](https://fontawesome.com/) was used to add social media icons and basket.

![social media icons](media/images/social_media_icons.png)

- Basket Icon

![basket icon](media/images/basket.png)

 
### Color scheme and styling

- [Coolors](https://coolors.co/) was used to generate Colors used for this project. As product images are colorful subtle colors were used to not distract user while browsing the shop.

![project colors](media/images/project_colors.png)

## Wireframes
All wireframes are created with [Balsamiq](https://balsamiq.com/) during the Scope Plane part of the design and planning process for this project.

Main Page
![main page](media/wireframes/main.png)

Chocolate Shop
![chocolate shop](media/wireframes/chocolate_shop.png)

Basket
![basket](media/wireframes/basket.png)

Register Page
![register](media/wireframes/register.png)

Sign In
![sign in](media/wireframes/sign_in.png)

Sign Out
![sign out](media/wireframes/sign_out.png)

Success
![success](media/wireframes/success.png)

Contact Us
![contact us](media/wireframes/contact_us.png)


## ERD Diagram
ERD Diagram is created with [Lucidchart](https://www.lucidchart.com/pages/) during the Scope Plane part of the design and planning process for this project.

![erd diagram](media/erd/database_diagram.png)

# Marketing Strategy

7 P's Marketing Strategy was used throughout the whole process of this project : 

- Product - Chocolate used is made from the finest cocoa solids and cocoa butter and as such will be marked as a "pure ingredients and high quality product".
- Promotion - Lot of promotions will be organised through Newsletters, Social Media, online events and other.
- Price - Price of all products is the same but the Company will make new strategies and planning for Newsletter and Social Media Campaigns. There will always be discounts there so we can engage more people to buy the product.
- Place - As a startup Company we will wait for few months before deciding on the best place to show off our product.
- People - People in our team will grow how the team grows, making sure customers are happy and that they are starting to promote the product free by "word of mouth".
- Process - All processes and materials used are sustainable and this will be presented to the customer.
- Physical Evidence - Company owns a factory where all chocolates are produced but main point of sale will be our Website.

Part of a Business Strategy is also a [Facebook](https://www.facebook.com/) mockup page, made with [Balsamiq](https://balsamiq.com/):

![mockup page](media/wireframes/facebook_mockup.png)


## SEO

### Keyword Research

Short-tail and long-tail words used for SEO implementation.

![SEO keywords](media/seo/keywords.png)

Further keywords research done :

[Wordtracker](https://www.wordtracker.com/) word chocolate within Ireland

![wordtracker keywords](media/seo/wordtracker_ireland.png)

[Google](https://www.google.com/) - Search for wordkey "chocolate"

![google search](media/seo/google_search.png)


### Mailchimp

To increase audience and to send news, offers and discounts, Mailchimp form was implemented so users can signup for Newsletter. 

![Mailchimp](media/images/mailchimp_email.png)

Message will show when user is successfully signed up.

![Mailchimp subscribed](media/images/mailchimp_email.png)

Audience - E-mail Address has been added to the audience list.

![Mailchimp audience](media/images/audience.png)


Embedded form can be generated through Mailchimp by going to Audience/Signup forms/Embedded forms

![Embedded form](media/images/embedded_form.png)

## Testings

To view all testing documentation, please refer to [TESTING.md](TESTING.md)

### Local Deployment

In order to make a local copy of this repository, you can type the following into your IDE Terminal:

- `git clone https://github.com/Ivana505/art-of-chocolate.git` 

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Ivana505/art-of-chocolate)

The site was deployed to [Heroku](https://art-of-chocolate.herokuapp.com/) pages using following steps: 
   - Sign up or Login to Heroku 
   - Click on the "NEW APPLICATION" and create an App name and choose your region
   - Click on "Deploy" and choose your deployment method
   - If you are connecting with Github choose your main branch and find your repository
   - Add config vars PORT = 8000 and buildpacks python and nodejs
   - Click on deploy manually or automatically
   - The project has now been deployed
   - When deployed click on view
   - If you click on settings on the main menu bar you will find your Heroku git URL

    To install the required packages for this application, type the following: pip3 install -r requirements.txt

NEED TO ADD REQUIREMENTS

The live site can be previewed [here](https://art-of-chocolate.herokuapp.com/).

  # Languages and technologies used
- [Python](https://www.python.org/) - used for core programming language and logic
- [Github](https://github.com/) - used for securely storing the code online
- [Git](https://git-scm.com/) - used for version control
- [Gitpod](https://www.gitpod.io/) - used for online cloud IDE and development
- [Heroku](https://heroku.com/) - platform used to deploy game to cloud online
- [Django Secret Key Generator](https://miniwebtool.com/django-secret-key-generator/) - for generating Secret Key
- [Font Awesome](https://fontawesome.com/) - for Icons on the page
- [Freeformatter](https://www.freeformatter.com/) - used to format and beautify HTML and CSS code
- [PEP8 validator](http://pep8online.com/) - used to validate Python code
- [Coloors](https://coolors.co/) - to create color scheme for the UX section
- [Sitemaps](https://www.xml-sitemaps.com/) - to create sitemaps for SEO.
- [Cloudinary](https://cloudinary.com/) - to store images.
- [Am I reponsive](https://ui.dev/amiresponsive) - to create am I responsive image.
- [Coolors](https://coolors.co/) - to generate color set used for the project.
- [Mailchimp](https://mailchimp.com/?currency=EUR) - to store E-mail Addresses for Users who signed up for Newsletter.
- [Mailjet](https://www.mailjet.com/) - to send order E-mail confirmations.

## Credits and Acknowledgements

  ADD CREDITS

  Image and Social Media sources:
- [YouTube channel ](https://www.youtube.com/)
- [Pixabay](https://pixabay.com/)


  Other sources
 
 - [YouTube channel CodingEx](https://www.youtube.com/watch?v=HsDSXh26yKc) - Helped me with creating chocolate_image.html page.
 - [YouTube channel Dennis Ivy Django Ecommerce series](https://www.youtube.com/watch?v=_ELCMngbM0E) - Used as a boilerplate for the project,.
 - [Smartinsights](https://www.smartinsights.com/marketing-planning/marketing-models/how-to-use-the-7ps-marketing-mix/) - Insight of 7 P's in Marketing.
 - [Emarsys](https://emarsys.com/learn/blog/what-is-b2c-marketing/) - More Information about B2C.
 - [Assemblo](https://assemblo.com/guides/what-are-the-7-ps-of-marketing/)- Insight of 7 P's in Marketing.
 - [Youtube channel Easy WebCode](https://www.youtube.com/watch?v=g55EQkDGdg4) - details in creating Newsletter.
 - [Youtube channel Codepiep](https://www.youtube.com/watch?v=66joNBEyNwE) - Used to set up STRIPE.
 - [Stack Overflow](https://stackoverflow.com/questions/64476542/stripe-error-in-order-to-use-checkout-you-must-set-an-account-or-business-name) - Helped to resolve STRIPE checkout error.
 - [Youtube channel Technology IT](https://www.youtube.com/watch?v=dpU3KY6mQ28) - For adding categories to Django.
 - [Youtube channel Codemy.com](https://www.youtube.com/watch?v=_ph8GF84fX4) - For adding categories to Django.
 - [Django Central](https://djangocentral.com/django-admin-making-model-fields-required/) - For resolving the issue where Django categories showed as objects rather than with their names.
 - [Computerhope.com](https://www.computerhope.com/issues/ch000317.htm) - Used to create go back button.
 - [Pythonstacks](https://www.pythonstacks.com/blog/post/integrating-mailchimp-django/) - For implementing mailchimp.
 - [Youtube channel Cryce Truly](https://www.youtube.com/watch?v=3SKjPppM_DU) - For implementing 404 error page.
 - [Youtube channel Code Varto](https://www.youtube.com/watch?v=g_5ZDrl2KKE) - For restricting letters in the phone input tag.
 - [W3 Schools](https://www.w3schools.com/css/css3_buttons.asp) - For button styling.
 - [Web dev](https://web.dev/csp-xss/?utm_source=lighthouse&utm_medium=devtools) - To add CSP to files to increase Lighthouse best practices.
I want to say thank you to my Mentor Tim for the guidance, and special thanks tp tutor support.


### Content
 - Content was created intentionally for the purpose of this project and this Website. 
 
 
 <!-- *Click to go back to the [top](#art-of-chocolate).* -->


