# HCI-Computing-Pet-Adoption-Website

## To Do

- [ ] View pet page
- [ ] Search page
- [ ] Submit interest
- [ ] Delete interest
- [ ] View interest
- [ ] Refactor to use Flask's logging system

---

## Design Requirements
- Design a web application for Pet Adoption.
- The web application will allow adoption of pet (eg. Dog, cat, etc)
- Each pet has
  - Name
  - Photographs of the Pet – up to 3 photos
  - Sex
  - Age
  - Fee ‐ adoption fee
  - Short write up of the pet
  - Type of pet – Dog, Cat, Reptile, Bird, Other
- Allow owners of the pet to post their pet for adoption, edit their post or delete their post
- Allow interested parties to submit their interest by providing their name, contact number. Each Pet can have multiple submissions of interested parties.
- The website should have a page to list down all the pets for adoption based on the type.
  - Search with filters 
- Allow owners of the pet to view the list of interested parties.
- Have it not look like trash

## Entity-Relationship Diagram
```mermaid
erDiagram
  USER || -- |{ INTERESTS : "request to adopt"
  USER || -- |{ PETS : "put up for adoption"
  PETS || -- |{ INTERESTS : "there can be multiple requests for each pet"
  PETS || -- || TYPE  : "have one type"
  PETS || -- |{ PET_PHOTOS : "photos of pets"

  USER {
    int userid PK
    string username
    string password
    int contactnumber
  }

  PETS {
    int petid PK
    int userid FK
    string name
    int age
    float fee
    string writeup
    string sex
    int typeid FK
  }

  TYPE {
    int typeid PK
    string type
  }

  INTERESTS {
    int requestid PK
    int userid FK
    int petid FK
  }

  PET_PHOTOS {
    int petid PK
    blob photos
  }
```
