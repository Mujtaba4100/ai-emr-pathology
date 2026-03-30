#!/usr/bin/env python3
"""Phase 6 Database Connection Test"""

import sys
import traceback

def test_database_connection():
    """Test PostgreSQL connection and table creation"""
    
    print("=" * 70)
    print("  PHASE 6: DATABASE DESIGN & STORAGE - CONNECTION TEST")
    print("=" * 70)
    
    print("\n[1/3] Checking database configuration...")
    try:
        from app.config import settings
        
        if not settings.POSTGRES_HOST:
            print("⚠️  PostgreSQL host not configured")
            print("    Add POSTGRES_HOST to .env file")
            return
        
        print(f"✅ Database config loaded")
        print(f"   Host: {settings.POSTGRES_HOST}")
        print(f"   Port: {settings.POSTGRES_PORT}")
        print(f"   Database: {settings.POSTGRES_DB}")
        print(f"   User: {settings.POSTGRES_USER}")
    
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        traceback.print_exc()
        return
    
    print("\n[2/3] Attempting database connection...")
    try:
        from app.database import engine
        from app.models.database_models import Base
        
        # Try to connect
        with engine.connect() as conn:
            print("✅ Database connection successful!")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n   Possible solutions:")
        print("   1. Ensure PostgreSQL is running")
        print("   2. Check credentials in .env:")
        print("      POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD")
        print("   3. Ensure database 'emr_system' exists, or create it:")
        print("      createdb -U postgres emr_system")
        traceback.print_exc()
        return
    
    print("\n[3/3] Verifying table structure...")
    try:
        from app.database import SessionLocal
        from app.models.database_models import Document, PathologyReport, DocumentEmbedding, User
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['documents', 'pathology_reports', 'document_embeddings', 'users']
        created_tables = [t for t in expected_tables if t in tables]
        
        print(f"✅ Tables verified:")
        for table in created_tables:
            print(f"   - {table}")
        
        if len(created_tables) == len(expected_tables):
            print("\n✅ ALL TABLES CREATED SUCCESSFULLY!")
        else:
            print(f"\n⚠️  Only {len(created_tables)}/{len(expected_tables)} tables created")
    
    except Exception as e:
        print(f"❌ Failed to verify tables: {e}")
        traceback.print_exc()
        return
    
    print("\n" + "=" * 70)
    print("✅ PHASE 6 DATABASE CONNECTION TEST COMPLETE")
    print("=" * 70)
    print("\nDatabase is ready for data storage!")

if __name__ == "__main__":
    test_database_connection()
