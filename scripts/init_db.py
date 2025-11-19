#!/usr/bin/env python3
"""
Database initialization script.

This script creates the SQLite database and tables needed for the application.

Usage:
    python scripts/init_db.py
"""
import asyncio
import os
import sys
from pathlib import Path

# Add app/backend to Python path
backend_path = Path(__file__).parent.parent / "app" / "backend"
sys.path.insert(0, str(backend_path))

from core.database import init_db, seed_sample_data


async def main():
    """Initialize database and optionally seed data."""
    print("🗄️  Initializing database...")

    try:
        # Initialize database tables
        await init_db()
        print("✅ Database tables created successfully!")

        # Ask if user wants to seed sample data
        seed = input("\n📦 Seed sample data? (y/n): ").lower().strip()

        if seed == 'y':
            await seed_sample_data()
            print("✅ Sample data seeded successfully!")
            print("\nSample tasks created:")
            print("  1. Learn Quart framework (pending)")
            print("  2. Build REST API (in_progress)")
            print("  3. Write unit tests (completed)")

        print("\n✨ Database initialization complete!")
        print(f"📁 Database location: {os.getenv('DATABASE_URL', 'sqlite:///app.db')}")

    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
