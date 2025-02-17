
# HBnB Evolution - Technical Documentation
## Introduction

This document serves as the technical blueprint for the HBnB Evolution project. The goal of the HBnB Evolution application is to provide a platform similar to AirBnB, where users can manage their profiles, list places they own, leave reviews, and interact with amenities. The application follows a layered architecture, utilizing the Facade pattern to simplify communication between layers. This document will guide the implementation phases by providing a clear understanding of the system architecture, business logic, and API interactions.
## 1. High-Level Architecture
### 1.1 High-Level Package Diagram

    classDiagram
    class PresentationLayer {
        +APIEndpoint
        +UserService
        +PlaceService
        +ReviewService
    }

    class Facade {
        +UserFacade
        +PlaceFacade
        +ReviewFacade
    }

    class BusinessLogicLayer {
        +UserModel
        +PlaceModel
        +ReviewModel
    }

    class PersistenceLayer {
        +UserRepository
        +PlaceRepository
        +ReviewRepository
        +AmenityRepository
    }

    %% Communication Pathways
    PresentationLayer --> Facade : Calls Facade Methods
    Facade --> BusinessLogicLayer : Calls Business Logic Methods
    BusinessLogicLayer --> PersistenceLayer : Accesses Database via Repositories

### 1.2 Explanatory Notes for High-Level Architecture

The HBnB Evolution application follows a three-layer architecture:

**Presentation Layer:**
        This layer is responsible for handling interactions with the user through the API and service endpoints. The UserService, PlaceService, and ReviewService manage all user-facing interactions.

**Facade:**
        The Facade pattern is used to simplify communication between the Presentation Layer and the Business Logic Layer. It provides a unified interface for the presentation layer to access the application’s core business logic, hiding the complexity and reducing direct dependencies between the layers.

**Business Logic Layer:**
        Contains the core application models, like UserModel, PlaceModel, and ReviewModel. This layer encapsulates the business logic and rules for managing the system’s core entities.

**Persistence Layer:**
        Handles data storage and retrieval through repositories. This includes the UserRepository, PlaceRepository, ReviewRepository, and AmenityRepository that perform CRUD operations on the database.

*The Facade acts as the intermediary that abstracts the complexity of business logic and provides the necessary functions to the Presentation Layer. This promotes a clean separation of concerns and simplifies maintenance. 

## 2. Business Logic Layer
### 2.1 Detailed Class Diagram

classDiagram
    class User {
        +String id
        +String username
        +String email
        +String password_hash
        +String full_name
        +String phone_number
        +String profile_picture
        +Boolean is_host
        +Boolean is_guest
        +Date created_at
        +Date updated_at
        +create_account()
        +login()
        +update_profile()
        +change_password()
    }
    
    class Place {
        +String id
        +String host_id
        +String name
        +String description
        +String location
        +Float price_per_night
        +Integer max_guests
        +Boolean is_available
        +Date created_at
        +Date updated_at
        +create_listing()
        +update_listing()
        +delete_listing()
    }

    class Review {
        +String id
        +String user_id
        +String place_id
        +Integer rating
        +String comments
        +Date created_at
        +Date updated_at
        +create_review()
        +update_review()
        +delete_review()
    }

    class Amenity {
        +String id
        +String name
        +String description
        +Date created_at
        +Date updated_at
        +add_amenity_to_place()
        +remove_amenity_from_place()
    }

    User "1" --> "*" Place : Owns
    Place "1" --> "*" Review : Receives
    User "1" --> "*" Review : Writes
    Place "1" --> "*" Amenity : Has

### 2.2 Explanatory Notes for Business Logic Layer

The Business Logic Layer contains the models representing the key entities in the system:

- User: Represents the user profile with attributes such as username, email, full_name, etc. Users can create accounts, login, update their profiles, and manage their information.

-  Place: Represents a property listed by a user. It includes details such as name, location, price_per_night, and methods for managing the listing, like create_listing(), update_listing(), and delete_listing().

- Review: Represents a review written by a user for a place. Reviews include a rating and a comment. Users can create, update, and delete their reviews.

- Amenity: Represents amenities available at a place, like Wi-Fi, parking, etc. Amenities can be added or removed from places.

The relationships between entities are defined as:

