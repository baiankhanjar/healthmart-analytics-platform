# HealthMart Analytics Engineering Platform

An end-to-end analytics engineering portfolio project that simulates a healthcare retail organization and demonstrates a modern ELT workflow using **Python, Google BigQuery, dbt Core, SQL/Jinja, and Git/GitHub**.

HealthMart was built from the business requirements forward: define operational processes and analytical questions, generate realistic synthetic source data, load raw data into a cloud warehouse, transform and test the data with dbt, and organize the final analytical layer as a dimensional model.

> **Data note:** All HealthMart data is synthetic. No real customer, patient, employee, or company data is used.

---

## Project Overview

HealthMart represents a healthcare retail organization with physical stores and multiple operational domains, including customers, loyalty accounts, products, suppliers, stores, inventory, point-of-sale transactions, marketing activity, and returns.

Operational systems are designed to run individual business processes, but analytical questions often require data from several systems at once. This project creates a centralized analytics layer that transforms those separate operational datasets into documented, tested, reusable analytical models.

### Main objectives

- Separate raw operational data from transformed analytical data.
- Build reusable dbt models instead of relying on one-off SQL queries.
- Organize transformations into staging, intermediate, and marts layers.
- Create a dimensional model for consistent business analysis.
- Add automated data-quality checks to the transformation workflow.
- Preserve data lineage and documentation through dbt.
- Practice historical tracking and incremental-processing patterns.
- Maintain the project with Git and GitHub.

---

## Business Processes

The project began by defining the business processes that generate HealthMart data.

| Business Process | Description |
| --- | --- |
| Customer Management | Customer identity, signup information, contact information, and customer status |
| Loyalty Management | Loyalty enrollment, tier, points balance, enrollment date, and account status |
| Customer Address Management | Multiple address records associated with customers |
| Customer Preference Management | Email/SMS preferences, preferred language, and preferred communication channel |
| Supplier Management | Supplier identity, type, location, contact information, and status |
| Product Management | Product catalog, category, brand, supplier, cost price, selling price, and status |
| Store Operations | Store location, region, store type, opening date, and operating status |
| Inventory Management | Store/product inventory, quantity on hand, reorder levels, and update timestamps |
| POS Transactions | Transaction headers including customer, store, transaction date, payment method, and total |
| Transaction Line Items | Product-level detail for each transaction including quantity, unit price, and line total |
| Marketing Campaigns | Marketing and promotional campaign activity |
| Returns | Return headers and returned product line items |

---

## Business Questions

The analytical platform was designed to support questions such as:

- Which stores generate the most revenue and gross profit?
- Which products and product categories perform best?
- How does revenue change by month and over time?
- Which customers are the most valuable?
- Which customers are repeat customers?
- What is the average basket size or transaction value?
- Where are inventory shortages or low-stock conditions occurring?
- Which suppliers are associated with stronger product performance?
- How effective are marketing campaigns and promotions?
- Which products or categories experience the most returns?

These requirements guided the dimensional model and the grain of the final sales fact table.

---

## Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Synthetic source-data generation and data preparation |
| pandas | DataFrame creation and CSV processing |
| Faker | Realistic synthetic customer and business data |
| Google BigQuery | Cloud data warehouse |
| dbt Core 1.11.12 | Transformation, testing, documentation, lineage, snapshots, and modeling |
| dbt-bigquery 1.11.3 | BigQuery adapter for dbt |
| SQL | Warehouse transformations and analytical modeling |
| Jinja | Dynamic and reusable dbt SQL logic |
| dbt-utils | Reusable dbt macros, including surrogate-key generation |
| Git | Version control |
| GitHub | Repository hosting and project history |
| VS Code | Development environment |

---

## Architecture

```text
Business Processes / Operational Domains
                ↓
      Python + Faker Generation
                ↓
         Raw CSV Source Files
                ↓
     Google BigQuery: healthmart_raw
                ↓
             dbt Sources
                ↓
      ┌─────────┼─────────┐
      ↓         ↓         ↓
     CRM       ERP       POS
      └─────────┼─────────┘
                ↓
       Intermediate Models
                ↓
       Dimensions + fct_sales
                ↓
           Star Schema
                ↓
   Executive Sales Dashboard Exposure
```

The project follows an **ELT architecture**: raw data is first loaded into BigQuery, then dbt performs transformations inside the warehouse.

---

## Synthetic Source Data

Python, pandas, Faker, and randomized business rules are used to create synthetic operational data while maintaining relationships between entities.

### Raw source files

