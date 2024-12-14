##  Database Schema Design

### 3.1 Database Tables

#### Users Table
- **Columns**:
  * `id` (Primary Key)
  * `username` (Unique)
  * `password_hash`
  * `role`
  * `created_at`
- **Constraints**:
  * Unique username
  * Non-null role
  * Timestamp tracking

#### Categories Table
- **Purpose**: Organize and classify products
- **Columns**:
  * `id` (Primary Key)
  * `name` (Unique)
  * `description`
  * `created_at`
- **Use Cases**:
  * Product classification
  * Inventory management
  * Reporting and analytics

#### Products Table
- **Columns**:
  * `id` (Primary Key)
  * `name`
  * `category_id` (Foreign Key to Categories)
  * `price`
  * `stock`
  * `created_at`
- **Features**:
  * Real-time inventory tracking
  * Price management
  * Category association

#### Customers Table
- **Columns**:
  * `id` (Primary Key)
  * `name`
  * `email` (Unique)
  * `phone` (Unique)
  * `address`
  * `created_at`
- **Validation Requirements**:
  * Unique email and phone constraints
  * Comprehensive contact information

#### Invoices Table
- **Columns**:
  * `id` (Primary Key)
  * `customer_id` (Foreign Key to Customers)
  * `total_amount`
  * `discount`
  * `created_at`
- **Functionality**:
  * Track sales transactions
  * Support discount mechanisms

#### Invoice Items Table
- **Columns**:
  * `id` (Primary Key)
  * `invoice_id` (Foreign Key to Invoices)
  * `product_id` (Foreign Key to Products)
  * `quantity`
  * `subtotal`
- **Purpose**:
  * Capture individual line items
  * Enable detailed transaction analysis

#### Payments Table
- **Columns**:
  * `id` (Primary Key)
  * `invoice_id` (Foreign Key to Invoices)
  * `amount_paid`
  * `payment_method`
  * `created_at`
- **Features**:
  * Track payment status
  * Support multiple payment methods