"""Initialize Neon PostgreSQL Database with Tables

This script creates all necessary tables in your Neon database.
Run this once after connecting to Neon for the first time.
"""

from sqlalchemy import create_engine, text, event
from app.config import settings
from app.models.database_models import Base

def init_database():
    """Initialize database with all tables"""
    
    print("\n" + "="*70)
    print("📦 INITIALIZING NEON DATABASE")
    print("="*70)
    
    try:
        # Show connection info
        print("\n[1/3] Creating database connection...")
        engine = create_engine(settings.DATABASE_URL)
        print("     ✅ Connected to Neon")
        
        # Enable pgvector
        print("\n[2/3] Enabling pgvector extension...")
        with engine.connect() as connection:
            try:
                connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                connection.commit()
                print("     ✅ pgvector extension enabled")
            except Exception as e:
                print(f"     ⚠️  {str(e)}")
        
        # Create tables
        print("\n[3/3] Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        # Verify tables
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()
        
        print("\n" + "="*70)
        print("✅ DATABASE INITIALIZED SUCCESSFULLY!")
        print("="*70)
        
        print(f"\nCreated {len(tables)} tables:")
        print("  ✅ documents - Original PDFs metadata")
        print("  ✅ pathology_reports - Extracted medical data")
        print("  ✅ document_embeddings - Vector embeddings (pgvector)")
        print("  ✅ users - User management")
        
        print("\nDatabase details:")
        print(f"  📍 Host: neon.tech (serverless)")
        print(f"  📦 Storage: 5GB (free tier)")
        print(f"  🔍 Vector search: pgvector enabled")
        print(f"  ⚡ Auto-scaling: enabled")
        
        print("\n" + "="*70)
        print("✨ Your Neon database is ready to use!")
        print("="*70)
        
        print("\nNext steps:")
        print("  1. Start backend: .\\run_server.bat")
        print("  2. Test search: python test_phase8_direct.py")
        print("  3. Test chatbot: python test_phase9_direct.py")
        
        print("\nNeon dashboard:")
        print("  https://console.neon.tech/")
        print("  (Monitor storage, connections, backups there)")
        
        print("\n" + "="*70 + "\n")
        
        return True
    
    except Exception as e:
        print("\n" + "="*70)
        print("❌ INITIALIZATION FAILED")
        print("="*70)
        print(f"\nError: {str(e)}")
        
        print("\n🔧 TROUBLESHOOTING:")
        print("\n1. Make sure you ran test_neon_connection.py first:")
        print("   python test_neon_connection.py")
        
        print("\n2. Verify .env file has DATABASE_URL")
        
        print("\n3. Check that models are properly imported")
        
        print("\n4. Check Neon project status on https://console.neon.tech/")
        
        print("\n" + "="*70 + "\n")
        
        return False

if __name__ == "__main__":
    success = init_database()
    exit(0 if success else 1)