| File | Purpose |
| --- | --- |
| `customers.csv` | Customer master data |
| `loyalty_accounts.csv` | Loyalty membership and points |
| `customer_addresses.csv` | Customer address records |
| `customer_preferences.csv` | Communication and language preferences |
| `suppliers.csv` | Supplier master data |
| `products.csv` | Product catalog and pricing |
| `stores.csv` | Store master and regional attributes |
| `inventory.csv` | Store/product inventory and reorder information |
| `transactions.csv` | POS transaction headers |
| `transaction_items.csv` | Transaction line-item detail |
| `campaigns.csv` | Marketing campaign data |
| `returns.csv` | Return header data |
| `return_items.csv` | Returned item detail |

Relationships are maintained across generated datasets using identifiers such as `customer_id`, `supplier_id`, `product_id`, `store_id`, and `transaction_id`.

Transaction and inventory generation was later enhanced with `loaded_at` timestamps to support incremental-processing and source-freshness patterns.

---

## BigQuery Warehouse

The generated source data is loaded into Google BigQuery.

- **Google Cloud project:** `healthmart-analytics`
- **Raw dataset:** `healthmart_raw`
- Raw tables are treated as dbt sources.
- Transformations are performed in separate dbt-managed schemas rather than modifying raw source tables.

Credentials and local dbt connection profiles are intentionally excluded from the repository.

---

## dbt Project Architecture

The dbt project is organized by transformation layer and operational domain.

```text
healthmart_dbt/
├── models/
│   ├── staging/
│   │   ├── crm/
│   │   │   ├── stg_crm.yml
│   │   │   ├── stg_customer_addresses.sql
│   │   │   ├── stg_customer_preferences.sql
│   │   │   ├── stg_customers.sql
│   │   │   └── stg_loyalty_accounts.sql
│   │   ├── erp/
│   │   │   ├── stg_erp.yml
│   │   │   ├── stg_inventory.sql
│   │   │   ├── stg_products.sql
│   │   │   ├── stg_stores.sql
│   │   │   └── stg_suppliers.sql
│   │   └── pos/
│   │       ├── stg_pos.yml
│   │       ├── stg_transaction_items.sql
│   │       └── stg_transactions.sql
│   ├── intermediate/
│   │   ├── int_product_pricing.sql
│   │   ├── int_transaction_items_enriched.sql
│   │   └── intermediate.yml
│   └── marts/
│       ├── dimensions/
│       │   ├── dim_customers.sql
│       │   ├── dim_date.sql
│       │   ├── dim_products.sql
│       │   ├── dim_stores.sql
│       │   └── dimensions.yml
│       ├── facts/
│       │   ├── fct_sales.sql
│       │   └── facts.yml
│       └── exposures.yml
├── macros/
├── seeds/
├── snapshots/
├── tests/
└── dbt_project.yml
```

---

## Staging Layer

The staging layer provides clean, consistently named models on top of raw BigQuery sources.

### CRM

- `stg_customers`
- `stg_customer_addresses`
- `stg_customer_preferences`
- `stg_loyalty_accounts`

### ERP

- `stg_inventory`
- `stg_products`
- `stg_stores`
- `stg_suppliers`

### POS

- `stg_transactions`
- `stg_transaction_items`

The YAML files in each domain contain model and column documentation and applicable data tests.

---

## Intermediate Layer

Intermediate models contain reusable business logic before the final analytical marts.

### `int_product_pricing`

Contains reusable product-pricing logic and was used to practice an **ephemeral** intermediate-model pattern.

### `int_transaction_items_enriched`

Combines transaction items with transaction headers and product/pricing information to create enriched sales detail at the transaction-item grain.

```text
stg_products ───────────────→ int_product_pricing ─┐
                                                   │
stg_transaction_items ─────────────────────────────┼→ int_transaction_items_enriched
                                                   │
stg_transactions ──────────────────────────────────┘
```

The enriched model provides customer, store, date, product, pricing, cost, and gross-profit context used by the sales fact.

---

## Dimensional Model

The final marts layer uses a star-schema-oriented design.

### Dimensions

| Model | Purpose |
| --- | --- |
| `dim_date` | Calendar attributes for time-based analysis |
| `dim_customers` | Customer attributes for customer analysis |
| `dim_products` | Product, category, and brand attributes |
| `dim_stores` | Store and regional attributes |

### Fact

#### `fct_sales`

The central sales fact is modeled at the **transaction-item grain**:

> One row represents one product line within one transaction.

Measures include:

- Quantity
- Unit price
- Sales amount
- Cost amount
- Gross profit

`transaction_id` may repeat because one transaction can contain multiple product lines. `transaction_item_id` identifies the source line item.

A deterministic surrogate sales key is generated with `dbt-utils`:

```sql
{{ dbt_utils.generate_surrogate_key(['sales.transaction_item_id']) }}
```

