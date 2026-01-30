from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def seed_products():
    db = SessionLocal()
    
    # Clear existing products if desired, or just add new ones
    # db.query(models.Product).delete()
    
    products = [
        {"name": "5 HP Top Bush Cover A", "description": "High-quality metal bush cover for 5 HP pumps.", "rate": 296.44, "image_url": "https://img.freepik.com/free-photo/mechanical-engineering-parts-steel_23-2148921102.jpg"},
        {"name": "5 HP Spacer Bush Cover A", "description": "Precision spacer bush cover for 5 HP systems.", "rate": 132.18, "image_url": "https://img.freepik.com/free-photo/industrial-metal-part-closeup_23-2148921105.jpg"},
        {"name": "3 HP Suction Cover", "description": "Durable suction cover designed for 3 HP pumps.", "rate": 104.97, "image_url": "https://img.freepik.com/free-photo/macro-shot-internal-combustion-engine-part_23-2148921108.jpg"},
        {"name": "3 HP NRD", "description": "Non-return device (NRD) for 3 HP water systems.", "rate": 251.25, "image_url": "https://img.freepik.com/free-photo/steel-valve-industrial-assembly_23-2148921110.jpg"},
        {"name": "1.12 kW NRV", "description": "Standard non-return valve for 1.12 kW motors.", "rate": 216.07, "image_url": "https://img.freepik.com/free-photo/industrial-components-arranged-table_23-2148921115.jpg"},
        {"name": "7.5 HP Top Bush Cover A", "description": "Heavy-duty top bush cover for 7.5 HP industrial pumps.", "rate": 432.55, "image_url": "https://img.freepik.com/free-photo/metal-spare-parts-white-background_23-2148312015.jpg"},
        {"name": "7.5 HP Indian Bush Cover", "description": "Specialized Indian bush cover & dragging valley.", "rate": 231.25, "image_url": "https://img.freepik.com/free-photo/metal-cylinder-machine-part_23-2148312018.jpg"},
        {"name": "7.5 HP Discharge Cover A", "description": "Robust discharge cover for 7.5 HP flow systems.", "rate": 221.32, "image_url": "https://img.freepik.com/free-photo/precision-metal-part-isolated_23-2148312020.jpg"},
        {"name": "Discharge Cover Stag BA", "description": "Specialized Stag BA discharge cover.", "rate": 110.12, "image_url": "https://img.freepik.com/free-photo/shiny-metalous-background_23-2148312025.jpg"},
        {"name": "7.5 HP Internal Bush Cover T", "description": "Internal version bush cover for T-type systems.", "rate": 216.07, "image_url": "https://img.freepik.com/free-photo/metal-gears-set-isolated_23-2148312030.jpg"},
        {"name": "7.5 HP Spacer Bush Cover T", "description": "Spacer bush cover for T-type pumps (7.5 HP).", "rate": 132.11, "image_url": "https://img.freepik.com/free-photo/complex-metal-part-manufactured_23-2148312035.jpg"},
        {"name": "7.5 HP Discharge Cover T", "description": "T-type discharge cover for high-capacity systems.", "rate": 221.32, "image_url": "https://img.freepik.com/free-photo/industrial-metal-hardware-closeup_23-2148312040.jpg"},
    ]

    for p in products:
        product = models.Product(**p)
        db.add(product)
    
    db.commit()
    db.close()
    print("Metal products seeded successfully!")

if __name__ == "__main__":
    seed_products()
