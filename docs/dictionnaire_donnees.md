# **Dictionnaire de données - Open Prices**


Le dataset utilisé est un dataset open source provenant du site datagouv nommé [Open Prices](https://www.data.gouv.fr/datasets/open-prices/).   
Il vise à collecter et partager des prix de produits à l’échelle mondiale.  
    
Le fichier est fourni au format Parquet et comprend 48 colonnes pour un total de 132 440 lignes.  
La version exploitée dans ce projet correspond à mise à jour du 27 novembre 2025. 
     
     
| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| id | int | The ID of the price in DB | 42629 |
| type | string | Type of the record | PRODUCT |
| product_code | string | The barcode of the product, null if the product is a "raw" product | 3560070283484 |
| product_name | string | Name of the product, if available | BIO SAURE SAHNE |
| category_tag | string | Category of the product, only for "raw" products. Uses Open Food Facts taxonomy | en:broccoli |
| labels_tags | string | Labels of the product, only for "raw" products. Uses Open Food Facts label taxonomy | ['en:organic'] |
| origins_tags | string | Origins of the product, only for "raw" products. Uses Open Food Facts origin taxonomy | ['en:unknown'] |
| price | float | Price of the product, with discount if any | 1.25 |
| price_is_discounted | bool | Whether the price is discounted | False |
| price_without_discount | float | Price without discount, null if not discounted | 9.99 |
| price_per | string | Unit for which the price is given (e.g., "KILOGRAM", "UNIT") | KILOGRAM |
| currency | string | Currency of the price | EUR |
| location_osm_id | int | OpenStreetMap ID of the location | 123456789 |
| location_osm_type | string | Type of OpenStreetMap location (e.g., NODE, WAY) | NODE |
| location_id | int | ID of the location in Open Prices DB | 9876 |
| date | datetime | Date when the price was recorded | 2024-01-16 |
| proof_id | int | ID of the proof of the price in Open Prices DB | 54321 |
| owner | string | Hashed owner of the price for privacy | abc123hash |
| created | datetime | Date when the price was created in Open Prices DB | 2024-01-16 18:29:47 |
| updated | datetime | Date when the price was last updated in Open Prices DB | 2024-08-25 13:41:04 |
| proof_file_path | string | Path to the proof file in Open Prices DB | /proofs/42629.pdf |
| proof_type | string | Type of the proof (RECEIPT, PRICE_TAG, GDPR_REQUEST, SHOP_IMPORT) | RECEIPT |
| proof_date | datetime | Date of the proof | 2024-01-15 |
| proof_currency | string | Currency of the proof, should match price currency | EUR |
| proof_created | datetime | Datetime when the proof was created in Open Prices DB | 2024-01-16 18:29:47 |
| proof_updated | datetime | Datetime when the proof was last updated in Open Prices DB | 2024-08-25 13:41:04 |
| location_osm_display_name | string | Display name of the OpenStreetMap location | Supermarché Paris 12 |
| location_osm_address_city | string | City of the OpenStreetMap location | Paris |
| location_osm_address_postcode | string | Postcode of the OpenStreetMap location | 75012 |
| location_osm_address_country | string | Country of the OpenStreetMap location | France |
| location_osm_address_country_code | string | Country code | FR |
| location_osm_lat | float | Latitude of the location | 48.848500 |
| location_osm_lon | float | Longitude of the location | 2.370951 |
| location_website_url | string | Website URL of the store if available | https://www.but.fr |
| location_source | string | Source of the location info | API |
| location_created | datetime | Timestamp when the location record was created | 2024-01-16 18:29:47 |
| location_updated | datetime | Timestamp when the location record was last updated | 2024-08-25 13:41:04 |