The fact connects to the date, customer, store, and product dimensions, allowing the same measures to be analyzed consistently across different business attributes.

---

## Data Quality and Testing

Data quality is integrated into the dbt workflow.

### Generic tests

The project uses reusable tests such as:

- `unique`
- `not_null`
- `relationships`
- `accepted_values`

These validate key uniqueness, required fields, referential integrity, and controlled categorical values.

Custom reusable test patterns were also practiced for rules such as positive prices, valid email formats, and accepted-list validation.

### Singular reconciliation test

The project contains:

```text
tests/transaction_totals_match.sql
```

This test compares each transaction header total with the sum of its transaction-item line totals.

```text
transaction header total
        vs.
SUM(transaction line totals)
        ↓
Mismatch returned by query
        ↓
dbt test failure
```

During testing, this rule exposed inconsistencies in the synthetic data-generation logic where transaction headers and line-item totals had been generated independently. The test therefore identified an upstream data-quality issue rather than simply validating SQL syntax.

---

## Snapshots and Historical Tracking

The project includes:

```text
snapshots/product_snapshot.sql
```

`product_snapshot` demonstrates historical change tracking using dbt snapshot / Slowly Changing Dimension Type 2 concepts.

The snapshot preserves previous versions of mutable product records rather than retaining only the latest state.

Relevant dbt snapshot metadata includes:

- `dbt_valid_from`
- `dbt_valid_to`
- `dbt_scd_id`

The current active version of a snapshot record is represented by:

```sql
dbt_valid_to IS NULL
```

The project also encountered a BigQuery Sandbox limitation when snapshot DML was attempted without billing enabled. This was a warehouse-environment limitation rather than a modeling dependency issue.

---

## Incremental Processing

Incremental-model patterns were practiced to avoid rebuilding an entire dataset when only new or changed records need processing.

Key concepts include:

```text
materialized='incremental'
is_incremental()
{{ this }}
unique_key
merge / append
--full-refresh
```

`loaded_at` timestamps were added to transaction and inventory source generation to create a realistic field for incremental-processing logic.

---

## Source Freshness

Source freshness is configured for the `inventory` and `transactions` sources using their `loaded_at` timestamps.

```yaml
config:
  loaded_at_field: loaded_at

  freshness:
    warn_after:
      count: 7
      period: day

    error_after:
      count: 14
      period: day
```

This configuration allows dbt to evaluate how recently these source tables were loaded:

- **Warning:** source data is more than 7 days old.
- **Error:** source data is more than 14 days old.

Freshness can be checked with:

```bash
dbt source freshness
```

This complements dbt data tests: freshness checks whether source data is arriving on time, while data tests validate the quality and integrity of the data.

---

## Materializations

The project was used to work with several dbt materialization patterns:

- **View** - lightweight warehouse views.
- **Table** - persisted analytical tables.
- **Ephemeral** - reusable SQL injected into downstream models rather than persisted as its own relation.
- **Incremental** - processes new/changed data rather than rebuilding all history.
- **Materialized view** - materialization configuration/concept.
- **Project and folder defaults** - centralized configuration through `dbt_project.yml`.

---

## Jinja, Macros, and dbt-utils

The project uses dbt/Jinja concepts to create modular and reusable transformations.

Examples include:

- `ref()`
- `source()`
- `config()`
- `var()`
- `is_incremental()`
- `target.name`
- reusable macros
- DRY transformation patterns

`dbt-utils` is used in the final sales fact to generate a surrogate key.

---

## Seeds

The dbt project includes a `seeds/` area for small, version-controlled reference datasets.

Seeds are loaded with:

```bash
dbt seed
```

This separates static lookup/reference data managed by dbt from operational raw-source data loaded into BigQuery.

---

## Documentation and Lineage

Model and column descriptions are maintained in YAML and surfaced through dbt Docs.

```bash
dbt docs generate
dbt docs serve
```

The generated lineage graph shows the complete transformation path from raw sources to the analytical marts.

```text
healthmart_raw sources
        ↓
CRM / ERP / POS staging
        ↓
intermediate transformations
        ↓
dimensions + fct_sales
        ↓
Executive Sales Dashboard exposure
```

The DAG also shows:

- `stg_products` feeding `product_snapshot`
- product staging feeding `int_product_pricing`
- POS staging feeding `int_transaction_items_enriched`
- transaction models feeding the `transaction_totals_match` test
- dimensions and enriched transaction data converging on `fct_sales`
- `fct_sales` feeding the Executive Sales Dashboard exposure

<img width="1840" height="933" alt="Screenshot 2026-09-16 103437" src="https://github.com/user-attachments/assets/2db4e4fc-536c-4379-83dc-eb4761f21ef9" />

---

## Executive Sales Dashboard Exposure

