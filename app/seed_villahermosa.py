# app/seed_villahermosa.py
"""
Script de precarga de datos reales para la región de Villahermosa, Municipio de Centro, Tabasco.
Organismo: Sistema de Agua y Saneamiento (SAS Centro)
Normativa de calidad: NOM-127-SSA1-2021
"""

from datetime import date, timedelta
from app.extensions import db
from app.Auth.blueprints.auth.models import User
from app.Admin.blueprints.source.models import WaterSource
from app.Admin.blueprints.chemical.models import Chemical
from app.Admin.blueprints.storage_tank.models import StorageTank
from app.Admin.blueprints.service_area.models import ServiceArea
from app.Admin.blueprints.pipeline.models import Pipeline
from app.Admin.blueprints.treatment_record.models import TreatmentRecord
from app.Admin.blueprints.customer.models import Customer
from app.Admin.blueprints.meter.models import Meter
from app.Admin.blueprints.meter_reading.models import MeterReading
from app.Admin.blueprints.invoice.models import Invoice
from app.Admin.blueprints.receipt.models import Receipt


def populate_villahermosa_data():
    """Inserta o actualiza la infraestructura y usuarios reales de Villahermosa."""
    db.create_all()

    # 1. Usuarios con roles para SERVITAB Villahermosa
    users_data = [
        ("admin_servitab", "AdminServitab2026!", "Admin"),
        ("admin_sas", "AdminVillahermosa2026!", "Admin"),
        ("operador_planta", "Operador2026!", "Staff"),
        ("logistica_pipas", "Pipas2026!", "Staff"),
        ("cajero_servitab", "CajaServitab2026!", "Counter"),
    ]
    for username, password, role in users_data:
        u = User.query.filter_by(username=username).first()
        if not u:
            u = User(username=username, role=role)
            u.set_password(password)
            db.session.add(u)
        else:
            u.role = role
            u.set_password(password)

    db.session.commit()

    # 2. Fuentes de Captación de Villahermosa
    sources_data = [
        {
            "source_name": "Río Carrizal (Bocatoma I - El Espejo)",
            "source_type": "river",
            "location": "Periférico Carlos Pellicer Cámara, Fracc. El Espejo",
            "capacity_m3_day": 95000.0,
            "status": "Active",
            "remarks": "Fuente superficial de menor turbiedad relativa. Abastece la PTAP Carrizal y la captación del Acueducto Usumacinta.",
        },
        {
            "source_name": "Río Grijalva (Captación Paseo de la Sierra)",
            "source_type": "river",
            "location": "Paseo de la Sierra, Col. Primero de Mayo",
            "capacity_m3_day": 180000.0,
            "status": "Active",
            "remarks": "Captación principal e histórica de la PTAP Villahermosa. Sujeta a fuertes incrementos de turbiedad y sólidos por lluvias en la sierra.",
        },
        {
            "source_name": "Río La Sierra / Mezcalapa (Captación Parrilla)",
            "source_type": "river",
            "location": "Corredor Parrilla - Torno Largo",
            "capacity_m3_day": 30000.0,
            "status": "Active",
            "remarks": "Alimenta la planta potabilizadora Parrilla y abastece el corredor sur hacia Playas del Rosario.",
        },
        {
            "source_name": "Batería de Pozos La Manga / Gaviotas",
            "source_type": "well",
            "location": "Colonia La Manga II",
            "capacity_m3_day": 15000.0,
            "status": "Active",
            "remarks": "Pozos profundos de extracción de acuífero para soporte en estiaje o paros por turbiedad en ríos.",
        },
        {
            "source_name": "Batería de Pozos Ocuiltzapotlán - Macultepec",
            "source_type": "well",
            "location": "Villa Ocuiltzapotlán, Carretera Villahermosa-Frontera",
            "capacity_m3_day": 10000.0,
            "status": "Active",
            "remarks": "Pozos de agua subterránea para la zona suburbana y conurbada norte de Centro.",
        },
    ]

    source_objs = {}
    for s in sources_data:
        existing = WaterSource.query.filter_by(source_name=s["source_name"]).first()
        if not existing:
            ws = WaterSource(**s)
            db.session.add(ws)
            db.session.flush()
            source_objs[s["source_name"]] = ws
        else:
            source_objs[s["source_name"]] = existing

    # 3. Químicos y Reactivos utilizados en PTAP de Villahermosa (NOM-127-SSA1-2021)
    chemicals_data = [
        {
            "chemical_name": "Sulfato de Aluminio Líquido",
            "unit": "kg",
            "default_dose_mgL": 35.0,
            "status": "Active",
            "remarks": "Coagulante primario para coagulación y reducción de turbiedad en aguas arcillosas del Grijalva y Carrizal.",
        },
        {
            "chemical_name": "Policloruro de Aluminio (PAC)",
            "unit": "L",
            "default_dose_mgL": 22.0,
            "status": "Active",
            "remarks": "Coagulante inorgánico de alta eficiencia para picos de turbiedad extrema (>1000 NTU) por lluvias.",
        },
        {
            "chemical_name": "Polímero Catiónico Floculante",
            "unit": "kg",
            "default_dose_mgL": 1.5,
            "status": "Active",
            "remarks": "Ayudante de coagulación para formación de floc pesado y sedimentación acelerada.",
        },
        {
            "chemical_name": "Gas Cloro (Cilindros de 1 Ton)",
            "unit": "kg",
            "default_dose_mgL": 2.5,
            "status": "Active",
            "remarks": "Desinfección terminal en PTAP Villahermosa y Carrizal. Garantiza 0.2 a 1.5 mg/L de cloro libre residual (NOM-127).",
        },
        {
            "chemical_name": "Hipoclorito de Sodio (13% p/p)",
            "unit": "L",
            "default_dose_mgL": 3.0,
            "status": "Active",
            "remarks": "Desinfectante para plantas menores, estaciones de bombeo y pozos profundos.",
        },
        {
            "chemical_name": "Cal Hidratada",
            "unit": "kg",
            "default_dose_mgL": 12.0,
            "status": "Active",
            "remarks": "Ajuste de pH y estabilización del agua cruda de captación.",
        },
    ]

    chemical_objs = {}
    for c in chemicals_data:
        existing = Chemical.query.filter_by(chemical_name=c["chemical_name"]).first()
        if not existing:
            ch = Chemical(**c)
            db.session.add(ch)
            db.session.flush()
            chemical_objs[c["chemical_name"]] = ch
        else:
            chemical_objs[c["chemical_name"]] = existing

    # 4. Tanques de Almacenamiento y Cárcamos de Rebombeo
    tanks_data = [
        {
            "source_key": "Río Carrizal (Bocatoma I - El Espejo)",
            "tank_name": "Tanque Elevado Ciudad Deportiva (Atasta)",
            "capacity_m3": 5000.0,
            "status": "Active",
            "remarks": "Tanque elevado icónico de Villahermosa. Suministra por gravedad a Atasta de Serra, Tamulté y Lindavista.",
        },
        {
            "source_key": "Río Grijalva (Captación Paseo de la Sierra)",
            "tank_name": "Cisterna Central y Rebombeo Paseo de la Sierra",
            "capacity_m3": 12000.0,
            "status": "Active",
            "remarks": "Cisterna de almacenamiento de agua tratada y estación de rebombeo de la PTAP Villahermosa hacia Centro y Mayito.",
        },
        {
            "source_key": "Río Carrizal (Bocatoma I - El Espejo)",
            "tank_name": "Tanque Elevado Tabasco 2000",
            "capacity_m3": 3500.0,
            "status": "Active",
            "remarks": "Almacenamiento y regulación para la zona ejecutiva, hotelera y fraccionamientos de Tabasco 2000.",
        },
        {
            "source_key": "Río Carrizal (Bocatoma I - El Espejo)",
            "tank_name": "Tanque de Rebombeo Loma de Caballo",
            "capacity_m3": 2500.0,
            "status": "Active",
            "remarks": "Regulación de presión para colonias del poniente y corredor hacia Anacleto Canabal.",
        },
        {
            "source_key": "Río La Sierra / Mezcalapa (Captación Parrilla)",
            "tank_name": "Cisterna de Rebombeo Gaviotas / Torno Largo",
            "capacity_m3": 2200.0,
            "status": "Active",
            "remarks": "Rebombeo de agua tratada para los sectores Gaviotas Norte, Gaviotas Sur y Manga.",
        },
    ]

    tank_objs = {}
    for t in tanks_data:
        existing = StorageTank.query.filter_by(tank_name=t["tank_name"]).first()
        if not existing:
            st = StorageTank(
                source_id=source_objs[t["source_key"]].id,
                tank_name=t["tank_name"],
                capacity_m3=t["capacity_m3"],
                status=t["status"],
                remarks=t["remarks"],
            )
            db.session.add(st)
            db.session.flush()
            tank_objs[t["tank_name"]] = st
        else:
            tank_objs[t["tank_name"]] = existing

    # 5. Sectores Hidráulicos y Colonias de Villahermosa
    areas_data = [
        {
            "area_code": "SEC-001",
            "area_name": "Sector 1: Centro Histórico - Jesús García - Guayabal",
            "remarks": "Comprende Centro, Mayito, Jesús García, Guayabal, Municipal y Paseo Tabasco.",
        },
        {
            "area_code": "SEC-002",
            "area_name": "Sector 2: Tabasco 2000 - Multiochenta - Prados",
            "remarks": "Zona residencial-comercial norte: Tabasco 2000, Multiochenta, Bosques de Saloya y Jesús Reyes Heroles.",
        },
        {
            "area_code": "SEC-003",
            "area_name": "Sector 3: Tamulté de las Barrancas - Atasta de Serra - Lindavista",
            "remarks": "Zona de alta densidad urbana: Tamulté, Atasta, Lindavista, Punta Brava y Guadalupe Borja.",
        },
        {
            "area_code": "SEC-004",
            "area_name": "Sector 4: Gaviotas Norte - Gaviotas Sur - La Manga",
            "remarks": "Sector margen derecho del Grijalva: Gaviotas Norte, Gaviotas Sur, Manga I, II y III, Torno Largo.",
        },
        {
            "area_code": "SEC-005",
            "area_name": "Sector 5: Tierra Colorada - Indeco - Ciudad Industrial",
            "remarks": "Sector nororiente: Indeco, Col. José María Pino Suárez, Tierra Colorada y Cd. Industrial.",
        },
        {
            "area_code": "SEC-006",
            "area_name": "Sector 6: Corredor Parrilla - Playas del Rosario - Las Mercedes",
            "remarks": "Sector suburbano sur: Parrilla I y II, Fracc. Las Mercedes, Playas del Rosario, Huapinol.",
        },
        {
            "area_code": "SEC-007",
            "area_name": "Sector 7: Villa Ocuiltzapotlán - Macultepec",
            "remarks": "Sector periurbano norte sobre carretera Villahermosa-Frontera.",
        },
    ]

    area_objs = {}
    for a in areas_data:
        existing = ServiceArea.query.filter_by(area_code=a["area_code"]).first()
        if not existing:
            sa = ServiceArea(
                area_code=a["area_code"],
                area_name=a["area_name"],
                remarks=a["remarks"],
            )
            db.session.add(sa)
            db.session.flush()
            area_objs[a["area_code"]] = sa
        else:
            area_objs[a["area_code"]] = existing

    # 6. Redes de Conducción y Acueductos de Villahermosa
    pipelines_data = [
        {
            "line_name": "Acueducto Usumacinta (36\" PEAD / Hierro Dúctil)",
            "tank_key": "Cisterna Central y Rebombeo Paseo de la Sierra",
            "area_key": "SEC-001",
            "diameter": 914.4,  # 36 pulg
            "status": "Active",
            "remarks": "Acueducto estratégico que conduce agua limpia del Río Carrizal hasta la PTAP Villahermosa en Paseo Usumacinta.",
        },
        {
            "line_name": "Línea Matriz Paseo de la Sierra - Centro (24\" HD)",
            "tank_key": "Cisterna Central y Rebombeo Paseo de la Sierra",
            "area_key": "SEC-001",
            "diameter": 609.6,  # 24 pulg
            "status": "Active",
            "remarks": "Línea matriz de agua potable tratada para abastecer el centro comercial e institucional de la ciudad.",
        },
        {
            "line_name": "Red de Distribución Tabasco 2000 (16\" PVC)",
            "tank_key": "Tanque Elevado Tabasco 2000",
            "area_key": "SEC-002",
            "diameter": 406.4,  # 16 pulg
            "status": "Active",
            "remarks": "Red secundaria de distribución a torres departamentales, hoteles y centros corporativos.",
        },
        {
            "line_name": "Línea de Presión Atasta - Tamulté (16\" AC / PVC)",
            "tank_key": "Tanque Elevado Ciudad Deportiva (Atasta)",
            "area_key": "SEC-003",
            "diameter": 406.4,  # 16 pulg
            "status": "Active",
            "remarks": "Distribución por gravedad desde Ciudad Deportiva hacia colonias tradicionales de Atasta y Tamulté.",
        },
        {
            "line_name": "Línea de Conducción Gaviotas - Torno Largo (14\" PEAD)",
            "tank_key": "Cisterna de Rebombeo Gaviotas / Torno Largo",
            "area_key": "SEC-004",
            "diameter": 355.6,  # 14 pulg
            "status": "Active",
            "remarks": "Línea de suministro en margen derecha del río Grijalva.",
        },
        {
            "line_name": "Red Principal Indeco - Ciudad Industrial (12\" PVC)",
            "tank_key": "Tanque Elevado Tabasco 2000",
            "area_key": "SEC-005",
            "diameter": 304.8,  # 12 pulg
            "status": "Active",
            "remarks": "Abastecimiento a naves industriales, talleres y colonias populares adyacentes.",
        },
        {
            "line_name": "Acueducto Corredor Parrilla (16\" PVC Hidráulico)",
            "tank_key": "Tanque de Rebombeo Loma de Caballo",
            "area_key": "SEC-006",
            "diameter": 406.4,  # 16 pulg
            "status": "Active",
            "remarks": "Suministro a los fraccionamientos residenciales del corredor Parrilla - Playas del Rosario.",
        },
    ]

    pipeline_objs = {}
    for p in pipelines_data:
        existing = Pipeline.query.filter_by(line_name=p["line_name"]).first()
        if not existing:
            pl = Pipeline(
                tank_id=tank_objs[p["tank_key"]].id,
                service_area_id=area_objs[p["area_key"]].id,
                line_name=p["line_name"],
                pipe_diameter_mm=p["diameter"],
                status=p["status"],
                remarks=p["remarks"],
            )
            db.session.add(pl)
            db.session.flush()
            pipeline_objs[p["line_name"]] = pl
        else:
            pipeline_objs[p["line_name"]] = existing

    # 7. Registros de Calidad y Potabilización en PTAP (NOM-127-SSA1)
    treatments_data = [
        {
            "source_name": "Río Carrizal (Bocatoma I - El Espejo)",
            "chemical_name": "Policloruro de Aluminio (PAC)",
            "date": date.today() - timedelta(days=2),
            "volume_m3": 85000.0,
            "amount": 1850.0,
            "unit": "L",
            "quality": "Safe",
            "operator": "Ing. Carlos Mendoza (PTAP Carrizal)",
            "remarks": "Turbiedad de entrada: 120 NTU. Turbiedad de salida: 1.8 NTU (Cumple NOM-127-SSA1-2021). Cloro libre: 1.2 mg/L.",
        },
        {
            "source_name": "Río Grijalva (Captación Paseo de la Sierra)",
            "chemical_name": "Sulfato de Aluminio Líquido",
            "date": date.today() - timedelta(days=1),
            "volume_m3": 140000.0,
            "amount": 4900.0,
            "unit": "kg",
            "quality": "Safe",
            "operator": "Q.F.B. Mariana Pérez (PTAP Villahermosa)",
            "remarks": "Pico de turbiedad por lluvias en Teapa: 850 NTU en agua cruda. Dosificación reforzada. Salida a red: 2.4 NTU.",
        },
        {
            "source_name": "Río Grijalva (Captación Paseo de la Sierra)",
            "chemical_name": "Gas Cloro (Cilindros de 1 Ton)",
            "date": date.today(),
            "volume_m3": 150000.0,
            "amount": 375.0,
            "unit": "kg",
            "quality": "Safe",
            "operator": "Téc. Roberto May (PTAP Villahermosa)",
            "remarks": "Desinfección terminal y mantenimiento de residual de cloro libre en red matriz Centro: 1.1 mg/L.",
        },
    ]

    for tr in treatments_data:
        tr_rec = TreatmentRecord(
            source_id=source_objs[tr["source_name"]].id,
            chemical_id=chemical_objs[tr["chemical_name"]].id,
            treatment_date=tr["date"],
            treated_water_m3=tr["volume_m3"],
            amount_used=tr["amount"],
            unit=tr["unit"],
            quality_status=tr["quality"],
            operator_name=tr["operator"],
            remarks=tr["remarks"],
        )
        db.session.add(tr_rec)

    # 8. Padrón de Usuarios de Prueba en Villahermosa
    customers_data = [
        {
            "name": "Lic. Alejandro Gómez Priego",
            "type": "Doméstico Residencial",
            "address": "Paseo Tabasco #1402, Fracc. Tabasco 2000, CP 86035",
            "phone": "993-315-4420",
            "area_code": "SEC-002",
            "pipeline_name": "Red de Distribución Tabasco 2000 (16\" PVC)",
        },
        {
            "name": "Sra. Carmen Méndez Torres",
            "type": "Doméstico Popular",
            "address": "Calle Gregorio Méndez Magaña #820, Col. Tamulté, CP 86150",
            "phone": "993-351-8890",
            "area_code": "SEC-003",
            "pipeline_name": "Línea de Presión Atasta - Tamulté (16\" AC / PVC)",
        },
        {
            "name": "Don Roberto Hernández Chan",
            "type": "Doméstico Medio",
            "address": "Calle Alfonso Vicens Saldívar #214, Col. Gaviotas Norte, CP 86090",
            "phone": "993-316-2244",
            "area_code": "SEC-004",
            "pipeline_name": "Línea de Conducción Gaviotas - Torno Largo (14\" PEAD)",
        },
        {
            "name": "Hotel Olmeca Plaza S.A. de C.V.",
            "type": "Comercial",
            "address": "Av. Francisco I. Madero #418, Col. Centro, CP 86000",
            "phone": "993-312-0055",
            "area_code": "SEC-001",
            "pipeline_name": "Línea Matriz Paseo de la Sierra - Centro (24\" HD)",
        },
        {
            "name": "Embotelladora del Sureste S.A.P.I. (Cd. Industrial)",
            "type": "Industrial",
            "address": "Av. Industria Nacional Mz 4 Lote 8, Ciudad Industrial, CP 86010",
            "phone": "993-353-1200",
            "area_code": "SEC-005",
            "pipeline_name": "Red Principal Indeco - Ciudad Industrial (12\" PVC)",
        },
        {
            "name": "Hospital Regional de Alta Especialidad Dr. Juan Graham",
            "type": "Servicios Públicos / Oficial",
            "address": "Carretera Villahermosa-La Isla Km 1.5, CP 86100",
            "phone": "993-310-0300",
            "area_code": "SEC-003",
            "pipeline_name": "Línea de Presión Atasta - Tamulté (16\" AC / PVC)",
        },
    ]

    for c_idx, c in enumerate(customers_data, start=1):
        existing = Customer.query.filter_by(customer_name=c["name"]).first()
        if not existing:
            cust = Customer(
                customer_id=f"SAS-VHSA-{c_idx:05d}",
                customer_name=c["name"],
                customer_type=c["type"],
                address=c["address"],
                phone=c["phone"],
                service_area_id=area_objs[c["area_code"]].id,
                supply_line_id=pipeline_objs[c["pipeline_name"]].id,
                created_date=date.today() - timedelta(days=60),
                status="active",
            )
            db.session.add(cust)
            db.session.flush()

            # Medidor
            meter = Meter(
                customer_id=cust.id,
                meter_serial=f"MED-VHSA-{1000 + c_idx}",
                install_date=date.today() - timedelta(days=60),
                status="Active",
            )
            db.session.add(meter)
            db.session.flush()

            # Lectura de consumo en m3
            last_m3 = 120.0 * c_idx
            curr_m3 = last_m3 + (18.5 if "Doméstico" in c["type"] else (145.0 if "Comercial" in c["type"] else 520.0))
            used_m3 = curr_m3 - last_m3
            rate_mxn = 12.50 if "Doméstico" in c["type"] else (24.00 if "Comercial" in c["type"] else 38.00)
            amount_mxn = round(used_m3 * rate_mxn, 2)

            mr = MeterReading(
                meter_id=meter.id,
                customer_id=cust.id,
                last_read_m3=last_m3,
                current_read_m3=curr_m3,
                used_water_m3=used_m3,
                rate_per_m3=rate_mxn,
                amount_due=amount_mxn,
                reading_date=date.today() - timedelta(days=5),
            )
            db.session.add(mr)
            db.session.flush()

            # Factura / Recibo de Agua
            inv_status = "paid" if c_idx in (1, 4) else "unpaid"
            amt_paid = amount_mxn if inv_status == "paid" else 0.0
            bal_due = 0.0 if inv_status == "paid" else amount_mxn

            inv = Invoice(
                invoice_no=f"REC-SAS-{2026000 + c_idx}",
                customer_id=cust.id,
                reading_id=mr.id,
                period_start=date.today() - timedelta(days=35),
                period_end=date.today() - timedelta(days=5),
                last_read_m3=last_m3,
                current_read_m3=curr_m3,
                used_water_m3=used_m3,
                rate_per_m3=rate_mxn,
                amount=amount_mxn,
                amount_paid=amt_paid,
                balance_due=bal_due,
                issue_date=date.today() - timedelta(days=5),
                due_date=date.today() + timedelta(days=15),
                status=inv_status,
                currency="MXN",
                remarks=f"Facturación bimestre SAS Centro para {c['type']}",
            )
            db.session.add(inv)
            db.session.flush()

            # Comprobante de pago en caja SAS si está pagada
            if inv_status == "paid":
                rc = Receipt(
                    receipt_no=f"PAGO-SAS-{5000 + c_idx}",
                    invoice_id=inv.id,
                    customer_id=cust.id,
                    amount_paid=amt_paid,
                    balance_before=amount_mxn,
                    balance_after=0.0,
                    payment_method="cash" if c_idx == 1 else "spei",
                    payment_date=date.today() - timedelta(days=2),
                    remarks="Pago recibido en Cajas de Recaudación SAS Centro / SPEI Banorte",
                )
                db.session.add(rc)

    db.session.commit()
    print("Precarga de infraestructura y datos de Villahermosa completada con éxito.")


if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        populate_villahermosa_data()
