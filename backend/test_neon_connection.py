"""Test Neon PostgreSQL Connection

This script verifies that your Neon database is properly configured
and accessible from your backend.
"""

from sqlalchemy import create_engine, text
from app.config import settings

def test_connection():
    """Test connection to Neon database"""
    
    print("\n" + "="*70)
    print("🔍 TESTING NEON CONNECTION")
    print("="*70)
    
    # Show connection details (masked password)
    db_url = settings.DATABASE_URL
    masked_url = db_url[:db_url.find("@")].replace(settings.DATABASE_URL.split("://")[1].split("@")[0], "***:***") + db_url[db_url.find("@"):]
    print(f"\n📍 Connection URL: {masked_url}")
    
    try:
        # Step 1: Create engine
        print("\n[1/4] Creating SQLAlchemy engine...")
        engine = create_engine(settings.DATABASE_URL)
        print("     ✅ Engine created successfully")
        
        # Step 2: Test basic connection
        print("\n[2/4] Testing database connection...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as connection_test"))
            data = result.fetchone()
            print("     ✅ Connected to database!")
            print(f"     📊 Test query result: {data[0]}")
        
        # Step 3: Check pgvector extension
        print("\n[3/4] Checking pgvector extension...")
        with engine.connect() as connection:
            try:
                connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                connection.commit()
                print("     ✅ pgvector extension is available!")
            except Exception as e:
                print(f"     ⚠️  pgvector: {str(e)}")
        
        # Step 4: Test table access
        print("\n[4/4] Testing table access...")
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            if tables:
                print(f"     ✅ Found {len(tables)} tables:")
                for table in tables:
                    print(f"        • {table[0]}")
            else:
                print("     ℹ️  No tables yet (run init_neon_db.py to create them)")
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED - NEON IS WORKING!")
        print("="*70)
        print("\nYour backend is ready to use Neon database.")
        print("\nNext steps:")
        print("  1. Run: python init_neon_db.py (to create tables)")
        print("  2. Run: python test_phase8_direct.py (to test search)")
        print("  3. Run: python test_phase9_direct.py (to test chatbot)")
        print("\n" + "="*70 + "\n")
        
        return True
    
    except Exception as e:
        print("\n" + "="*70)
        print("❌ CONNECTION FAILED")
        print("="*70)
        print(f"\nError: {str(e)}")
        
        print("\n🔧 TROUBLESHOOTING:")
        print("\n1. Check your .env file:")
        print("   - File should be at: E:\\FYP\\backend\\.env")
        print("   - Should contain: DATABASE_URL=postgresql://...")
        
        print("\n2. Verify DATABASE_URL format:")
        print("   - Should be: postgresql://user:password@host/database")
        print("   - Example: postgresql://neonuser:pass@ep-xxx.neon.tech/emr_database")
        
        print("\n3. Check Neon console:")
        print("   - Login to: https://console.neon.tech/")
        print("   - Verify project is active")
        print("   - Copy fresh connection string")
        
        print("\n4. Test connectivity:")
        print("   - Check internet connection")
        print("   - Try ping: ping ep-cool-moon-12345.neon.tech")
        
        print("\n5. Check credentials:")
        print("   - Verify password has no special characters (or proper escaping)")
        print("   - Check username is correct (usually 'neonuser')")
        
        print("\n" + "="*70 + "\n")
        
        return False

if __name__ == "__main__":
    success = test_connection()
    exit(0 if success else 1)