The project includes `models/marts/exposures.yml`.

The **Executive Sales Dashboard** exposure documents the downstream analytical consumer of `fct_sales` and makes that dependency visible in dbt lineage.

The exposure represents the modeled downstream BI dependency; it does not imply that a Power BI report file is included in this repository.

---

## DAG and Dependency Management

dbt determines execution order from dependencies rather than filenames.

- `source()` connects models to raw warehouse tables.
- `ref()` connects dbt models to one another.
- The resulting DAG determines build order.

```text
Source
  ↓
Staging
  ↓
Intermediate
  ↓
Dimensions / Fact
  ↓
Exposure
```

This makes dependencies explicit and allows testing, documentation, lineage, and selective execution to operate on the same graph.

---

## State and Slim CI Concepts

The project work also included practice with dbt State and Slim CI concepts.

State comparison allows dbt to identify resources that changed relative to a previous project state.

```bash
dbt build --select state:modified
dbt build --select state:modified+
```

`state:modified` selects changed resources, while the downstream `+` can include affected descendants.

The Slim CI pattern uses state-based selection to avoid rebuilding an entire dbt project for every pull request.

```text
Code change
    ↓
Pull request
    ↓
State comparison
    ↓
Build/test modified resources
    ↓
Validate affected downstream nodes
    ↓
Merge
```

These concepts were practiced as part of the project workflow. A fully automated GitHub Actions or dbt Cloud CI pipeline is **not** represented as deployed in this repository.

---

## Common dbt Commands Used or Practiced

```bash
dbt debug
dbt run
dbt test
dbt build
dbt seed
dbt snapshot
dbt deps
dbt docs generate
dbt docs serve
dbt source freshness
dbt run --full-refresh
dbt build --select state:modified
dbt build --select state:modified+
```

---

## Repository Security

The repository was reviewed before public publishing.

Security-related repository practices include:

- Local credential files are not committed.
- `profiles.yml` is not tracked.
- `.env` and `.env.*` are ignored.
- `secrets/` is ignored.
- JSON credential files are ignored.
- dbt `logs/` and generated `target/` artifacts are ignored.
- A previously tracked dbt log was removed from Git tracking.
- New commits use a GitHub noreply email address.

This keeps local credentials, environment configuration, generated logs, and other machine-specific files outside the public project.

---

## Project Workflow

The project was developed in the following sequence:

1. Define the HealthMart business scenario.
2. Identify operational business processes.
3. Define analytical questions and requirements.
4. Design source domains and the ELT architecture.
5. Create the GitHub repository and business-requirements documentation.
6. Generate synthetic operational data with Python and Faker.
7. Load raw CSV data into BigQuery.
8. Declare raw tables as dbt sources.
9. Build CRM, ERP, and POS staging models.
10. Build reusable intermediate transformations.
11. Create conformed dimensions and the `fct_sales` star schema.
12. Add generic and singular data tests.
13. Implement product historical tracking with a dbt snapshot.
14. Practice incremental processing and add source load timestamps.
15. Work with Jinja, macros, dbt-utils, seeds, and materialization patterns.
16. Add the Executive Sales Dashboard exposure.
17. Generate dbt Docs and validate the full lineage graph.
18. Version and publish project changes with Git/GitHub.
19. Review repository security before public publishing.
20. Practice state-based selection and Slim CI concepts.

---

## Key Project Components

```text
Python/Faker
     ↓
Synthetic operational data
     ↓
BigQuery raw warehouse
     ↓
dbt sources
     ↓
Staging models
     ↓
Intermediate business logic
     ↓
Star schema
     ↓
Data tests + snapshots + documentation
     ↓
dbt lineage + exposure
```

---

## Project Status

The core analytics engineering platform is complete as a portfolio implementation, including:

- Business requirements and source-domain design
- Synthetic data generation
- BigQuery raw warehouse
- dbt source declarations
- CRM / ERP / POS staging models
- Intermediate transformations
- Dimensional marts
- `fct_sales`
- Generic and singular data testing
- Snapshot implementation
- Incremental-model practice
- Multiple dbt materialization patterns
- Jinja / macros / dbt-utils
- Seeds
- dbt documentation and lineage
- Executive Sales Dashboard exposure
- Git/GitHub version control and repository security cleanup

Source freshness is configured for the `inventory` and `transactions` sources using `loaded_at`, with 7-day warning and 14-day error thresholds. State/Slim CI concepts were practiced, while a fully automated CI pipeline is not presented as deployed.

---

## Repository

**Project:** `healthmart-analytics-platform`  
**dbt project:** `healthmart_dbt`  
**Warehouse:** Google BigQuery  
**Raw dataset:** `healthmart_raw`

