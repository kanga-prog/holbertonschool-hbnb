# er Diagramm

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
    
[![](https://mermaid.ink/img/pako:eNqNU99rwjAQ_ldCnjbQp8Ee-iZbH4RtDN0PNgrlTM42LE1Kks6J-r8v0Wpbq5splOS-7-6-u-RWlGmONKJo7gVkBopEEb9ep_GErHb7sFgO5urm9poI3hitM0JlZC6MdamCAnuQhHMIFiBkz1qCtQttWjlmWksERYRNgRdC7ZBNUm-eH0Z38aVCnXCypcThjyMcLTOidEKrBuHIRAGSlEawlsNcanC-Jh-n4n27VtkRcBCjFwpNupd0UD-J38bx-7_yt0LDrzEJ5YjxQlR2wreyrWQdpJTAsK9j9Bg_jV8-Lu1jc6Hde0j_itNN3YF8OCXcsq9r-wrX6-FQr-qbjkhCfTNtQvuMupuB4p_MN54k7SUGFjMIrqHtMvSD5XCa0q35iLk3n-XOMDwYS5wOLuGjA1qg8XPB_TxuW5hQl6PvNQ0OHMxXoG48Dyqnp0vFaORMhQNqdJXlNJqDtP5UldzXVc_znlKC-tS6qEmbXwztKtg?type=png)](https://mermaid.live/edit#pako:eNqNU99rwjAQ_ldCnjbQp8Ee-iZbH4RtDN0PNgrlTM42LE1Kks6J-r8v0Wpbq5splOS-7-6-u-RWlGmONKJo7gVkBopEEb9ep_GErHb7sFgO5urm9poI3hitM0JlZC6MdamCAnuQhHMIFiBkz1qCtQttWjlmWksERYRNgRdC7ZBNUm-eH0Z38aVCnXCypcThjyMcLTOidEKrBuHIRAGSlEawlsNcanC-Jh-n4n27VtkRcBCjFwpNupd0UD-J38bx-7_yt0LDrzEJ5YjxQlR2wreyrWQdpJTAsK9j9Bg_jV8-Lu1jc6Hde0j_itNN3YF8OCXcsq9r-wrX6-FQr-qbjkhCfTNtQvuMupuB4p_MN54k7SUGFjMIrqHtMvSD5XCa0q35iLk3n-XOMDwYS5wOLuGjA1qg8XPB_TxuW5hQl6PvNQ0OHMxXoG48Dyqnp0vFaORMhQNqdJXlNJqDtP5UldzXVc_znlKC-tS6qEmbXwztKtg)
