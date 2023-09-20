from src.database_manager.connection_manager import InsertType, create_engine

engine = create_engine(insert_type=InsertType.BULK_INSERT)
print(engine)
