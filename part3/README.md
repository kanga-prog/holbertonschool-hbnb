# HBnB Application

## Structure du projet

- `app/` : Code principal de l'application
  - `api/` : Routes API organisées par version
  - `models/` : Modèles de données (user, place, review, amenity)
  - `services/` : Logique de service, y compris la façade
  - `persistence/` : Gestion du stockage (référentiel en mémoire)

## Installation

1. Clonez le projet.
2. Installez les dépendances avec :
   ```bash
   pip install -r requirements.txt

## er Diagramm

    erDiagram
      USER {
          char(36) id
          string first_name
          string last_name
          string email
          string password
          boolean is_admin
      }

      PLACE {
          char(36) id
          string title
          text description
          decimal price
          float latitude
          float longitude
          char(36) owner_id
      }

      REVIEW {
          char(36) id
          text text
          int rating
          char(36) user_id
          char(36) place_id
      }

      AMENITY {
          char(36) id
          string name
          string description
      }

      PLACE_AMENITY {
          char(36) place_id
          char(36) amenity_id
      }

      USER ||--o{ PLACE : "owns"
      USER ||--o{ REVIEW : "leaves"
      PLACE ||--o{ REVIEW : "has"
      PLACE ||--o{ PLACE_AMENITY : "has"
      AMENITY ||--o{ PLACE_AMENITY : "belongs to"
    
      %% Admin permissions (special privileges)
      USER ||--o{ USER : "can create"
      USER ||--o{ AMENITY : "can create"

[![](https://mermaid.ink/img/pako:eNqNVN9rwjAQ_ldCYOBAnwZ78E22Pgy2MdwvNgpyJmc9liYlSXWi_u9LbbWtdZt5COl93919ubt0zYWRyIcc7S1BYiGNNQvr9Tkas3V5LpaYg-1dXV8ykrXReUs6YTOyzk80pNiBFPyGYAqkOtYMnFsa28gxNUYhaEZuAjIlXSLbuDo83Y9uonOFevKqocTjt2cSnbCUeTK6RiQKSkGxzJJoOMyUAR_uFOLksms3OjkCDmLMUqOd7CUd1I-jt7vo_V_5O6HFVptIe2aDEJ2c8M1dI1kLyRQI7OoYPUSPdy8f59axbmi7D5O_4rRTt6AQTpNfdXXtpnCzGQzMuur0kMU8FNPFvMuoqllQwsgs8EAqXbusOZymtC9zxNybf-VOsZgEx7zZu5T7xQUbFRPMMrQpORcmzrGey8KslaO2IIUJusvuzXbnIrYIL0FYBI-nCtBU0WbyPk9DViAZnvquOzH3cwxt5AVZgv0qaNvAg9yb55UWfOhtjn1uTZ7M-XAGyoWvPJMhZPWr2FMy0J_GpBVp-wMYiUcS?type=png)](https://mermaid.live/edit#pako:eNqNVN9rwjAQ_ldCYOBAnwZ78E22Pgy2MdwvNgpyJmc9liYlSXWi_u9LbbWtdZt5COl93919ubt0zYWRyIcc7S1BYiGNNQvr9Tkas3V5LpaYg-1dXV8ykrXReUs6YTOyzk80pNiBFPyGYAqkOtYMnFsa28gxNUYhaEZuAjIlXSLbuDo83Y9uonOFevKqocTjt2cSnbCUeTK6RiQKSkGxzJJoOMyUAR_uFOLksms3OjkCDmLMUqOd7CUd1I-jt7vo_V_5O6HFVptIe2aDEJ2c8M1dI1kLyRQI7OoYPUSPdy8f59axbmi7D5O_4rRTt6AQTpNfdXXtpnCzGQzMuur0kMU8FNPFvMuoqllQwsgs8EAqXbusOZymtC9zxNybf-VOsZgEx7zZu5T7xQUbFRPMMrQpORcmzrGey8KslaO2IIUJusvuzXbnIrYIL0FYBI-nCtBU0WbyPk9DViAZnvquOzH3cwxt5AVZgv0qaNvAg9yb55UWfOhtjn1uTZ7M-XAGyoWvPJMhZPWr2FMy0J_GpBVp-wMYiUcS)
