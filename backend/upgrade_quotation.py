from sqlalchemy import text
from app.db.session import engine

def upgrade_quotation():
    print("Iniciando actualización de la tabla quotations...")
    with engine.connect() as conn:
        # Add customer_id column
        try:
            conn.execute(text("ALTER TABLE quotations ADD COLUMN customer_id UUID;"))
            print("Columna 'customer_id' añadida.")
        except Exception as e:
            print(f"Columna 'customer_id' ya existe o error: {e}")
        
        # Add customer_order_id column
        try:
            conn.execute(text("ALTER TABLE quotations ADD COLUMN customer_order_id UUID;"))
            print("Columna 'customer_order_id' añadida.")
        except Exception as e:
            print(f"Columna 'customer_order_id' ya existe o error: {e}")
        
        # Add foreign key constraint for customer_id (if customers table exists)
        try:
            conn.execute(text("ALTER TABLE quotations ADD CONSTRAINT quotations_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customers(id);"))
            print("Constraint FOREIGN KEY para customer_id añadida.")
        except Exception as e:
            print(f"Error añadiendo constraint para customer_id (podría ya existir): {e}")
        
        # Add foreign key constraint for customer_order_id
        try:
            conn.execute(text("ALTER TABLE quotations ADD CONSTRAINT quotations_customer_order_id_fkey FOREIGN KEY (customer_order_id) REFERENCES customer_orders(id);"))
            print("Constraint FOREIGN KEY para customer_order_id añadida.")
        except Exception as e:
            print(f"Error añadiendo constraint para customer_order_id (podría ya existir): {e}")
        
        conn.commit()
    print("Actualización de quotations completada.")

if __name__ == "__main__":
    upgrade_quotation()
