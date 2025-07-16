# Database Setup Guide for MASS Framework

## DATABASE_URL Format
```
postgresql://username:password@host:port/database_name
```

## Option 1: Google Cloud SQL (Recommended for Production)

Since you're already using Google Cloud Platform, this is the most integrated solution.

### Step 1: Create Cloud SQL Instance
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **SQL** in the left menu
3. Click **"CREATE INSTANCE"**
4. Choose **PostgreSQL**
5. Configure:
   - **Instance ID**: `mass-framework-db`
   - **Password**: Create a strong password
   - **Database version**: PostgreSQL 15 (latest)
   - **Machine type**: `db-f1-micro` (for testing) or `db-g1-small` (for production)
   - **Storage**: 10 GB (minimum)
6. Click **"CREATE INSTANCE"**

### Step 2: Create Database and User
1. Once the instance is created, click on it
2. Go to **"DATABASES"** tab
3. Click **"CREATE DATABASE"**
   - **Database name**: `mass_framework`
4. Go to **"USERS"** tab
5. Click **"CREATE USER ACCOUNT"**
   - **Username**: `mass_user`
   - **Password**: Create a strong password
   - **Host**: `%` (allows connections from anywhere)

### Step 3: Get Connection Details
1. Go to **"OVERVIEW"** tab
2. Note the **Public IP address**
3. Your DATABASE_URL will be:
```
postgresql://mass_user:your_password@PUBLIC_IP:5432/mass_framework
```

## Option 2: Railway (Easy Cloud Database)

### Step 1: Create Railway Account
1. Go to [Railway](https://railway.app/)
2. Sign up with GitHub
3. Click **"New Project"**

### Step 2: Add PostgreSQL
1. Click **"Add Service"**
2. Choose **"Database"** → **"PostgreSQL"**
3. Wait for it to provision

### Step 3: Get Connection String
1. Click on your PostgreSQL service
2. Go to **"Connect"** tab
3. Copy the **Postgres Connection URL**
4. It will look like: `postgresql://postgres:password@railway-host:5432/railway`

## Option 3: Supabase (Free Tier Available)

### Step 1: Create Supabase Project
1. Go to [Supabase](https://supabase.com/)
2. Sign up and create a new project
3. Wait for setup to complete

### Step 2: Get Connection String
1. Go to **Settings** → **Database**
2. Copy the **Connection string**
3. Format: `postgresql://postgres:password@db.supabase.co:5432/postgres`

## Option 4: Local PostgreSQL (Development Only)

### Install PostgreSQL on Windows
1. Download from [PostgreSQL Downloads](https://www.postgresql.org/download/windows/)
2. Run the installer
3. Set password for `postgres` user
4. Keep default port (5432)

### Create Database and User
```sql
-- Connect to PostgreSQL as postgres user
psql -U postgres

-- Create database
CREATE DATABASE mass_framework;

-- Create user
CREATE USER mass_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mass_framework TO mass_user;

-- Connect to the database
\c mass_framework

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO mass_user;
```

### Local DATABASE_URL
```
postgresql://mass_user:your_password@localhost:5432/mass_framework
```

## Security Best Practices

### 1. Strong Passwords
- Use at least 12 characters
- Include uppercase, lowercase, numbers, and symbols
- Avoid common words or patterns

### 2. Network Security
- Use SSL connections when possible
- Restrict IP access in cloud databases
- Use private networks when available

### 3. User Permissions
- Create dedicated users for the application
- Grant only necessary permissions
- Avoid using superuser accounts

## Testing the Connection

### Using psql (PostgreSQL client)
```bash
# Test connection
psql "postgresql://username:password@host:5432/database"

# If successful, you'll see the PostgreSQL prompt
```

### Using Python
```python
import psycopg2

try:
    conn = psycopg2.connect("postgresql://username:password@host:5432/database")
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
```

## Common Issues and Solutions

### 1. "Connection refused"
- Check if database server is running
- Verify host and port are correct
- Check firewall settings

### 2. "Authentication failed"
- Verify username and password
- Check if user exists and has proper permissions
- Ensure password doesn't contain special characters that need escaping

### 3. "Database does not exist"
- Create the database first
- Check database name spelling
- Ensure user has access to the database

### 4. "SSL connection required"
- Add `?sslmode=require` to the end of your DATABASE_URL
- Example: `postgresql://user:pass@host:5432/db?sslmode=require`

## Recommended Setup for Production

### Google Cloud SQL with Private IP
1. Create Cloud SQL instance with private IP
2. Set up VPC connector for Cloud Run
3. Use private IP in DATABASE_URL
4. Enable SSL connections

### Example Production DATABASE_URL
```
postgresql://mass_user:strong_password@10.0.0.1:5432/mass_framework?sslmode=require
```

## Next Steps

1. **Choose your database option** (recommend Google Cloud SQL)
2. **Set up the database** following the steps above
3. **Test the connection** using the provided methods
4. **Use the DATABASE_URL** in your GitHub secrets setup
5. **Verify it works** with the test workflow

## Quick Setup Commands

### For Google Cloud SQL (if you have gcloud CLI):
```bash
# Create instance
gcloud sql instances create mass-framework-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --root-password=your_root_password

# Create database
gcloud sql databases create mass_framework --instance=mass-framework-db

# Create user
gcloud sql users create mass_user \
    --instance=mass-framework-db \
    --password=your_user_password

# Get connection info
gcloud sql instances describe mass-framework-db --format="value(connectionName)"
```

**Which option would you like to use?** I can help you set up any of these database solutions! 