- A User can own multiple Places. 

- A Place can have many Reviews. 

- A User can write multiple Reviews. 

- A Place can have multiple Amenities.

## 3. API Interaction Flow
### 3.1 Sequence Diagram for User Registration

sequenceDiagram 

    participant User
    participant API
    participant Facade
    participant UserModel
    participant UserRepository

    User->>API: Sends registration request
    API->>Facade: Calls registerUser()
    Facade->>UserModel: Creates new User
    UserModel->>UserRepository: Saves User to DB
    UserRepository->>UserModel: Confirms user creation
    UserModel->>Facade: Returns success
    Facade->>API: Sends success response
    API->>User: Returns success message

### 3.2 Explanatory Notes for User Registration Sequence Diagram

In the User Registration process:

- The User sends a registration request via the API.
- The API calls the registerUser() method in the Facade.
- The Facade creates a new UserModel and interacts with the UserRepository to store the user in the database.
- Once the user is saved, the UserModel returns a success message, which is passed back through the Facade to the API.
- Finally, the API sends the success message to the User.

### 3.3 Sequence Diagram for Place Creation

sequenceDiagram 

    participant User
    participant API
    participant Facade
    participant PlaceModel
    participant PlaceRepository

    User->>API: Sends create place request
    API->>Facade: Calls createPlace()
    Facade->>PlaceModel: Creates new Place
    PlaceModel->>PlaceRepository: Saves Place to DB
    PlaceRepository->>PlaceModel: Confirms place creation
    PlaceModel->>Facade: Returns success
    Facade->>API: Sends success response
    API->>User: Returns place created message

### 3.4 Explanatory Notes for Place Creation Sequence Diagram

The Place Creation process is similar to user registration, where the user sends a request to create a place. The Facade orchestrates the interaction with the PlaceModel and PlaceRepository to save the new place in the database and return a success message to the User via the API.

### 3.5 Sequence Diagram for Fetching a List of Places

sequenceDiagram 

    participant User
    participant API
    participant Facade
    participant PlaceModel
    participant PlaceRepository

    User->>API: Sends request to fetch list of places
    API->>Facade: Calls getPlaces()
    Facade->>PlaceRepository: Queries places from DB
    PlaceRepository->>PlaceModel: Returns list of places
    PlaceModel->>Facade: Sends list of places
    Facade->>API: Sends list of places to User
    API->>User: Returns list of places response

### 3.6 Explanatory Notes for Fetching a List of Places

In the Fetching a List of Places process:

- The User sends a request to the API to retrieve a list of available places.
- The API calls the getPlaces() method from the Facade.
- The Facade queries the PlaceRepository to fetch the places from the database.
- The PlaceRepository returns the list of places, which is passed back to the Facade.
- The Facade sends the list of places to the API, which then sends it back as a response to the User.

This sequence represents the process of fetching a list of places and how the application interacts between the API, Facade, Business Logic, and Persistence Layer.

### 3.7 Sequence Diagram for Review Submission

sequenceDiagram 

    participant User
    participant API
    participant Facade
    participant ReviewModel
    participant ReviewRepository

    User->>API: Sends review submission request
    API->>Facade: Calls submitReview()
    Facade->>ReviewModel: Creates new Review
    ReviewModel->>ReviewRepository: Saves review to DB
    ReviewRepository->>ReviewModel: Confirms review creation
    ReviewModel->>Facade: Returns success
    Facade->>API: Sends success response
    API->>User: Returns review submission confirmation

### 3.8 Explanatory Notes for Review Submission Sequence Diagram

The Review Submission process works as follows:

    The User submits a review via the API.
    The API calls the submitReview() method from the Facade.
    The Facade creates a new ReviewModel and interacts with the ReviewRepository to store the review in the database.
    Once the review is saved, the ReviewModel returns a success response, which is passed back through the Facade to the API.
    Finally, the API sends the review submission confirmation back to the User.


## Conclusion

This technical documentation provides a comprehensive blueprint for the HBnB Evolution project. It outlines the overall three-layer architecture, detailed class structures for the Business Logic Layer, and the flow of interactions in key API calls, such as User Registration and Place Creation. These diagrams and explanations will guide the development and ensure a well-structured implementation of the application.
